# A Survey on Agentic LLMs — Study Guide

> **Citation:** Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei. arXiv 2025
> **arxiv:** https://arxiv.org/abs/2503.23037
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

By 2025, agentic LLM research had exploded in scope — covering planning, tool use, memory, multi-agent coordination, safety, and evaluation — but no recent survey synthesized the state of the field post-GPT-4. Practitioners needed an up-to-date map covering both foundational concepts and the latest production systems.

## The Core Idea (How did they solve it?)

The survey provides a structured overview of agentic LLM systems across six components: perception (how agents observe the world), memory (short and long term), planning (task decomposition strategies), action (tool use, code execution, agent delegation), learning (in-context, fine-tuning, RLHF), and safety. It covers both research systems and production frameworks (including AutoGen, LangChain, ADK), making it a practical reference for engineers building real systems.

## Key Figure to Understand

**Figure 1** — The agentic LLM system architecture showing the six-component loop: Perception → Memory → Planning → Action → (environment) → Observation → back to Perception. This is the unified mental model for every agentic system covered in the survey. Any paper in this reading list can be placed within this loop.

## How This Connects to MCP / A2A / ADK

- **MCP:** Sits in the Action layer — it is the protocol that makes tool use composable and server-agnostic across the entire agentic stack the survey describes.
- **A2A:** Sits in the Action layer alongside MCP, specifically for the "agent delegation" action type — calling another agent is an action, and A2A governs that interaction.
- **ADK:** Is the most complete framework coverage in the survey — it implements all six components. Understanding the survey's taxonomy makes ADK's design decisions legible.

## Three-Line Note (fill this in after reading)

- **Problem:**
- **Solution:**
- **Key insight:**

## Completion Checklist

- [ ] Read Abstract + Introduction
- [ ] Understood the key figure
- [ ] Can explain the core idea in 30 seconds without notes
- [ ] Filled in the Three-Line Note above
