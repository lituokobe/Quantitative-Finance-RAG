# data model
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.models import agent_llm


class GradeAnswer(BaseModel):
    """Evaluate if the answer solve user's question's binary grading model"""

    binary_score: Literal["yes", "no"] = Field(
        description="Whether the generated content answers the question, the value can only be either 'yes' or 'no'"
    )


# build the llm
structured_llm_grader = agent_llm.with_structured_output(GradeAnswer)

# prompt template
system_prompt = """
You are an evaluator to decide whether a generated content answers the question.  

You MUST respond in JSON format using the following schema:
{{
  "binary_score": "yes" | "no"
}}

Rules:
- Answer "yes" if the generated content directly and sufficiently answers the question.
- Answer "no" if the content is irrelevant, incomplete, evasive, or does not address the question.
"""
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Question: \n{question} \n\n Generated content: \n{generation}"),
    ]
)

# build the chain
answer_grader_chain = answer_prompt | structured_llm_grader