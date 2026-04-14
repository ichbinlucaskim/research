"""
AgentBench: Evaluating LLMs as Agents — Solution

This is the reference implementation.
Study this ONLY after attempting exercise_problem.py for at least 20 minutes.

Key insight demonstrated:
  A good evaluation harness separates task definition, agent execution, and metric
  aggregation into distinct layers — making it easy to swap agents or add tasks.
"""

from dataclasses import dataclass, field
from typing import Any, Callable


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "search" in prompt.lower():
        return "Action: search[relevant query here]"
    return "Final Answer: [mock answer]"


@dataclass
class Task:
    """A single evaluation task with a verifiable success criterion."""
    task_id: str
    description: str
    expected_output: str
    environment: dict = field(default_factory=dict)


def evaluate_agent(agent_fn: Callable, tasks: list[Task]) -> dict:
    """
    Run agent_fn on each task and aggregate metrics.

    agent_fn(task_description, environment) -> (final_answer: str, steps_taken: int)
    """
    successes = 0
    total_steps = 0
    failure_reasons: list[str] = []

    for task in tasks:
        answer, steps = agent_fn(task.description, task.environment)
        total_steps += steps
        if answer == task.expected_output:
            successes += 1
        else:
            failure_reasons.append(
                f"{task.task_id}: expected '{task.expected_output}' got '{answer}'"
            )

    n = len(tasks)
    return {
        "success_rate": successes / n if n > 0 else 0.0,
        "avg_steps": total_steps / n if n > 0 else 0.0,
        "failure_reasons": failure_reasons,
    }


# ── Sample tasks and mock agent ───────────────────────────────────────────────

tasks = [
    Task(
        task_id="T1",
        description="What is the capital of France?",
        expected_output="Paris",
        environment={"knowledge_base": {"France": "Paris"}},
    ),
    Task(
        task_id="T2",
        description="What is 3 + 5?",
        expected_output="8",
        environment={"calculator": True},
    ),
    Task(
        task_id="T3",
        description="List files in the home directory.",
        expected_output="['.bashrc', '.profile']",
        environment={"filesystem": {"~": [".bashrc", ".profile"]}},
    ),
]


def mock_agent(description: str, environment: dict) -> tuple[str, int]:
    """A mock agent that succeeds on 2 of the 3 sample tasks."""
    if "capital" in description.lower():
        kb = environment.get("knowledge_base", {})
        answer = kb.get("France", "unknown")
        return answer, 1
    if "3 + 5" in description:
        return "8", 2
    # Deliberately wrong on T3 to generate a failure reason
    return "unknown", 3


if __name__ == "__main__":
    metrics = evaluate_agent(mock_agent, tasks)
    print("Evaluation Results:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
