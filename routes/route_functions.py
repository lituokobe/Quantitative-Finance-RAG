# -------- Create the route function before starting of each round of conversation --------
from langchain_core.messages import AIMessage
from langgraph.constants import END

from config.state import State
from chains.answer_grader_chain import answer_grader_chain
from chains.hallucination_grader_chain import hallucination_grader_chain
from utils.log_utils import log


# -------- Create the route function after shortcut retriever node --------
def shortcut_retriever_route(state: State):
    dialog_states = state.get("dialog_state", [])
    if not dialog_states:
        return "starting_intention_node" # safety check, should not happen
    last_dialog_state: str = dialog_states[-1] # should also be starting intention node

    messages = state.get("messages", [])
    if not messages:
        return "starting_intention_node" # safety check, should not happen
    last_message = messages[-1]

    if not isinstance(last_message, AIMessage):
        return "starting_intention_node"  # safety check, should not happen
    last_message_content = last_message.content

    if not last_message_content: # meaning the shortcut_retriever_node can't answer the question
        return last_dialog_state
    return END #shortcut_retriever_node has a reply, go to end first to output the reply and let user speak. But next round will start from starting_intention_node as well.

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