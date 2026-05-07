from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


LIVE_SOURCES = {"live", "cached"}
FALLBACK_SOURCES = {"simulated", "disabled", "fallback"}


def default_api_health() -> dict[str, Any]:
    return {
        "gtfs_static": {"status": "not_checked", "data_source": None, "message": "Not checked for this request."},
        "gtfs_realtime": {"status": "not_checked", "data_source": None, "message": "Not checked for this request."},
        "weather": {"status": "not_checked", "data_source": None, "message": "Not checked for this request."},
        "fallback_used": False,
        "overall_status": "not_checked",
        "confidence": "medium",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def health_status_from_payload(payload: dict[str, Any]) -> str:
    if payload.get("status") == "error":
        return "error"
    data_source = payload.get("data_source")
    if data_source in LIVE_SOURCES:
        return "ok"
    if data_source in FALLBACK_SOURCES or payload.get("status") in {"fallback", "disabled"}:
        return "fallback"
    return "error"


def first_error_message(payload: dict[str, Any], fallback: str) -> str:
    errors = payload.get("errors")
    if isinstance(errors, list) and errors:
        return str(errors[0])
    return payload.get("message") or fallback


def mark(
    health: dict[str, Any],
    source: str,
    status: str,
    message: str | None = None,
    data_source: str | None = None,
) -> dict[str, Any]:
    health[source] = {
        "status": status,
        "data_source": data_source,
        "message": message or ("Live data available." if status == "ok" else "Using deterministic simulation fallback."),
    }
    if status in {"error", "fallback"}:
        health["fallback_used"] = True
    statuses = [health[key]["status"] for key in ("gtfs_static", "gtfs_realtime", "weather")]
    if all(status == "ok" for status in statuses):
        health["overall_status"] = "ok"
        health["confidence"] = "high"
    elif "ok" in statuses:
        health["overall_status"] = "degraded"
        health["confidence"] = "medium"
    elif all(status in {"fallback", "not_checked"} for status in statuses):
        health["overall_status"] = "fallback"
        health["confidence"] = "medium"
    else:
        health["overall_status"] = "degraded"
        health["confidence"] = "low"
    return health


def mark_from_payload(health: dict[str, Any], source: str, payload: dict[str, Any], fallback_message: str) -> dict[str, Any]:
    status = health_status_from_payload(payload)
    if status == "ok":
        message = "Live data available." if payload.get("data_source") == "live" else "Using cached live data."
    else:
        message = first_error_message(payload, fallback_message)
    return mark(health, source, status, message, payload.get("data_source"))
