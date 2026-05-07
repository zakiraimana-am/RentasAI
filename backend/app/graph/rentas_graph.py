from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.agents.communication_agent import communication_agent
from app.agents.cost_agent import cost_and_convenience_agent
from app.agents.data_fetch_agent import data_fetch_agent
from app.agents.impact_agent import disruption_impact_agent
from app.agents.observer_agent import mobility_observer_agent
from app.agents.operator_impact_agent import operator_impact_agent
from app.agents.route_agent import route_recovery_agent
from app.agents.safety_agent import safety_validation_agent
from app.agents.weather_agent import weather_and_flood_agent
from app.graph.state import RentasState


def build_graph():
    graph = StateGraph(RentasState)
    graph.add_node("data_fetch_node", data_fetch_agent)
    graph.add_node("mobility_observer_node", mobility_observer_agent)
    graph.add_node("weather_and_flood_node", weather_and_flood_agent)
    graph.add_node("disruption_impact_node", disruption_impact_agent)
    graph.add_node("route_recovery_node", route_recovery_agent)
    graph.add_node("cost_and_convenience_node", cost_and_convenience_agent)
    graph.add_node("safety_validation_node", safety_validation_agent)
    graph.add_node("communication_node", communication_agent)
    graph.add_node("operator_impact_node", operator_impact_agent)

    graph.add_edge(START, "data_fetch_node")
    graph.add_edge("data_fetch_node", "mobility_observer_node")
    graph.add_edge("mobility_observer_node", "weather_and_flood_node")
    graph.add_edge("weather_and_flood_node", "disruption_impact_node")
    graph.add_edge("disruption_impact_node", "route_recovery_node")
    graph.add_edge("route_recovery_node", "cost_and_convenience_node")
    graph.add_edge("cost_and_convenience_node", "safety_validation_node")
    graph.add_edge("safety_validation_node", "communication_node")
    graph.add_edge("communication_node", "operator_impact_node")
    graph.add_edge("operator_impact_node", END)
    return graph.compile()


rentas_graph = build_graph()
