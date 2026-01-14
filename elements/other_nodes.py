from langchain_core.messages import AIMessage
from config.state import State
from utils.log_utils import log
from utils.utils import get_last_user_message

# Function for the hang_up node in every thread
def hang_up(state: State) -> dict:
    log.info("The conversation is over. Thank you for your time.")
    return {
        "messages": state["messages"],
        "dialog_state": None,
        "logs": state["logs"],
    }

def starting_reply_node(state: State):
    try:
        log.info("starting_reply_node starts to work.")
        ai_message = "Hi, I am your Quantitative Finance Assistant. You can ask me anything about quantitative finance."
        log.info("starting_reply_node finishes working.")
        return {
            "messages": state.get("messages", []) + [AIMessage(content=ai_message)],
            "dialog_state": "starting_intention_node",
            "logs":state.get("logs", [])
        }
    except Exception as e:
        log.error(f"starting_reply_node has error: {e}")
        raise

def fallback_node(state: State):
    try:
        log.info("fallback_node starts to work.")

        messages = state.get("messages", [])
        user_input = get_last_user_message(messages)
        ai_message = "Sorry, I can only answer questioned related to quantitative finance."

        current_log = {
            "node": "fallback_node",
            "user_input": user_input,
            "agent_reply": ai_message
        }

        log.info("fallback_node finishes working.")
        return {
            "messages": state["messages"] + [AIMessage(content=ai_message)],
            "dialog_state": "starting_intention_node",
            "logs": state.get("logs", []) + [current_log]
        }
    except Exception as e:
        log.error(f"fallback_node has error: {e}")
        raise
