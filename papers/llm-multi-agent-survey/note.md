# LLM-Enabled Multi-Agent Systems (Survey)

Taicheng Guo, Xiuying Chen, Yaqi Wang et al. | IJCAI 2024 | 2024 | Link: https://arxiv.org/pdf/2402.01680.pdf

---

## One-Line Claim

A structured survey that organizes the LLM multi-agent field into four dimensions — agents, environments, interactions, and collective capabilities — so you have a shared vocabulary before reading any implementation paper.

---

## Problem Being Solved

When you read AutoGen, MetaGPT, and CAMEL back to back, they all use the same words ("role," "agent," "collaboration") to mean different things. There was no standard taxonomy, which made it impossible to compare designs, identify what was genuinely novel in each paper, or make principled architecture choices. This survey builds that shared language.

---

## Core Contribution

A four-dimension framework for classifying any LLM multi-agent system:

1. **Agent profiles** — how individual agents are characterized. This includes role assignment (job title + instructions), memory access (what history the agent can see), and capability specification (what tools or skills the agent has).

2. **Environments** — what the agents operate inside. Can be virtual (text-based tasks, code sandboxes), physical (robotics), or hybrid. The environment determines what observations agents receive and what actions are valid.

3. **Interactions** — how agents communicate with each other. Three main patterns: cooperation (agents share a goal and divide work), competition (agents argue toward a better answer), and coevolution (agents adapt their strategies based on other agents' behavior over time).

4. **Collective capabilities** — what the system can do that a single agent cannot. Most common: task decomposition and parallel execution, cross-agent verification, and emergent specialization where agents develop distinct expertise during a run.

---

## Architecture / Method

This is a classification framework, not a runnable system. The authors reviewed roughly 150 papers from 2022–2024 and mapped each one onto the four dimensions. For each dimension they identified the most common patterns and named them consistently.

The most useful output is the interaction taxonomy. Under cooperation: role-playing pipelines (MetaGPT-style), hub-and-spoke (one orchestrator dispatches to workers), and peer-to-peer negotiation. Under competition: debate (two agents argue, a judge decides), adversarial critique (one agent generates, another attacks it). Under coevolution: agents update their prompts or behaviors based on what other agents did in prior rounds.

---

## Key Results

- Cooperation dominates the literature. Very few papers explore competition or coevolution, which are potentially powerful but harder to implement reliably.
- Role-based profiles (give each agent a job title and a system prompt) are by far the most common agent design. More sophisticated capability specifications (tool-equipped, memory-layered) are less common.
- Task decomposition + parallel execution is the most commonly implemented multi-agent pattern. Most "multi-agent" papers are essentially parallel CoT with a final aggregation step.
- Evaluation is the weakest part of the field. Most papers report only task success rate on a single benchmark. No paper in the survey comprehensively measures latency, token cost, and failure modes together.

---

## Limitations and What It Does Not Address

- Snapshots age fast. The taxonomy was built on papers through early 2024. Systems like AgentScope, OpenDevin, and AWM either postdate it or were not covered in depth.
- The four dimensions say nothing about timing: whether agents run synchronously or asynchronously, and how that affects coherence when shared state is involved.
- Heavy focus on text-based environments. The "physical" and "hybrid" environment categories are thin.
- Does not cover inference cost, latency, or anything about how these systems perform under real production load.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [AutoGen (Wu, 2023)](../autogen-wu-2023/note.md) | Primary example of the hub-and-spoke interaction pattern described here |
| [MetaGPT (Hong, 2023)](../metagpt-hong-2023/note.md) | Primary example of role-based profiles + sequential pipeline collaboration |
| [CAMEL (Li, 2023)](../camel-li-2023/note.md) | Primary example of peer-to-peer role-playing interaction |
| [CoALA (2023)](../coala-2023/note.md) | Fills in the memory detail that this survey's "agent profile" dimension leaves vague |
| [AgentBench (Liu, 2023)](../agentbench-liu-2023/note.md) | Directly addresses the evaluation gap this survey identifies |

---

## Implementation Angles

1. **Design checklist**: Before starting any multi-agent project, use the four dimensions as a checklist. Write down: what is each agent's profile, what environment does it operate in, what interaction pattern connects the agents, and what collective capability justifies using multiple agents at all.

2. **Interaction pattern selection**: Read the interaction section before choosing an architecture for experiments/multi-agent-patterns. Cooperation, competition, and coevolution produce different error modes and different token cost profiles — pick based on what failure mode you can tolerate.

3. **Evaluation design**: Use the survey's finding that most papers only measure success rate as a warning. Design experiments to capture latency and cost alongside accuracy from the start.

---

## Open Questions

- Does the coevolution pattern (agents updating strategies across rounds) work at inference time without fine-tuning, or does it require weight updates to stick?
- The survey shows cooperation dominates — is that because competition genuinely underperforms, or because it is harder to implement correctly and gets abandoned?

---

## Revision Notes

