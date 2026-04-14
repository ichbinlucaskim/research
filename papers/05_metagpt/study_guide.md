# MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework — Study Guide

> **Citation:** Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber. ICLR 2024
> **arxiv:** https://arxiv.org/abs/2308.00352
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

Multi-agent systems for software development tend to produce inconsistent output because agents communicate in free-form natural language, leading to ambiguity and compounding errors. There was no framework that enforced structured, role-appropriate outputs that downstream agents could reliably consume.

## The Core Idea (How did they solve it?)

MetaGPT assigns each agent a human software role (PM, Architect, Engineer, QA) and requires each role to produce structured artifacts matching real-world deliverables: the PM produces a PRD, the Architect produces a system design document, the Engineer produces code files, the QA produces test cases. Agents communicate via a shared message pool, but they only consume messages tagged for their role. This "standardized operating procedure" eliminates the ambiguity of free-form inter-agent chat.

## Key Figure to Understand

**Figure 3** — The MetaGPT workflow diagram showing the sequential pipeline: human requirement → PM (PRD) → Architect (System Design) → Engineer (Code) → QA (Tests) → execution. The structured documents at each step are shown as artifacts, making it clear that structured outputs — not conversations — are the inter-agent interface.

## How This Connects to MCP / A2A / ADK

- **MCP:** MetaGPT's structured artifacts are MCP resources — the PRD, design doc, and code files are resources that downstream agents retrieve via MCP, not freeform messages.
- **A2A:** MetaGPT's role-to-role handoffs are A2A task delegations. The structured artifact format is the A2A task payload schema — strongly typed, role-appropriate.
- **ADK:** ADK's `SequentialAgent` implements the MetaGPT pipeline pattern. Each sub-agent is a role; ADK's shared `State` object is the message pool.

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
