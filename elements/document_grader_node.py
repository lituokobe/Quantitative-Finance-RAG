from config.state import State
from elements.grader_chain import retrieval_grader_chain
from utils.log_utils import log


def document_grader_node(state: State):
    try:
        log.info("document_grader_node starts to work.")

        logs = state.get("logs", [])
        last_log = logs[-1] if logs else {}
        if last_log:
            question = last_log.get("question", "")
            documents = last_log.get("retrieved_documents", [])
        else:
            question = ""
            documents = []
    except Exception as e:
        log.error(f"document_grader_node failed to obtain questions and documents: {e}")
        question = ""
        documents = []

    # Filter the retrieved documents
    filtered_docs = []
    try:
        for d in documents:
            result = retrieval_grader_chain.invoke(
                {"question": question, "document": d.page_content}
            )
            relevancy = result.relevancy
            if relevancy == "yes":
                log.info(f"Retrieved document {d.page_content} is relevant")
                filtered_docs.append(d)
            else:
                log.info(f"Retrieved document {d.page_content} is NOT relevant, dump it.")
                continue
        current_log = {
            **last_log,
            "node":"document_grader_node",
            "filtered_docs": filtered_docs
        }

        log.info("document_grader_node finishes working.")
        return {
            "logs": state.get("logs",[]) + [current_log]
        }
    except Exception as e:
        log.error(f"document_grader_node has error grading documents: {e}")
        raise