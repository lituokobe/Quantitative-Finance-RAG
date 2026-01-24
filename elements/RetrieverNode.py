from tools.retriever_tools import create_hybrid_retriever
from utils.log_utils import log


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
    result = RetrieverNode(
        {
            "logs":[
                {
                    "question":"what is an option?"
                }
            ]
        }
    )
    print(result)