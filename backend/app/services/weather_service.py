from __future__ import annotations

from typing import Any

import httpx

from app.config import get_settings
from app.services.cache_service import cache


FORECAST_URL = "https://api.data.gov.my/weather/forecast"
WARNING_URL = "https://api.data.gov.my/weather/warning"


async def fetch_weather_summary() -> dict[str, Any]:
    settings = get_settings()
    if not settings.enable_live_apis:
        return {
            "status": "disabled",
            "forecast": [],
            "warnings": [],
            "data_source": "simulated",
            "message": "Live APIs disabled; using scenario weather.",
            "errors": [],
        }

    errors: list[str] = []
    forecast: Any = []
    warnings: Any = []
    async with httpx.AsyncClient(timeout=settings.live_api_timeout_seconds, follow_redirects=True) as client:
        try:
            response = await client.get(FORECAST_URL)
            response.raise_for_status()
            data = response.json()
            forecast = data[:12] if isinstance(data, list) else data
        except Exception as exc:
            errors.append(f"forecast: {exc}")
        try:
            response = await client.get(WARNING_URL)
            response.raise_for_status()
            data = response.json()
            warnings = data[:8] if isinstance(data, list) else data
        except Exception as exc:
            errors.append(f"warning: {exc}")

    if forecast or warnings:
        payload = {
            "status": "ok",
            "forecast": forecast,
            "warnings": warnings,
            "data_source": "live",
            "message": "Malaysia Weather API data available.",
            "errors": errors,
        }
        cache.weather = payload
        return payload

    if cache.weather:
        cached = dict(cache.weather)
        cached["data_source"] = "cached"
        cached["errors"] = errors
        cached["message"] = "Live weather unavailable; using cached weather summary."
        return cached

    return {
        "status": "fallback",
        "forecast": [],
        "warnings": [],
        "data_source": "simulated",
        "message": "Weather API unavailable; using scenario weather.",
        "errors": errors or ["Malaysia Weather API did not return forecast or warnings."],
    }
