# Voyager: An Open-Ended Embodied Agent with Large Language Models — Study Guide

> **Citation:** Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar. arXiv 2023
> **arxiv:** https://arxiv.org/abs/2305.16291
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

Prior agents in open-ended environments (like Minecraft) had to re-learn skills from scratch every time, could not accumulate knowledge across episodes, and could not generalize learned behaviors to new tasks. There was no mechanism for an agent to build a growing library of reusable capabilities over its lifetime.

## The Core Idea (How did they solve it?)

Voyager introduces three components that work together: an automatic curriculum (the agent proposes its own next task based on what it can already do), a skill library (verified executable code snippets stored and retrieved by semantic similarity), and an iterative prompting mechanism (the agent refines code until it works, then commits it to the library). The key insight is that skills are programs, not weights — storing them as code makes them human-readable, combinable, and transferable without retraining.

## Key Figure to Understand

**Figure 2** — The Voyager system overview showing the three-component loop: curriculum proposes a task → code-writing LLM generates a skill → execution environment tests it → if it succeeds, the skill is added to the library → curriculum uses the library state to propose the next task. This closed loop is what enables lifelong learning.

## How This Connects to MCP / A2A / ADK

- **MCP:** The skill library is an MCP resource — skills are stored externally and retrieved as tool definitions that the agent can invoke. MCP's tool schema is a natural format for Voyager-style skill signatures.
- **A2A:** Skills verified by one agent can be shared to others via A2A's capability advertisement. An agent can publish a new skill as a new A2A endpoint.
- **ADK:** ADK's custom tools are Voyager skills made explicit — a verified skill becomes an ADK `FunctionTool`. ADK's tool registry is the production skill library.

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
