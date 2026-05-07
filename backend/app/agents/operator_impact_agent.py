from __future__ import annotations

from app.graph.state import RentasState


async def operator_impact_agent(state: RentasState) -> RentasState:
    scenario_operator = state["simulation_context"]["operator"]
    mobility = state["mobility_context"]
    live_used = state["app_mode"] == "live" and not state.get("fallback_used", False)
    output = {
        "affected_area": "Wangsa Maju to KL Sentral corridor",
        "severity": scenario_operator.get("severity", mobility.get("severity", "medium")),
        "affected_users_estimate": scenario_operator.get("affected_users_estimate", 850),
        "recommended_action": "Prioritize feeder reliability messaging and surface e-hailing-to-rail recovery guidance near Wangsa Maju.",
        "live_data_used": bool(live_used),
        "fallback_used": bool(state.get("api_health", {}).get("fallback_used", False)),
    }
    return {
        **state,
        "operator_impact": output,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Operator Impact Agent", "data_source": state["app_mode"], "summary": output["recommended_action"], "output": output}],
    }
