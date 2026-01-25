import time
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from config.state import State
from models.models import agent_llm
from tools.retriever_tools import create_hybrid_retriever
from utils.log_utils import log, log_node_start, log_node_end


# ==================== Shortcut Retriever ====================
class ShortcutQuestions(BaseModel):
    """
    Data class to regulate the output of the LLM for classifying shortcut question types.
    """
    question_type: Literal[
        "greetings",
        "user_how_to",
        "answer_scope",
        "assistant_how_to",
        "whether_accurate",
        "others"
    ]

class ShortcutRetrieverNode:
    def __init__(self):
        self.node_name = "shortcut_retriever_node"

        # Create a chain with structured output
        llm_runnable_structured_output = agent_llm.with_structured_output(ShortcutQuestions)

        shortcut_system_prompt = """
        ## === YOUR ROLE ===
        You are a question classifier of an AI assistant. 
        
        ## === YOUR TASK ===
        You classify user's question and output JSON with only one key: `question_type`.
        Follow the instruction below (- value: explanation) and choose the the value of the key:
        - "greetings": a greeting or check-up to the AI assistant, e.g. "How are you?", "How have you been?", "Hoep you are doing well!"
        - "user_how_to": how does the user use the service of AI assistant, e.g. "How can I get started?", "Can I directly ask you anything?", "How do I talk to you?"
        - "answer_scope": what kinds of topics can the AI assistant answer, e.g. "What question can I ask?", "What do you know?", "Do you answer questions about accounting?"
        - "assistant_how_to": how does he AI assistant answer, e.g. "Why do you know this answer?", "What's your mechanism for answering question?", "How did you come up with that answer?"
        - "whether_accurate": whether the AI assistant's answer is accurate, e.g. "Are you sure your reply is correct?", "Is your answer accurate enough?", "Can I believe you in this?"
        - "others": the question doesn't fall into any of the above categories
        You are a grader to identify the relevancy between retrieved documents and the question.  

        ## === IMPORTANT RULES ==="  
        You MUST strictly follow the instruction and respond in JSON format matching this schema:
        {{
          "question_type": "greetings" | "user_how_to" | "answer_scope" | "assistant_how_to" | "whether_accurate" | "others"
        }}
        Don't output any other values or any other type of data. Don't conduct a conversation.
        """

        shortcut_type_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", shortcut_system_prompt),
                ("human", "User question: {question}")
            ]
        )

        self.shortcut_type_chain = shortcut_type_prompt | llm_runnable_structured_output

        self.shortcut_reply_lookup = {
            "greetings": "Thanks for checking out. I'm doing great! You can ask me anything about quantitative finance.",
            "user_how_to": "Just simply input what you want to know. I will try my best to answer you.",
            "answer_scope": "I am specialized in topics of quantitative finance like option pricing, stochastic calculus, portfolio theory and risk management. Besides, I can also help you with questions of FinTech, AI, corporate finance, economy, and finance history",
            "assistant_how_to": "I am powered by AI and RAG. All my answers come from creditable sources of information. I won't reply you based only the AI model's own training data and inference.",
            "whether_accurate": "Yes, my answers are accurate and trustworthy. If you have any further questions on any of my answers, just continue asking me and I am happy to discuss more with you in detail."
        }
    #
    # def retriever_node(state):
    #     try:
    #         log.info("retriever_node starts to work.")
    #
    #         logs = state.get("logs", [])
    #         last_log = logs[-1] if logs else {}
    #         if last_log:
    #             question = last_log.get("question", "")
    #         else:
    #             question = ""
    #
    #         retriever = create_hybrid_retriever()
    #         documents = retriever.invoke(question)
    #
    #         current_log = {
    #             **last_log,
    #             "node": "retriever_node",
    #             "retrieved_documents": documents,
    #         }
    #
    #         log.info("retriever_node finishes working.")
    #         return {
    #             "dialog_state": "document_grader_node",
    #             "logs": state.get("logs", []) + [current_log]
    #         }
    #     except Exception as e:
    #         log.error(f"retriever_node has error: {e}")
    #         raise

    def __call__(self, state: State):
        prev_time = time.time()
        node_name = "shortcut_retriever_node"
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
            log.error(f"{node_name} fails to get user question: {e}")
            last_log = {}
            question = ""

        # ------------------ Classify user question ------------------
        try:
            question_type_result = self.shortcut_type_chain.invoke({"question": question})
            question_type = question_type_result.question_type

            # Security check:
            if question_type not in ["greetings", "user_how_to", "answer_scope", "assistant_how_to", "whether_accurate", "others"]:
                question_type = "others"
        except Exception as e:
            log.error(f"{node_name} fails to classify user question: {e}")
            question_type = "others"

        # ------------------ choose reply ------------------
        if question_type == "others":
            ai_message = ""
        else:
            ai_message = self.shortcut_reply_lookup["question_type"]

        time_cost = round(time.time() - prev_time, 3)
        current_log = {
            **last_log,
            "node": "shortcut_retriever_node",
            "time_cost": time_cost,
        }
        log_node_end(self.node_name, time_cost)

        return {
            "dialog_state": "starting_intention_node", # No matter there is a reply or not, we always need to redirect the chat to starting_intention_node
            "logs": state.get("logs", []) + [current_log]
        }


def retriever_node(state):
    try:
        log.info("retriever_node starts to work.")

        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
        if last_log:
            question = last_log.get("question", "")
        else:
            question = ""

        retriever = create_hybrid_retriever()
        documents = retriever.invoke(question)

        current_log = {
            **last_log,
            "node": "retriever_node",
            "retrieved_documents": documents,
        }

        log.info("retriever_node finishes working.")
        return {
            "dialog_state": "document_grader_node",
            "logs": state.get("logs", []) + [current_log]
        }
    except Exception as e:
        log.error(f"retriever_node has error: {e}")
        raise

# Test
if __name__ == "__main__":
    result = retriever_node(
        {
            "logs":[
                {
                    "question":"what is an option?"
                }
            ]
        }
    )
    print(result)