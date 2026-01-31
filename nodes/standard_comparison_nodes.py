import time

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from agent_adaptive_rag.adaptive_rage_child_graph_builder import build_adaptive_child_rag_graph
from config.prompts import DECOMPOSE_SYSTEM_PROMPT
from config.state import State
from models.models import agent_llm
from utils.log_utils import log_node_start, log, log_node_end

class Decompose(BaseModel):
    """
    Data class to regulate the output of the LLM for question decompose.
    """
    decomposed_questions: list[str]

class ComparisonRetrieverNode:
    def __init__(self):
        self.node_name = "comparison_retriever_node"
        self.llm_runnable_structured_output = agent_llm.with_structured_output(Decompose)
        self.child_graph = build_adaptive_child_rag_graph()
        self.conv_config = {"configurable": {"thread_id": "CRN"}}

    def _decompose_question(self, question: str):
        prev_time = time.time()

        # -------- Build the decompose chain ---------
        decompose_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", DECOMPOSE_SYSTEM_PROMPT),
                ("human", "The user question: \n{question}"),
            ]
        )
        decompose_chain = decompose_prompt | self.llm_runnable_structured_output

        # ------------------ Use LLM to decompose the question ------------------
        try:
            resp = decompose_chain.invoke({"question": question})
            d_questions = resp.decomposed_questions
            # prepare the data for calculation_answer_node, so no need to repeat the process
            if not isinstance(d_questions, list) or not d_questions:
                d_questions = [] # output empty list when abnormality happens
        except Exception as e:
            log.error(f"Error decomposing question at {self.node_name}: {e}")
            d_questions = []

        time_cost = round(time.time() - prev_time, 3)
        log.info(f"{self.node_name} decomposes question \"{question}\", time costed: {time_cost} seconds.")

        return d_questions

    def _child_graph_retrieval(self, question: str):
        prev_time = time.time()
        try:
            child_state = self.child_graph.invoke(
                {"question": question},
                config=self.conv_config
            )
            filtered_docs = child_state.get("filtered_docs",[])
            rewrite_count = child_state.get("rewrite_count", 0)
            web_results = child_state.get("web_results", [])

            time_cost = round(time.time() - prev_time, 3)
            log.info(f"{self.node_name} finishes child graph retrieval for question \"{question}\", time costed: {time_cost} seconds.")

            if web_results:
                # Invariant: web_results only exists after rewrite_count >= MAX_REWRITE, consider it first as it is fallback
                return {
                    "documents": web_results,
                    "type": "web_search",
                    "rewrite_count": rewrite_count,
                    "time_cost": time_cost
                }
            if filtered_docs:
                return {
                    "documents": filtered_docs,
                    "type": "retrieval",
                    "rewrite_count": rewrite_count,
                    "time_cost": time_cost
                }
            return {
                "documents": [],
                "type": "no_result",
                "rewrite_count": rewrite_count,
                "time_cost": time_cost
            }
        except Exception as e:
            time_cost = round(time.time() - prev_time, 3)
            log.error(f"{self.node_name} has error on child graph retrieval of question \"{question}\": {e}\n\n Time costed: {time_cost} seconds.")
            return {
                "documents": [],
                "type": "retrieval_error",
                "rewrite_count": 0,
                "time_cost": time_cost
            }

    def __call__(self, state: State):
        prev_time = time.time()
        log_node_start(self.node_name)

        # ------------------ Get user question ------------------
        try:
            logs = state.get("logs", [])
            last_log = logs[-1] if logs else {}
            if last_log:
                question = last_log.get("question", "")
            else:
                question = ""
        except Exception as e:
            log.error(f"{self.node_name} fails to get user question: {e}")
            last_log = {}
            question = ""

        # ------------------ Call the chain to decompose the question ------------------
        # Should be N+1 question list for child graphs, with the first one is always the overarching user questions
        decomposed_questions: list = self._decompose_question(question)

        # ------------------ Call the adaptive RAG child graphs to retrieve ------------------
        # results from child graphs
        child_graph_results = []

        for q in decomposed_questions:
            result = self._child_graph_retrieval(q)
            child_graph_results.append({
                "question": q,
                **result
            })
            """
            dict appended:
            - question: str
            - documents: list
            - type: "web_search"|"retrieval"|"no_result"|"retrieval_error"
            - rewrite_count: 0|1|2
            - time_cost: float
            """

        time_cost = round(time.time() - prev_time, 3)
        current_log = {
            **last_log,
            "node": self.node_name,
            "retrieved_documents": child_graph_results,
            "time_cost": time_cost
        }
        log_node_end(self.node_name, time_cost)

        return {
            "logs": state.get("logs", []) + [current_log]
        }

class StandardRetrieverNode:
    def __init__(self):
        self.node_name = "standard_retrieval_node"
        self.child_graph = build_adaptive_child_rag_graph()
        self.conv_config = {"configurable": {"thread_id": "SRN"}}

    def _child_graph_retrieval(self, question: str):
        prev_time = time.time()
        try:
            child_state = self.child_graph.invoke(
                {"question": question},
                config=self.conv_config
            )
            filtered_docs = child_state.get("filtered_docs", [])
            rewrite_count = child_state.get("rewrite_count", 0)
            web_results = child_state.get("web_results", [])

            time_cost = round(time.time() - prev_time, 3)
            log.info(
                f"{self.node_name} finishes child graph retrieval for question \"{question}\", time costed: {time_cost} seconds.")

            if web_results:  # Consider web search result first as this is fallback
                return {
                    "documents": web_results,
                    "type": "web_search",
                    "rewrite_count": rewrite_count, # it should be 2
                    "time_cost": time_cost
                }
            if filtered_docs:
                return {
                    "documents": filtered_docs,
                    "type": "retrieval",
                    "rewrite_count": rewrite_count,
                    "time_cost": time_cost
                }
            return {
                "documents": [],
                "type": "no_result",
                "rewrite_count": rewrite_count,
                "time_cost": time_cost
            }
        except Exception as e:
            time_cost = round(time.time() - prev_time, 3)
            log.error(
                f"{self.node_name} has error on child graph retrieval of question \"{question}\": {e}\n\n Time costed: {time_cost} seconds.")
            return {
                "documents": [],
                "type": "retrieval_error",
                "rewrite_count": 0,
                "time_cost": time_cost
            }

    def __call__(self, state: State):
        pass

# Test
# if __name__ == "__main__":
#     comparison_retriever_node = ComparisonRetrieverNode()
#     # ----------------- Decompose question test -----------------
#     Q1 = "Can you compare apples and bananas?"
#     result1 = comparison_retriever_node(
#         {
#             "messages": [],
#             "dialog_state": [],
#             "logs": [{"question": Q1}]
#         }
#     )
#     print(f"Question:{Q1}")
#     decomposed_questions = result1["logs"][-1].get("decomposed_questions", [])
#     print(f"{len(decomposed_questions)} questions decomposed: ")
#     for q in decomposed_questions:
#         print(q)
#         print("--------")
#
#     Q2 = "What's the difference between MBA, MPA and MFA?"
#     result2 = comparison_retriever_node(
#         {
#             "messages": [],
#             "dialog_state": [],
#             "logs": [{"question": Q2}]
#         }
#     )
#     print(f"Question:{Q2}")
#     decomposed_questions = result2["logs"][-1].get("decomposed_questions", [])
#     print(f"{len(decomposed_questions)} questions decomposed: ")
#     for q in decomposed_questions:
#         print(q)
#         print("--------")
#
#     Q3 = "Compare the foreign policies in US, France, India and China."
#     result3 = comparison_retriever_node(
#         {
#             "messages": [],
#             "dialog_state": [],
#             "logs": [{"question": Q3}]
#         }
#     )
#     print(f"Question:{Q3}")
#     decomposed_questions = result3["logs"][-1].get("decomposed_questions", [])
#     print(f"{len(decomposed_questions)} questions decomposed: ")
#     for q in decomposed_questions:
#         print(q)
#         print("--------")