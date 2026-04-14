# MemGPT: Towards LLMs as Operating Systems — Study Guide

> **Citation:** Charles Packer, Vivian Fang, Shishir G. Patil, Kevin Lin, Sarah Wooders, Joseph E. Gonzalez. NeurIPS 2023
> **arxiv:** https://arxiv.org/abs/2310.08560
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

LLMs have a fixed context window, which means they forget everything outside that window. For long-running agents — personal assistants, coding agents, customer service bots — this is a fundamental limitation. There was no principled architecture for managing what an agent "remembers" across arbitrarily long conversations and tasks.

## The Core Idea (How did they solve it?)

MemGPT treats the LLM context window like a CPU's registers: fast and limited. It introduces a two-tier memory hierarchy — main context (in-window, immediately accessible) and archival storage (out-of-window, retrieved on demand). The LLM itself decides when to move memories between tiers by calling special memory-management functions. This mirrors how an OS manages RAM vs. disk: the program (LLM) controls paging, not the hardware (runtime).

## Key Figure to Understand

**Figure 2** — The MemGPT architecture diagram showing main context (system prompt, conversation history, working memory) and the archival/recall storage tiers. The arrows show the LLM issuing `memory_append`, `memory_search`, and `memory_replace` function calls to manage state across tiers.

## How This Connects to MCP / A2A / ADK

- **MCP:** MemGPT's memory functions are MCP tools — `memory_search` and `memory_append` are tool calls the LLM makes via MCP's tool-use protocol. The memory backend is an MCP server resource.
- **A2A:** In a multi-agent system, MemGPT's archival storage can be shared across agents via A2A — one agent writes to archival, another retrieves it, enabling persistent shared state.
- **ADK:** ADK's `Session` and `State` objects are the production equivalent of MemGPT's memory tiers. ADK's `MemoryService` directly implements the archival storage concept.

## Three-Line Note (fill this in after reading)

- **Problem:**
- **Solution:**
- **Key insight:**

## Completion Checklist

- [ ] Read Abstract + Introduction
- [ ] Understood the key figure
- [ ] Can explain the core idea in 30 seconds without notes
- [ ] Filled in the Three-Line Note above
- [ ] Implemented the coding exercise (if applicable)
