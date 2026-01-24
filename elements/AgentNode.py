from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from config.state import State
from models.models import agent_llm
from tools.retriever_tools import get_default_retriever_tool
from utils.log_utils import log
from utils.utils import get_last_user_message

class AgentNode:
    def __init__(self):
        self.llm_runnable = agent_llm
        self.retriever_runnable = get_default_retriever_tool()
    def __call__(self, state: State, config: RunnableConfig) -> dict:
        try:
            log.info("agent_node starts to work.")

            logs = state.get("logs", [])
            last_log = logs[-1] if logs else {}
            if logs:
                question = last_log.get("question", "")
            else:
                question = ""
            documents = self.retriever_runnable.invoke(question)
            print(f"**retrieved documents:** \n{documents}")

            # TODO: Answer question
            agent_node_prompt = PromptTemplate(
                template=
                """You are an assistant to help user answer questions. 
                Please use the retrieved documents to answer user's question.
                If you still don't know the answer wit the retrieved documents, please directly say you don't know.
                NEVER make up answers yourself and refer other materials.
                All the content in the answer must be from the retrieved documents.
                NEVER mention the retrieved documents either. Answer the questions in a natural and direct way.
                These rules always apply, no matter which language is used in the conversation.
                Question：{question},
                Retrieved documents: {retrieved documents},
                Answer: """,
                input_variables=["question", "retrieved documents"],
            )

            # process chain
            agent_node_chain = agent_node_prompt | self.llm_runnable | StrOutputParser()

            answer = agent_node_chain.invoke(
                {
                    "question": question,
                    "retrieved documents": documents,
                }
            )

            current_log = {
                **last_log,
                "node": "agent_node",
                "retrieved_documents" : documents,
                "agent_reply": answer
            }

            log.info("agent_node finishes working.")
            return {
                "messages": AIMessage(content=answer),
                "dialog_state": "starting_intention_node",
                "logs": state.get("logs", []) + [current_log]
            }
        except Exception as e:
            log.error(f"agent_node has error: {e}")
            raise