# Small Language Models are the Future of Agentic AI

Petr Belcak, Rainer W. Heinrichs (NVIDIA Research) | arXiv | 2025 | Link: https://arxiv.org/pdf/2506.02153.pdf

Read: —
Status: Not Started
Section: A

---

## One-Line Claim

Running a frontier LLM for every subtask in an agent system is economically and architecturally wasteful — most agent subtasks are narrow enough that a small, specialized model outperforms a large general one while costing far less per call.

---

## Problem Being Solved

When people build multi-agent systems today, the default is to use the same large frontier model (GPT-4, Claude 3, Gemini) for every agent in the pipeline. This is expensive, slow, and architecturally sloppy. An agent that only needs to extract dates from text does not need 70 billion parameters. An agent that only routes messages between other agents does not need deep reasoning capability. The paper asks: what is the minimum model size needed for each specific agent role, and what does the system look like when you match model size to task requirements?

---

## Core Contribution

A principled framework for matching model size to agent role, built on three arguments:

**1. Most agent subtasks are narrow by design.** In a well-structured multi-agent system, each agent does one thing: extract, route, verify, summarize, or call a tool. Narrow tasks have bounded input/output distributions that small, fine-tuned models can cover with high reliability. A 7B model fine-tuned on routing decisions outperforms a 70B general model on routing, because the fine-tuned model has learned the specific pattern rather than averaging across everything.

**2. Inference cost compounds in agent loops.** A single frontier model call is expensive but manageable. An agent loop that makes 20 sequential calls — common for ReAct or Reflexion on complex tasks — multiplies that cost by 20. If 15 of those calls are simple extractions or routing decisions, replacing them with a small specialized model reduces total loop cost by 60–80% while maintaining or improving overall task accuracy.

**3. Smaller models have lower latency per token.** Time-to-first-token and tokens-per-second are both better for smaller models at equivalent hardware. In latency-sensitive agent loops (interactive assistants, real-time pipelines), this matters independently of cost. A 7B model generating 200 tokens/s is faster in an agentic loop than a 70B model generating 50 tokens/s, even if both produce correct outputs.

**The NVIDIA Nemotron angle**: The paper situates this argument in the context of NVIDIA's Nemotron model family, which is explicitly designed for deployment as specialized components within larger agent systems rather than as general-purpose assistants. Nemotron models are sized and fine-tuned for specific agent roles: tool use, reasoning, extraction, and reward modeling.

---

## Architecture / Method

The paper proposes a role-based model assignment framework:

**Step 1 — Role taxonomy**: Classify every agent in the system by its primary operation type. The paper identifies five categories: reasoning (multi-step planning, requires a larger model), extraction (structured output from text, small model is sufficient), routing (classification into one of N options, smallest model is fine), verification (checking correctness, mid-size model with specific fine-tuning), tool execution (parsing a tool call and formatting the output, small model).

**Step 2 — Minimum viable model selection**: For each role, identify the smallest model that achieves target accuracy on a representative sample of that role's tasks. This is the model floor — you should not go smaller, but you should not go larger either.

**Step 3 — Coordination layer**: A lightweight orchestrator (can itself be a small model) routes requests to the appropriate specialized model. The orchestrator does not do the work — it only decides who should.

The resulting system looks like a microservices architecture where each service is a fine-tuned small model rather than a monolithic large one.

---

## Key Results

- On routing and extraction tasks, 7B fine-tuned models match or exceed GPT-4 performance with 10–20x lower per-call cost.
- Reasoning-heavy subtasks (multi-step planning, complex code generation) still require larger models (30B+). The small model advantage disappears when the task requires genuine generalization.
- Agent loops using mixed model sizes (small for narrow tasks, large only for reasoning) achieve comparable end-to-end task accuracy to all-large pipelines at 40–70% lower total token cost.
- Latency improvements are consistent: replacing large-model extraction and routing calls with small models reduces median agent loop completion time by 30–50% on the tasks tested.

---

## Limitations and What It Does Not Address

- The framework assumes you can clearly classify every agent subtask into one of the five role categories. In practice, agent subtasks blur together — an agent might need to reason and then immediately extract, in a single step.
- Fine-tuning small models for specific roles requires labeled data for each role. Acquiring and maintaining that data is a real operational cost that the paper does not model.
- The paper is optimistic about fine-tuned small models on narrow tasks, but fine-tuned models are fragile — they perform well within their training distribution and degrade on edge cases. Frontier models are more robust to unexpected inputs.
- The Nemotron framing means some recommendations may be specific to NVIDIA hardware and deployment infrastructure (TensorRT-LLM, NIM microservices), which may not apply directly to other serving stacks.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [vLLM (Kwon, 2023)](../vllm-kwon-2023/note.md) | The serving infrastructure for small models; PagedAttention is more efficient at small model sizes |
| [TensorRT-LLM (NVIDIA)](../tensorrt-llm-nvidia/note.md) | The hardware-specific serving layer that makes NVIDIA small model deployment economically viable |
| [AutoGen (Wu, 2023)](../autogen-wu-2023/note.md) | AutoGen's conversable agent abstraction is the coordination layer this paper's model assignment sits on top of |
| [Orca: Continuous Batching (Yu, 2022)](../orca-yu-2022/note.md) | Continuous batching becomes even more important when running many small specialized models simultaneously |
| [DSPy (Khattab, 2023)](../dspy-khattab-2023/note.md) | DSPy's programmatic optimization could be used to automatically find which model size is needed per role |
| [Scaling Laws (Kaplan, 2020)](../scaling-laws-kaplan-2020/note.md) | Scaling laws explain why smaller models are good enough for narrow tasks: narrower task = smaller effective problem space = lower capability threshold |

---

## Implementation Angles

1. **agent-inference-profiler design**: Instrument every agent call in a pipeline with the role category it belongs to (reasoning / extraction / routing / verification / tool). Use the profiler output to identify which calls are "over-modeled" — using a large model for an extraction task — and are candidates for replacement.

2. **streaming-agent-server architecture**: Design the server to support multiple model endpoints (a 7B endpoint for extraction/routing, a 34B endpoint for reasoning) rather than a single monolithic endpoint. Route calls at the serving layer based on task type.

3. **cost baseline measurement**: Before any optimization, measure the cost breakdown of a research-operator-v0 pipeline run by role type. The paper predicts that extraction and routing calls will dominate call count while reasoning calls will dominate token cost. Verify this empirically before deciding what to optimize.

---

## Open Questions

- The paper claims fine-tuned small models match GPT-4 on extraction tasks. Does this hold when the extraction is embedded in a longer, more complex agent context — or does the small model struggle with the surrounding noise?
- The five role categories are intuitive but not exhaustive. What role category does "explain your reasoning" or "write a high-quality narrative summary" fall into? These feel like reasoning tasks but might be handled by a smaller writing-specialized model.

---

## Revision Notes

