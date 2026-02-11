import time

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel
from agent_adaptive_rag.adaptive_rage_child_graph_builder import build_adaptive_child_rag_graph
from config.prompts import DECOMPOSE_SYSTEM_PROMPT, GENERATE_COMPARISON_PROMPT, GENERATE_STANDARD_PROMPT
from config.state import State
from models.models import agent_llm
from chains.comparison_rewrite_chain import comparison_rewrite_chain
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
                    "info_type": "web_search",
                    "rewrite_count": rewrite_count,
                    "time_cost": time_cost
                }
            if filtered_docs:
                return {
                    "documents": filtered_docs,
                    "info_type": "retrieval",
                    "rewrite_count": rewrite_count,
                    "time_cost": time_cost
                }
            return {
                "documents": [],
                "info_type": "no_result",
                "rewrite_count": rewrite_count,
                "time_cost": time_cost
            }
        except Exception as e:
            time_cost = round(time.time() - prev_time, 3)
            log.error(f"{self.node_name} has error on child graph retrieval of question \"{question}\": {e}\n\n Time costed: {time_cost} seconds.")
            return {
                "documents": [],
                "info_type": "retrieval_error",
                "rewrite_count": 0,
                "time_cost": time_cost
            }

    def _align_and_annotate(self, child_graph_results: list):
        aligned = []

        for idx, r in enumerate(child_graph_results):
            docs = []
            for d in r["documents"]:
                if isinstance(d, Document):
                    d.metadata = {
                        **d.metadata,
                        "entity_index": idx,
                        "entity_question": r["question"],
                        "rewrite_count": r["rewrite_count"],
                        "info_type": r["info_type"]
                    }
                    docs.append(d)
                elif isinstance(d, tuple) and d[0] == "page_content": # sometimes web search returns tuple
                    docs.append(
                        Document(
                            page_content=d[1],
                            metadata = {
                                "entity_index": idx,
                                "entity_question": r["question"],
                                "rewrite_count": r["rewrite_count"],
                                "info_type": r["info_type"]
                            }
                        )
                    )
                else:
                    print(f"{self.node_name} - not valid document:")
                    print(f"{d}")

            aligned.append({
                "entity_index": idx,
                "entity_question": r["question"],
                "info_type": r["info_type"],
                "documents": docs,
                "rewrite_count": r["rewrite_count"],
                "time_cost": r["time_cost"]
            })

        return aligned

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
            - info_type: "web_search"|"retrieval"|"no_result"|"retrieval_error"
            - rewrite_count: 0|1|2
            - time_cost: float
            """

        # ------------------ Simple alignment function to embed retrieval info to doc's metadata ------------------
        aligned_docs:list = self._align_and_annotate(child_graph_results)
        """
        dict in aligned_docs:
        - entity_index: int
        - entity_question: str
        - info_type: "web_search"|"retrieval"|"no_result"|"retrieval_error"
        - documents: list
        - rewrite_count: 0|1|2
        - time_cost: float
        In each item in documents is Document:
        - page_content: str
        - metadata:
          - entity_index: int
          - entity_question: str
          - info_type: "web_search"|"retrieval"|"no_result"|"retrieval_error"
          - rewrite_count: 0|1|2
        """

        time_cost = round(time.time() - prev_time, 3)
        current_log = {
            **last_log,
            "node": self.node_name,
            "retrieved_documents": aligned_docs,
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

            if web_results:
                # Invariant: web_results only exists after rewrite_count >= MAX_REWRITE, consider it first as it is fallback
                return {
                    "documents": web_results,
                    "info_type": "web_search",
                    "rewrite_count": rewrite_count,
                    "time_cost": time_cost
                }
            if filtered_docs:
                return {
                    "documents": filtered_docs,
                    "info_type": "retrieval",
                    "rewrite_count": rewrite_count,
                    "time_cost": time_cost
                }
            return {
                "documents": [],
                "info_type": "no_result",
                "rewrite_count": rewrite_count,
                "time_cost": time_cost
            }
        except Exception as e:
            time_cost = round(time.time() - prev_time, 3)
            log.error(
                f"{self.node_name} has error on child graph retrieval of question \"{question}\": {e}\n\n Time costed: {time_cost} seconds.")
            return {
                "documents": [],
                "info_type": "retrieval_error",
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

        # ------------------ Call the adaptive RAG child graphs to retrieve ------------------
        result = self._child_graph_retrieval(question)
        child_graph_result ={
            "question": question,
            **result
        }
        """
        dict:
        - question: str
        - documents: list
        - info_type: "web_search"|"retrieval"|"no_result"|"retrieval_error"
        - rewrite_count: 0|1|2
        - time_cost: float
        """

        # ------------------ Simple alignment function to embed retrieval info to doc's metadata ------------------
        aligned_docs = []
        docs = []
        for d in child_graph_result["documents"]:
            if isinstance(d, Document):
                d.metadata = {
                    **d.metadata,
                    "entity_index": 0,
                    "entity_question": child_graph_result["question"],
                    "rewrite_count": child_graph_result["rewrite_count"],
                    "info_type": child_graph_result["info_type"]
                }
                docs.append(d)
            elif isinstance(d, tuple) and d[0] == "page_content":  # sometimes web search returns tuple
                docs.append(
                    Document(
                        page_content=d[1],
                        metadata={
                            "entity_index": 0,
                            "entity_question": child_graph_result["question"],
                            "rewrite_count": child_graph_result["rewrite_count"],
                            "info_type": child_graph_result["info_type"]
                        }
                    )
                )
            else:
                print(f"{self.node_name} - not valid document:")
                print(f"{d}")

        aligned_docs.append({
            "entity_index": 0,
            "entity_question": child_graph_result["question"],
            "info_type": child_graph_result["info_type"],
            "documents": docs,
            "rewrite_count": child_graph_result["rewrite_count"],
            "time_cost": child_graph_result["time_cost"]
        })
        """
        dict in aligned_docs:
        - entity_index: 0
        - entity_question: str
        - info_type: "web_search"|"retrieval"|"no_result"|"retrieval_error"
        - documents: list
        - rewrite_count: 0|1|2
        - time_cost: float
        In each item in documents is Document:
        - page_content: str
        - metadata:
          - entity_index: 0
          - entity_question: str
          - info_type: "web_search"|"retrieval"|"no_result"|"retrieval_error"
          - rewrite_count: 0|1|2
        """

        time_cost = round(time.time() - prev_time, 3)
        current_log = {
            **last_log,
            "node": self.node_name,
            "retrieved_documents": aligned_docs,
            "time_cost": time_cost
        }
        log_node_end(self.node_name, time_cost)

        return {
            "logs": state.get("logs", []) + [current_log]
        }

class GenerateNode:
    def __init__(self):
        self.node_name = "generate_node"

        generate_comparison_prompt = PromptTemplate(
            template=GENERATE_COMPARISON_PROMPT,
            input_variables=["question", "context"],
        )
        self.generate_comparison_chain = generate_comparison_prompt | agent_llm | StrOutputParser()

        generate_standard_prompt = PromptTemplate(
            template=GENERATE_STANDARD_PROMPT,
            input_variables=["question", "context"],
        )
        self.generate_standard_chain = generate_standard_prompt | agent_llm | StrOutputParser()

    # --------- Context Formatter for comparison---------
    def _format_aligned_docs_comparison(self, aligned_results: list) -> str:
        """
        Format entity-aligned documents into a structured context
        """
        blocks = []

        for group in aligned_results:
            entity_q = group.get("entity_question", "Unknown Entity")
            info_type = group.get("info_type", "unknown")
            rewrite_count = group.get("rewrite_count", 0)
            docs = group.get("documents", [])

            header = f"[Entity question: {entity_q} | times of question rewrite: {rewrite_count} | type of information: {info_type}]"
            blocks.append(header)
            blocks.append("Information:")

            if not docs:
                blocks.append("No reliable documents found.\n")
                continue

            for d in docs:
                blocks.append(d.page_content)

            blocks.append("")  # spacing between entities
            blocks.append("-----------------------")
            blocks.append("")

        aligned_results_formatted = "\n\n".join(blocks)
        print(f"{self.node_name} - Aligned docs after being formatted: {aligned_results_formatted}")

        return aligned_results_formatted

    def _format_aligned_docs_standard(self, aligned_results: list) -> str:
        """
        Format entity-aligned documents into a structured context
        """
        blocks = []
        aligned_result = {}
        if aligned_results:
            aligned_result = aligned_results[0] # There should be only one dict in aligned_results

        info_type = aligned_result.get("info_type", "unknown")
        rewrite_count = aligned_result.get("rewrite_count", 0)
        docs = aligned_result.get("documents", [])

        header = f"[Type of information: {info_type} | times of question rewrite: {rewrite_count}]"
        blocks.append(header)
        blocks.append("Information:")

        if not docs:
            blocks.append("No reliable documents found.\n")

        for d in docs:
            blocks.append(d.page_content)

        aligned_results_formatted = "\n\n".join(blocks)
        print(f"{self.node_name} - Aligned docs after being formatted: {aligned_results_formatted}")

        return aligned_results_formatted

    def __call__(self, state: State) -> dict:
        prev_time = time.time()
        log_node_start(self.node_name)

        # ------------------ Get information from state ------------------
        try:
            dialog_state = state["dialog_state"]
            last_state = dialog_state[-1]
            logs = state["logs"]
            last_log = logs[-1]
            question = last_log["question"]
            generation_time = last_log.get("generation_time", 0)
        except Exception as e:
            log.error(f"{self.node_name} fails to get information from state: {e}")
            # fallback values
            last_state = "standard_agent"
            last_log = {}
            question = ""
            generation_time = 0

        # ------------------ If the the workflow is from comparison retrieval ------------------
        try:
            if last_state == "comparison_agent":
                aligned_results = last_log.get("retrieved_documents", [])
                context = self._format_aligned_docs_comparison(aligned_results)
                # execute
                generation = self.generate_comparison_chain.invoke(
                    {
                        "context": context,
                        "question": question,
                    }
                )
            # ------------------ If the the workflow is from standard retrieval ------------------
            elif last_state == "standard_agent":
                aligned_results = last_log.get("retrieved_documents", [])
                context = self._format_aligned_docs_standard(aligned_results)
                # execute
                generation = self.generate_standard_chain.invoke(
                    {
                        "context": context,
                        "question": question,
                    }
                )
            else:
                log.error(f"{self.node_name} has wrong last state.")
                context = ""
                generation = ""
        except Exception as e:
            log.error(f"{self.node_name} has error in generating answers for question \"{question} \": {e}")
            context = ""
            generation = ""

        time_cost = round(time.time() - prev_time, 3)
        log_node_end(self.node_name, time_cost)
        current_log = {
            **last_log,
            "node": self.node_name,
            "context": context,
            "generation": generation,
            "generation_time": generation_time+1,
            "time_cost": time_cost
        }

        return {
            "logs": state.get("logs", []) + [current_log]
        }


def comparison_rewrite_query_node(state: State) -> dict:
    prev_time = time.time()
    node_name = "comparison_rewrite_query_node"
    log_node_start(node_name)

    # ------------------ Get information from state ------------------
    try:
        logs = state["logs"]
        last_log = logs[-1]
        question = last_log["question"]
        comparison_rewrite_count = last_log.get("comparison_rewrite_count", 0)
    except Exception as e:
        log.error(f"{node_name} fails to get information from state: {e}")
        # fallback values
        last_log = {}
        question = ""
        comparison_rewrite_count = 0

    # --------- Rewrite the question ---------
    try:
        optimized_question = comparison_rewrite_chain.invoke({"question": question})
    except Exception as e:
        log.error(f"{node_name} has error on rewriting comparison question \"{question}\": {e}")
        optimized_question = question

    print(f"After rewriting, the comparison question becomes {optimized_question}.")

    time_cost = round(time.time() - prev_time, 3)
    log_node_end(node_name, time_cost)
    current_log = {
        **last_log,
        "node": node_name,
        "question": optimized_question,
        "comparison_rewrite_count": int(comparison_rewrite_count + 1),
        "time_cost": time_cost
    }

    return {
        "logs": state.get("logs", []) + [current_log]
    }

def reply_with_generation_node(state: State):
    node_name = "rely_with_generation_node"
    log_node_start(node_name)

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
    log_node_end(node_name)

    return {
        "messages": AIMessage(content=generation),
        "dialog_state": "starting_intention_node",
        "logs": state.get("logs", []) + [current_log]
    }

# Test
if __name__ == "__main__":
    comparison_retriever_node = ComparisonRetrieverNode()
    # ----------------- Decompose question test -----------------
    Q1 = "Can you compare apples and bananas?"
    result1 = comparison_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q1}]
        }
    )
    print(f"Question:{Q1}")
    questions = result1["logs"][-1].get("decomposed_questions", [])
    print(f"{len(questions)} questions decomposed: ")
    for qq in questions:
        print(qq)
        print("--------")

    Q2 = "What's the difference between MBA, MPA and MFA?"
    result2 = comparison_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q2}]
        }
    )
    print(f"Question:{Q2}")
    questions = result2["logs"][-1].get("decomposed_questions", [])
    print(f"{len(questions)} questions decomposed: ")
    for qq in questions:
        print(qq)
        print("--------")

    Q3 = "Compare the foreign policies in US, France, India and China."
    result3 = comparison_retriever_node(
        {
            "messages": [],
            "dialog_state": [],
            "logs": [{"question": Q3}]
        }
    )
    print(f"Question:{Q3}")
    questions = result3["logs"][-1].get("decomposed_questions", [])
    print(f"{len(questions)} questions decomposed: ")
    for qq in questions:
        print(qq)
        print("--------")