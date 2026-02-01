import time
from typing import Literal

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from config.prompts import VERIFICATION_SYSTEM_PROMPT, CALCULATION_SYSTEM_PROMPT
from config.state import State
from models.models import agent_llm
from tools.retriever_tools import create_hybrid_retriever
from utils.build_prompt import build_history_prompt, build_document_prompt
from utils.log_utils import log, log_node_start, log_node_end

def calculation_retriever_node(state: State):
    prev_time = time.time()
    node_name = "calculation_retriever_node"
    log_node_start(node_name)

    # ------------------ Get user question ------------------
    try:
        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
        if last_log:
            question = last_log.get("question", "")
        else:
            question = ""
    except Exception as e:
        log.error(f"{node_name} fails to get user question: {e}")
        last_log = {}
        question = ""

    # ------------------ Retrieve math results only ------------------
    try:
        math_retriever = create_hybrid_retriever(
            k=10,
            score_threshold=0.05, # High recall
            filter_dict={"contains_math": True}, # Math only. But this only applies to vector search, BM25 won't follow. There will be none-math docs in the results as well.
        )
        # documents = math_retriever.invoke({"question":question})
        documents = math_retriever.invoke(question)
    except Exception as e:
        log.error(f"{node_name} has error when retrieving documents: {e}")
        raise

    time_cost = round(time.time() - prev_time, 3)
    current_log = {
        **last_log,
        "node": node_name,
        "retrieved_documents": documents,
        "time_cost": time_cost
    }

    log_node_end(node_name, time_cost)

    return {
        "logs": state.get("logs", []) + [current_log]
    }

class Verification(BaseModel):
    """
    Data class to regulate the output of the LLM for math verification.
    """
    decision: Literal[
        "good",
        "missing_info",
        "others",
    ]
    missing_info_message: str

class MathVerificationNode:
    def __init__(self):
        self.node_name = "math_verification_node"
        self.llm_runnable_structured_output = agent_llm.with_structured_output(Verification)

    def _verify(self, question: str, documents: list, history:list) -> tuple:
        # -------- check the availability of the agent LLM --------
        if not self.llm_runnable_structured_output:
            log.error(f"Agent LLM at {self.node_name} is not ready.")
            return "others", "", {}

        # -------- Formulate the prompt with dynamic chat data --------
        try:
            document_prompt_list: list = build_document_prompt(documents)
            history_prompt_list: list = build_history_prompt(history)
            document_prompt = "\n".join(document_prompt_list)
            history_prompt = "\n".join(history_prompt_list)
        except Exception as e:
            log.error(f"Error formulating prompt at {self.node_name}: {e}")
            return "others", "", {}

        # -------- Build the verification chain ---------
        verification_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", VERIFICATION_SYSTEM_PROMPT),
                ("human", "The chat history: \n{history_prompt} \n\n"
                          "The user's question: \n{question} \n\n"
                          "The retrieved documents:\n{document_prompt}"),
            ]
        )
        verification_chain = verification_prompt | self.llm_runnable_structured_output

        # -------- Use the LLM to do math verification ---------
        try:
            calculation_material = {"history_prompt": history_prompt, "question": question, "document_prompt": document_prompt}
            resp = verification_chain.invoke(calculation_material)
            decision: str = resp.decision
            missing_info_message: str = resp.missing_info_message
            # prepare the data for calculation_answer_node, so no need to repeat the process
            if decision == "good":
                return decision, "", calculation_material
            elif decision == "missing_info":
                return decision, missing_info_message, {}
            else:
                return decision, "", {}
        except Exception as e:
            log.error(f"Error generating decision at {self.node_name}: {e}")
            return "others", "", {}

    def __call__(self, state:State):
        prev_time = time.time()
        log_node_start(self.node_name)

        # -------- Get data from state --------
        messages = state.get("messages", [])
        try:
            logs = state.get("logs", [])
            last_log = logs[-1] if logs else {}
            if last_log:
                question = last_log.get("question", "")
                retrieved_documents = last_log.get("retrieved_documents", [])
            else:
                question = ""
                retrieved_documents = []
        except Exception as e:
            log.error(f"{self.node_name} fails to get user question and retrieved documents: {e}")
            last_log = {}
            question = ""
            retrieved_documents = []

        # -------- Verify the math calculation --------
        try:
            decision, missing_info_message, calculation_material = self._verify(question, retrieved_documents, messages)
            print(f"input to verification:/n"
                  f"question: {question}/n"
                  f"retrieved_docs (first one): {retrieved_documents[0]}"
                  f"chat history: {messages}")
            print(f"output of verification:/n"
                  f"decision: {decision}/n"
                  f"mising_info_message: {missing_info_message}/n"
                  f"calculation_material: {calculation_material}")

            time_cost = round(time.time() - prev_time, 3)

            if decision == "good": # pass the calculation material to let calculate_answer_node output
                current_log = {
                    **last_log,
                    "node": self.node_name,
                    "time_cost": time_cost,
                    "calculation_material":calculation_material
                }
                log_node_end(self.node_name, time_cost)
                return {
                    "dialog_state": "calculation_answer_node",
                    "logs": state["logs"] + [current_log]
                }
            elif decision == "missing_info": # output the missing_info_message and let math_verification_node do another check
                current_log = {
                    **last_log,
                    "node": self.node_name,
                    "agent_reply": missing_info_message,
                    "time_cost": time_cost
                }
                log_node_end(self.node_name, time_cost)
                return {
                    "messages": AIMessage(content=missing_info_message),
                    "dialog_state": "math_verification_node",
                    "logs": state["logs"] + [current_log]
                }
            else: # got to calculation_fallback_node and let it output
                current_log = {
                    **last_log,
                    "node": self.node_name,
                    "time_cost": time_cost,
                }
                log_node_end(self.node_name, time_cost)
                return {
                    "dialog_state": "calculation_fallback_node",
                    "logs": state["logs"] + [current_log]
                }
        except Exception as e:
            log.error(f"{self.node_name} has error: {e}")
            raise

def calculation_answer_node(state: State):
    prev_time = time.time()
    node_name = "calculation_answer_node"
    log_node_start(node_name)

    # -------- Get data from state --------
    try:
        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
        if last_log:
            calculation_material = last_log.get("calculation_material", {})

    except Exception as e:
        log.error(f"{node_name} fails to get calculation_material including chat history, user question and retrieved documents: {e}")
        last_log = {}
        calculation_material = {}

    # -------- Form the calculation chain --------
    calculation_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CALCULATION_SYSTEM_PROMPT),
            ("human", "The chat history: \n{history_prompt} \n\n"
                      "The user's question: \n{question} \n\n"
                      "The retrieved documents:\n{document_prompt}")
        ]
    )
    calculation_chain = calculation_prompt | agent_llm | StrOutputParser()

    # -------- Use the LLM to perform the calculation ---------
    try:
        ai_message: str = calculation_chain.invoke(calculation_material)
        time_cost = round(time.time() - prev_time, 3)
        current_log = {
            **last_log,
            "node": node_name,
            "agent_reply": ai_message,
            "time_cost": time_cost
        }
        log_node_end(node_name, time_cost)
        return {
            "messages": AIMessage(content=ai_message),
            "dialog_state": "starting_intention_node",
            "logs": state["logs"] + [current_log]
        }
    except Exception as e:
        log.error(f"Error generating response at {node_name}: {e}")
        raise

def calculation_fallback_node(state: State):
    node_name = "calculation_fallback_node"
    log_node_start(node_name)

    # ------------------ Get last log ------------------
    try:
        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
    except Exception as e:
        log.error(f"{node_name} fails to get last log: {e}")
        last_log = {}

    # ------------------ Generate reply ------------------
    ai_message = "Sorry, this calculation is beyond my knowledge scope."

    current_log = {
        **last_log,
        "node": node_name,
        "agent_reply": ai_message
    }

    log_node_end(node_name)
    return {
        "messages": AIMessage(content=ai_message),
        "dialog_state": "starting_intention_node", # Start again from starting_intention_node
        "logs": state.get("logs", []) + [current_log]
    }

# Test
if __name__ == "__main__":
    # ----------------- Calculation Retriever test -----------------
    Q1 = "What is an option?"
    result1 = calculation_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q1}]
        }
    )
    print(f"Question:{Q1}")
    documents = result1["logs"][-1].get("retrieved_documents", [])
    print(f"{len(documents)} documents retrieved: ")
    for doc in documents:
        print(f"Contains math: {doc.metadata['contains_math']}")
        print(doc.page_content)
        print("--------")

    Q2 = "What is the formula for SMA?"
    result2 = calculation_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q2}]
        }
    )
    print(f"Question:{Q2}")
    documents = result2["logs"][-1].get("retrieved_documents", [])
    print(f"{len(documents)} documents retrieved: ")
    for doc in documents:
        print(f"Contains math: {doc.metadata['contains_math']}")
        print(doc.page_content)
        print("--------")

    Q3 = "What is ROE if NPM is 30$?"
    result3 = calculation_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q3}]
        }
    )
    print(f"Question:{Q3}")
    documents = result3["logs"][-1].get("retrieved_documents", [])
    print(f"{len(documents)} documents retrieved: ")
    for doc in documents:
        print(f"Contains math: {doc.metadata['contains_math']}")
        print(doc.page_content)
        print("--------")