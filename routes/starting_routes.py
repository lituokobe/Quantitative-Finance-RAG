# -------- Import dependencies --------
from langgraph.constants import END
from config.state import State

# -------- Create the route function before starting of each round of conversation --------
def start_route(state: State) -> str:
    dialog_state = state.get("dialog_state", [])
    if not dialog_state:  # At the beginning, send to the first node
        return "starting_reply_node"
    elif dialog_state[-1] == "hang_up":
        return END
    else:
        return dialog_state[-1]

# -------- Create the route function after starting node --------
def starting_intention_route(state: State) -> str:
    dialog_state = state.get("dialog_state", [])
    if not dialog_state:
        return "fallback"
    # Get the last dialog state from stating_intention_node
    last_dialog_state: str = dialog_state[-1]

    # If no last dialog state is empty string or not regular
    if not last_dialog_state or last_dialog_state not in [
        "shortcut_agent",
        "calculation_agent",
        "comparison_agent",
        "standard_agent",
        "fallback"
    ]:
        return "fallback"
    return last_dialog_state
