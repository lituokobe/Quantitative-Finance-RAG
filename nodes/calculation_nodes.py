import time
from typing import Literal

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from config.state import State
from models.models import agent_llm
from tools.retriever_tools import create_hybrid_retriever
from utils.log_utils import log, log_node_start, log_node_end
from utils.utils import get_last_user_message


def calculation_retriever_node(state: State):
    prev_time = time.time()
    node_name = "calculation_retriever_node"
    log_node_start(node_name)

    # ------------------ Get user question ------------------
    try:
        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
        if last_log:
            question = last_log.get("question", "")
        else:
            question = ""
    except Exception as e:
        log.error(f"{node_name} fails to get user question: {e}")
        last_log = {}
        question = ""

    # ------------------ Retrieve math results only ------------------
    try:
        math_retriever = create_hybrid_retriever(
            k=10,
            score_threshold=0.05, # High recall
            filter_dict={"contains_math": True}, # Math only. But this only applies to vector search, BM25 won't follow. There will be none-math docs in the results as well.
        )
        documents = math_retriever.invoke(question)
    except Exception as e:
        log.error(f"{node_name} has error when retrieving documents: {e}")
        raise

    time_cost = round(time.time() - prev_time, 3)
    current_log = {
        **last_log,
        "node": node_name,
        "retrieved_documents": documents,
        "time_cost": time_cost
    }

    log_node_end(node_name, time_cost)

    return {
        "logs": state.get("logs", []) + [current_log]
    }

def calculation_fallback_node(state: State):
    node_name = "calculation_fallback_node"
    log_node_start(node_name)

    # ------------------ Get last log ------------------
    try:
        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
    except Exception as e:
        log.error(f"{node_name} fails to get last log: {e}")
        last_log = {}

    # ------------------ Generate reply ------------------
    ai_message = "Sorry, this calculation is beyond my knowledge scope."

    current_log = {
        **last_log,
        "node": node_name,
        "agent_reply": ai_message
    }

    log_node_end(node_name)
    return {
        "messages": AIMessage(content=ai_message),
        "dialog_state": "starting_intention_node", # Start again from starting_intention_node
        "logs": state.get("logs", []) + [current_log]
    }

def retriever_node(state):
    try:
        log.info("retriever_node starts to work.")

        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
        if last_log:
            question = last_log.get("question", "")
        else:
            question = ""

        retriever = create_hybrid_retriever()
        documents = retriever.invoke(question)

        current_log = {
            **last_log,
            "node": "retriever_node",
            "retrieved_documents": documents,
        }

        log.info("retriever_node finishes working.")
        return {
            "dialog_state": "document_grader_node",
            "logs": state.get("logs", []) + [current_log]
        }
    except Exception as e:
        log.error(f"retriever_node has error: {e}")
        raise

# Test
if __name__ == "__main__":
    # ----------------- Calculation Retriever test -----------------
    Q1 = "What is an option?"
    result1 = calculation_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q1}]
        }
    )
    print(f"Question:{Q1}")
    documents = result1["logs"][-1].get("retrieved_documents", [])
    print(f"{len(documents)} documents retrieved: ")
    for doc in documents:
        print(f"Contains math: {doc.metadata['contains_math']}")
        print(doc.page_content)
        print("--------")

    Q2 = "What is the formula for SMA?"
    result2 = calculation_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q2}]
        }
    )
    print(f"Question:{Q2}")
    documents = result2["logs"][-1].get("retrieved_documents", [])
    print(f"{len(documents)} documents retrieved: ")
    for doc in documents:
        print(f"Contains math: {doc.metadata['contains_math']}")
        print(doc.page_content)
        print("--------")

    Q3 = "What is ROE if NPM is 30$?"
    result3 = calculation_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q3}]
        }
    )
    print(f"Question:{Q3}")
    documents = result3["logs"][-1].get("retrieved_documents", [])
    print(f"{len(documents)} documents retrieved: ")
    for doc in documents:
        print(f"Contains math: {doc.metadata['contains_math']}")
        print(doc.page_content)
        print("--------")