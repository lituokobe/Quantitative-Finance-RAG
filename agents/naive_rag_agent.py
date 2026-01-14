from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from config.rag_config import SYSTEM_PROMPT
from models.models import agent_llm
from tools.retriever_tools import retriever_tool
from utils.pretty_print import pretty_print

# TODO: Build naive RAG agent with simple retriever tool call
# prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
])

naive_rag_planner = create_tool_calling_agent( # Only plans to call the tool if needed
    agent_llm,
    [retriever_tool],
    prompt
)

naive_rag_executor = AgentExecutor( # plan to call the tool and actually call the tool if needed
    agent=naive_rag_planner,
    tools=[retriever_tool],
    handle_parsing_errors=True, # When tool calls fail, LLM is prompted to retry instead of crashes
    return_intermediate_steps=True
)

"""
In LangChain, you only need AgentExecutor when your agent must use tools.
In LangGraph, you almost never use AgentExecutor, because the graph becomes the executor
"""

# TODO: add history to the agent
# simulate a chat ID management system
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get the chat history for a given session."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

naive_rag_agent_w_history = RunnableWithMessageHistory( # type: ignore[arg-type]
    naive_rag_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

if __name__ == "__main__":
    user_question = 'What is European call option?'
    print(f"User question: {user_question}")

    res1 = naive_rag_executor.invoke({'input': user_question})
    print(f"Executor response: {res1}")
    pretty_print(res1)

    rep2 = naive_rag_agent_w_history.invoke(
        {'input': user_question},
        config = {"configurable":{"session_id":"test123"}}
    )
    pretty_print(rep2)

