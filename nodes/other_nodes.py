from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from config.state import State
from models.models import agent_llm, web_search_tool
from utils.log_utils import log, log_node_start, log_node_end
from utils.utils import get_last_user_message

# Function for the hang_up node in every thread
def hang_up(state: State) -> dict:
    node_name = "hang_up"
    log_node_start(node_name)
    ai_message = "The conversation is over. Thank you for chatting with me."
    current_log = {
        "node": node_name,
        "agent_reply": ai_message
    }
    log_node_end(node_name)
    return {
        "messages": AIMessage(content=ai_message),
        "logs": state.get("logs", []) + [current_log] # For hang_up node, no need to include previous node's log
    }

def starting_reply_node(state: State) -> dict:
    node_name = "starting_reply_node"
    log_node_start(node_name)
    ai_message = "Hi, I am your Quantitative Finance Assistant. You can ask me anything about quantitative finance."
    current_log = {
        "node": node_name,
        "agent_reply": ai_message
    }
    log_node_end(node_name)
    return {
        "messages": AIMessage(content=ai_message),
        "dialog_state": "starting_intention_node",
        "logs": state.get("logs", []) + [current_log] # For starting nodes, no need to include previous node's log
    }

def fallback_node(state: State) -> dict:
    log.info("fallback_node starts to work.")
    try:
        messages = state.get("messages", [])
        user_input = get_last_user_message(messages)
    except Exception as e:
        log.error(f"fallback_node has error to fetch the last user message: {e}")
        raise

    ai_message = "Sorry, I can only answer questioned related to quantitative finance."

    current_log = {
        "node": "fallback_node",
        "user_input": user_input,
        "agent_reply": ai_message
    }

    log.info("fallback_node finishes working.")
    return {
        "messages": AIMessage(content=ai_message),
        "dialog_state": "starting_intention_node",
        "logs": state.get("logs", []) + [current_log]
    }


def generate_node(state: State) -> dict:
    log.info("generate_node starts to work.")

    logs = state.get("logs", [])
    last_log = logs[-1] if logs else {}
    if logs:
        question = last_log.get("question", "")
        documents = last_log.get("filtered_docs", []) or last_log.get("web_results", [])
    else:
        question = ""
        documents = []

    prompt = PromptTemplate(
        template="You are an assistant to help user answer questions. Please answer the question based on the context. If you cannot find the answer in the context, please politely say you don't know the answer. Keep the answer concise. \nQuestion：{question} \nContext：{context} \nAnswer：",
        input_variables=["question", "context"],
    )

    # after-process function - format documents after retrieval
    def format_docs(docs):
        """Merge all documents into one string with 2 change lines as separator"""
        if isinstance(docs, list):
            return "\n\n".join(doc.page_content for doc in docs)
        else:
            return "\n\n" + docs.page_content


    #process chain
    rag_chain = prompt | agent_llm | StrOutputParser()

    #execute
    generation = rag_chain.invoke(
        {
            "context": format_docs(documents),
            "question": question,
        }
    )

    current_log = {
        **last_log,
        "node": "generate_node",
        "generation":generation,
    }

    log.info("generate_node finishes working.")

    return {
        "logs": state.get("logs", []) + [current_log]
    }

def reply_with_generation_node(state: State):
    log.info("reply_with_generation_node starts to work.")

    logs = state.get("logs", [])
    last_log = logs[-1] if logs else {}
    if logs:
        generation = last_log.get("generation", "")
    else:
        generation = ""

    current_log = {
        **last_log,
        "node": "reply_with_generation_node",
    }

    log.info("reply_with_generation_node finishes working.")

    return {
        "messages": AIMessage(content = generation),
        "dialog_state":"starting_intention_node",
        "logs": state.get("logs", []) + [current_log]
    }