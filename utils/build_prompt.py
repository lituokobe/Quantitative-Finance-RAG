from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage

def build_history_prompt(chat_history: list) -> list:
    """
    Manually create the chat history.
    This is for the convenience to manipulate the position of chat history in the prompt
    :param chat_history: List of conversation records of LangChain message object.
    :return: List of the same records but of plan strings.
    """
    doc_string_chat_history = []
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            doc_string_chat_history.append(f"  -[User]: {msg.content}")
        elif isinstance(msg, AIMessage):
            doc_string_chat_history.append(f"  -[AI assistant]: {msg.content}")
    return doc_string_chat_history

def build_document_prompt(documents: list) -> list:
    """
        Manually create the documents.
        This is for the convenience to manipulate the position of chat history in the prompt
        :param chat_history: List of conversation records of LangChain message object.
        :return: List of the same records but of plan strings.
        """
    doc_string_documents = []
    for doc in documents:
        if isinstance(doc, Document):
            page_content = doc.page_content
            if isinstance(page_content, str) and page_content:
                doc_string_documents.append(page_content)
    return doc_string_documents