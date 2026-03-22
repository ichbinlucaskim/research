# Papers — Note-Taking Standard

This folder contains one subfolder per paper.
Every paper gets the same structured note. No exceptions.

The goal is not to summarize. The goal is to extract what is
architecturally useful, identify what the paper does not address,
and connect it to the rest of the reading list.

A note that cannot answer "how does this change how I would design
a system tomorrow" is incomplete.

---

## Folder Structure

```
papers/
├── README.md                        # This file
├── react-yao-2022/
│   ├── note.md                      # Your structured note (required)
│   ├── figures/                     # Key diagrams you redrew or annotated
│   └── refs.md                      # Papers this one cites that you should read next
├── chain-of-thought-wei-2022/
│   └── note.md
└── ...
```

Folder naming convention: `{short-title}-{first-author}-{year}`
Example: `lats-2023`, `memgpt-packer-2023`, `vllm-kwon-2023`

---

## note.md Template

Copy this exactly. Fill every section. Do not delete sections because
they feel hard to fill — that difficulty is the signal that you have
not understood the paper yet.

---

```markdown
# {Full Paper Title}

{Authors} | {Venue} | {Year} | {Link to paper}

Read: {YYYY-MM-DD}
Status: {Reading / Done / Needs Revisit}
Section: {Which section of the main README this belongs to}

---

## One-Line Claim

What does this paper claim to do, in one sentence?
Write this in your own words. Do not copy the abstract.

---

## Problem Being Solved

What specific limitation or gap does this paper address?
What was the state of the field before this paper, and why was
that insufficient?

Be concrete. Name the prior work being improved upon.

---

## Core Contribution

What is the single most important thing this paper introduces?
This could be:
- A new architecture or component
- A new training method
- A new benchmark or evaluation method
- A formal framework or taxonomy
- An empirical finding that changes assumptions

If there are multiple contributions, rank them. What would still
matter if everything else were stripped away?

---

## Architecture / Method

Describe how it works mechanically.

If there is a loop or pipeline, write it out step by step:
  Step 1: ...
  Step 2: ...
  Step 3: ...

If there are key design decisions (why did they choose X over Y),
explain the reasoning. This is often buried in ablation sections.

Include a diagram if one helps. Either reference a figure from the
paper or draw your own in ASCII or in the figures/ subfolder.

---

## Key Results

What did they actually show? Be specific about numbers and tasks.

Format:
- Task: {name}
- Baseline: {method} at {score}
- This paper: {method} at {score}
- Conditions: {dataset, model size, any important caveats}

If the result is benchmark-specific, note whether the benchmark
has known limitations or whether the improvement has been
reproduced elsewhere.

---

## Limitations and What It Does Not Address

This section is as important as the results section.

What assumptions does the method rely on?
What task types or conditions would cause it to fail?
What did the authors explicitly say they did not test?
What did the authors not say, but you suspect is a problem?

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| {paper name} | {this paper improves on / is improved by / contradicts / complements} |

After reading this paper, which papers in the reading list
should you re-read or read next? Why?

---

## Implementation Angles

Three specific ideas for how this paper's contribution could be
applied in your experiments or projects.

Each one should be concrete enough that you could start building
it tomorrow.

1. {Experiment or project idea}: {one sentence on what you would build
   and what you would measure or demonstrate}

2. {Experiment or project idea}: {same format}

3. {Experiment or project idea}: {same format}

---

## Open Questions

What do you still not understand after reading this?
What would you need to run to verify or challenge the claims?

List these. Come back to them after running related experiments.

---

## Revision Notes

{YYYY-MM-DD}: {What changed in your understanding after running
an experiment or reading a related paper}
```

---

## Quality Standard

A note is complete when it can do the following:

- Explain the paper's contribution to someone who has not read it,
  in under two minutes, without looking at your notes
- Identify at least one specific thing the paper does not solve
  that matters for your research
- Produce at least one concrete experiment idea

If any of these three are missing, the note is not done.

---

## Cross-Reference Index

Maintain this table at the bottom of this README as you add notes.
It gives you a quick map of how papers connect.

### A. Big Picture and Multi-Agent

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [LLM-Enabled Multi-Agent Systems (Survey)](./llm-multi-agent-survey/note.md) | — | — | Component taxonomy and control-flow pattern survey across agent literature |
| [Multi-Agent Collaboration Mechanisms Survey](./multi-agent-collab-survey/note.md) | — | — | Taxonomy of collaboration mechanisms: cooperation, competition, coevolution |
| [LLM-Powered Multi-Agent Systems (IEEE)](./llm-framework-ieee/note.md) | — | — | Technical framework for collaborative intelligence with optimized retrieval |
| [LLM-Based Multi-Agent Systems for SWE (ACM)](./llm-agents-swe-acm/note.md) | — | — | Systematic mapping of multi-agent architectures to software engineering workflows |
| [NVIDIA: Smaller LMs for Agents](./nvidia-slm-agents/note.md) | — | — | Role-specialized small model assignment within larger agent systems |

### B. Reasoning Foundation

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [Chain-of-Thought (Wei, 2022)](./chain-of-thought-wei-2022/note.md) | Standard prompting | Self-Consistency, ToT, ReAct, LATS | Explicit step-by-step reasoning elicitation via prompt format |
| [Self-Consistency (Wang, 2023)](./self-consistency-wang-2023/note.md) | CoT (single path) | Aggregation reliability experiments | Multiple reasoning path sampling + majority vote for reliability |
| [Tree of Thoughts (Yao, 2023)](./tree-of-thoughts-yao-2023/note.md) | CoT, ReAct | LATS | Tree search over intermediate reasoning steps with backtracking |
| [LATS (2023)](./lats-2023/note.md) | ToT + ReAct | — | MCTS-guided planning with reflection integrated into the search loop |

### C. ReAct / Tool-Use / Reflection / Planning

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [ReAct (Yao, 2022)](./react-yao-2022/note.md) | CoT (reasoning only) | Reflexion, ReflAct, FuseMind, LATS | Interleaved Thought → Act → Observe loop grounded in external tools |
| [Reflexion (Shinn, 2023)](./reflexion-shinn-2023/note.md) | ReAct | ReflAct, FuseMind | Verbal reinforcement: post-task self-reflection stored as episodic memory |
| [ReflAct](./reflact-2023/note.md) | ReAct + Reflexion | — | Unified single-loop structure combining reflection and action without two-phase separation |
| [FuseMind](./fusemind-2023/note.md) | ReAct + Reflexion | — | Fused reflection and next-action prediction for efficiency via anticipation |

### D. Tool Use and Function Calling

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [Toolformer (Schick, 2023)](./toolformer-schick-2023/note.md) | Static tool use | Gorilla, ToolBench | Self-supervised learning of when and where to insert tool calls |
| [Gorilla (Patil, 2023)](./gorilla-patil-2023/note.md) | Toolformer | ToolBench | Retrieval-aware training for accurate API call generation from specifications |
| [ToolBench / ToolLLM (Qin, 2023)](./toolbench-qin-2023/note.md) | Gorilla | — | 16K-API benchmark + DFS decision tree for multi-step tool selection |

### E. Multi-Agent Framework Papers

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [AutoGen (Wu, 2023)](./autogen-wu-2023/note.md) | Single-agent loops | MetaGPT, AgentScope | Conversable agent abstraction: any agent can initiate or respond to any other |
| [MetaGPT (Hong, 2023)](./metagpt-hong-2023/note.md) | AutoGen | — | SOPs encoded as agent collaboration structure; role = PM / Engineer / QA |
| [CAMEL (Li, 2023)](./camel-li-2023/note.md) | AutoGen | — | Inception prompting for role-playing; autonomous agent-to-agent task completion |
| [HuggingGPT / JARVIS (Shen, 2023)](./hugginggpt-shen-2023/note.md) | Single-model pipelines | — | LLM as controller dispatching to specialized external models as tools |

### F. RAG / Memory / Context

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [RAG (Lewis, 2020)](./rag-lewis-2020/note.md) | Parametric-only knowledge | MemGPT, Self-RAG, RAPTOR | Dense Passage Retriever + joint fine-tuning; first retrieval-augmented generation |
| [MemGPT (Packer, 2023)](./memgpt-packer-2023/note.md) | RAG | — | OS virtual memory concepts applied to LLMs: tiered main/external memory with paging |
| [CoALA (2023)](./coala-2023/note.md) | Ad-hoc memory designs | — | Working / Episodic / Semantic / Procedural memory taxonomy as design language |
| [Self-RAG (Asai, 2023)](./self-rag-asai-2023/note.md) | Always-retrieve RAG | — | Model decides whether retrieval is needed; self-evaluated critique tokens |
| [RAPTOR (Sarthi, 2024)](./raptor-sarthi-2024/note.md) | Flat chunk RAG | — | Recursive document summarization into tree-indexed structures for long-doc QA |

### G. Reliability / Ops / Evaluation

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [Reliable Decision-Making](./reliable-decision-making/note.md) | Single-agent outputs | — | Ensemble and weighted-vote aggregation methods specific to LLM agent decisions |
| [AI Agents: Expectations vs. Reality (IBM)](./ai-agents-reality-ibm/note.md) | — | — | Empirical catalog of production deployment failure modes and operational limits |
| [SWE-bench (Jimenez, 2024)](./swe-bench-jimenez-2024/note.md) | Synthetic benchmarks | OpenDevin, SWE-agent | Real GitHub issues as agent evaluation; end-to-end code change + test execution |
| [AgentBench (Liu, 2023)](./agentbench-liu-2023/note.md) | Single-domain evals | — | Multi-environment agent benchmark: OS, DB, web, code, card games in one suite |
| [WebArena (Zhou, 2023)](./webarena-zhou-2023/note.md) | Toy web tasks | — | Fully functional web environments with real applications for autonomous agents |
| [LLM-as-a-Judge (Zheng, 2023)](./llm-as-judge-zheng-2023/note.md) | Human-only evaluation | — | LLM pairwise evaluation with position-bias and self-enhancement bias analysis |

### H. Safety and Alignment

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [Constitutional AI (Bai, 2022)](./constitutional-ai-bai-2022/note.md) | RLHF | — | Principle-guided self-critique and revision; AI feedback replacing human labels |
| [R-Judge (2024)](./r-judge-2024/note.md) | General benchmarks | — | Safety risk awareness benchmark targeting dangerous actions in agent environments |
| [Prompt Injection Attacks (2023)](./prompt-injection-2023/note.md) | — | — | Indirect prompt injection taxonomy: attacker-controlled content in retrieved data |

### I. LLM Foundations

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [Attention Is All You Need (Vaswani, 2017)](./attention-vaswani-2017/note.md) | RNN / LSTM sequence models | Every paper in this list | Self-attention transformer architecture; positional encoding |
| [Scaling Laws (Kaplan, 2020)](./scaling-laws-kaplan-2020/note.md) | Empirical model selection | — | Power-law relationships between compute, data, parameters, and loss |
| [GPT-4 (OpenAI, 2023)](./gpt4-openai-2023/note.md) | GPT-3 | — | RLHF-aligned multimodal frontier model; capability ceiling most agents run on |
| [LLaMA / LLaMA 2 / LLaMA 3 (Meta)](./llama-meta-2023/note.md) | Closed-weight LLMs | Mixtral | Open-weight foundation models enabling local deployment and fine-tuning |
| [Mixtral / Mistral (2024)](./mixtral-2024/note.md) | Dense LLaMA | — | Sparse mixture-of-experts for efficient inference; expert routing per token |

### J. Inference and Systems

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [FlashAttention 1 & 2 (Dao, 2022)](./flashattention-dao-2022/note.md) | Standard attention | vLLM, SGLang | IO-aware tiled attention computation; avoids materializing the full attention matrix |
| [Orca: Continuous Batching (Yu, 2022)](./orca-yu-2022/note.md) | Static batching | vLLM | Iteration-level scheduling: new requests fill slots as sequences finish |
| [vLLM (Kwon, 2023)](./vllm-kwon-2023/note.md) | Orca batching | SGLang | PagedAttention: non-contiguous KV cache paging eliminates fragmentation |
| [Speculative Decoding (Leviathan, 2023)](./speculative-decoding-leviathan-2023/note.md) | Standard autoregressive decoding | — | Draft model + verifier for parallel token generation without accuracy loss |
| [SGLang (Zheng, 2024)](./sglang-zheng-2024/note.md) | vLLM | — | Radix attention for prefix caching; structured generation co-design with serving |
| [TensorRT-LLM (NVIDIA)](./tensorrt-llm-nvidia/note.md) | General inference frameworks | — | NVIDIA hardware-optimized serving: kernel fusion, in-flight batching, INT8/FP8 |

### K. Control Flow and Compiler-Level Architecture

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [Executable Code Actions (Wang, 2024)](./executable-code-actions-wang-2024/note.md) | JSON action representation | — | Python code as action space: composable, error-recoverable, generalized actions |
| [LangGraph / LCEL](./langgraph-lcel/note.md) | Linear chain pipelines | — | Stateful cyclic graphs for agent control flow; explicit state machine design |
| [Flows (EPFL, 2024)](./flows-epfl-2024/note.md) | Ad-hoc agent composition | — | Formal compositional framework: atomic flows, composite flows, typed interfaces |
| [DSPy (Khattab, 2023)](./dspy-khattab-2023/note.md) | Manual prompt engineering | — | Declarative prompt programs compiled and optimized against labeled metrics |

### L. 2024–2025 Frontier

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| [Agent Workflow Memory (AWM, 2024)](./awm-2024/note.md) | Single-session ReAct | — | Learning and reusing workflow patterns across tasks; procedural memory update |
| [OpenDevin / SWE-agent (2024)](./opendevin-2024/note.md) | SWE-bench baselines | — | Open coding agent platform; agent-computer interface with shell + editor tools |
| [AgentScope (Alibaba, 2024)](./agentscope-alibaba-2024/note.md) | AutoGen | — | Fault-tolerant multi-agent scheduling with actor model and message routing |
| [LLM Agent Survey 2024 (Xi et al.)](./llm-agent-survey-xi-2024/note.md) | 2023 surveys | — | Comprehensive brain / perception / action taxonomy; 2024 frontier coverage |
| [Anthropic Model Specification (2024)](./anthropic-model-spec-2024/note.md) | Constitutional AI | — | Operationalized alignment spec: priority ordering of safety / ethics / principles |