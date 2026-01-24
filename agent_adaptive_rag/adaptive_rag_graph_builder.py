from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from config.state import State
from elements.document_grader_node import document_grader_node
from elements.RetrieverNode import retriever_node
from elements.StartingIntentionNode import StartingIntentionNode
from elements.other_nodes import starting_reply_node, rewrite_query_node, web_search_node, fallback_node, hang_up, \
    generate_node, reply_with_generation_node
from elements.route_functions import start_route, starting_intention_route, grade_documents_route, generate_node_route
from utils.log_utils import log

def build_adaptive_rag_graph():

    # -------- Build the graph --------
    graph = StateGraph(State)

    starting_intention_node = StartingIntentionNode()

    # add nodes
    graph.add_node("starting_reply_node", starting_reply_node)
    graph.add_node("starting_intention_node", starting_intention_node)
    graph.add_node("fallback_node", fallback_node)
    graph.add_node("retriever_node", retriever_node)
    graph.add_node("document_grader_node", document_grader_node)
    graph.add_node("rewrite_query_node", rewrite_query_node)
    graph.add_node("generate_node", generate_node)
    graph.add_node("reply_with_generation_node", reply_with_generation_node)
    graph.add_node("web_search_node", web_search_node)
    graph.add_node("hang_up", hang_up)

    # add edges
    graph.add_conditional_edges(START, start_route)
    graph.add_edge("starting_reply_node", END)
    graph.add_conditional_edges(
        "starting_intention_node",
        starting_intention_route,
        {
            "agent_node":"retriever_node", # If he intention node decide to go to the agent, we start from retriever node
            "fallback_node":"fallback_node"
        }
    )
    graph.add_edge("retriever_node", "document_grader_node")

    graph.add_conditional_edges(
        "document_grader_node",
        grade_documents_route
    )
    graph.add_edge("rewrite_query_node", "retriever_node")
    graph.add_edge("web_search_node", "generate_node")
    graph.add_conditional_edges(
        "generate_node",
        generate_node_route,
        {
            "not supported": "generate_node",
            "useful": "reply_with_generation_node",
            "not useful": "rewrite_query_node",
        }
    )
    graph.add_edge("reply_with_generation_node", END)
    graph.add_edge("fallback_node", END)
    graph.add_edge("hang_up", END)

    log.info("The graph has been successfully built.")
    return graph.compile(checkpointer=MemorySaver())
