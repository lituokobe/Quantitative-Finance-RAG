from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.models import agent_llm

class GradeDocuments(BaseModel):
    """Identify whether the retrieved documents are relevant to the question"""
    relevancy: Literal["yes", "no"] = Field(
        description="Whether the document is relevant to the question. The value can only be 'yes' or 'no'."
    )

structured_llm_grader = agent_llm.with_structured_output(GradeDocuments)

grader_system_prompt="""
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

retrieval_grader_chain = grader_prompt | structured_llm_grader