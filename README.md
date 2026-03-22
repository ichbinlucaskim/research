# Agent AI Architecture — Solo Research Lab

Personal research conducted with the rigor of an institutional lab.
> The pipeline is: read paper -> run experiment -> build project -> iterate.

---

## Repository Structure

```
/
├── papers/          # Paper notes: summary, core ideas, implementation angles
├── experiments/     # Controlled pattern comparison experiments
└── projects/        # Small end-to-end systems combining multiple patterns
```

---

## Reading Priority

Start here before opening any paper folder.

```
1.  CoALA                                    Establish design vocabulary and architecture taxonomy first
2.  Attention Is All You Need                Understand the substrate everything runs on
3.  CoT -> Self-Consistency -> ToT -> LATS   Trace the full reasoning evolution in sequence
4.  ReAct -> Reflexion -> FuseMind           Core agent loop design
5.  AutoGen + MetaGPT                        Most-referenced frameworks during implementation
6.  MemGPT + CoALA (revisit)                 Memory layer design decisions
7.  Self-RAG + RAPTOR                        Selective retrieval and long-document indexing
8.  Toolformer -> Gorilla -> ToolBench       Tool use from first principles to benchmark
9.  vLLM + FlashAttention 2                  Inference economics: every agent runs on a serving stack
10. SWE-bench + LLM-as-Judge                 Set measurement baselines before designing experiments
11. Constitutional AI + Prompt Injection      Safety is an architectural constraint, not a post-hoc filter
12. DSPy                                     Rethink how you approach prompt engineering entirely
13. 2024-2025 papers                         Close the gap to the current frontier
```

---

## Papers

---

### A. Big Picture and Multi-Agent

The map of what components exist, what control-flow patterns are available, and how agents are deployed in real software systems.

| Paper | Role |
|---|---|
| [LLM-Enabled Multi-Agent Systems (Survey)](./papers/llm-multi-agent-survey/note.md) | Component taxonomy and control-flow pattern overview |
| [Multi-Agent Collaboration Mechanisms: A Survey of LLMs](./papers/multi-agent-collab-survey/note.md) | Collaboration mechanism classification |
| [LLM-Powered Multi-Agent Systems: A Technical Framework (IEEE)](./papers/llm-framework-ieee/note.md) | Technical framework and architectural perspective |
| [LLM-Based Multi-Agent Systems for Software Engineering (ACM)](./papers/llm-agents-swe-acm/note.md) | Application to real software engineering workflows |
| [NVIDIA: Smaller LMs for Agents (Nemotron / SLM)](./papers/nvidia-slm-agents/note.md) | Small model roles in agent systems, inference cost perspective |

---

### B. Reasoning Foundation

ReAct without understanding its reasoning lineage is a partial understanding. Read these in order. Each paper is a direct response to the limitations of the previous one.

| Paper | Role |
|---|---|
| [Chain-of-Thought Prompting (Wei et al., 2022)](./papers/chain-of-thought-wei-2022/note.md) | The root of all agent reasoning. Explicit step-by-step reasoning elicitation |
| [Self-Consistency (Wang et al., 2023)](./papers/self-consistency-wang-2023/note.md) | Multiple reasoning paths + majority vote = reliability improvement. Directly feeds into aggregation experiments |
| [Tree of Thoughts (Yao et al., 2023)](./papers/tree-of-thoughts-yao-2023/note.md) | Breaks linear reasoning into tree search. Enables backtracking and exploration. Direct predecessor to LATS |
| [LATS: Language Agent Tree Search (2023)](./papers/lats-2023/note.md) | Integrates ToT + MCTS + ReAct. Currently the strongest single-agent planning architecture |

Experiments: [`experiments/reasoning-evolution`](./experiments/reasoning-evolution/README.md)

---

### C. ReAct / Tool-Use / Reflection / Planning

The canonical agent loop and its direct extensions.

| Paper | Role |
|---|---|
| [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](./papers/react-yao-2022/note.md) | The origin of the Reason + Act loop. Reference point for all agent loop design |
| [Reflexion (Shinn et al., 2023)](./papers/reflexion-shinn-2023/note.md) | Post-task verbal reflection for self-improvement without gradient updates |
| [ReflAct](./papers/reflact-2023/note.md) | Combines Reflexion + ReAct into a unified structure |
| [FuseMind: Fusing Reflection and Prediction in Agents](./papers/fusemind-2023/note.md) | Adds next-action prediction to reflection. Efficiency improvement through anticipation |

Experiments: [`experiments/react-vs-cot`](./experiments/react-vs-cot/README.md), [`experiments/react-vs-reflexion-vs-fusemind`](./experiments/react-vs-reflexion-vs-fusemind/README.md)

---

### D. Tool Use and Function Calling

Tool calling is the agent's interface to the world. Without this lineage, half of agent system design is missing.

| Paper | Role |
|---|---|
| [Toolformer (Schick et al., 2023)](./papers/toolformer-schick-2023/note.md) | First work on LLMs learning where to insert tool calls via self-supervised training |
| [Gorilla (Patil et al., 2023)](./papers/gorilla-patil-2023/note.md) | API-call-specialized LLM. Core reference for how tool specifications are injected into context |
| [ToolBench / ToolLLM (Qin et al., 2023)](./papers/toolbench-qin-2023/note.md) | 16,000-API benchmark + DFS decision tree for tool selection. Largest tool-use evaluation suite |

Experiments: [`experiments/tool-use-strategies`](./experiments/tool-use-strategies/README.md)

---

### E. Multi-Agent Framework Papers

Not surveys. These are the papers that actually defined the implementation patterns in common use today.

| Paper | Role |
|---|---|
| [AutoGen (Wu et al., Microsoft, 2023)](./papers/autogen-wu-2023/note.md) | Closest to an industry standard for multi-agent conversation. Conversable agent abstraction |
| [MetaGPT (Hong et al., 2023)](./papers/metagpt-hong-2023/note.md) | Role-based agents (PM / Engineer / QA). Encodes SOPs into agent collaboration structure |
| [CAMEL (Li et al., 2023)](./papers/camel-li-2023/note.md) | Role-playing for autonomous agent-to-agent collaboration. Inception prompting concept |
| [HuggingGPT / JARVIS (Shen et al., 2023)](./papers/hugginggpt-shen-2023/note.md) | LLM as controller, external specialized models as tools. Canonical orchestration pattern |

Experiments: [`experiments/multi-agent-patterns`](./experiments/multi-agent-patterns/README.md)

---

### F. RAG / Memory / Context

RAG alone is not a memory architecture. This section covers the full stack from naive retrieval to cognitive memory design.

| Paper | Role |
|---|---|
| [Retrieval-Augmented Generation (Lewis et al., 2020)](./papers/rag-lewis-2020/note.md) | Dense Passage Retriever + joint fine-tuning. The baseline for all agent knowledge layers |
| [MemGPT (Packer et al., 2023)](./papers/memgpt-packer-2023/note.md) | Applies OS virtual memory concepts to LLMs. The reference design for infinite-context agents |
| [CoALA: Cognitive Architectures for Language Agents (2023)](./papers/coala-2023/note.md) | Classifies agent memory into Working / Episodic / Semantic / Procedural. The most rigorous architectural taxonomy available. Without this, design language is unstable |
| [Self-RAG (Asai et al., 2023)](./papers/self-rag-asai-2023/note.md) | Model decides whether retrieval is needed at all. Defines the always-retrieve vs. selective-retrieve tradeoff |
| [RAPTOR (Sarthi et al., 2024)](./papers/raptor-sarthi-2024/note.md) | Recursive document summarization into tree-indexed structures. Current best practice for long-document RAG |

Experiments: [`experiments/rag-comparison`](./experiments/rag-comparison/README.md), [`experiments/rag-retriever-strategies`](./experiments/rag-retriever-strategies/README.md), [`experiments/self-rag-vs-naive-rag`](./experiments/self-rag-vs-naive-rag/README.md), [`experiments/memory-architecture`](./experiments/memory-architecture/README.md), [`experiments/raptor-vs-flat-rag`](./experiments/raptor-vs-flat-rag/README.md)

---

### G. Reliability / Ops / Evaluation

How to aggregate agent outputs to improve reliability, and how real deployments fail.

| Paper | Role |
|---|---|
| [Reliable Decision-Making for Multi-Agent LLM Systems](./papers/reliable-decision-making/note.md) | Aggregation and ensemble methods for reliability improvement across agent runs |
| [AI Agents in 2025: Expectations vs. Reality (IBM)](./papers/ai-agents-reality-ibm/note.md) | Realistic operational limits and deployment failure modes |
| [SWE-bench (Jimenez et al., 2024)](./papers/swe-bench-jimenez-2024/note.md) | Real GitHub issues as agent tasks. De facto standard benchmark for software agents |
| [AgentBench (Liu et al., 2023)](./papers/agentbench-liu-2023/note.md) | Comprehensive agent evaluation across 8 environments: web, database, OS, etc. |
| [WebArena (Zhou et al., 2023)](./papers/webarena-zhou-2023/note.md) | Realistic web task automation benchmark with live environments |
| [LLM-as-a-Judge (Zheng et al., 2023)](./papers/llm-as-judge-zheng-2023/note.md) | Using LLMs to evaluate LLM outputs. Foundation for automated evaluation pipelines |

Experiments: [`experiments/aggregation-reliability`](./experiments/aggregation-reliability/README.md), [`experiments/monitoring-ops`](./experiments/monitoring-ops/README.md), [`experiments/llm-as-judge-pipeline`](./experiments/llm-as-judge-pipeline/README.md)

---

### H. Safety and Alignment

Once an agent takes real actions, safety is an architectural constraint, not an add-on.

| Paper | Role |
|---|---|
| [Constitutional AI (Anthropic, 2022)](./papers/constitutional-ai-bai-2022/note.md) | Model-level safety principles. Thinking framework for designing guard agents |
| [R-Judge / Agent Safety Bench (2024)](./papers/r-judge-2024/note.md) | Benchmark for detecting dangerous actions in agent environments |
| [Prompt Injection Attacks on LLM Agents (2023+)](./papers/prompt-injection-2023/note.md) | Instruction injection from external data. The primary attack surface for RAG + tool agents |

Experiments: [`experiments/guard-agent`](./experiments/guard-agent/README.md), [`experiments/prompt-injection-defense`](./experiments/prompt-injection-defense/README.md)

---

### I. LLM Foundations

An agent architect who does not understand what is happening inside the model is essentially an API wrapper engineer. These are non-negotiable.

| Paper | Role |
|---|---|
| [Attention Is All You Need (Vaswani et al., 2017)](./papers/attention-vaswani-2017/note.md) | Mechanical understanding of transformers. Required to reason about latency, context window cost, and orchestration overhead |
| [Scaling Laws for Neural Language Models (Kaplan et al., 2020)](./papers/scaling-laws-kaplan-2020/note.md) | Informs every decision about model size selection for specific agent roles |
| [GPT-4 Technical Report (OpenAI, 2023)](./papers/gpt4-openai-2023/note.md) | Understanding the current capability frontier you are architecting on top of |
| [LLaMA / LLaMA 2 / LLaMA 3 (Meta)](./papers/llama-meta-2023/note.md) | The open-weight foundation. Most production inference infrastructure is built around these |
| [Mistral 7B / Mixtral 8x7B](./papers/mixtral-2024/note.md) | MoE architecture. Directly relevant to efficient agent inference and role-specialized routing |

---

### J. Inference and Systems

This is the category most agent builders ignore, and the one NVIDIA operates at. An architect who cannot identify where the compute bottleneck is in their system is not an architect.

| Paper / Resource | Role |
|---|---|
| [FlashAttention 1 and 2 (Dao et al., 2022 / 2023)](./papers/flashattention-dao-2022/note.md) | Why long-context agents are expensive and how it is being solved at the hardware level |
| [Orca: Continuous Batching (Yu et al., 2022)](./papers/orca-yu-2022/note.md) | How inference servers handle concurrent agent requests. The foundation for vLLM |
| [vLLM: PagedAttention (Kwon et al., 2023)](./papers/vllm-kwon-2023/note.md) | The actual system running most production agent backends today. KV cache paging |
| [Speculative Decoding (Leviathan et al., 2023)](./papers/speculative-decoding-leviathan-2023/note.md) | How fast token generation is achieved. Critical for latency-sensitive agent loops |
| [SGLang (Zheng et al., 2024)](./papers/sglang-zheng-2024/note.md) | Structured generation and agent-specific inference optimization. Radix attention for prefix caching |
| [TensorRT-LLM (NVIDIA documentation)](./papers/tensorrt-llm-nvidia/note.md) | If you are building on NVIDIA hardware, this is not optional reading |

Experiments: [`experiments/inference-serving-comparison`](./experiments/inference-serving-comparison/README.md), [`experiments/latency-cost-profiling`](./experiments/latency-cost-profiling/README.md), [`experiments/speculative-decoding-impact`](./experiments/speculative-decoding-impact/README.md), [`experiments/context-window-scaling`](./experiments/context-window-scaling/README.md)

---

### K. Control Flow and Compiler-Level Architecture

What separates someone who builds agents from someone who architects agent systems is the ability to reason about control flow at the structural level.

| Paper / Resource | Role |
|---|---|
| [Executable Code Actions Elevate LLM Agents (Wang et al., 2024)](./papers/executable-code-actions-wang-2024/note.md) | Code as action space vs. JSON as action space. One of the most consequential architectural decisions in agent design |
| [LangGraph design documentation and LCEL](./papers/langgraph-lcel/note.md) | Control flow patterns for stateful agent graphs. Cyclic vs. DAG structures and why it matters |
| [Flows: Building Blocks for Multi-Agent Systems (EPFL, 2024)](./papers/flows-epfl-2024/note.md) | Formal treatment of agent composition. Most rigorous available framework for agent interface design |
| [DSPy (Khattab et al., 2023 / 2024)](./papers/dspy-khattab-2023/note.md) | Programmatic prompt optimization. Changes how you think about prompt engineering: from manual tuning to compiled programs |

Experiments: [`experiments/code-vs-json-action-space`](./experiments/code-vs-json-action-space/README.md), [`experiments/dspy-vs-manual-prompting`](./experiments/dspy-vs-manual-prompting/README.md)

---

### L. 2024-2025 Frontier Papers

The earlier sections skew heavily toward 2023. These close the gap to the current frontier.

| Paper | Role |
|---|---|
| [Agent Workflow Memory (AWM, 2024)](./papers/awm-2024/note.md) | Agents that learn and reuse workflow patterns from experience, beyond episodic memory |
| [OpenDevin / SWE-agent (2024)](./papers/opendevin-2024/note.md) | Current state of the art for coding agents. SWE-bench is the benchmark; these are the actual systems |
| [AgentScope (Alibaba, 2024)](./papers/agentscope-alibaba-2024/note.md) | Production-grade multi-agent framework with serious fault-tolerance and scheduling design |
| [LLM Agent Survey 2024 (Xi et al.)](./papers/llm-agent-survey-xi-2024/note.md) | Most comprehensive and current survey. Should supplement or replace the 2023 surveys |
| [Anthropic Model Specification (2024)](./papers/anthropic-model-spec-2024/note.md) | How alignment is operationalized at the model level. Required reading for safety agent design |

---

### M. Reference Collections

| Resource | Use |
|---|---|
| Multi-Agent-Papers GitHub Collection | Starting point for new paper discovery in the multi-agent space |

---

## Experiments

Every experiment follows the same measurement structure: identical task, varying architecture or strategy, evaluated across performance / latency / token cost / failure rate.

---

### Experiment Group 1: Core Patterns

Run these first. They establish the empirical intuitions that everything else builds on.

| Folder | What is being compared | Key papers |
|---|---|---|
| [`experiments/react-vs-cot`](./experiments/react-vs-cot/README.md) | CoT only vs. ReAct + tool calls on identical tasks. Success rate, failure mode analysis | ReAct, Chain-of-Thought |
| [`experiments/react-vs-reflexion-vs-fusemind`](./experiments/react-vs-reflexion-vs-fusemind/README.md) | ReAct vs. ReAct + Reflection vs. FuseMind on multi-step reasoning. Accuracy, attempt count, token cost | Reflexion, [ReflAct](./papers/reflact-2023/note.md), FuseMind |
| [`experiments/reasoning-evolution`](./experiments/reasoning-evolution/README.md) | CoT -> Self-Consistency -> ToT -> LATS: accuracy and cost at each step of the evolution | CoT, Self-Consistency, ToT, LATS |
| [`experiments/multi-agent-patterns`](./experiments/multi-agent-patterns/README.md) | Single LLM vs. Planner-Worker vs. 3-4 agent collaboration on a complex task. Performance, latency, cost | AutoGen, MetaGPT, CAMEL |

---

### Experiment Group 2: Memory and Retrieval

| Folder | What is being compared | Key papers |
|---|---|---|
| [`experiments/rag-comparison`](./experiments/rag-comparison/README.md) | No-RAG vs. naive RAG vs. task-specific structured RAG. Answer quality and hallucination rate | RAG original |
| [`experiments/rag-retriever-strategies`](./experiments/rag-retriever-strategies/README.md) | DPR dense retrieval vs. embedding search vs. keyword search. Quality and speed tradeoffs | RAG, RAPTOR |
| [`experiments/self-rag-vs-naive-rag`](./experiments/self-rag-vs-naive-rag/README.md) | Always-retrieve vs. model-decides-when-to-retrieve. Accuracy, latency, unnecessary retrieval rate | Self-RAG |
| [`experiments/memory-architecture`](./experiments/memory-architecture/README.md) | No memory vs. flat conversation history vs. CoALA-style layered memory. Task coherence over long sessions | MemGPT, CoALA |
| [`experiments/raptor-vs-flat-rag`](./experiments/raptor-vs-flat-rag/README.md) | Flat chunk indexing vs. RAPTOR recursive tree indexing on long documents. Recall and coherence | RAPTOR |

---

### Experiment Group 3: Reliability and Aggregation

| Folder | What is being compared | Key papers |
|---|---|---|
| [`experiments/aggregation-reliability`](./experiments/aggregation-reliability/README.md) | Single agent vs. majority vote vs. weighted vote vs. critic-agent final selection. Confidence calibration | Reliable Decision-Making, Self-Consistency |
| [`experiments/llm-as-judge-pipeline`](./experiments/llm-as-judge-pipeline/README.md) | Human evaluation vs. LLM-as-Judge correlation measurement. Failure mode analysis under adversarial outputs | LLM-as-Judge |
| [`experiments/monitoring-ops`](./experiments/monitoring-ops/README.md) | Collect agent execution logs, cluster failure patterns, identify input types with high failure rates | AI Agents: Expectations vs. Reality |

---

### Experiment Group 4: Tool Use and Action Space

| Folder | What is being compared | Key papers |
|---|---|---|
| [`experiments/tool-use-strategies`](./experiments/tool-use-strategies/README.md) | Tool spec injection methods: description density, example count, structured vs. free-form. DFS vs. greedy tool selection | Toolformer, Gorilla, ToolBench |
| [`experiments/code-vs-json-action-space`](./experiments/code-vs-json-action-space/README.md) | JSON action representation vs. Python code as actions. Task success rate, error recovery, generalization to unseen tasks | Executable Code Actions |
| [`experiments/dspy-vs-manual-prompting`](./experiments/dspy-vs-manual-prompting/README.md) | Hand-tuned prompts vs. DSPy compiled prompts. Accuracy, iteration time, sensitivity to model version changes | DSPy |

---

### Experiment Group 5: Inference and Systems

These require infrastructure work. This tier is what separates application-layer builders from systems-level architects.

| Folder | What is being compared | Key papers |
|---|---|---|
| [`experiments/inference-serving-comparison`](./experiments/inference-serving-comparison/README.md) | Naive sequential inference vs. continuous batching vs. PagedAttention. Throughput and latency under concurrent agent load | vLLM, Orca |
| [`experiments/latency-cost-profiling`](./experiments/latency-cost-profiling/README.md) | Full agent loop profiling. Where time and tokens are actually spent: reasoning / retrieval / tool call / generation breakdown | FlashAttention, vLLM |
| [`experiments/speculative-decoding-impact`](./experiments/speculative-decoding-impact/README.md) | Standard decoding vs. speculative decoding in latency-sensitive agent loops. Token/s and accuracy preservation | Speculative Decoding |
| [`experiments/context-window-scaling`](./experiments/context-window-scaling/README.md) | Fixed short context vs. MemGPT-style virtual context vs. single long-context model. Cost and coherence at scale | MemGPT, FlashAttention |

---

### Experiment Group 6: Safety

| Folder | What is being compared | Key papers |
|---|---|---|
| [`experiments/guard-agent`](./experiments/guard-agent/README.md) | No guard vs. rule-based filter vs. Constitutional AI critic. Dangerous action detection rate and false positive rate | Constitutional AI, R-Judge |
| [`experiments/prompt-injection-defense`](./experiments/prompt-injection-defense/README.md) | Baseline agent vs. sanitized input agent vs. instruction-hierarchy agent. Injection success rate under adversarial inputs | Prompt Injection Attacks |

---

## Projects

Each project delivers a minimum working version within one day to one week. The goal is to combine patterns validated in experiments into something functional, not to produce polished software.

---

### A. Workflow / Coding / Research Tools

| Project | Architecture | Linked experiments |
|---|---|---|
| [`projects/research-operator-v0`](./projects/research-operator-v0/README.md) | Retriever + Summarizer + Applicator agents. URL input -> summary + core ideas + 3 implementation angles | rag-comparison, react-vs-cot |
| [`projects/code-review-agent-v0`](./projects/code-review-agent-v0/README.md) | PR diff input -> change summary + bug and style issues + test suggestions | react-vs-reflexion-vs-fusemind, tool-use-strategies |
| [`projects/experiment-log-analyzer`](./projects/experiment-log-analyzer/README.md) | Experiment results table or log -> trend analysis + failure cases + next experiment suggestions | llm-as-judge-pipeline, monitoring-ops |

---

### B. Multi-Agent Structure Practice

| Project | Architecture | Linked experiments |
|---|---|---|
| [`projects/planner-researcher-writer`](./projects/planner-researcher-writer/README.md) | Planner -> Researcher -> Writer three-agent pipeline. Topic input -> research plan -> document search -> report | multi-agent-patterns, rag-comparison |
| [`projects/bug-triage-team`](./projects/bug-triage-team/README.md) | Classifier + Root-Cause Guesser + Fix Planner. Issue ticket or log input -> collaborative triage output | multi-agent-patterns, aggregation-reliability |

---

### C. Memory / RAG / Context Practice

| Project | Architecture | Linked experiments |
|---|---|---|
| [`projects/personal-note-rag`](./projects/personal-note-rag/README.md) | Full index of personal notes, blogs, and documents. Query -> relevant notes + past idea summary with selective retrieval | rag-retriever-strategies, self-rag-vs-naive-rag, memory-architecture |
| [`projects/task-memory-agent`](./projects/task-memory-agent/README.md) | Agent that tracks job applications, positions, and interview history. Auto-saves new entries, provides next-session reminders | memory-architecture, rag-comparison |

---

### D. Reliability / Ops Practice

| Project | Architecture | Linked experiments |
|---|---|---|
| [`projects/agent-execution-viewer`](./projects/agent-execution-viewer/README.md) | Records all agent calls. Dashboard showing success rate, latency, and cost broken down by agent and time window | monitoring-ops, aggregation-reliability |
| [`projects/guard-critic-agent`](./projects/guard-critic-agent/README.md) | Reviews outputs of other agents. Blocks dangerous actions and attaches a confidence score and risk comment | guard-agent, aggregation-reliability |

---

### E. Systems-Level Projects

These do not exist in the original plan. They are added because an agent architect who cannot build or reason about the serving layer is operating with a fundamental blind spot.

| Project | Architecture | Linked experiments |
|---|---|---|
| [`projects/agent-inference-profiler`](./projects/agent-inference-profiler/README.md) | Wraps any agent loop with instrumentation. Reports per-call token count, time-to-first-token, total latency, cost estimate, and KV cache hit rate | latency-cost-profiling, inference-serving-comparison |
| [`projects/streaming-agent-server`](./projects/streaming-agent-server/README.md) | FastAPI + vLLM backend serving an agent loop with streaming output. Handles concurrent requests with continuous batching | inference-serving-comparison, context-window-scaling |
| [`projects/dspy-optimized-agent`](./projects/dspy-optimized-agent/README.md) | Takes an existing manually-prompted agent, rewrites it in DSPy, runs compiled optimization against a small labeled dataset, compares before and after | dspy-vs-manual-prompting |

---

## Scope of This Curriculum and Expectations

What reading and completing this list covers:

- Architectural vocabulary and design patterns for single and multi-agent systems
- The full reasoning evolution from Chain-of-Thought to LATS
- Memory taxonomy and retrieval architecture from naive RAG to cognitive layering
- Tool use from first principles through large-scale benchmarking
- Production evaluation methodology
- Safety as a structural design constraint

What the experiments and systems projects are specifically designed to build, because reading alone does not produce it:

- Inference economics intuition: KV cache sizing, memory bandwidth ceilings, batching tradeoffs under real load
- The ability to profile a running agent system and identify where the actual bottleneck is
- An informed position on the 2024 architecture debates: single long-context model vs. multi-agent with smaller windows, code-as-action vs. JSON-as-action, static workflow vs. dynamic planning
- Enough benchmark familiarity to identify when a paper's claimed improvement is real vs. benchmark overfitting
- A realistic threat model for production agent systems, built from empirical failure analysis rather than theory

The systems-level projects in section E are the primary mechanism for closing that gap.

