from __future__ import annotations

from app.graph.state import RentasState
from app.services.api_health_service import default_api_health, mark, mark_from_payload
from app.services.gtfs_realtime_service import fetch_vehicle_positions
from app.services.gtfs_static_service import fetch_gtfs_static_summary
from app.services.weather_service import fetch_weather_summary
from app.simulation.scenario_engine import get_scenario


async def data_fetch_agent(state: RentasState) -> RentasState:
    mode = state["app_mode"]
    scenario = get_scenario(state["trip_request"]["scenario"])
    health = default_api_health()
    errors = state.get("errors", [])
    live_transport_data = {"static": None, "realtime": None}
    live_weather_data = {}
    fallback_used = mode == "simulation"

    if mode in {"live", "hybrid"}:
        static = await fetch_gtfs_static_summary()
        live_transport_data["static"] = {
            "stops_count": len(static.get("stops", [])),
            "routes_count": static.get("routes_count", 0),
            "data_source": static.get("data_source"),
            "status": static.get("status"),
        }
        mark_from_payload(health, "gtfs_static", static, "GTFS Static unavailable; using demo stop metadata.")
        if static.get("errors"):
            errors.extend({"source": "gtfs_static", "message": item} for item in static["errors"])

        realtime = await fetch_vehicle_positions()
        live_transport_data["realtime"] = {
            "vehicles_count": len(realtime.get("vehicles", [])),
            "data_source": realtime.get("data_source"),
            "status": realtime.get("status"),
            "message": realtime.get("message"),
        }
        mark_from_payload(health, "gtfs_realtime", realtime, "GTFS Realtime unavailable or malformed; bus movement is simulation-only.")
        if realtime.get("errors"):
            errors.extend({"source": "gtfs_realtime", "message": item} for item in realtime["errors"])

        weather = await fetch_weather_summary()
        live_weather_data = {
            "forecast_count": len(weather.get("forecast", [])) if isinstance(weather.get("forecast"), list) else 1,
            "warnings_count": len(weather.get("warnings", [])) if isinstance(weather.get("warnings"), list) else 1,
            "data_source": weather.get("data_source"),
            "status": weather.get("status"),
        }
        mark_from_payload(health, "weather", weather, "Weather API unavailable; using scenario weather.")
        if weather.get("errors"):
            errors.extend({"source": "weather", "message": item} for item in weather["errors"])
        fallback_used = health["fallback_used"]
    else:
        mark(health, "gtfs_static", "fallback", "Simulation mode uses built-in GTFS-like demo stops.", "simulated")
        mark(health, "gtfs_realtime", "fallback", "Simulation mode uses deterministic vehicle context.", "simulated")
        mark(health, "weather", "fallback", "Simulation mode uses deterministic weather context.", "simulated")
        live_transport_data = {"static": {"stops_count": 4, "routes_count": 1, "data_source": "simulated"}, "realtime": {"vehicles_count": 2, "data_source": "simulated"}}
        live_weather_data = {"forecast_count": 1, "warnings_count": 0, "data_source": "simulated"}

    output = {
        "api_health": health,
        "live_transport_data": live_transport_data,
        "live_weather_data": live_weather_data,
        "fallback_used": fallback_used,
    }
    return {
        **state,
        **output,
        "simulation_context": scenario,
        "errors": errors,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Data Fetch Agent", "data_source": mode, "summary": f"Data layer completed with {health['overall_status']} status; fallback_used={health['fallback_used']}.", "output": output}],
    }
