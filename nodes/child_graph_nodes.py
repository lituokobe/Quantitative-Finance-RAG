import time
from chains.rewrite_chain import rewrite_chain
from config.state import ChildState
from tools.retriever_tools import create_hybrid_retriever
from utils.log_utils import log_node_start, log, log_node_end
from langchain_core.documents import Document
from models.models import web_search_tool

def retriever_node(state: ChildState):
    prev_time = time.time()
    node_name = "child graph - retriever_node"
    log_node_start(node_name)

    # ----------- Retrieve documents from Milvus -----------
    question = state.get("question", "")
    try:
        retriever = create_hybrid_retriever()
        retrieved_documents: list = retriever.invoke(question)
    except Exception as e:
        log.error(f"{node_name} has error on retrieving documents for question \"{question}\": {e}")
        retrieved_documents = []

    print(f"{node_name} - retrieved documents: /n {retrieved_documents}")

    time_cost = round(time.time() - prev_time, 3)
    log_node_end(node_name, time_cost)
    return {
        "retrieved_documents" : retrieved_documents
    }

def rewrite_query_node(state: ChildState) -> dict:
    prev_time = time.time()
    node_name = "child graph - rewrite_query_node"
    log_node_start(node_name)

    question = state.get("question", "")
    rewrite_count = state.get("rewrite_count", 0)

    # --------- Rewrite the question ---------
    try:
        optimized_question = rewrite_chain.invoke({"question":question})
    except Exception as e:
        log.error(f"{node_name} has error on rewriting question \"{question}\": {e}")
        optimized_question = question

    print(f"After rewriting, the question becomes {optimized_question}.")

    time_cost = round(time.time() - prev_time, 3)
    log_node_end(node_name, time_cost)

    return {
        "question" : optimized_question,
        "rewrite_count": int(rewrite_count + 1)
    }

def web_search_node(state: ChildState) -> dict:
    prev_time = time.time()
    node_name = "child graph - web_search_node"
    log_node_start(node_name)
    question = state.get("question", "")

    # ------- search web content ----------
    try:
        web_results_raw = web_search_tool.invoke(question)
        # print(web_results_raw)
        web_results_string = "\n".join(
            d.get("content", "") for d in web_results_raw.get("results", [])
        )

        web_results = Document(page_content = web_results_string)
    except Exception as e:
        log.error(f"{node_name} has error searching web result on question \"{question}\": {e}")
        web_results = Document(page_content = "")

    time_cost = round(time.time() - prev_time, 3)
    log_node_end(node_name, time_cost)

    return {
        "web_results": web_results
    }

# Test
if __name__ == "__main__":
    # test_state = retriever_node(
    #     {
    #         "question": "What is Black Scholes Model?",
    #         "retrieved_documents":[],
    #         "filtered_docs":[],
    #         "rewrite_count":0,
    #         "web_results":Document(page_content="")
    #     }
    # )

    test_state = web_search_node(
        {
            "question": "What is Black Scholes Model?",
            "retrieved_documents":[],
            "filtered_docs":[],
            "rewrite_count":0,
            "web_results":Document(page_content="")
        }
    )

    print(test_state)