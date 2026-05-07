from typing import Any, Literal, TypedDict


AppMode = Literal["live", "simulation", "hybrid"]
Preference = Literal["balanced", "fastest", "cheapest", "least_walking", "rain_safe"]


class TripRequest(TypedDict):
    origin: str
    destination: str
    arrival_deadline: str
    preference: Preference
    scenario: str
    mode: AppMode


class RentasState(TypedDict, total=False):
    trip_request: TripRequest
    app_mode: AppMode
    api_health: dict[str, Any]
    live_transport_data: dict[str, Any]
    live_weather_data: dict[str, Any]
    simulation_context: dict[str, Any]
    mobility_context: dict[str, Any]
    weather_context: dict[str, Any]
    impact_analysis: dict[str, Any]
    route_options: list[dict[str, Any]]
    scored_routes: list[dict[str, Any]]
    safety_result: dict[str, Any]
    final_recommendation: dict[str, Any]
    operator_impact: dict[str, Any]
    agent_trace: list[dict[str, Any]]
    errors: list[dict[str, Any]]
    fallback_used: bool
