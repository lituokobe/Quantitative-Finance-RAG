from langchain_core.messages import AIMessage
from config.state import State
from utils.log_utils import log, log_node_start, log_node_end
from utils.utils import get_last_user_message

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
    node_name = "fallback_node"
    log_node_start(node_name)
    try:
        messages = state.get("messages", [])
        user_input = get_last_user_message(messages)
    except Exception as e:
        log.error(f"{node_name} has error to fetch the last user message: {e}")
        raise

    ai_message = "Sorry, I can only answer questions related to quantitative finance."

    current_log = {
        "node": node_name ,
        "user_input": user_input,
        "agent_reply": ai_message
    }

    log_node_end(node_name)
    return {
        "messages": AIMessage(content=ai_message),
        "dialog_state": "starting_intention_node",
        "logs": state.get("logs", []) + [current_log]
    }