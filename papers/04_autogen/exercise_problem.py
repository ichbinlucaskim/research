"""
AutoGen: Multi-Agent Conversation Framework — Coding Exercise

Goal: Implement a minimal multi-agent conversation system in under 60 lines.
This exercise makes the paper's key concept tangible.

Instructions:
  1. Read the TODO comments carefully.
  2. Do NOT look at exercise_solution.py until you have tried for at least 20 minutes.
  3. You do not need to reproduce the paper exactly — capture the core idea only.

Core concept being implemented:
  A ConversableAgent abstraction where agents with different system prompts exchange
  messages, with a termination condition to stop the conversation automatically.
"""

# ── Dependencies ───────────────────────────────────────────────────────────────
# No external packages required.

from typing import Any


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "review" in prompt.lower():
        return "The code looks correct. TERMINATE"
    if "write" in prompt.lower() or "implement" in prompt.lower():
        return "Here is the implementation:\n```python\nresult = 42\n```\nPlease review."
    return "I understand. Let me think about this. TERMINATE"


# ── TODO: Implement below ──────────────────────────────────────────────────────

# TODO 1: Implement the Agent class.
# Each agent has:
#   - name: str
#   - system_prompt: str (defines the agent's role/persona)
# Implement receive(self, message: str) -> str:
#   Build a prompt from system_prompt + message, call mock_llm(), return the response.
class Agent:
    pass  # Your implementation here


# TODO 2: Implement the ConversationManager class.
# It holds a list of messages (dicts with "sender" and "content" keys).
# Implement send(self, sender: Agent, receiver: Agent, message: str) -> str:
#   Record the message, call receiver.receive(message), record the response, return it.
class ConversationManager:
    pass  # Your implementation here


# TODO 3: Implement run_conversation(agent_a, agent_b, initial_message, max_turns=4) -> list.
# Orchestrates the conversation:
#   1. agent_a sends initial_message to agent_b
#   2. agent_b responds, then agent_a responds, alternating until max_turns
#   3. Return the full list of message dicts from the ConversationManager


# TODO 4: Add a termination check inside run_conversation.
# If any response contains the word "TERMINATE" (case-insensitive), stop the loop early
# and append a final message: {"sender": "system", "content": "Conversation terminated."}


if __name__ == "__main__":
    coder = Agent(
        name="Coder",
        system_prompt="You are an expert Python programmer. Write clean, correct code.",
    )
    reviewer = Agent(
        name="Reviewer",
        system_prompt="You are a code reviewer. Review the code and say TERMINATE when satisfied.",
    )

    messages = run_conversation(
        coder, reviewer, "Please implement a function that returns 42.", max_turns=4
    )

    for msg in messages:
        print(f"[{msg['sender']}]: {msg['content']}\n")
