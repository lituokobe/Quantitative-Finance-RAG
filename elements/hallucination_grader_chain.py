from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.models import agent_llm

class GradeHallucinations(BaseModel):
    """
    Grade the generated answers to see if there is any hallucination or not.
    """
    binary_score: Literal["yes", "no"] = Field(description="Whether the generated content is based on the given facts, value is either 'yes' or 'no'")


#Build the llm
structured_llm_grader = agent_llm.with_structured_output(GradeHallucinations)

#prompt template
system = """
You are an evaluator to decide whether the generated content is based on the given facts.  

You MUST respond in JSON format using the following schema:
{{
  "binary_score": "yes" | "no"
}}

Rules:
- Answer "yes" only if ALL claims in the generated content are supported by the given facts.
- Answer "no" if any part of the generated content is not supported or contradicts the facts.
"""

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Given facts: \n{documents} \n\n Generated content: \n{generation}")
    ]
)

hallucination_grader_chain = hallucination_prompt | structured_llm_grader