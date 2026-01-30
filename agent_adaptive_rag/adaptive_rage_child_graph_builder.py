from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from config.state import ChildState
from nodes.DocumentGraderNode import DocumentGraderNode
from nodes.child_graph_nodes import retriever_node
from nodes.other_nodes import rewrite_query_node
from routes.route_functions import grade_documents_route
from utils.log_utils import log


# The child graph of modularized adaptive rag service
def build_adaptive_child_rag_graph():

    # -------- Build the graph --------
    graph = StateGraph(ChildState)

    # add nodes
    document_grader_node = DocumentGraderNode()
    graph.add_node("retriever_node", retriever_node)
    graph.add_node("document_grader_node", document_grader_node)
    graph.add_node("rewrite_query_node", rewrite_query_node)
    graph.add_node("generate_node", generate_node)
    graph.add_node("reply_with_generation_node", reply_with_generation_node)
    graph.add_node("web_search_node", web_search_node)
    graph.add_node("hang_up", hang_up)

    # add edges
    graph.add_edge(START, "retriever_node")
    graph.add_edge("retriever_node", "document_grader_node")

    graph.add_conditional_edges(
        "document_grader_node",
        grade_documents_route,
        {
            "END":END
        }
    )
    graph.add_edge("rewrite_query_node", "retriever_node")
    graph.add_edge("web_search_node", END)

    graph.add_edge("reply_with_generation_node", END)

    log.info("The adaptive RAG child graph has been successfully built.")
    return graph.compile(checkpointer=MemorySaver())