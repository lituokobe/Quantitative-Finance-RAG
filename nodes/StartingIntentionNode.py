import time
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from config.prompts import INTENTION_PROMPT1, INTENTION_PROMPT2, INTENTION_PROMPT3
from config.state import State
from utils.build_prompt import build_history_prompt
from models.models import agent_llm
from utils.log_utils import log, log_node_start, log_node_end
from utils.utils import get_last_user_message

class Intention(BaseModel):
    """
    Data class to regulate the output of the LLM for intention identifying.
    """
    question: str
    decision: Literal[
        "standard_agent",
        "shortcut_agent",
        "calculation_agent",
        "comparison_agent",
        "fallback"
    ]

class StartingIntentionNode:
    def __init__(self):
        # Initiate the agent with structured output
        self.llm_runnable_structured_output = agent_llm.with_structured_output(Intention)
        self.node_name = "starting_intention_node"

    def _infer(self, history:list, user_input:str):
        # -------- check the availability of the agent LLM --------
        if not self.llm_runnable_structured_output:
            log.error(f"Agent LLM at {self.node_name} is not ready.")
            return user_input, "fallback_node"

        # -------- Formulate the full prompt with dynamic chat data --------
        try:
            history_prompt = build_history_prompt(history)
            doc_string = INTENTION_PROMPT1 + history_prompt + INTENTION_PROMPT2 + [user_input] + INTENTION_PROMPT3
            full_prompt = "\n".join(doc_string)
            print(f"Full prompt at {self.node_name} to identify intention:\n{full_prompt}")

        except Exception as e:
            log.error(f"Error formulating prompt at {self.node_name}: {e}")
            full_prompt = user_input

        # -------- Use the agent LLM to identify intention with the full prompt --------
        try:
            resp = self.llm_runnable_structured_output.invoke([HumanMessage(content=full_prompt)])
            question: str = resp.question
            decision: str = resp.decision
            return question, decision
        except Exception as e:
            log.error(f"Error generating decision at {self.node_name}: {e}")
            return user_input, "fallback_node"

    def __call__(self, state: State, config: RunnableConfig) -> dict:
        prev_time = time.time()
        log_node_start(self.node_name)

        # -------- Get data from state --------
        messages = state.get("messages", [])
        user_input = get_last_user_message(messages)

        # -------- Rephrase the user input and identify intention --------
        try:
            question, decision = self._infer(messages, user_input)
            time_cost = round(time.time() - prev_time, 3)
            current_log = { # For starting nodes, no need to include previous node's log
                "node": "starting_intention_node",
                "time_cost": time_cost,
                "user_input": user_input,
                "question": question,
            }
            log_node_end(self.node_name, time_cost)
            return {
                "dialog_state": decision,
                "logs": state["logs"] + [current_log]
            }
        except Exception as e:
            log.error(f"{self.node_name} has error: {e}")
            raise

if __name__ == "__main__":
    intention_identifier = StartingIntentionNode()
    decision1, question1 = intention_identifier._infer([], "I want to know what is a banana")
    print(decision1, question1)
    print()

    decision2, question2 = intention_identifier._infer([
        AIMessage(content="How can I help you?"),
        HumanMessage(content="I want to know what is a banana."),
        AIMessage(content="Sorry, I can only answer questions related to quantitative finance."),
        HumanMessage(content="I want to know what is option?"),
        AIMessage(content="An option is a choice or possibility in general, but in finance, it's a contract giving the buyer the right, but not the obligation, to buy (call) or sell (put) an underlying asset (like stocks, commodities) at a set price (strike price) by a specific date (expiration date)."),
        HumanMessage(content="How to calculate it?"),
    ], "How to calculate it?")
    print(decision2, question2)
    print()

    decision3, question3 = intention_identifier._infer([
        AIMessage(content="How can I help you?"),
        HumanMessage(content="What is inflation?"),
        AIMessage(content="Inflation is the rate at which the general level of prices for goods and services rises, decreasing the purchasing power of money over time."),
        HumanMessage(content="What's its difference from deflation?"),
    ], "What's its difference from deflation?")
    print(decision3, question3)
    print()

    decision4, question4 = intention_identifier._infer([
        AIMessage(content="How can I help you?"),
        HumanMessage(content="Who are you?"),
        AIMessage(content="I am an AI assistant to answer questions related to quantitative finance."),
        HumanMessage(content="How can I get start?"),
    ], "How can I get start?")
    print(decision4, question4)