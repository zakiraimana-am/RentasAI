from __future__ import annotations

from app.graph.state import RentasState


async def mobility_observer_agent(state: RentasState) -> RentasState:
    mode = state["app_mode"]
    simulated = state["simulation_context"]["mobility"]
    data_source = "simulated" if mode == "simulation" else "hybrid" if mode == "hybrid" else "live"
    realtime = state.get("live_transport_data", {}).get("realtime", {})

    output = dict(simulated)
    output["data_source"] = data_source
    if mode == "live" and realtime.get("vehicles_count", 0) > 0:
        output["detected_issue"] = "Live bus vehicle-position feed is available; MVP treats it as supporting evidence for bus reliability."
        output["severity"] = "medium"
    elif mode == "live" and state.get("api_health", {}).get("gtfs_realtime", {}).get("status") != "ok":
        output["detected_issue"] = "Realtime rail data is unavailable; disruption inference fell back to deterministic demo logic."
        output["data_source"] = "simulated"

    return {
        **state,
        "mobility_context": output,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Mobility Observer Agent", "data_source": output["data_source"], "summary": output["detected_issue"], "output": output}],
    }
