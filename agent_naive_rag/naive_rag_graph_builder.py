from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from config.state import State
from nodes.AgentNode import AgentNode
from nodes.StartingIntentionNode import StartingIntentionNode
from nodes.other_nodes import fallback_node, hang_up, starting_reply_node
from utils.log_utils import log


def build_naive_rag_graph():
    #-------- Create the route function before starting of each round of conversation --------
    def start_route(state: State) -> str:
        dialog_state = state.get("dialog_state", [])
        if not dialog_state:  # At the beginning, send to the first node
            return "starting_reply_node"
        elif dialog_state[-1] == "hang_up":
            return END
        else:
            return dialog_state[-1]

    #-------- Create the route function after starting node --------
    def starting_intention_route(state: State) -> str:
        dialog_state = state.get("dialog_state", [])
        if not dialog_state:
            return "starting_reply_node"
        last_dialog_state: str = dialog_state[-1]
        if not last_dialog_state or last_dialog_state == "hang_up":
            return "hang_up"
        return last_dialog_state

    #-------- Build the graph --------
    graph = StateGraph(State)

    starting_intention_node = StartingIntentionNode()
    agent_node = AgentNode()

    graph.add_node("starting_reply_node", starting_reply_node)
    graph.add_node("starting_intention_node", starting_intention_node)
    graph.add_node("agent_node", agent_node)
    graph.add_node("fallback_node", fallback_node)
    graph.add_node("hang_up", hang_up)

    graph.add_conditional_edges(START, start_route)
    graph.add_edge("starting_reply_node", END)
    graph.add_conditional_edges("starting_intention_node", starting_intention_route)
    graph.add_edge("fallback_node", END)
    graph.add_edge("agent_node", END)
    graph.add_edge("hang_up", END)

    log.info("The graph has been successfully built.")
    return graph.compile(checkpointer=MemorySaver())
