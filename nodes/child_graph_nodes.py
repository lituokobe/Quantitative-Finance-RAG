import time
from config.state import ChildState
from tools.retriever_tools import create_hybrid_retriever
from utils.log_utils import log_node_start, log, log_node_end
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from models.models import agent_llm, web_search_tool


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

def rewrite_query_node(state: ChildState) -> dict:
    prev_time = time.time()
    node_name = "child graph - rewrite_query_node"
    log_node_start(node_name)

    question = state.get("question", "")
    rewrite_count = state.get("rewrite_count", 0)

    system_prompt = """
    You are a query rewriter. Please rewrite the question with optimization for answer-retrieval in a vector database.
    Before rewriting, please analyse and comprehend the true meaning and intention behind the question.
    """

    rewrite_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                "This is the question to rewrite: \n{question}\n\n Please generate an optimized version"
            )
        ]
    )
    question_rewriter = rewrite_prompt | agent_llm | StrOutputParser()

    optimized_question = question_rewriter.invoke({"question":question})

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


    web_results_raw = web_search_tool.invoke({"query":question})
    web_results_string = "\n".join(d["content"] for d in web_results_raw)
    web_results = Document(page_content = web_results_string)

    time_cost = round(time.time() - prev_time, 3)
    log_node_end(node_name, time_cost)

    return {
        "web_results": web_results
    }