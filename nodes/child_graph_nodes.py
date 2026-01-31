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
    question = state.get("question", "")
    try:
        retriever = create_hybrid_retriever()
        retrieved_documents: list = retriever.invoke(question)
    except Exception as e:
        log.error(f"{node_name} has error on retrieving documents for question \"{question}\": {e}")
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

    # --------- Prepare the rewriter chain ---------
    system_prompt = """
    ## === YOUR ROLE ===
    You are a query rewriter. You rewrite the question with optimization for answer-retrieval in a vector database.
    
    ## === YOUR CORE TASK ===
    You will be given a question, please:
    - analyse and comprehend the true meaning and intention behind the question.
    - rewrite the question to keep its original intention and meaning but with better wordings for retrieval in vector database.
    
    ## === IMPORTANT RULES ===
    - **Only output the optimized question alone**, don't add any extra words including introductory text, explanation, summary, etc.
    - **Don't conduct any conversation**, only output the optimized question.
    
    ## === OUTPUT EXAMPLES ===
    - If you are given the question: "What is a put option?", output "What is the definition of put option?"
    - If you are given the question: "What did the financial crisis do to the world?", output "What are the impacts of the financial crisis to the world?"
    """

    rewrite_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "This is the question to rewrite: \n{question}\n\n Please generate an optimized version")
    ])
    question_rewriter = rewrite_prompt | agent_llm | StrOutputParser()

    # --------- Rewrite the question ---------
    try:
        optimized_question = question_rewriter.invoke({"question":question})
    except Exception as e:
        log.error(f"{node_name} has error on rewriting question \"{question}\": {e}")
        optimized_question = question

    print(f"After rewrting, the question becomes {optimized_question}.")

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
    # state = retriever_node(
    #     {
    #         "question": "What is Black Scholes Model?"
    #     }
    # )

    state = web_search_node(
        {
            "question": "What is Black Scholes Model?"
        }
    )

    print(state)