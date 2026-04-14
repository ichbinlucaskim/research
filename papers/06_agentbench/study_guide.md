# AgentBench: Evaluating LLMs as Agents — Study Guide

> **Citation:** Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhiyuan Liu, Yuxiao Dong, Jie Tang. ICLR 2024
> **arxiv:** https://arxiv.org/abs/2308.03688
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

As LLM agents proliferated, there was no standardized benchmark for evaluating them across realistic, interactive environments. Existing benchmarks tested static QA or code generation but not multi-step decision-making in OS, web, database, or game environments. Without a shared evaluation framework, comparing agent architectures was impossible.

## The Core Idea (How did they solve it?)

AgentBench defines 8 distinct interactive environments (web browsing, OS shell, database manipulation, card games, etc.) and a unified evaluation protocol: each task has a structured description, a real or simulated environment the agent acts in, and a verifiable success criterion. The benchmark reveals that commercial LLMs dramatically outperform open-source models on agent tasks — a gap that doesn't appear in static benchmarks — exposing the unique demands of sequential decision-making.

## Key Figure to Understand

**Figure 1** — The AgentBench evaluation pipeline: a task description is given to the agent, the agent emits actions, the environment executes them and returns observations, and this loop continues until the agent declares completion or hits a step limit. The figure also shows the 8 environment types and how each maps to a real-world agentic use case.

## How This Connects to MCP / A2A / ADK

- **MCP:** AgentBench's Action→Observation loop is the MCP tool call cycle at evaluation time — each action is a tool invocation, each observation is a tool result. Building an AgentBench environment is equivalent to building an MCP server.
- **A2A:** AgentBench environments can be wrapped as A2A agents — the evaluation harness becomes an A2A client, and each environment is a specialized A2A agent that accepts tasks and returns results.
- **ADK:** ADK's `EvaluationHarness` (evaluation tools) is the production version of AgentBench's eval loop. Designing ADK agent evaluations requires the same task/environment/metric decomposition AgentBench defines.

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
