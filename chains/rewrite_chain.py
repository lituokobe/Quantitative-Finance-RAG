# --------- Prepare the rewriter chain ---------
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from models.models import agent_llm

prompt = """
    ## === YOUR ROLE ===
    You are a query rewriter. You rewrite the question with optimization for answer-retrieval in a vector database.

    ## === YOUR CORE TASK ===
    You will be given a question, please:
    - analyse and comprehend the true meaning and intention behind the question.
    - rewrite the question to keep its original intention and meaning but with better wordings for retrieval in vector database.

    ## === IMPORTANT RULES ===
    - **Only output the optimized question alone**, don't add any extra words including introductory text, explanation, summary, etc.
    - **Don't conduct any conversation**, only output the optimized question.

    ## === OUTPUT EXAMPLES ===
    - If you are given the question: "What is a put option?", output "What is the definition of put option?"
    - If you are given the question: "What did the financial crisis do to the world?", output "What are the impacts of the financial crisis to the world?"
    
    Now, please start to rewrite the question **strictly based on above instruction**.
    
    Question:
    {question}
    
    Answer of rewriting:
    """

rewrite_prompt = PromptTemplate(
    template=prompt,
    input_variables=["question"]
)
rewrite_chain = rewrite_prompt | agent_llm | StrOutputParser()