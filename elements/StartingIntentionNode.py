from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from config.prompts import INTENTION_PROMPT1, INTENTION_PROMPT2, INTENTION_PROMPT3
from config.state import State
from models.models import agent_llm
from utils.log_utils import log
from utils.utils import get_last_user_message


class Intention(BaseModel):
    decision: Literal["agent_node", "fallback_node"]

class StartingIntentionNode:
    def __init__(self):
        self.llm_runnable = agent_llm.with_structured_output(Intention)

    @staticmethod
    def _build_history_prompt(chat_history:list) -> list:
        doc_string_chat_history = []
        for msg in chat_history:
            if isinstance(msg, HumanMessage):
                doc_string_chat_history.append(f"  -[User]: {msg.content}")
            elif isinstance(msg, AIMessage):
                ai_message = msg.content
                if ai_message:
                    doc_string_chat_history.append(f"  -[AI assistant]: {ai_message}")
        doc_string_chat_history.append("")
        return doc_string_chat_history

    def _infer(self, chat_history:list, user_input:str) -> str:
        log.info("starting_intention_node starts to work.")
        if not self.llm_runnable:
            log.error("Agent LLM is not ready")
            return "fallback_node"
        try:
            history_prompt = self._build_history_prompt(chat_history)
            doc_string = INTENTION_PROMPT1 + [user_input] + INTENTION_PROMPT2 +  history_prompt +INTENTION_PROMPT3
            full_prompt = "\n".join(doc_string)
            print(f"Full prompt to identify intention:\n{full_prompt}")

        except Exception as e:
            log.error(f"Error formulating prompt for starting_intention_node: {e}")

        try:
            resp = self.llm_runnable.invoke([HumanMessage(content=full_prompt)])
            decision: str = resp.decision
            log.info("starting_intention_node ends working.")
            return decision
        except Exception as e:
            log.error(f"Error generating decision for starting_intention_node: {e}")

    def __call__(self, state: State, config: RunnableConfig) -> dict:
        try:
            log.info("starting_intention_node starts to work.")

            messages = state.get("messages", [])
            user_input = get_last_user_message(messages)

            decision: str = self._infer(messages, user_input)

            current_log = {
                "node": "starting_intention_node",
                "user_input": user_input,
                "agent_reply": ""
            }

            log.info("starting_intention_node finishes working.")
            return {
                "messages": state["messages"],
                "dialog_state": decision,
                "logs": state["logs"] + [current_log]
            }
        except Exception as e:
            log.error(f"starting_intention_node has error: {e}")
            raise

if __name__ == "__main__":
    intention_identifier = StartingIntentionNode()
    result = intention_identifier._infer([], "I want to know what is a banana")
    print(result)