"""
MemGPT: Towards LLMs as Operating Systems — Solution

This is the reference implementation.
Study this ONLY after attempting exercise_problem.py for at least 20 minutes.

Key insight demonstrated:
  The LLM's context window is a finite resource — the memory manager, not the LLM,
  is responsible for deciding what stays in-context and what gets paged to archival.
"""


class MemoryManager:
    """Two-tier memory: fixed-size main_context (hot) + unlimited archival_storage (cold)."""

    MAX_CONTEXT_SIZE = 10

    def __init__(self):
        self.main_context: list[str] = []
        self.archival_storage: list[str] = []

    def add_memory(self, item: str) -> None:
        """Add item to main context, evicting oldest to archival if at capacity."""
        if len(self.main_context) >= self.MAX_CONTEXT_SIZE:
            evicted = self.main_context.pop(0)  # evict oldest
            self.archival_storage.append(evicted)
        self.main_context.append(item)

    def search_archival(self, query: str) -> list[str]:
        """Return all archival items containing query (case-insensitive substring match)."""
        query_lower = query.lower()
        return [item for item in self.archival_storage if query_lower in item.lower()]

    def get_context_for_llm(self) -> str:
        """Format main_context as a numbered string for inclusion in an LLM prompt."""
        return "\n".join(f"[{i}] {item}" for i, item in enumerate(self.main_context))


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
