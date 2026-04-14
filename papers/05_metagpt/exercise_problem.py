"""
MetaGPT: Meta Programming for Multi-Agent Collaboration — Coding Exercise

Goal: Implement a role-based multi-agent pipeline (PM → Dev → QA) in under 60 lines.
This exercise makes the paper's key concept tangible.

Instructions:
  1. Read the TODO comments carefully.
  2. Do NOT look at exercise_solution.py until you have tried for at least 20 minutes.
  3. You do not need to reproduce the paper exactly — capture the core idea only.

Core concept being implemented:
  A sequential pipeline where each agent has a fixed role with structured output,
  and the output of each role becomes the structured input to the next.
"""

# ── Dependencies ───────────────────────────────────────────────────────────────
# No external packages required.

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


# ── TODO: Implement below ──────────────────────────────────────────────────────

# TODO 1: Implement the Role base class.
# Each Role has:
#   - name: str
#   - goal: str (what this role is trying to achieve)
#   - constraints: str (rules this role must follow)
# Implement process(self, input_text: str) -> str:
#   Build a role-specific prompt incorporating name, goal, constraints, and input_text.
#   Call mock_llm(prompt) and return the result.
class Role:
    pass  # Your implementation here


# TODO 2: Implement three concrete Role subclasses:
#   - ProductManager: goal="Write a clear PRD", constraints="Be concise, use bullet points"
#   - Developer: goal="Implement the requirements", constraints="Write clean Python code"
#   - QAEngineer: goal="Write test cases", constraints="Cover edge cases, use assert statements"
# Each subclass should call super().__init__() with the appropriate name/goal/constraints.


# TODO 3: Implement the SoftwareTeam class.
# It holds a list of roles in pipeline order: [ProductManager, Developer, QAEngineer]
# Implement run(self, user_requirement: str) -> dict:
#   Pass the user_requirement through each role sequentially.
#   Each role's output becomes the next role's input.
#   Return a dict: {"requirement": ..., "prd": ..., "code": ..., "tests": ...}
class SoftwareTeam:
    pass  # Your implementation here


# TODO 4: Each Role's process() should embed its name, goal, and constraints in the prompt
# so mock_llm can return role-appropriate output. The prompt should look like:
# "You are a {name}. Goal: {goal}. Constraints: {constraints}.\nInput: {input_text}"


if __name__ == "__main__":
    team = SoftwareTeam()
    result = team.run("Build a simple calculator with four basic operations.")

    print("=== Software Development Pipeline ===")
    for stage, output in result.items():
        print(f"\n[{stage.upper()}]\n{output}")
