import time

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

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
        self.adaptive_rag_graph = build_adaptive_rag_graph()

    def _decompose_question(self, question: str):
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
                d_questions = [question]
        except Exception as e:
            log.error(f"Error decomposing question at {self.node_name}: {e}")
            d_questions = [question]

        return d_questions

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
        decomposed_questions = self._decompose_question(question)

        time_cost = round(time.time() - prev_time, 3)
        log(f"{self.node_name} finishes decomposing questions, time costed: {time_cost} seconds.")

        # ------------------ Call the adaptive RAG graph to retrieve for th questions ------------------
        rag_results = []

        for q in decomposed_questions:
            adaptive_rag_state = {
                "question": q
            }

            result = self.adaptive_rag_graph.invoke(adaptive_rag_state)
            rag_results.append({
                "question": q,
                "answer": result["answer"],
                "documents": result.get("filtered_documents", [])
            })


        time_cost = round(time.time() - prev_time, 3)
        current_log = {
            **last_log,
            "node": self.node_name,
            "decomposed_questions": decomposed_questions,
            "time_cost": time_cost
        }

        log_node_end(self.node_name, time_cost)

        return {
            "logs": state.get("logs", []) + [current_log]
        }

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