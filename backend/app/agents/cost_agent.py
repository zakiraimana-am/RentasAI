from __future__ import annotations

from app.graph.state import RentasState
from app.services.scoring_service import score_routes


async def cost_and_convenience_agent(state: RentasState) -> RentasState:
    scored = score_routes(
        state["route_options"],
        state["trip_request"]["preference"],
        state["weather_context"],
        state["api_health"].get("confidence", "medium"),
    )
    return {
        **state,
        "scored_routes": scored,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Cost and Convenience Agent", "data_source": "deterministic", "summary": "Scored route options using fixed weights for time, walking, risk, cost, preference, weather, and API confidence.", "output": {"scored_routes": scored}}],
    }
