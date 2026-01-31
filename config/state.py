from typing import TypedDict, Annotated
from langchain_core.documents import Document
from langgraph.graph import add_messages

# Reducer function to edit dialog_state in ChatState
def update_dialog_state(left: list[str], right: str | None)->list[str]:
    """
    Update the dialog state stack
    :param left: current state stack
    :param right: new state or action to add to the stack. If none, no action;
                  if 'pop', pop up the top (last one) of the stack; otherwise add it to the stack.
    :return: updates stack
    """
    if right is None:
        return left
    if right == 'pop':
        return left[:-1] #remove the last one of the stack
    if isinstance(right, list):
        return left + right
    if isinstance(right, str):
        return left + [right]
    return left  # fallback

class State(TypedDict):
    messages: Annotated[list[dict], add_messages]
    dialog_state: Annotated[
        list[str],
        update_dialog_state
    ]
    logs: list[dict]
    """
    Structure of one dict item in logs
    - node: str # the node outputting this item
    - time_cost: float # the processing time of the node
    - user_input: str # original user input, ingested in starting_intention_node
    - question: str # rephrased question, ingested in starting_intention_node
    - agent_reply: str # agent's reply, ingested by shortcut_retriever_node, math_verification_node, calculation_fallback_node, calculation_answer_node
    - retrieved_documents: list[Documents] # ingested by calculation_retriever_node, comparison_retriever_node, standard_retriever_node
    """

class ChildState(TypedDict):
    question: str
    retrieved_documents: list
    filtered_docs: list
    rewrite_count: int
    web_results: Document
