import time
from config.state import ChildState
from tools.retriever_tools import create_hybrid_retriever
from utils.log_utils import log_node_start, log, log_node_end


def retriever_node(state: ChildState):
    prev_time = time.time()
    node_name = "child graph - retriever_node"
    log_node_start(node_name)

    # ----------- Retrieve documents from Milvus -----------
    try:
        question = state.get("question", "")

        retriever = create_hybrid_retriever()
        retrieved_documents: list = retriever.invoke({"question":question})

    except Exception as e:
        log.error(f"{node_name} has error: {e}")
        retrieved_documents = []

    time_cost = round(time.time() - prev_time, 3)
    log_node_end(node_name, time_cost)
    return {
        "retrieved_documents" : retrieved_documents
    }
