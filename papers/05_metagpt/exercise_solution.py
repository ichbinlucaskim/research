"""
MetaGPT: Meta Programming for Multi-Agent Collaboration — Solution

This is the reference implementation.
Study this ONLY after attempting exercise_problem.py for at least 20 minutes.

Key insight demonstrated:
  Structured role-specific outputs (PRD, code, tests) are better inter-agent interfaces
  than freeform messages — they reduce ambiguity and make each handoff verifiable.
"""

from typing import Any


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "product manager" in prompt.lower() or "prd" in prompt.lower():
        return "PRD: Build a calculator. Requirements: add, subtract, multiply, divide."
    if "developer" in prompt.lower() or "implement" in prompt.lower():
        return "CODE:\ndef add(a, b): return a + b\ndef subtract(a, b): return a - b"
    if "qa" in prompt.lower() or "test" in prompt.lower():
        return "TESTS:\ndef test_add(): assert add(1,2)==3\ndef test_subtract(): assert subtract(3,1)==2"
    return "OUTPUT: [role output here]"


class Role:
    """Base class for a software team role that processes inputs and produces structured output."""

    def __init__(self, name: str, goal: str, constraints: str):
        self.name = name
        self.goal = goal
        self.constraints = constraints

    def process(self, input_text: str) -> str:
        prompt = (
            f"You are a {self.name}. "
            f"Goal: {self.goal}. "
            f"Constraints: {self.constraints}.\n"
            f"Input: {input_text}"
        )
        return mock_llm(prompt)


class ProductManager(Role):
    def __init__(self):
        super().__init__(
            name="Product Manager",
            goal="Write a clear PRD",
            constraints="Be concise, use bullet points",
        )


class Developer(Role):
    def __init__(self):
        super().__init__(
            name="Developer",
            goal="Implement the requirements",
            constraints="Write clean Python code",
        )


class QAEngineer(Role):
    def __init__(self):
        super().__init__(
            name="QA Engineer",
            goal="Write test cases",
            constraints="Cover edge cases, use assert statements",
        )


class SoftwareTeam:
    """Runs a sequential PM → Dev → QA pipeline, passing structured artifacts between roles."""

    def __init__(self):
        self.roles = [ProductManager(), Developer(), QAEngineer()]

    def run(self, user_requirement: str) -> dict:
        keys = ["requirement", "prd", "code", "tests"]
        result = {"requirement": user_requirement}
        current_input = user_requirement

        for role, key in zip(self.roles, keys[1:]):
            output = role.process(current_input)
            result[key] = output
            current_input = output  # structured output becomes next role's input

        return result


if __name__ == "__main__":
    team = SoftwareTeam()
    result = team.run("Build a simple calculator with four basic operations.")

    print("=== Software Development Pipeline ===")
    for stage, output in result.items():
        print(f"\n[{stage.upper()}]\n{output}")
