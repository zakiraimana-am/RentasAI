from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any


SCENARIOS: dict[str, dict[str, Any]] = {
    "normal_route": {
        "label": "Normal Route",
        "mobility": {
            "status": "normal",
            "severity": "low",
            "bus_delay_minutes": 3,
            "crowding": "moderate",
            "detected_issue": "Minor peak-hour variability on feeder access.",
        },
        "weather": {
            "rain_level": "light",
            "flood_risk": "low",
            "walking_risk": "low",
            "advice": "Normal interchange conditions. Walking remains acceptable.",
        },
        "operator": {"affected_users_estimate": 180, "severity": "low"},
    },
    "heavy_rain_bus_delay": {
        "label": "Heavy Rain + Bus Delay",
        "mobility": {
            "status": "disrupted",
            "severity": "high",
            "bus_delay_minutes": 18,
            "crowding": "high",
            "detected_issue": "Feeder bus headway is stretched near Wangsa Maju during morning peak.",
        },
        "weather": {
            "rain_level": "heavy",
            "flood_risk": "medium",
            "walking_risk": "high",
            "advice": "Avoid long walking and uncovered transfers until rain eases.",
        },
        "operator": {"affected_users_estimate": 1250, "severity": "high"},
    },
    "flash_flood_risk": {
        "label": "Flash Flood Risk",
        "mobility": {
            "status": "disrupted",
            "severity": "critical",
            "bus_delay_minutes": 15,
            "crowding": "high",
            "detected_issue": "Surface road reliability is degraded around low-lying access roads.",
        },
        "weather": {
            "rain_level": "heavy",
            "flood_risk": "high",
            "walking_risk": "very_high",
            "advice": "Avoid exposed walking and routes through flood-prone road segments.",
        },
        "operator": {"affected_users_estimate": 2200, "severity": "critical"},
    },
    "feeder_bus_delay": {
        "label": "Feeder Bus Delay",
        "mobility": {
            "status": "disrupted",
            "severity": "medium",
            "bus_delay_minutes": 14,
            "crowding": "high",
            "detected_issue": "Nearby feeder buses are delayed against expected peak service.",
        },
        "weather": {
            "rain_level": "moderate",
            "flood_risk": "low",
            "walking_risk": "medium",
            "advice": "Short walking is acceptable; avoid relying on delayed feeder access.",
        },
        "operator": {"affected_users_estimate": 900, "severity": "medium"},
    },
    "road_congestion": {
        "label": "Road Congestion",
        "mobility": {
            "status": "disrupted",
            "severity": "medium",
            "bus_delay_minutes": 12,
            "crowding": "moderate",
            "detected_issue": "Road congestion is slowing feeder and e-hailing movement.",
        },
        "weather": {
            "rain_level": "light",
            "flood_risk": "low",
            "walking_risk": "low",
            "advice": "Rail-first options are preferred; road segments should stay short.",
        },
        "operator": {"affected_users_estimate": 760, "severity": "medium"},
    },
}


DEMO_STOPS = [
    {"stop_id": "KJ3", "name": "Wangsa Maju", "lat": 3.2058, "lon": 101.7317, "type": "LRT"},
    {"stop_id": "KJ4", "name": "Sri Rampai", "lat": 3.1999, "lon": 101.7371, "type": "LRT"},
    {"stop_id": "KJ15", "name": "KL Sentral", "lat": 3.1342, "lon": 101.6861, "type": "Transit Hub"},
    {"stop_id": "BUS-WM-01", "name": "Wangsa Maju Feeder Stop", "lat": 3.2101, "lon": 101.7296, "type": "Bus"},
]


def list_scenarios() -> list[dict[str, str]]:
    return [{"id": key, "label": value["label"]} for key, value in SCENARIOS.items()]


def get_scenario(scenario_id: str) -> dict[str, Any]:
    return deepcopy(SCENARIOS.get(scenario_id, SCENARIOS["heavy_rain_bus_delay"]))


def parse_deadline_today(deadline: str) -> datetime:
    hour, minute = [int(part) for part in deadline.split(":", 1)]
    base = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    return base


def arrival_from_deadline(deadline: str, minutes_before_or_after: int) -> str:
    arrival = parse_deadline_today(deadline) + timedelta(minutes=minutes_before_or_after)
    return arrival.strftime("%H:%M")


def demo_route_geometry(route_id: str) -> dict[str, Any]:
    geometries = {
        "A": [
            [101.7296, 3.2101],
            [101.7317, 3.2058],
            [101.7200, 3.1900],
            [101.7040, 3.1600],
            [101.6861, 3.1342],
        ],
        "B": [
            [101.7296, 3.2101],
            [101.7317, 3.2058],
            [101.7186, 3.1845],
            [101.7015, 3.1569],
            [101.6861, 3.1342],
        ],
        "C": [
            [101.7296, 3.2101],
            [101.7371, 3.1999],
            [101.7200, 3.1800],
            [101.7015, 3.1569],
            [101.6861, 3.1342],
        ],
    }
    return {"type": "LineString", "coordinates": geometries[route_id]}


def demo_vehicles() -> list[dict[str, Any]]:
    return [
        {"vehicle_id": "sim-bus-01", "route_id": "T222", "lat": 3.2132, "lon": 101.7281, "status": "delayed"},
        {"vehicle_id": "sim-bus-02", "route_id": "T222", "lat": 3.2032, "lon": 101.7246, "status": "slow"},
    ]
