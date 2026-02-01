from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from config.state import State
from nodes.calculation_nodes import calculation_retriever_node, calculation_fallback_node, \
    calculation_answer_node, MathVerificationNode
from nodes.StartingIntentionNode import StartingIntentionNode
from nodes.child_graph_nodes import rewrite_query_node
from nodes.other_nodes import starting_reply_node, fallback_node
from nodes.standard_comparison_nodes import ComparisonRetrieverNode, StandardRetrieverNode, GenerateNode, \
    comparison_rewrite_query_node, reply_with_generation_node
from routes.calculation_routes import math_verification_route, calculation_retriever_route
from routes.route_functions import generate_node_route, shortcut_retriever_route
from nodes.shortcut_nodes import ShortcutRetrieverNode
from routes.starting_routes import start_route, starting_intention_route
from utils.log_utils import log

def build_adaptive_rag_graph():

    # -------- Build the graph --------
    graph = StateGraph(State)

    # -------- Prepare nodes --------
    starting_intention_node = StartingIntentionNode()
    shortcut_retriever_node = ShortcutRetrieverNode()
    math_verification_node = MathVerificationNode()
    comparison_retriever_node = ComparisonRetrieverNode()
    standard_retriever_node = StandardRetrieverNode()
    generate_node = GenerateNode()

    # -------- Add starting nodes --------
    graph.add_node("starting_reply_node", starting_reply_node)
    graph.add_node("starting_intention_node", starting_intention_node)

    # -------- Add shortcut nodes --------
    graph.add_node("shortcut_retriever_node", shortcut_retriever_node)

    # -------- Add calculation nodes --------
    graph.add_node("calculation_retriever_node", calculation_retriever_node)
    graph.add_node("math_verification_node", math_verification_node)
    graph.add_node("calculation_fallback_node", calculation_fallback_node)
    graph.add_node("calculation_answer_node", calculation_answer_node)

    # -------- Add comparison nodes --------
    graph.add_node("comparison_retriever_node", comparison_retriever_node)
    graph.add_node("comparison_rewrite_query_node", comparison_rewrite_query_node)

    # -------- Add standard nodes --------
    graph.add_node("standard_retriever_node", standard_retriever_node)
    graph.add_node("generate_node", generate_node)
    graph.add_node("rewrite_query_node", rewrite_query_node)
    graph.add_node("reply_with_generation_node", reply_with_generation_node)

    # -------- Add other nodes --------
    graph.add_node("fallback_node", fallback_node)

    # -------- Add edges --------
    graph.add_conditional_edges(START, start_route)
    graph.add_edge("starting_reply_node", END)
    graph.add_conditional_edges(
        "starting_intention_node",
        starting_intention_route,
        {
            "shortcut_agent":"shortcut_retriever_node",
            "calculation_agent": "calculation_retriever_node",
            "comparison_agent": "comparison_retriever_node",
            "standard_agent": "standard_retriever_node",
            "fallback":"fallback_node"
        }
    )
    # -------- Add shortcut edges --------
    graph.add_conditional_edges("shortcut_retriever_node", shortcut_retriever_route)

    # -------- Add calculation edges --------
    graph.add_conditional_edges("calculation_retriever_node", calculation_retriever_route)
    graph.add_conditional_edges(
        "math_verification_node",
        math_verification_route,
        {
            "calculation_answer_node":"calculation_answer_node",
            "math_verification_node":END, # Let user input, then redirect to math_verification_node
            "calculation_fallback_node":"calculation_fallback_node"
        }
    )
    graph.add_edge("calculation_answer_node", END)
    graph.add_edge("calculation_fallback_node", END)

    # -------- Add comparison retriever edges --------
    graph.add_edge("comparison_retriever_node", "generate_node")

    # -------- Add standard retriever edges --------
    graph.add_edge("standard_retriever_node", "generate_node")
    graph.add_conditional_edges(
        "generate_node",
        generate_node_route,
        {
            "not supported": "generate_node",
            "useful": "reply_with_generation_node",
            "not useful": "comparison_rewrite_query_node",
        }
    )
    graph.add_edge("comparison_rewrite_query_node", "comparison_retriever_node")
    graph.add_edge("reply_with_generation_node", END)
    graph.add_edge("fallback_node", END)

    log.info("The graph has been successfully built.")
    return graph.compile(checkpointer=MemorySaver())
