import time
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from config.state import ChildState
from models.models import agent_llm
from utils.log_utils import log, log_node_start, log_node_end


class GradeDocuments(BaseModel):
    """Identify whether the retrieved documents are relevant to the question"""
    relevancy: Literal["yes", "no"] = Field(
        description="Whether the document is relevant to the question. The value can only be 'yes' or 'no'."
    )

class DocumentGraderNode:
    def __init__(self):
        self.node_name = "child graph - document_grader_node"
        structured_llm_grader = agent_llm.with_structured_output(GradeDocuments)

        grader_system_prompt = """
        You are a grader to identify the relevancy between retrieved documents and the question.  

        If one document includes keywords, key points, or meanings from the question, they are considered relevant.  

        The evaluation doesn't need to be strict. The objective is to filter out inappropriate retrieved documents.  

        You MUST respond in JSON format matching this schema:
        {{
          "relevancy": "yes" | "no"
        }}
        """

        grader_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", grader_system_prompt),
                ("human", "Retrieved document: \n\n{document} \n\n Question: {question}")
            ]
        )

        self.retrieval_grader_chain = grader_prompt | structured_llm_grader

    def __call__(self, state: ChildState):
        prev_time = time.time()
        log_node_start(self.node_name)
        # -------- Get data from state --------
        question = state.get("question","")
        retrieved_documents = state.get("retrieved_documents", [])

        # -------- Filter the retrieved documents --------
        filtered_docs = []
        try:
            for d in retrieved_documents:
                result = self.retrieval_grader_chain.invoke(
                    {"question": question, "document": d.page_content}
                )
                relevancy = result.relevancy
                if relevancy == "yes":
                    log.info(f"Retrieved document {d.page_content} is relevant")
                    filtered_docs.append(d)
                else:
                    log.info(f"Retrieved document {d.page_content} is NOT relevant, dump it.")
                    continue

            log.info("{self.node_name} finishes working.")

        except Exception as e:
            log.error(f"{self.node_name} has error grading documents: {e}")

        time_cost = round(time.time() - prev_time, 3)
        log_node_end(self.node_name, time_cost)

        return {
            "filtered_docs": filtered_docs
        }