from __future__ import annotations

from typing import Any

from app.config import get_settings


def deterministic_explanation(
    recommended_route: dict[str, Any],
    impact_analysis: dict[str, Any],
    weather_context: dict[str, Any],
    safety_result: dict[str, Any],
    api_confidence: str,
) -> dict[str, str]:
    route_name = recommended_route.get("name", "the recommended route")
    backup = safety_result.get("backup_route_name") or "Use the next safest rail-based option if conditions change."
    source_note = "OpenAI not configured or unavailable; using deterministic template explanation."
    return {
        "user_message": f"Recommended: {route_name}. This gets you to KL Sentral around {recommended_route.get('estimated_arrival')} while limiting rain exposure.",
        "reason": (
            f"It saves about {recommended_route.get('delay_saved_minutes')} minutes, keeps walking to "
            f"{recommended_route.get('walking_minutes')} minutes, and responds to {weather_context.get('rain_level')} rain plus "
            f"{impact_analysis.get('impact_reason')}."
        ),
        "backup_option": backup,
        "confidence": "high" if api_confidence == "high" and safety_result.get("safety_status") == "safe" else "medium",
        "data_note": f"Route choice is deterministic. Live API confidence: {api_confidence}. {source_note}",
    }


async def generate_structured_explanation(
    recommended_route: dict[str, Any],
    impact_analysis: dict[str, Any],
    weather_context: dict[str, Any],
    safety_result: dict[str, Any],
    api_confidence: str,
) -> dict[str, str]:
    settings = get_settings()
    if not settings.openai_api_key:
        return deterministic_explanation(recommended_route, impact_analysis, weather_context, safety_result, api_confidence)

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        schema = {
            "name": "rentasai_explanation",
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "user_message": {"type": "string"},
                    "reason": {"type": "string"},
                    "backup_option": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
                    "data_note": {"type": "string"},
                },
                "required": ["user_message", "reason", "backup_option", "confidence", "data_note"],
            },
        }
        prompt_payload = {
            "recommended_route": recommended_route,
            "impact_analysis": impact_analysis,
            "weather_context": weather_context,
            "safety_result": safety_result,
            "api_confidence": api_confidence,
        }
        response = await client.responses.create(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You explain a commuter route recommendation. Use only the supplied JSON facts. "
                        "Do not add stations, fares, travel times, weather, or live conditions not present in the input."
                    ),
                },
                {"role": "user", "content": str(prompt_payload)},
            ],
            text={"format": {"type": "json_schema", **schema}},
        )
        parsed: Any = response.output_parsed
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return deterministic_explanation(recommended_route, impact_analysis, weather_context, safety_result, api_confidence)
