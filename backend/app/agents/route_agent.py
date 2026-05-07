from __future__ import annotations

from app.graph.state import RentasState
from app.simulation.scenario_engine import arrival_from_deadline, demo_route_geometry


async def route_recovery_agent(state: RentasState) -> RentasState:
    deadline = state["trip_request"]["arrival_deadline"]
    mobility = state["mobility_context"]
    weather = state["weather_context"]
    delay = int(mobility.get("bus_delay_minutes", 0))
    heavy_rain = weather.get("rain_level") == "heavy"
    if state.get("api_health", {}).get("overall_status") == "fallback":
        data_source = "simulated"
    elif state["app_mode"] == "hybrid":
        data_source = "hybrid"
    else:
        data_source = state["app_mode"]

    routes = [
        {
            "id": "A",
            "name": "Wait for feeder bus, then rail",
            "estimated_arrival": arrival_from_deadline(deadline, 8 if delay >= 14 else -2),
            "delay_saved_minutes": max(0, delay - 6),
            "cost_level": "low",
            "walking_minutes": 7,
            "risk_level": "high" if delay >= 14 else "medium",
            "description": "Stay with the planned feeder connection before continuing by rail.",
            "data_source": data_source,
            "geometry": demo_route_geometry("A"),
        },
        {
            "id": "B",
            "name": "E-hailing to nearest LRT, then rail",
            "estimated_arrival": arrival_from_deadline(deadline, -7 if heavy_rain or delay >= 12 else -4),
            "delay_saved_minutes": delay + 10,
            "cost_level": "medium",
            "walking_minutes": 2,
            "risk_level": "low" if weather.get("flood_risk") != "high" else "medium",
            "description": "Use a short e-hailing hop to avoid the delayed feeder and reduce rain exposure, then continue by rail.",
            "data_source": data_source,
            "geometry": demo_route_geometry("B"),
        },
        {
            "id": "C",
            "name": "Walk to alternative station, then rail",
            "estimated_arrival": arrival_from_deadline(deadline, -1 if not heavy_rain else 5),
            "delay_saved_minutes": max(4, delay - 2),
            "cost_level": "low",
            "walking_minutes": 18,
            "risk_level": "very_high" if weather.get("flood_risk") == "high" else "high" if heavy_rain else "medium",
            "description": "Walk to a nearby alternative station and continue by rail.",
            "data_source": data_source,
            "geometry": demo_route_geometry("C"),
        },
    ]
    return {
        **state,
        "route_options": routes,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Route Recovery Agent", "data_source": data_source, "summary": "Generated exactly three deterministic recovery options for the demo corridor.", "output": {"route_count": 3, "routes": routes}}],
    }
