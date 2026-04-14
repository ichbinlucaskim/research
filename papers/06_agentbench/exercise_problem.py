"""
AgentBench: Evaluating LLMs as Agents — Coding Exercise

Goal: Implement a minimal agent evaluation harness in under 60 lines.
This exercise makes the paper's key concept tangible.

Instructions:
  1. Read the TODO comments carefully.
  2. Do NOT look at exercise_solution.py until you have tried for at least 20 minutes.
  3. You do not need to reproduce the paper exactly — capture the core idea only.

Core concept being implemented:
  A structured evaluation loop that runs an agent on a set of tasks, tracks per-task
  success/failure, counts steps, and aggregates metrics across tasks.
"""

# ── Dependencies ───────────────────────────────────────────────────────────────
# No external packages required.

from dataclasses import dataclass, field
from typing import Any, Callable


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "search" in prompt.lower():
        return "Action: search[relevant query here]"
    return "Final Answer: [mock answer]"


# ── TODO: Implement below ──────────────────────────────────────────────────────

# TODO 1: Implement the Task dataclass.
# Fields:
#   - task_id: str
#   - description: str
#   - expected_output: str
#   - environment: dict  (key-value pairs the agent can query, e.g. {"db": {...}})
@dataclass
class Task:
    pass  # Your implementation here


# TODO 2: Implement evaluate_agent(agent_fn: Callable, tasks: list[Task]) -> dict.
# agent_fn signature: agent_fn(task_description: str, environment: dict) -> tuple[str, int]
#   where the tuple is (final_answer: str, steps_taken: int)
# For each task:
#   - Call agent_fn(task.description, task.environment)
#   - Check if final_answer == task.expected_output (exact match)
#   - Track success/failure and steps_taken
# Return a metrics dict (see TODO 3 for required keys).
def evaluate_agent(agent_fn: Callable, tasks: list) -> dict:
    pass  # Your implementation here


# TODO 3: The returned metrics dict must include:
#   - "success_rate": float (successes / total tasks)
#   - "avg_steps": float (average steps taken across all tasks)
#   - "failure_reasons": list of strings describing each failure
#     Format each reason as: "task_id: expected '{expected}' got '{actual}'"


# TODO 4: Write 3 sample Task objects and a mock_agent function, then run the evaluation.
# mock_agent should succeed on 2 out of 3 tasks to make the metrics interesting.
# Print the final metrics dict.


if __name__ == "__main__":
    # Define your 3 sample tasks here
    tasks = []  # TODO: fill in

    # Define your mock agent here
    def mock_agent(description: str, environment: dict) -> tuple:
        pass  # TODO: fill in

    metrics = evaluate_agent(mock_agent, tasks)
    print("Evaluation Results:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
