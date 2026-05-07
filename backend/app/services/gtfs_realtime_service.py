from __future__ import annotations

from typing import Any

import httpx

from app.config import get_settings
from app.services.cache_service import cache, get_demo_vehicle_payload


GTFS_RT_ENDPOINTS = [
    "https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-mrtfeeder",
    "https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl",
]


async def fetch_vehicle_positions() -> dict[str, Any]:
    settings = get_settings()
    if not settings.enable_live_apis:
        return get_demo_vehicle_payload()

    errors: list[str] = []
    vehicles: list[dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=settings.live_api_timeout_seconds, follow_redirects=True) as client:
        for url in GTFS_RT_ENDPOINTS:
            try:
                response = await client.get(url)
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if not response.content:
                    errors.append(f"{url}: empty GTFS Realtime response")
                    continue
                if "json" in content_type.lower():
                    errors.append(f"{url}: expected GTFS Realtime protobuf but received JSON")
                    continue
                if len(response.content) < 8:
                    errors.append(f"{url}: malformed GTFS Realtime response ({len(response.content)} bytes)")
                    continue
                vehicles.append(
                    {
                        "source_url": url,
                        "content_type": content_type or "application/octet-stream",
                        "bytes": len(response.content),
                        "parse_status": "protobuf_received_unparsed",
                        "note": "GTFS Realtime protobuf received; used only as supporting evidence in the MVP.",
                    }
                )
            except Exception as exc:
                errors.append(f"{url}: {exc}")

    if vehicles:
        payload = {
            "status": "ok",
            "vehicles": vehicles,
            "data_source": "live",
            "message": "GTFS Realtime bus feed responded with protobuf payloads.",
            "errors": errors,
        }
        cache.gtfs_realtime = payload
        return payload

    if cache.gtfs_realtime:
        cached = dict(cache.gtfs_realtime)
        cached["data_source"] = "cached"
        cached["errors"] = errors
        cached["message"] = "Live realtime feed unavailable; using cached realtime summary."
        return cached

    return {
        "status": "fallback",
        "vehicles": [],
        "data_source": "simulated",
        "message": "No valid GTFS Realtime payload available; route planning remains deterministic.",
        "errors": errors or ["No GTFS Realtime vehicle-position payloads were available."],
    }
