from langchain_core.agents import AgentAction
import json
from typing import Any


def pretty_print(result: dict[str, Any], max_tool_output_len: int = 800):
    """
    Pretty-print the result returned by AgentExecutor.invoke() or
    RunnableWithMessageHistory.invoke().

    Handles:
    - final answer
    - tool calls
    - tool inputs
    - tool outputs
    - extra metadata

    Args:
        result: dict returned by .invoke()
        max_tool_output_len: truncate tool output for readability
    """

    print("\n" + "=" * 60)
    print("🤖 RAG AGENT INVOCATION RESULT")
    print("=" * 60)

    # --------------------------------------------------
    # Final answer
    # --------------------------------------------------
    output = result.get("output")
    if output:
        print("\n🧠 FINAL ANSWER")
        print("-" * 60)
        print(output)

    # --------------------------------------------------
    # Tool calls (planning + execution trace)
    # --------------------------------------------------
    intermediate_steps = result.get("intermediate_steps", [])

    if intermediate_steps:
        print("\n🔧 TOOL CALL TRACE")
        print("-" * 60)

        for idx, step in enumerate(intermediate_steps, 1):
            try:
                action, observation = step
            except ValueError:
                # Defensive: unexpected format
                print(f"\nStep {idx}: <unrecognized step format>")
                print(step)
                continue

            if isinstance(action, AgentAction):
                print(f"\nStep {idx}")
                print(f"  Tool name : {action.tool}")

                print("  Tool input:")
                print(json.dumps(action.tool_input, indent=2, ensure_ascii=False))

                print("  Tool output:")
                text = str(observation)
                if len(text) > max_tool_output_len:
                    text = text[:max_tool_output_len] + "..."
                print(text)
            else:
                print(f"\nStep {idx}: <non-AgentAction>")
                print(action)

    else:
        print("\n🔍 NO TOOL CALLS (LLM answered directly)")

    # --------------------------------------------------
    # Any extra fields (future-proof)
    # --------------------------------------------------
    known_keys = {"output", "intermediate_steps"}
    extra_keys = set(result.keys()) - known_keys

    if extra_keys:
        print("\n📦 ADDITIONAL FIELDS")
        print("-" * 60)
        for k in extra_keys:
            print(f"{k}: {result[k]}")

    print("\n" + "=" * 60 + "\n")
