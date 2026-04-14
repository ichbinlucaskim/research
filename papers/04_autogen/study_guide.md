# AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation — Study Guide

> **Citation:** Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang, Xiaoyun Zhang, Chi Wang. arXiv 2023
> **arxiv:** https://arxiv.org/abs/2308.08155
> **Reading time:** ~1 hour

---

## The Problem (Why does this paper exist?)

Single LLM agents hit capability ceilings on complex tasks: one model cannot simultaneously excel at planning, coding, testing, and critique. There was no general framework for decomposing complex tasks across multiple specialized LLM agents that could converse, check each other's work, and iterate to a solution.

## The Core Idea (How did they solve it?)

AutoGen defines a `ConversableAgent` abstraction where each agent has a system prompt (defining its role), a set of tools, and the ability to send and receive messages from any other agent. Conversations between agents are the primitive — an orchestrator agent delegates to specialists, specialists reply, and the orchestrator decides when the conversation is done. The human-in-the-loop is just another agent with a special input mechanism, making it trivial to add or remove human oversight.

## Key Figure to Understand

**Figure 1** — The AutoGen conversation patterns diagram showing three configurations: two-agent chat, group chat with a GroupChatManager, and hierarchical nested chat. This illustrates that AutoGen's agent abstraction composes — you can build any topology from the same primitive.

## How This Connects to MCP / A2A / ADK

- **MCP:** Each AutoGen agent's tools are MCP tools — the agent sends MCP-formatted tool calls and receives results within the conversation turn.
- **A2A:** AutoGen's inter-agent messaging is exactly what A2A formalizes at the protocol level. A2A adds authentication, discovery, and transport guarantees to what AutoGen does informally in-process.
- **ADK:** ADK's multi-agent patterns (orchestrator + sub-agents) directly implement the AutoGen group chat pattern. ADK's `AgentTool` wraps a sub-agent the same way AutoGen treats agents as callable tools.

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
