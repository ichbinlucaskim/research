"""
MemGPT: Towards LLMs as Operating Systems — Coding Exercise

Goal: Implement a hierarchical memory manager with hot/cold storage in under 60 lines.
This exercise makes the paper's key concept tangible.

Instructions:
  1. Read the TODO comments carefully.
  2. Do NOT look at exercise_solution.py until you have tried for at least 20 minutes.
  3. You do not need to reproduce the paper exactly — capture the core idea only.

Core concept being implemented:
  A two-tier memory system where a fixed-size main context automatically evicts to
  unlimited archival storage, and the agent can search archival on demand.
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

# TODO 1: Implement the MemoryManager class.
# It should have:
#   - main_context: list of strings, max capacity of 10 items (the "in-window" memory)
#   - archival_storage: list of strings, unlimited capacity (the "out-of-window" memory)
class MemoryManager:
    pass  # Your implementation here


# TODO 2: Implement add_memory(self, item: str) on MemoryManager.
# If main_context is at capacity, evict the oldest item to archival_storage first.
# Then append the new item to main_context.


# TODO 3: Implement search_archival(self, query: str) -> list on MemoryManager.
# Return all items in archival_storage that contain the query string (case-insensitive).
# If no matches, return an empty list.


# TODO 4: Implement get_context_for_llm(self) -> str on MemoryManager.
# Return main_context as a formatted string, one item per line, with index numbers.
# Example output:
#   [0] First memory item
#   [1] Second memory item


if __name__ == "__main__":
    mem = MemoryManager()

    # Add 12 items — the first 2 should be evicted to archival
    for i in range(12):
        mem.add_memory(f"Memory item {i}: some content about topic_{i}")

    print("Main context (should have 10 items):")
    print(mem.get_context_for_llm())

    print("\nArchival storage (should have 2 items):")
    print(mem.archival_storage)

    print("\nSearch archival for 'topic_0':")
    print(mem.search_archival("topic_0"))
