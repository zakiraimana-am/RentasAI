from __future__ import annotations

from typing import Any
from zipfile import ZipFile
from io import BytesIO, TextIOWrapper
import csv

import httpx

from app.config import get_settings
from app.services.cache_service import cache, get_demo_stops


GTFS_STATIC_ENDPOINTS = [
    "https://api.data.gov.my/gtfs-static/prasarana?category=rapid-rail-kl",
    "https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-mrtfeeder",
    "https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl",
    "https://api.data.gov.my/gtfs-static/ktmb",
]


async def fetch_gtfs_static_summary() -> dict[str, Any]:
    settings = get_settings()
    if not settings.enable_live_apis:
        return {
            "status": "disabled",
            "stops": get_demo_stops(),
            "routes_count": 0,
            "data_source": "simulated",
            "message": "Live APIs disabled; using demo stop metadata.",
            "errors": [],
        }

    stops: list[dict[str, Any]] = []
    routes_count = 0
    errors: list[str] = []
    async with httpx.AsyncClient(timeout=settings.live_api_timeout_seconds, follow_redirects=True) as client:
        for url in GTFS_STATIC_ENDPOINTS:
            try:
                response = await client.get(url)
                response.raise_for_status()
                payload = response.content
                with ZipFile(BytesIO(payload)) as zf:
                    if "stops.txt" in zf.namelist():
                        with zf.open("stops.txt") as raw:
                            reader = csv.DictReader(TextIOWrapper(raw, encoding="utf-8-sig"))
                            for row in list(reader)[:80]:
                                try:
                                    stops.append(
                                        {
                                            "stop_id": row.get("stop_id"),
                                            "name": row.get("stop_name"),
                                            "lat": float(row.get("stop_lat") or 0),
                                            "lon": float(row.get("stop_lon") or 0),
                                            "type": "GTFS",
                                        }
                                    )
                                except (TypeError, ValueError):
                                    continue
                    if "routes.txt" in zf.namelist():
                        with zf.open("routes.txt") as raw:
                            routes_count += sum(1 for _ in TextIOWrapper(raw, encoding="utf-8-sig")) - 1
            except Exception as exc:  # live-ready graceful fallback
                errors.append(f"{url}: {exc}")

    if stops:
        summary = {
            "status": "ok",
            "stops": stops,
            "routes_count": max(routes_count, 0),
            "data_source": "live",
            "message": "GTFS Static loaded from Malaysia public data endpoints.",
            "errors": errors,
        }
        cache.gtfs_static = summary
        return summary

    if cache.gtfs_static:
        cached = dict(cache.gtfs_static)
        cached["data_source"] = "cached"
        cached["errors"] = errors
        cached["message"] = "Live GTFS Static unavailable; using cached GTFS metadata."
        return cached

    return {
        "status": "fallback",
        "stops": get_demo_stops(),
        "routes_count": 0,
        "data_source": "simulated",
        "message": "GTFS Static unavailable; using built-in demo stops.",
        "errors": errors or ["No GTFS Static endpoints returned usable stops."],
    }
