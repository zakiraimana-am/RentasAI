from __future__ import annotations

from fastapi import APIRouter, Query

from app.services.cache_service import get_demo_stops
from app.services.gtfs_realtime_service import fetch_vehicle_positions
from app.services.gtfs_static_service import fetch_gtfs_static_summary
from app.services.weather_service import fetch_weather_summary
from app.simulation.scenario_engine import get_scenario


router = APIRouter(prefix="/live", tags=["live"])


@router.get("/stops/search")
async def search_stops(q: str = Query(default="")):
    live = await fetch_gtfs_static_summary()
    stops = live.get("stops") or get_demo_stops(q)
    if q:
        stops = [stop for stop in stops if q.lower() in (stop.get("name") or "").lower()]
    return {"stops": stops[:20], "data_source": live.get("data_source", "simulated")}


@router.get("/vehicles")
async def vehicles():
    payload = await fetch_vehicle_positions()
    return {
        "vehicles": payload.get("vehicles", []),
        "api_health": {"gtfs_realtime": payload.get("status", "fallback")},
        "data_source": payload.get("data_source"),
        "message": payload.get("message"),
        "errors": payload.get("errors", []),
    }


@router.get("/weather")
async def weather():
    payload = await fetch_weather_summary()
    if payload.get("data_source") in {"live", "cached"}:
        return payload
    scenario = get_scenario("heavy_rain_bus_delay")
    return {"status": "fallback", "data_source": "simulated", "weather": scenario["weather"]}
