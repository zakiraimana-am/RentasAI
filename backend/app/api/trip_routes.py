from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.rentas_graph import rentas_graph
from app.services.cache_service import cache
from app.services.database_service import persist_trip_result


router = APIRouter(prefix="/trip", tags=["trip"])


class TripPlanRequest(BaseModel):
    origin: str = "Wangsa Maju"
    destination: str = "KL Sentral"
    arrival_deadline: str = "08:45"
    preference: Literal["balanced", "fastest", "cheapest", "least_walking", "rain_safe"] = "rain_safe"
    scenario: str = "heavy_rain_bus_delay"
    mode: Literal["live", "simulation", "hybrid"] = "hybrid"


@router.post("/plan")
async def plan_trip(payload: TripPlanRequest):
    final_state = await run_graph_with_recovery(payload)
    route_options = final_state.get("scored_routes") or final_state.get("route_options", [])
    selected_route = final_state["final_recommendation"]["selected_route"]
    result = {
        "trip": payload.model_dump(),
        "mode": payload.mode,
        "effective_mode": final_state.get("app_mode", payload.mode),
        "api_health": final_state["api_health"],
        "recommendation": final_state["final_recommendation"],
        "agent_trace": final_state["agent_trace"],
        "route_options": route_options,
        "map_geometry": selected_route.get("geometry"),
        "operator_impact": final_state["operator_impact"],
        "errors": final_state.get("errors", []),
    }
    cache.operator_impact = result["operator_impact"]
    trip_id = await persist_trip_result(result)
    result["persistence"] = {
        "database": "ok" if trip_id else "error",
        "message": "Trip stored in PostgreSQL." if trip_id else "PostgreSQL unavailable or schema not initialized; response was still generated.",
    }
    if trip_id:
        result["trip_id"] = trip_id
    return result


async def run_graph_with_recovery(payload: TripPlanRequest):
    initial_state = build_initial_state(payload, payload.mode)
    try:
        return await rentas_graph.ainvoke(initial_state)
    except Exception as exc:
        if payload.mode == "simulation":
            return await build_emergency_simulation_result(payload, exc)
        fallback_state = build_initial_state(payload, "simulation")
        fallback_state["errors"].append(
            {
                "source": "graph",
                "message": f"{payload.mode} planning failed and was retried in simulation mode: {exc}",
            }
        )
        try:
            return await rentas_graph.ainvoke(fallback_state)
        except Exception as fallback_exc:
            return await build_emergency_simulation_result(payload, fallback_exc)


def build_initial_state(payload: TripPlanRequest, mode: str):
    trip = payload.model_dump()
    trip["mode"] = mode
    return {
        "trip_request": trip,
        "app_mode": mode,
        "api_health": {},
        "live_transport_data": {},
        "live_weather_data": {},
        "simulation_context": {},
        "mobility_context": {},
        "weather_context": {},
        "impact_analysis": {},
        "route_options": [],
        "scored_routes": [],
        "safety_result": {},
        "final_recommendation": {},
        "operator_impact": {},
        "agent_trace": [],
        "errors": [],
        "fallback_used": False,
    }


async def build_emergency_simulation_result(payload: TripPlanRequest, exc: Exception):
    from app.agents.communication_agent import communication_agent
    from app.agents.cost_agent import cost_and_convenience_agent
    from app.agents.impact_agent import disruption_impact_agent
    from app.agents.observer_agent import mobility_observer_agent
    from app.agents.operator_impact_agent import operator_impact_agent
    from app.agents.route_agent import route_recovery_agent
    from app.agents.safety_agent import safety_validation_agent
    from app.agents.weather_agent import weather_and_flood_agent
    from app.services.api_health_service import default_api_health, mark
    from app.simulation.scenario_engine import get_scenario

    state = build_initial_state(payload, "simulation")
    health = default_api_health()
    mark(health, "gtfs_static", "fallback", "Emergency fallback: live data bypassed.", "simulated")
    mark(health, "gtfs_realtime", "fallback", "Emergency fallback: realtime data bypassed.", "simulated")
    mark(health, "weather", "fallback", "Emergency fallback: weather data bypassed.", "simulated")
    state.update(
        {
            "api_health": health,
            "simulation_context": get_scenario(payload.scenario),
            "errors": [{"source": "emergency_fallback", "message": str(exc)}],
            "agent_trace": [
                {
                    "agent": "Emergency Fallback",
                    "data_source": "simulated",
                    "summary": "Recovered from an unexpected failure by running deterministic simulation-only planning.",
                    "output": {"error": str(exc), "effective_mode": "simulation"},
                }
            ],
        }
    )
    for agent in (
        mobility_observer_agent,
        weather_and_flood_agent,
        disruption_impact_agent,
        route_recovery_agent,
        cost_and_convenience_agent,
        safety_validation_agent,
        communication_agent,
        operator_impact_agent,
    ):
        state = await agent(state)
    return state
