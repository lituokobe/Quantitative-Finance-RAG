from langchain_core.messages import HumanMessage
from agents.naive_rag_graph_builder import build_naive_rag_graph
from utils.log_utils import log


def main(thread_id: str):
    conv_config = {"configurable":{"thread_id":thread_id}}

    graph = build_naive_rag_graph()

    # TODO: Start the chat
    print("=== The conversation is over ===\n")
    # Step 1 :by sending an empty message
    state = graph.invoke({"messages": [HumanMessage(content="")]}, config=conv_config)

    # Print initial assistant message
    messages = state.get("messages")
    if messages:
        if isinstance(messages, list):
            last_msg = messages[-1]
            if last_msg.__class__.__name__ == "AIMessage":
                print(f"Assistant: {last_msg.content}")
    print()
    # Step 2: Main conversation loop
    while True:
        # Get user input
        user_input = input("User: ").strip()
        if user_input == "quit":
            log.info("User has quit the conversation.")
            break

        # Record current state BEFORE processing
        prev_msg_count = len(state["messages"])
        # Create user message
        new_user_message = {"messages": [HumanMessage(content=user_input)]}

        # Resume workflow
        try:
            state = graph.invoke(new_user_message, config=conv_config)
        except Exception as e:
            log.error(f"Error when processing user input '{user_input}': {e}")
            break

        # Get ONLY new messages and metadata generated in this turn
        new_messages = state.get("messages", [])[prev_msg_count:]

        # Print all new assistant messages with their metadata
        for idx, msg in enumerate(new_messages):
            if msg.__class__.__name__ == "AIMessage":
                print(f"Assistant: {msg.content}")  # Use .content, not ['content']
        print()  # Extra newline after all messages

    return state

if __name__ == "__main__":
    state = main("test_call")

    # Print final messages
    print("=== Quantitative Finance RAG Assistant has left the conversation ===\n")
    print("Chat history: ")
    for msg in state["messages"]:
        if msg.__class__.__name__ == "AIMessage":
            print(f"Assistant: {msg.content}")
        if msg.__class__.__name__ == "HumanMessage":
            print(f"User: {msg.content}")
    print("-"*50)
    print("State history: ")
    print(state["dialog_state"])
    print("-" * 50)
    print("LOGS：")
    for log in state["logs"]:
        print(log)