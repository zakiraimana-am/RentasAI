from __future__ import annotations

from fastapi import APIRouter

from app.simulation.scenario_engine import list_scenarios


router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.get("")
async def scenarios():
    return {"scenarios": list_scenarios()}
