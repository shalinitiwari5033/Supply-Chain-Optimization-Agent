from langgraph.graph import StateGraph, START, END

from agents.state import SupplyChainState

from agents.data_processing_agent import data_processing_agent
from agents.demand_forecasting_agent import demand_forecasting_agent
from agents.inventory_optimization_agent import inventory_optimization_agent
from agents.supplier_analysis_agent import supplier_analysis_agent
from agents.decision_agent import decision_agent


def build_supply_chain_graph():

    graph = StateGraph(SupplyChainState)

    # Add agents as nodes
    graph.add_node(
        "data_processing",
        data_processing_agent
    )

    graph.add_node(
        "demand_forecasting",
        demand_forecasting_agent
    )

    graph.add_node(
        "inventory_optimization",
        inventory_optimization_agent
    )

    graph.add_node(
        "supplier_analysis",
        supplier_analysis_agent
    )

    graph.add_node(
        "decision",
        decision_agent
    )

    # Workflow
    graph.add_edge(
        START,
        "data_processing"
    )

    graph.add_edge(
        "data_processing",
        "demand_forecasting"
    )

    graph.add_edge(
        "demand_forecasting",
        "inventory_optimization"
    )

    graph.add_edge(
        "inventory_optimization",
        "supplier_analysis"
    )

    graph.add_edge(
        "supplier_analysis",
        "decision"
    )

    graph.add_edge(
        "decision",
        END
    )

    return graph.compile()