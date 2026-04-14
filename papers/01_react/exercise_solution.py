"""
ReAct: Synergizing Reasoning and Acting — Solution

This is the reference implementation.
Study this ONLY after attempting exercise_problem.py for at least 20 minutes.

Key insight demonstrated:
  The Thought-Action-Observation history is the agent's working memory — each turn
  the LLM sees the full trace and reasons about what to do next given past results.
"""

import re
from typing import Any


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "search" in prompt.lower() and "Observation" not in prompt:
        return "Thought: I need to search for this topic.\nAction: search[relevant query]"
    if "calculate" in prompt.lower() and "Observation" not in prompt:
        return "Thought: I should calculate this.\nAction: calculate[2 + 2]"
    return "Thought: I now have enough information.\nAction: finish[The answer is 42]"


def parse_action(response: str) -> dict:
    """Extract thought, action_type, and action_input from an LLM response."""
    thought = ""
    action_type = "finish"
    action_input = response

    # Extract thought
    thought_match = re.search(r"Thought:\s*(.+?)(?=\nAction:|$)", response, re.DOTALL)
    if thought_match:
        thought = thought_match.group(1).strip()

    # Extract action of the form: action_type[action_input]
    action_match = re.search(r"Action:\s*(\w+)\[(.+?)\]", response, re.DOTALL)
    if action_match:
        action_type = action_match.group(1).strip()
        action_input = action_match.group(2).strip()

    return {"thought": thought, "action_type": action_type, "action_input": action_input}


def execute_action(action: dict, tools: dict) -> str:
    """Dispatch to the appropriate tool and return the observation."""
    if action["action_type"] == "finish":
        return action["action_input"]
    tool_fn = tools.get(action["action_type"])
    if tool_fn is None:
        return f"Error: unknown action type '{action['action_type']}'"
    return tool_fn(action["action_input"])


def react_loop(task: str, tools: dict, max_steps: int = 5) -> str:
    """Run the ReAct Thought-Action-Observation loop until done or max_steps."""
    history = []

    for step in range(max_steps):
        # Build prompt: task + all prior (Thought, Action, Observation) triples
        prompt_parts = [f"Task: {task}\n"]
        for entry in history:
            prompt_parts.append(f"Thought: {entry['thought']}")
            prompt_parts.append(f"Action: {entry['action_type']}[{entry['action_input']}]")
            prompt_parts.append(f"Observation: {entry['observation']}")
        prompt = "\n".join(prompt_parts)

        # Get next thought + action from LLM
        response = mock_llm(prompt)
        action = parse_action(response)

        if action["action_type"] == "finish":
            return action["action_input"]

        # Execute action and record observation
        observation = execute_action(action, tools)
        history.append({
            "thought": action["thought"],
            "action_type": action["action_type"],
            "action_input": action["action_input"],
            "observation": observation,
        })

        print(f"[Step {step + 1}] Thought: {action['thought']}")
        print(f"         Action: {action['action_type']}[{action['action_input']}]")
        print(f"         Observation: {observation}\n")

    return "Max steps reached."


if __name__ == "__main__":
    sample_tools = {
        "search": lambda q: f"Search results for '{q}': [result1, result2]",
        "calculate": lambda expr: str(eval(expr)),  # noqa: S307 — toy demo only
    }

    result = react_loop("What is 2 + 2?", sample_tools)
    print("Final answer:", result)
