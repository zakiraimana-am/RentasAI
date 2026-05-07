from __future__ import annotations

from app.graph.state import RentasState


async def weather_and_flood_agent(state: RentasState) -> RentasState:
    mode = state["app_mode"]
    output = dict(state["simulation_context"]["weather"])
    output["data_source"] = "simulated" if mode == "simulation" else "hybrid" if mode == "hybrid" else "live"

    if mode == "live" and state.get("api_health", {}).get("weather", {}).get("status") != "ok":
        output["data_source"] = "simulated"
        output["advice"] = "Live weather was unavailable, so the system used safe deterministic weather assumptions."

    return {
        **state,
        "weather_context": output,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Weather and Flood Agent", "data_source": output["data_source"], "summary": output["advice"], "output": output}],
    }
