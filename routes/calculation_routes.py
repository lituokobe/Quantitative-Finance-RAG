# -------- Import dependencies --------
from langchain_core.messages import AIMessage
from langgraph.constants import END

from config.state import State
from chains.answer_grader_chain import answer_grader_chain
from chains.hallucination_grader_chain import hallucination_grader_chain
from utils.log_utils import log

# -------- Create the route function after calculation retriever node --------
def calculation_retriever_route(state: State):
    logs = state.get("logs", [])
    if not logs:
        return "calculation_fallback_node" # safety check, should not happen
    last_log: dict = logs[-1] # should also be starting intention node

    retrieved_documents = last_log.get("retrieved_documents", [])
    if not retrieved_documents:
        return "calculation_fallback_node" # safety check
    return "math_verification_node"

# -------- Create the route function after math verification node --------
def math_verification_route(state: State):
    dialog_states = state.get("dialog_state", [])
    if not dialog_states:
        return "calculation_fallback_node"  # safety check, should not happen
    last_dialog_state: str = dialog_states[-1]
    return last_dialog_state