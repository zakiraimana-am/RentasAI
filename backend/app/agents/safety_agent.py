from __future__ import annotations

from app.graph.state import RentasState


async def safety_validation_agent(state: RentasState) -> RentasState:
    weather = state["weather_context"]
    validated = []
    for route in state["scored_routes"]:
        item = dict(route)
        unsafe_walk = item["walking_minutes"] >= 15 and weather.get("walking_risk") in {"high", "very_high"}
        flood_exposure = item["risk_level"] in {"high", "very_high"} and weather.get("flood_risk") in {"medium", "high"}
        if unsafe_walk or flood_exposure:
            item["safety_status"] = "penalized"
            item["safety_reason"] = "Long or exposed walking is not recommended under current rain/flood risk."
            item["score"] = round(item["score"] * 0.72, 1)
        else:
            item["safety_status"] = "safe"
            item["safety_reason"] = "Walking exposure and route risk are acceptable for this scenario."
        validated.append(item)
    validated.sort(key=lambda route: route["score"], reverse=True)
    safe_routes = [route for route in validated if route["safety_status"] == "safe"]
    recommended = safe_routes[0] if safe_routes else validated[0]
    backup = validated[1]["name"] if len(validated) > 1 else None
    output = {
        "safety_status": recommended["safety_status"],
        "safety_reason": recommended["safety_reason"],
        "recommended_route": recommended,
        "backup_route_name": backup,
        "all_routes_validated": validated,
    }
    return {
        **state,
        "scored_routes": validated,
        "safety_result": output,
        "agent_trace": state.get("agent_trace", []) + [{"agent": "Safety Validation Agent", "data_source": "deterministic", "summary": output["safety_reason"], "output": output}],
    }
