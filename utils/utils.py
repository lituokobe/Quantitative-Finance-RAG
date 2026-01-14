# Retrieve the last message from the user in the stack of messages
def get_last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.__class__.__name__ == "HumanMessage":
            return msg.content
    return ""