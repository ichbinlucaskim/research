# ReAct: Synergizing Reasoning and Acting in Language Models — Study Guide

> **Citation:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. ICLR 2023
> **arxiv:** https://arxiv.org/abs/2210.03629
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

Prior to ReAct, LLMs were used either for reasoning (chain-of-thought) or for acting (tool use), but never in a unified loop. Pure reasoning approaches hallucinated facts, and pure action approaches lacked the ability to plan or recover from errors. There was no framework that let an agent think about what to do, do it, and then incorporate what it learned.

## The Core Idea (How did they solve it?)

ReAct interleaves Thought, Action, and Observation traces in a single LLM prompt. The model generates a thought about what to do next, emits an action (e.g., search a query), receives an observation from the environment, then repeats. This loop lets the model self-correct mid-task: if a search returns unexpected results, the next thought can adjust the plan. The key insight is that reasoning and acting are not separate phases — they inform each other turn by turn.

## Key Figure to Understand

**Figure 1** — The side-by-side comparison of ReAct vs. CoT vs. Act-only traces on a HotpotQA question. It shows how CoT hallucinates an answer, Act-only takes wrong actions without reasoning, and ReAct recovers from a bad search by thinking before the next action.

## How This Connects to MCP / A2A / ADK

- **MCP:** The Action step in ReAct maps directly to MCP tool calls — the model emits a structured tool invocation and receives an observation (tool result). MCP is essentially the transport layer for the Action→Observation steps.
- **A2A:** ReAct's loop can span multiple agents — one agent's Observation is another agent's Task. A2A's task delegation protocol is the multi-agent generalization of the single-agent ReAct loop.
- **ADK:** ADK's `LlmAgent` runs a ReAct-style loop internally. The `tools` list in ADK corresponds to the action space; the agent's scratchpad is the Thought trace.

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
