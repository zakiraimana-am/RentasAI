from __future__ import annotations

from typing import Any


COST_PENALTY = {"low": 2, "medium": 8, "high": 16}
RISK_PENALTY = {"low": 2, "medium": 9, "high": 18, "very_high": 28}


def score_route(route: dict[str, Any], preference: str, weather_context: dict[str, Any], api_confidence: str) -> dict[str, Any]:
    score = 55 + route["delay_saved_minutes"] * 1.4
    score -= route["walking_minutes"] * 1.2
    score -= COST_PENALTY.get(route["cost_level"], 8)
    score -= RISK_PENALTY.get(route["risk_level"], 9)

    rain_level = weather_context.get("rain_level", "light")
    flood_risk = weather_context.get("flood_risk", "low")
    if rain_level in {"heavy", "very_heavy"}:
        score -= route["walking_minutes"] * 1.8
    if flood_risk in {"medium", "high"}:
        score -= RISK_PENALTY.get(route["risk_level"], 9) * 0.7

    if preference == "fastest":
        score += route["delay_saved_minutes"] * 1.2
    elif preference == "cheapest":
        score -= COST_PENALTY.get(route["cost_level"], 8) * 1.7
    elif preference == "least_walking":
        score -= route["walking_minutes"] * 2.2
    elif preference == "rain_safe":
        score -= route["walking_minutes"] * 2.0
        score -= RISK_PENALTY.get(route["risk_level"], 9) * 0.9

    if api_confidence == "low":
        score -= 4
    elif api_confidence == "high":
        score += 2

    enriched = dict(route)
    enriched["score"] = round(max(score, 0), 1)
    return enriched


def score_routes(
    routes: list[dict[str, Any]],
    preference: str,
    weather_context: dict[str, Any],
    api_confidence: str,
) -> list[dict[str, Any]]:
    return sorted(
        [score_route(route, preference, weather_context, api_confidence) for route in routes],
        key=lambda item: item["score"],
        reverse=True,
    )
