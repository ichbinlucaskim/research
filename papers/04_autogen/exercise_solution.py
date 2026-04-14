"""
AutoGen: Multi-Agent Conversation Framework — Solution

This is the reference implementation.
Study this ONLY after attempting exercise_problem.py for at least 20 minutes.

Key insight demonstrated:
  Agents are just system prompts + receive() methods — the conversation topology
  (who talks to whom, when to stop) is separate from the agent definition itself.
"""

from typing import Any


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "review" in prompt.lower():
        return "The code looks correct. TERMINATE"
    if "write" in prompt.lower() or "implement" in prompt.lower():
        return "Here is the implementation:\n```python\nresult = 42\n```\nPlease review."
    return "I understand. Let me think about this. TERMINATE"


class Agent:
    """A conversable agent defined by a name and a system prompt."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    def receive(self, message: str) -> str:
        """Build a prompt from system_prompt + message and return the LLM response."""
        prompt = f"{self.system_prompt}\n\nMessage received:\n{message}"
        return mock_llm(prompt)


class ConversationManager:
    """Records the conversation history and routes messages between agents."""

    def __init__(self):
        self.messages: list[dict] = []

    def send(self, sender: Agent, receiver: Agent, message: str) -> str:
        """Record sender's message, get receiver's response, record and return it."""
        self.messages.append({"sender": sender.name, "content": message})
        response = receiver.receive(message)
        self.messages.append({"sender": receiver.name, "content": response})
        return response


def run_conversation(
    agent_a: Agent, agent_b: Agent, initial_message: str, max_turns: int = 4
) -> list[dict]:
    """Orchestrate a back-and-forth conversation, stopping on TERMINATE or max_turns."""
    manager = ConversationManager()
    current_message = initial_message
    current_sender, current_receiver = agent_a, agent_b

    for _ in range(max_turns):
        response = manager.send(current_sender, current_receiver, current_message)
        if "terminate" in response.lower():
            manager.messages.append({"sender": "system", "content": "Conversation terminated."})
            break
        # Swap roles for next turn
        current_message = response
        current_sender, current_receiver = current_receiver, current_sender

    return manager.messages


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
