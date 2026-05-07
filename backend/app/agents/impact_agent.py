from __future__ import annotations

from app.graph.state import RentasState


async def disruption_impact_agent(state: RentasState) -> RentasState:
    mobility = state["mobility_context"]
    weather = state["weather_context"]
    extra_delay = int(mobility.get("bus_delay_minutes", 0))
    if weather.get("rain_level") == "heavy":
        extra_delay += 5
    if weather.get("flood_risk") == "high":
        extra_delay += 10

    output = {
        "estimated_extra_delay_minutes": extra_delay,
        "missed_connection_risk": "high" if extra_delay >= 18 else "medium" if extra_delay >= 10 else "low",
        "lateness_risk": "high" if extra_delay >= 18 else "medium" if extra_delay >= 10 else "low",
        "walking_risk": weather.get("walking_risk"),
        "impact_reason": f"{mobility.get('detected_issue')} Walking risk is {weather.get('walking_risk')}.",
    }
    return {
        **state,
        "impact_analysis": output,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Disruption Impact Agent", "data_source": mobility.get("data_source"), "summary": output["impact_reason"], "output": output}],
    }
