from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard_routes import router as dashboard_router
from app.api.live_routes import router as live_router
from app.api.scenario_routes import router as scenario_router
from app.api.trip_routes import router as trip_router
from app.config import get_settings
from app.services.database_service import database_status


app = FastAPI(title="RentasAI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trip_router, prefix="/api")
app.include_router(scenario_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(live_router, prefix="/api")


@app.get("/")
async def root():
    return {"name": "RentasAI", "backend": "ok"}


@app.get("/api/health")
async def health():
    settings = get_settings()
    return {
        "backend": "ok",
        "database": await database_status(),
        "openai": "configured" if settings.openai_api_key else "not_configured_template_fallback",
        "mapbox": "frontend_only",
        "live_apis": {
            "gtfs_static": "not_checked",
            "gtfs_realtime": "not_checked",
            "weather": "not_checked",
        },
        "demo_reliability": {
            "simulation_mode": "available",
            "database_required": False,
            "openai_required": False,
            "mapbox_required": False,
        },
    }
