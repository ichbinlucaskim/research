# Large Language Model based Multi-Agents: A Survey of Progress and Challenges — Study Guide

> **Citation:** Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V. Chawla, Olaf Wiest, Xiangliang Zhang. arXiv 2024
> **arxiv:** https://arxiv.org/abs/2402.01680
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

The multi-agent LLM space was fragmented: dozens of systems (AutoGen, MetaGPT, CAMEL, etc.) were proposed in quick succession with no unified taxonomy. Researchers and practitioners needed a comprehensive map of the design space — what dimensions differ, what has been tried, what remains unsolved.

## The Core Idea (How did they solve it?)

The survey organizes LLM multi-agent systems along five dimensions: (1) agent profiles (how roles are defined), (2) agent communication (topology and message format), (3) agent capabilities (memory, planning, tool use), (4) application domains, and (5) evaluation methodologies. By mapping every major system onto these axes, the survey reveals which combinations have been explored and which represent open research problems.

## Key Figure to Understand

**Figure 2** — The taxonomy tree of LLM multi-agent systems. The tree branches on agent profile type (role-based vs. model-based), then on communication topology (layered vs. decentralized vs. centralized), then on capability primitives. Reading this figure gives you a mental model for placing any new paper you encounter.

## How This Connects to MCP / A2A / ADK

- **MCP:** Maps to "tool use" in the capabilities dimension — MCP standardizes the tool-use interface across all agent types the survey covers.
- **A2A:** Maps to "agent communication" — A2A is a concrete protocol instantiation of the decentralized communication topology the survey identifies as an open challenge.
- **ADK:** Maps to the full stack — ADK implements agent profiles (roles), communication (AgentTool), and capabilities (memory, tools) in a single framework.

## Three-Line Note (fill this in after reading)

- **Problem:**
- **Solution:**
- **Key insight:**

## Completion Checklist

- [ ] Read Abstract + Introduction
- [ ] Understood the key figure
- [ ] Can explain the core idea in 30 seconds without notes
- [ ] Filled in the Three-Line Note above
