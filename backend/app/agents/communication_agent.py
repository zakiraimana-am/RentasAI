from __future__ import annotations

from app.graph.state import RentasState
from app.services.openai_service import generate_structured_explanation


async def communication_agent(state: RentasState) -> RentasState:
    recommended = state["safety_result"]["recommended_route"]
    explanation = await generate_structured_explanation(
        recommended,
        state["impact_analysis"],
        state["weather_context"],
        state["safety_result"],
        state["api_health"].get("confidence", "medium"),
    )
    output = {"selected_route": recommended, "explanation": explanation}
    source = "template" if "deterministic template" in explanation.get("data_note", "") else "openai"
    return {
        **state,
        "final_recommendation": output,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Communication Agent", "data_source": source, "summary": explanation["user_message"], "output": output}],
    }
