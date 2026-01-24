# -------- Create the route function before starting of each round of conversation --------
from langgraph.constants import END

from config.state import State
from elements.answer_grader_chain import answer_grader_chain
from elements.hallucination_grader_chain import hallucination_grader_chain
from utils.log_utils import log


def start_route(state: State) -> str:
    dialog_state = state.get("dialog_state", [])
    if not dialog_state:  # At the beginning, send to the first node
        return "starting_reply_node"
    elif dialog_state[-1] == "hang_up":
        return END
    else:
        return dialog_state[-1]

# -------- Create the route function after starting node --------
def starting_intention_route(state: State) -> str:
    dialog_state = state.get("dialog_state", [])
    if not dialog_state:
        return "fallback_node"
    # Get the last dialog state from stating_intention_node
    last_dialog_state: str = dialog_state[-1]

    # If no last dialog state is empty string or not regular
    if not last_dialog_state or last_dialog_state not in ["agent_node", "fallback_node"]:
        return "fallback_node"
    return last_dialog_state

# -------- Create the route function after grading documents --------
def grade_documents_route(state: State):
    """
    Decide to generated answer or to reoptimize question
    :param state: current graph state, including filtered documents
    :return: name of next node (transform_query or generate)
    """
    log.info("---ASSESS GRADED DOCUMENTS---")

    logs = state.get("logs", [])
    last_log = logs[-1] if logs else {}

    if last_log:
        filtered_docs = last_log.get("filtered_docs", [])
    else:
        filtered_docs = []

    rewrite_count = last_log.get("rewrite_count", 0)

    if not filtered_docs:
        if rewrite_count >= 2:
            log.info("---Decision: all documents are not relevant, and looped twice, need to redo web search---")
            return "web_search_node"
        log.info("---Decision: all documents are not relevant, need to convert questions---")
        return "rewrite_query_node"
    else:
        log.info("---Decision: generate final answer---")
        return "generate_node"

# -------- Create the route function after generating content --------
def generate_node_route(state: State):
    """
    Evaluate if the generated result is based on documents and answers the question.
    :param state: current graph state, including user question, documents, and generated results
    :return: name of next node (useful, not useful or not supported)
    """
    log.info("---Check if generated result has hallucination---")

    logs = state.get("logs", [])
    last_log = logs[-1] if logs else {}
    if logs:
        question = last_log.get("question", "")
        documents = last_log.get("filtered_docs", []) or last_log.get("web_results", [])
        generation = last_log.get("generation", "")
    else:
        question = ""
        documents = []
        generation = ""

    # check if generated result is based on documents
    score = hallucination_grader_chain.invoke({"documents": documents, "generation": generation})
    grade = score.binary_score

    if grade == 'yes':
        log.info("---Decision: generated result is based on documents---")

        # check if generated result solves the problem from the question
        log.info("---Check if generated result solves the problem from the question---")
        score = answer_grader_chain.invoke({"question": question, "generation": generation})
        grade = score.binary_score

        if grade == 'yes':
            log.info("---Decision: generated result solves the problem from the question---")
            return "useful"

        else:
            log.info("---Decision: generated result does not solve the problem from the question---")
            return "not useful"
    else:
        log.info("---Decision: generated result is not based on documents, will try again---")
        return "not supported"