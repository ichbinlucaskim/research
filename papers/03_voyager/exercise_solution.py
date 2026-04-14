"""
Voyager: An Open-Ended Embodied Agent — Solution

This is the reference implementation.
Study this ONLY after attempting exercise_problem.py for at least 20 minutes.

Key insight demonstrated:
  Skills are stored as executable code strings, not model weights — this makes them
  inspectable, composable, and transferable without any retraining.
"""

from typing import Any


class SkillLibrary:
    """A registry of reusable executable skills, retrieved by semantic keyword match."""

    def __init__(self):
        self.skills: list[dict] = []

    def add_skill(self, name: str, description: str, code: str) -> None:
        """Add or update a skill by name."""
        for skill in self.skills:
            if skill["name"] == name:
                skill["description"] = description
                skill["code"] = code
                return
        self.skills.append({"name": name, "description": description, "code": code})

    def retrieve_skill(self, task_description: str) -> dict | None:
        """Find the most relevant skill by word-overlap with name+description."""
        if not self.skills:
            return None
        query_words = set(task_description.lower().split())
        best_skill = None
        best_score = -1
        for skill in self.skills:
            combined = (skill["name"] + " " + skill["description"]).lower()
            score = sum(1 for word in query_words if word in combined)
            if score > best_score:
                best_score = score
                best_skill = skill
        return best_skill

    def execute_skill(self, skill: dict, **kwargs) -> Any:
        """Execute skill code with kwargs as local variables; return 'result'."""
        local_vars = dict(kwargs)
        try:
            exec(skill["code"], {}, local_vars)  # noqa: S102 — intentional skill execution
            return local_vars.get("result")
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    lib = SkillLibrary()

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

    task = "I need to count words in my document"
    skill = lib.retrieve_skill(task)
    print(f"Retrieved skill: {skill['name']}")

    output = lib.execute_skill(skill, text="hello world foo bar")
    print(f"Result: {output}")  # Expected: 4
