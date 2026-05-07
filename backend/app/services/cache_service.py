from __future__ import annotations

from typing import Any

from app.simulation.scenario_engine import DEMO_STOPS, demo_vehicles


class MemoryCache:
    def __init__(self) -> None:
        self.gtfs_static: dict[str, Any] | None = None
        self.gtfs_realtime: dict[str, Any] | None = None
        self.weather: dict[str, Any] | None = None
        self.operator_impact: dict[str, Any] | None = None


cache = MemoryCache()


def get_demo_stops(query: str | None = None) -> list[dict[str, Any]]:
    if not query:
        return DEMO_STOPS
    q = query.lower()
    return [stop for stop in DEMO_STOPS if q in stop["name"].lower()]


def get_demo_vehicle_payload() -> dict[str, Any]:
    return {
        "status": "fallback",
        "vehicles": demo_vehicles(),
        "data_source": "simulated",
        "message": "Using deterministic simulated vehicle positions.",
        "errors": [],
    }
