"""
Voyager: An Open-Ended Embodied Agent — Coding Exercise

Goal: Implement a simple skill library that stores and retrieves reusable agent skills.
This exercise makes the paper's key concept tangible.

Instructions:
  1. Read the TODO comments carefully.
  2. Do NOT look at exercise_solution.py until you have tried for at least 20 minutes.
  3. You do not need to reproduce the paper exactly — capture the core idea only.

Core concept being implemented:
  A persistent skill library where verified executable code snippets can be stored,
  semantically retrieved by task description, and executed on demand.
"""

# ── Dependencies ───────────────────────────────────────────────────────────────
# No external packages required.

from typing import Any


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without an API key. Replace with real LLM call."""
    if "search" in prompt.lower():
        return "Action: search[relevant query here]"
    return "Final Answer: [mock answer]"


# ── TODO: Implement below ──────────────────────────────────────────────────────

# TODO 1: Implement the SkillLibrary class.
# Each skill is a dict with keys: "name" (str), "description" (str), "code" (str).
# Store skills in a list called self.skills.
class SkillLibrary:
    pass  # Your implementation here


# TODO 2: Implement add_skill(self, name: str, description: str, code: str) on SkillLibrary.
# Create a skill dict and append it to self.skills.
# If a skill with the same name already exists, replace it (update in place).


# TODO 3: Implement retrieve_skill(self, task_description: str) -> dict | None on SkillLibrary.
# Find the most relevant skill by counting how many words in task_description
# appear in the skill's name or description (case-insensitive word match).
# Return the skill with the highest match count, or None if the library is empty.


# TODO 4: Implement execute_skill(self, skill: dict, **kwargs) -> Any on SkillLibrary.
# Execute the skill's "code" string using exec().
# The code has access to kwargs as local variables.
# The code should assign its result to a variable named "result".
# Return the value of "result" after execution.
# If execution fails, return the exception message as a string.


if __name__ == "__main__":
    lib = SkillLibrary()

    # Add some skills
    lib.add_skill(
        name="count_words",
        description="Count the number of words in a text string",
        code="result = len(text.split())",
    )
    lib.add_skill(
        name="reverse_string",
        description="Reverse a string character by character",
        code="result = text[::-1]",
    )

    # Retrieve and execute
    task = "I need to count words in my document"
    skill = lib.retrieve_skill(task)
    print(f"Retrieved skill: {skill['name']}")

    output = lib.execute_skill(skill, text="hello world foo bar")
    print(f"Result: {output}")  # Expected: 4
