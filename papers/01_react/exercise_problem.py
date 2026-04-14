"""
ReAct: Synergizing Reasoning and Acting — Coding Exercise

Goal: Implement the core ReAct Thought-Action-Observation loop in under 60 lines.
This exercise makes the paper's key concept tangible.

Instructions:
  1. Read the TODO comments carefully.
  2. Do NOT look at exercise_solution.py until you have tried for at least 20 minutes.
  3. You do not need to reproduce the paper exactly — capture the core idea only.

Core concept being implemented:
  An agent loop that interleaves natural-language Thoughts with tool Actions and
  incorporates the resulting Observations before the next step.
"""

# ── Dependencies ───────────────────────────────────────────────────────────────
# pip install openai  (or use any LLM client you prefer)
# All exercises use a simple mock_llm() if you don't have an API key.

import json
from typing import Any


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "search" in prompt.lower() and "Observation" not in prompt:
        return "Thought: I need to search for this topic.\nAction: search[relevant query]"
    if "calculate" in prompt.lower() and "Observation" not in prompt:
        return "Thought: I should calculate this.\nAction: calculate[2 + 2]"
    return "Thought: I now have enough information.\nAction: finish[The answer is 42]"


# ── TODO: Implement below ──────────────────────────────────────────────────────

# TODO 1: Implement parse_action(response: str) -> dict
# Parse the LLM response to extract the action type and input.
# The response format is: "Thought: ...\nAction: action_type[action_input]"
# Return a dict with keys "thought", "action_type", and "action_input".
# If no action is found, return {"thought": response, "action_type": "finish", "action_input": response}
def parse_action(response: str) -> dict:
    pass  # Your implementation here


# TODO 2: Implement execute_action(action: dict, tools: dict) -> str
# Dispatch to the right tool based on action["action_type"].
# tools is a dict mapping action_type strings to callable functions.
# If the action_type is "finish", return action["action_input"] directly.
# If the action_type is not in tools, return "Error: unknown action type."
def execute_action(action: dict, tools: dict) -> str:
    pass  # Your implementation here


# TODO 3: Implement react_loop(task: str, tools: dict, max_steps: int = 5) -> str
# The main ReAct loop:
#   1. Build a prompt from the task + history of (Thought, Action, Observation) triples
#   2. Call mock_llm(prompt) to get the next Thought+Action
#   3. Parse the action, execute it, get the observation
#   4. If action_type is "finish", return the final answer
#   5. Otherwise, append the triple to history and loop
#   6. If max_steps is reached, return "Max steps reached."
def react_loop(task: str, tools: dict, max_steps: int = 5) -> str:
    pass  # Your implementation here


if __name__ == "__main__":
    # Sample tools to test with
    sample_tools = {
        "search": lambda q: f"Search results for '{q}': [result1, result2]",
        "calculate": lambda expr: str(eval(expr)),  # noqa: S307 — toy demo only
    }

    result = react_loop("What is 2 + 2?", sample_tools)
    print("Final answer:", result)
