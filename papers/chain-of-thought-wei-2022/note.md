# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou | NeurIPS 2022 | 2022 | Link: https://arxiv.org/pdf/2201.11903.pdf

Read: —
Status: Not Started
Section: B

---

## One-Line Claim

Including step-by-step worked examples in the prompt causes large language models to produce intermediate reasoning chains, dramatically improving performance on multi-step reasoning tasks — no fine-tuning required.

---

## Problem Being Solved

Before CoT, prompting a model to solve a multi-step problem meant giving it the question and expecting the answer directly. The model would often produce a plausible-looking but wrong answer because it was pattern-matching the surface form to similar answers seen during training. There was no mechanism for the model to work through intermediate steps — the entire reasoning process was compressed into a single next-token prediction.

The specific failure mode: the model would skip steps, confuse intermediate values, or short-circuit to a memorized answer format. On arithmetic, commonsense, and symbolic tasks, standard few-shot prompting was stuck at a ceiling that had nothing to do with the model's underlying capability — it was a prompting failure, not a capability failure.

---

## Core Contribution

A prompting format change: in your few-shot examples, include not just the question and the final answer, but the complete step-by-step reasoning chain between them. The model infers from these examples that it should produce reasoning steps before committing to a final answer.

**Few-shot CoT** (this paper) — include 3–8 examples with full chains:
```
Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many does he have?
A: Roger started with 5 balls. 2 cans × 3 balls = 6 new balls. 5 + 6 = 11. The answer is 11.

Q: [new question]
A:
```

**Zero-shot CoT** (Kojima et al., 2022 — a separate paper, not this one) — append "Let's think step by step" to any question with no examples. This paper is the few-shot version.

**The emergence finding** is as important as the technique itself: CoT only works reliably in models above roughly 100B parameters at the time of writing. Below that threshold, the chains are incoherent and performance can actually drop. CoT does not create capability — it unlocks capability that was already latent in a sufficiently large model.

---

## Architecture / Method

The mechanism works because externalizing reasoning into text changes the problem structure. Instead of predicting the answer in one step, the model generates a sequence of individually manageable sub-steps. Each step is within the model's capability because it is simple relative to the full problem. The committed text also serves as a working memory — the model can reference what it wrote in earlier steps rather than holding everything implicitly in attention.

**Implementation parameters for the experiment:**

- Temperature: 0.0 for greedy (deterministic) CoT. This is the baseline.
- Few-shot examples: 3–8 examples covering the task type. The quality of examples matters — bad chains produce bad output. Each example should show a clean, correct, step-by-step derivation.
- Output format: instruct the model to produce the reasoning chain first, then a clearly marked final answer (e.g., "The answer is X"). This makes parsing reliable.
- Max tokens: CoT chains for typical reasoning tasks run 100–400 tokens. Set a ceiling of 600 to avoid runaway generation.

**Prompt template for reasoning-evolution experiment:**
```
You are solving [task type] problems. Think through each problem step by step before giving your final answer. Show all intermediate steps clearly.

[Example 1: question + chain + answer]
[Example 2: question + chain + answer]
[Example 3: question + chain + answer]

Q: [test question]
A: Let me think through this step by step.
```

---

## Key Results

| Task | Standard Prompting | CoT Prompting | Model |
|---|---|---|---|
| GSM8K (grade school math) | 17.9% | 56.9% | PaLM 540B |
| GSM8K | ~15% | ~46% | GPT-3 175B |
| MAWPS (arithmetic) | ~78% | ~93% | PaLM 540B |
| CommonsenseQA | ~73% | ~79% | PaLM 540B |
| StrategyQA | ~65% | ~75% | PaLM 540B |
| Last Letter Concat (symbolic) | ~2% | ~63% | PaLM 540B |

The arithmetic improvements are the most dramatic. Symbolic tasks (last letter concatenation, coin flip) show extreme gains — these tasks have almost no useful surface pattern to match, so standard prompting completely fails while CoT succeeds by following explicit rules.

**The emergence curve**: at PaLM 8B, CoT hurts or does nothing. At PaLM 62B, CoT starts to help on simpler tasks. At PaLM 540B, the full benefit appears. This curve has shifted downward significantly with instruction-tuning — by 2024, models at 7–13B show CoT benefits on many tasks.

---

## Limitations and What It Does Not Address

- **Single path, no correction**: CoT produces exactly one reasoning chain. If the chain goes wrong at step 2, every subsequent step inherits that error with no mechanism to catch or fix it. This is the primary limitation that Self-Consistency directly addresses.
- **No backtracking**: once the model commits to a reasoning step, it cannot go back. Dead ends are not detected. ToT exists specifically to fix this.
- **No grounding**: CoT reasons entirely within the model's parametric knowledge. If the task requires current facts, file contents, or code execution results, CoT cannot retrieve them. This is the motivation for ReAct.
- **Hallucination within the chain**: intermediate steps can be confidently stated but factually wrong. The chain format makes errors look more credible, not less — a plausible-looking wrong chain is harder to spot than a wrong one-word answer.
- **Example quality sensitivity**: the quality of few-shot reasoning examples directly determines output quality. Manual chain writing is required and is harder than it looks.
- **Cost**: CoT generates 3–5× more tokens than standard prompting. For the reasoning-evolution experiment, track tokens per call from the first run.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [Self-Consistency (Wang, 2023)](../self-consistency-wang-2023/note.md) | Direct fix for CoT's single-path brittleness: sample N chains, take majority vote |
| [Tree of Thoughts (Yao, 2023)](../tree-of-thoughts-yao-2023/note.md) | Replaces the linear chain with a tree, enabling exploration and backtracking |
| [ReAct (Yao, 2022)](../react-yao-2022/note.md) | Extends CoT by interleaving reasoning steps with external tool calls, grounding the chain |
| [LATS (2023)](../lats-2023/note.md) | Unifies CoT reasoning, ToT tree search, ReAct tool use, and reflection in one architecture |
| [DSPy (Khattab, 2023)](../dspy-khattab-2023/note.md) | Treats CoT as a compilable, optimizable module rather than a manually written prompt |
| [Reflexion (Shinn, 2023)](../reflexion-shinn-2023/note.md) | Addresses the no-correction limitation by adding post-task reflection on failed chains |

---

## Implementation Angles

1. **Baseline for reasoning-evolution**: implement greedy CoT (temperature=0, single sample) as Strategy 1 in the experiment. This is the reference point every other strategy must beat. Measure accuracy, token cost, and latency before running anything else.

2. **Failure mode taxonomy**: on every wrong answer from CoT, classify the failure as: (a) wrong first step, (b) correct early steps then wrong intermediate step, (c) correct chain but wrong final answer extraction, or (d) hallucinated fact in the chain. This breakdown directly predicts which improvement — Self-Consistency, ToT, or LATS — will address each failure type.

3. **Example quality experiment**: run CoT with two prompt variants — hand-crafted high-quality chains vs. auto-generated chains. If the gap is large, the experiment results are more sensitive to prompt engineering than to the method itself. Flag this as a confound.

---

## Open Questions

- With instruction-tuned models like Claude 3.5 Sonnet or GPT-4o, do few-shot CoT examples still matter, or does zero-shot "think step by step" achieve comparable accuracy? The 2022 paper uses base models — the answer may differ for instruction-tuned models.
- The paper shows CoT helps more on tasks with clear intermediate structure (arithmetic). For the research synthesis tasks in reasoning-evolution, which are more open-ended, what does the failure distribution look like?

---

## Revision Notes

