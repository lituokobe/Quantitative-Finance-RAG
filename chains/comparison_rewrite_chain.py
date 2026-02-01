from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from models.models import agent_llm

prompt = """
    ## === YOUR ROLE ===
    You are a query rewriter. You rewrite the question with optimization for answer-retrieval in a vector database.
    The question is about comparing or checking at least 2 entities.

    ## === YOUR CORE TASK ===
    You will be given a question, please:
    - analyse and comprehend the true meaning and intention behind the question.
    - rewrite the question to keep its original intention and meaning but with better wordings for retrieval in vector database, especially make the comparison more explicit.

    ## === IMPORTANT RULES ===
    - **Only output the optimized question alone**, don't add any extra words including introductory text, explanation, summary, etc.
    - **Don't conduct any conversation**, only output the optimized question.

    ## === OUTPUT EXAMPLES ===
    - If you are given the question: "What is the difference between put option and call option?", output "What is put option? What is call option? What is their difference?"
    - If you are given the question: "Can you compare gross income and net income?", output "What is gross income? What is net income? Compare them."
    
    Now, please start to rewrite the question **strictly based on above instruction**.
    
    Question:
    {question}
    
    Answer of rewriting:
    """

comparison_rewrite_prompt = PromptTemplate(
    template=prompt,
    input_variables=["question"]
)

comparison_rewrite_chain = comparison_rewrite_prompt | agent_llm | StrOutputParser()