# Multi-Agent Collaboration Mechanisms: A Survey of LLMs

Tran, Dao et al. | arXiv | 2025 | Link: https://arxiv.org/pdf/2501.06322.pdf

Read: —
Status: Not Started
Section: A

---

## One-Line Claim

A focused survey on how LLM agents actually communicate and coordinate — not what they do, but how the collaboration is structured — giving you a decision framework for choosing between centralized, decentralized, hierarchical, and dynamic topologies.

---

## Problem Being Solved

The previous surveys (like the IJCAI 2024 one) classified multi-agent systems by what they accomplish. This paper asks a more concrete design question: when you have multiple agents, how do you wire them together? The choice of communication topology, coordination strategy, and role assignment directly determines latency, fault tolerance, and scalability — but most papers just picked a structure without explaining why.

---

## Core Contribution

A three-layer classification of collaboration mechanisms:

**Layer 1 — Communication topology** (the wiring):
- *Centralized*: one orchestrator agent receives all inputs and routes to workers. Easy to reason about, single point of failure.
- *Decentralized*: agents communicate peer-to-peer. More resilient, but harder to keep globally coherent.
- *Hierarchical*: manager agents coordinate worker agents, possibly multiple levels deep. Scales to complex tasks but adds latency at each level.
- *Dynamic*: topology changes during execution. An agent that finishes a subtask can be reassigned. Rare but powerful for unpredictable workloads.

**Layer 2 — Coordination strategy** (how agents decide what to do next):
- *Sequential pipeline*: agent A outputs to agent B outputs to agent C. Simple, predictable, no parallelism.
- *Parallel execution*: multiple agents run simultaneously and outputs are merged. Faster but requires a coherent merge step.
- *Debate and voting*: agents generate competing responses, a judge or majority vote picks the winner. Better quality at higher cost.
- *Feedback loops*: agents review and revise each other's outputs iteratively. Highest quality ceiling, highest token cost.

**Layer 3 — Role assignment** (who does what):
- *Static*: roles defined in the system prompt before the run starts. Predictable but inflexible.
- *Dynamic*: an orchestrator assigns roles at runtime based on the task. More flexible, adds one LLM call overhead per assignment.
- *Emergent*: agents negotiate roles among themselves. Least predictable, occasionally discovers effective specializations that static assignment would miss.

---

## Architecture / Method

This is a literature review, not a system implementation. The authors collected papers implementing multi-agent LLM collaboration and annotated each one along the three layers. The value is the cross-layer analysis: most papers pick a topology, strategy, and role assignment independently, but the authors show these choices interact — for example, dynamic topology only makes sense paired with dynamic role assignment, and feedback loops require centralized coordination to avoid loops.

---

## Key Results

- Sequential pipelines are the most common coordination strategy, even though they leave parallelism on the table. The reason is simplicity: it is much easier to debug a linear chain than a parallel fan-out.
- Hierarchical topology + feedback loops is the highest-performing combination on complex tasks, but also the most expensive. The token cost scales roughly as O(depth × iterations).
- Dynamic role assignment improves performance on open-ended tasks where the right decomposition is not known upfront, but hurts on well-defined tasks where static assignment is faster and equally accurate.
- No paper in the survey used all three layers optimally together. Most implementations fix two layers and only vary one.

---

## Limitations and What It Does Not Address

- The three-layer model is clean but the layers interact in ways the survey acknowledges without fully resolving. Choosing a topology doesn't fully determine which coordination strategies are viable.
- Almost no coverage of async communication: all surveyed systems assume agents block and wait for responses. Real production systems will need async agent interactions.
- Does not address what happens when agents disagree and there is no clear winner — the "debate" pattern assumes a judge exists, but who judges the judge?
- No cost modeling. The survey describes what each pattern does but does not quantify what each combination costs in tokens or latency.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [LLM-Enabled Multi-Agent Systems Survey (IJCAI 2024)](../llm-multi-agent-survey/note.md) | Companion survey; that one classifies by capability, this one classifies by mechanism |
| [AutoGen (Wu, 2023)](../autogen-wu-2023/note.md) | Example of centralized topology + static roles + sequential/feedback coordination |
| [MetaGPT (Hong, 2023)](../metagpt-hong-2023/note.md) | Example of hierarchical topology + static roles + sequential pipeline |
| [CAMEL (Li, 2023)](../camel-li-2023/note.md) | Example of decentralized topology + static roles + peer-to-peer negotiation |
| [AgentScope (Alibaba, 2024)](../agentscope-alibaba-2024/note.md) | Example of dynamic topology; designed to handle the fault-tolerance gaps this survey identifies |
| [Reliable Decision-Making](../reliable-decision-making/note.md) | Directly addresses the debate/voting coordination strategy with aggregation methods |

---

## Implementation Angles

1. **Architecture decision log**: For every multi-agent project, explicitly document the choice for each of the three layers and why. This prevents the common failure mode where the wiring is decided implicitly and becomes impossible to change.

2. **Cost estimation before building**: The survey's observation that hierarchical + feedback loops is highest-cost is a direct input to experiments/aggregation-reliability. Measure token cost per layer combination before committing.

3. **Upgrade path**: Start with the simplest combination (centralized + sequential + static roles) and upgrade one layer at a time. This gives you a controlled baseline and isolates which layer is responsible for any performance improvement.

---

## Open Questions

- Is there a reliable way to detect at runtime when a sequential pipeline should be converted to a parallel fan-out? This would be the key to a truly adaptive coordination strategy.
- The emergent role assignment pattern is described as unpredictable. Is it unpredictable because the mechanism is noisy, or because the problem decomposition itself is ambiguous?

---

## Revision Notes

