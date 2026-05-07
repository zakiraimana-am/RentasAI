from __future__ import annotations

from fastapi import APIRouter

from app.services.cache_service import cache


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/operator")
async def operator_dashboard():
    return cache.operator_impact or {
        "affected_area": "Wangsa Maju to KL Sentral corridor",
        "severity": "medium",
        "affected_users_estimate": 850,
        "recommended_action": "Run a trip plan to generate the latest operator impact summary.",
        "live_data_used": False,
        "fallback_used": True,
    }
