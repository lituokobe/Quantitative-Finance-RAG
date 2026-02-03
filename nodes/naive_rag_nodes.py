import time
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from config.prompts import NAIVE_RAG_INTENTION_PROMPT1, NAIVE_RAG_INTENTION_PROMPT2, NAIVE_RAG_INTENTION_PROMPT3, \
    AGENT_NODE_PROMPT
from config.state import State
from models.models import agent_llm
from tools.retriever_tools import get_default_retriever_tool
from utils.build_prompt import build_history_prompt
from utils.log_utils import log, log_node_start, log_node_end
from utils.utils import get_last_user_message

class Intention(BaseModel):
    """
    Data class to regulate the output of the LLM for intention identifying.
    """
    question: str
    decision: Literal["agent_node", "fallback_node"]

class StartingIntentionNode:
    def __init__(self):
        # Initiate the agent with structured output
        self.llm_runnable_structured_output = agent_llm.with_structured_output(Intention)
        self.node_name = "naive rag - starting_intention_node"

    def _infer(self, history:list, user_input:str):
        # -------- check the availability of the agent LLM --------
        if not self.llm_runnable_structured_output:
            log.error(f"Agent LLM at {self.node_name} is not ready.")
            return user_input, "fallback_node"

        # -------- Formulate the full prompt with dynamic chat data --------
        try:
            history_prompt = build_history_prompt(history)
            doc_string = NAIVE_RAG_INTENTION_PROMPT1 + history_prompt + NAIVE_RAG_INTENTION_PROMPT2 + [user_input] + NAIVE_RAG_INTENTION_PROMPT3
            full_prompt = "\n".join(doc_string)

        except Exception as e:
            log.error(f"Error formulating prompt at {self.node_name}: {e}")
            full_prompt = user_input

        # -------- Use the agent LLM to identify intention with the full prompt --------
        try:
            resp = self.llm_runnable_structured_output.invoke([HumanMessage(content=full_prompt)])
            question: str = resp.question
            decision: str = resp.decision
            print(f"User question after considering chat history: {question}")
            print(f"Decision made: {decision}")
            return question, decision
        except Exception as e:
            log.error(f"Error generating decision at {self.node_name}: {e}")
            raise # Need to raise error as the conversation cannot continue

    def __call__(self, state: State, config: RunnableConfig) -> dict:
        prev_time = time.time()
        log_node_start(self.node_name)

        # -------- Get data from state --------
        messages = state.get("messages", [])
        user_input = get_last_user_message(messages)

        # -------- Rephrase the user input and identify intention --------
        question, decision = self._infer(messages, user_input)
        time_cost = round(time.time() - prev_time, 3)
        current_log = { # For starting nodes, no need to include previous node's log
            "node": self.node_name,
            "time_cost": time_cost,
            "user_input": user_input,
            "question": question,
        }
        log_node_end(self.node_name, time_cost)
        return {
            "dialog_state": decision,
            "logs": state["logs"] + [current_log]
        }

class AgentNode:
    def __init__(self):
        self.node_name="naive rag - agent_node"
        self.retriever_runnable = get_default_retriever_tool()

        # Build the answer chain
        agent_node_prompt = PromptTemplate(
            template=AGENT_NODE_PROMPT,
            input_variables=["question", "retrieved documents"]
        )
        self.agent_node_chain = agent_node_prompt | agent_llm | StrOutputParser()

    def __call__(self, state: State, config: RunnableConfig) -> dict:
        try:
            prev_time = time.time()
            log_node_start(self.node_name)

            logs = state.get("logs", [])
            last_log = logs[-1] if logs else {}
            if logs:
                question = last_log.get("question", "")
            else:
                question = ""
            documents = self.retriever_runnable.invoke(question)
            print(f"**retrieved documents:** \n{documents}")

            # TODO: Answer question


            answer = self.agent_node_chain.invoke(
                {
                    "question": question,
                    "retrieved documents": documents,
                }
            )

            time_cost = round(time.time() - prev_time, 3)
            current_log = {
                **last_log,
                "node": self.node_name,
                "time_cost": time_cost,
                "retrieved_documents" : documents,
                "agent_reply": answer
            }

            log_node_end(self.node_name, time_cost)
            return {
                "messages": AIMessage(content=answer),
                "dialog_state": "starting_intention_node",
                "logs": state.get("logs", []) + [current_log]
            }
        except Exception as e:
            log.error(f"{self.node_name} has error: {e}")
            raise