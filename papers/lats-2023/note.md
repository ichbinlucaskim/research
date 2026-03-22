# LATS: Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models

Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, Yu-Xiong Wang | ICML 2024 | 2023 | Link: https://arxiv.org/pdf/2310.04406.pdf

Read: —
Status: Not Started
Section: B

---

## One-Line Claim

LATS combines the tree structure of ToT, the principled exploration of MCTS, the tool-use grounding of ReAct, and the self-correction of Reflexion into a single unified architecture — the strongest general-purpose single-agent planning framework available as of 2023.

---

## Problem Being Solved

Each paper in this section fixed one specific failure mode of its predecessor but left others unaddressed:
- CoT: single path, no correction.
- Self-Consistency: N paths but no exploration, no backtracking, blind sampling.
- ToT: tree search with backtracking, but no grounding (can't use tools), no reflection (discards the search history), and naive BFS/DFS without principled exploration.

LATS was built to address all of these at once. The core question it answers: what does a single agent look like when it has access to tree search, real environmental feedback, and the ability to learn from failed branches within a single run?

---

## Core Contribution

A unified agent loop that integrates four previously separate ideas:

**1. MCTS-guided tree search** — replaces ToT's BFS/DFS with Monte Carlo Tree Search. MCTS uses the UCT (Upper Confidence bound for Trees) formula to select which node to expand next:

```
UCT(node) = V(node) + C × sqrt(ln(N_parent) / N_node)
```

Where V(node) is the estimated value of the node, N_parent is how many times the parent was visited, N_node is how many times this node was visited, and C is an exploration constant (typically 1.0–1.5). This formula balances exploitation (expand high-value nodes) with exploration (expand under-visited nodes). DFS and BFS ignore this balance — DFS exploits too aggressively, BFS explores too uniformly.

**2. LLM as all four MCTS components** — in standard MCTS, you need a simulation policy and a value function. LATS uses the LLM for both:
- *Selection*: UCT formula applied to tree nodes.
- *Expansion*: LLM generates k candidate next actions or reasoning steps.
- *Simulation/Rollout*: LLM evaluates the quality of a node (same as ToT's state evaluation).
- *Backpropagation*: values propagate up the tree after rollout.

**3. ReAct-style tool use** — nodes in the tree are not just reasoning steps, they are (thought, action, observation) triples. The agent can call tools, receive real environment feedback, and incorporate that feedback into the node's value. This grounds the search in reality rather than pure model self-evaluation.

**4. Reflection on failure** — when a terminal node is reached and the task fails (either by explicit failure signal or by reaching max depth), the agent writes a reflection: "What went wrong? What should be tried differently?" This reflection is stored and prepended to subsequent expansion prompts, steering future branches away from the same mistakes.

This is the key advance over ToT: ToT discards failed branches entirely. LATS learns from them within the same run.

---

## Architecture / Method

The full LATS loop:

```
Initialize: root node = initial task state, empty reflection memory
While budget not exhausted:
    1. SELECTION: traverse tree from root using UCT to find unexplored node
    2. EXPANSION: at selected node, generate k candidate next (thought, action) pairs
    3. EVALUATION: for each candidate, optionally run tool call to get observation,
       then ask LLM to score the resulting state (0.0–1.0)
    4. SIMULATION/ROLLOUT: for the best candidate, simulate forward to a terminal
       state (using LLM to generate the remaining steps quickly)
    5. BACKPROPAGATION: update V(node) for all ancestors using the terminal reward
    6. REFLECTION: if terminal state is a failure, generate a reflection and store it
    7. Next iteration: reflection text is prepended to expansion prompts

Return: highest-value path through the tree
```

**Key parameters:**
- k (branching factor): typically 3–5. Same as ToT.
- C (exploration constant in UCT): 1.0 is a reasonable default. Higher C = more exploration.
- max_depth: task-dependent. For coding tasks, 10–15 steps. For reasoning tasks, 5–8.
- budget: total number of node expansions, not depth. Typically 10–50 depending on cost tolerance.
- Reflection: stored as a string, prepended to future expansion prompts. Keep reflections to 2–3 sentences — too long and they dominate the context.

**Prompt design for expansion (with reflection):**
```
Task: [original task]

Previous attempts and what went wrong:
- [reflection 1]
- [reflection 2]

Current reasoning state: [node state]

Generate [k] different next steps to continue solving this task.
Each step should be meaningfully different and should avoid the
mistakes noted above.
```

**Cost**: similar to ToT but higher due to reflection generation and additional value estimation calls. Expect 50–150 LLM calls per task depending on budget. This is 5–15× ToT and 50–150× greedy CoT.

---

## Key Results

| Task | CoT | ReAct | ToT | LATS |
|---|---|---|---|---|
| HumanEval (code gen, pass@1) | ~65% | 80.5% | — | 88.1% |
| HotPotQA (multi-hop QA) | ~43% | 35.1% | — | 73.2% |
| WebArena (web tasks) | — | ~14% | — | ~17% |
| Game of 24 | 4% | — | 74% | ~80% |

**HumanEval is the key result**: LATS at 88.1% pass@1 is state-of-the-art for single-agent code generation as of the paper's publication. The improvement over ReAct (80.5%) comes specifically from the reflection mechanism — when code fails a test, the reflection stores what was wrong and subsequent branches avoid the same error.

**HotPotQA** shows the largest jump: LATS at 73.2% vs. ReAct at 35.1%. Multi-hop QA requires chaining multiple retrieval and reasoning steps — exactly the kind of task where MCTS exploration and reflection compound.

**WebArena improvement over ReAct is modest** (+3%). Web tasks have many external failure sources (page layout changes, dynamic content) that reflection cannot address because they are environmental, not model errors.

---

## Limitations and What It Does Not Address

- **Cost**: LATS is the most expensive strategy in this section by a large margin. 50–150 LLM calls per task means it is impractical as a default strategy — it is best reserved for high-value, high-difficulty tasks where the cost is justified.
- **Reflection quality is not guaranteed**: the model writes its own reflection on failure. If the reflection misdiagnoses the problem ("I should have used different words" instead of "I took the wrong algorithmic approach"), subsequent branches inherit the wrong correction.
- **Single-session learning only**: reflections persist within one LATS run but are discarded afterward. AWM (Agent Workflow Memory) is specifically designed to persist workflow patterns across runs — the natural next step after LATS.
- **No global memory**: LATS builds up a tree of one problem. It cannot transfer insights from solving problem A to solving problem B, even in the same session.
- **Implementation complexity**: LATS is significantly harder to implement correctly than CoT or Self-Consistency. The UCT selection, backpropagation, and reflection pipeline all need to work together. Start with a simplified version (depth-limited DFS + reflection, no UCT) before attempting full MCTS.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [Tree of Thoughts (Yao, 2023)](../tree-of-thoughts-yao-2023/note.md) | Direct predecessor: LATS adds MCTS selection, tool use, and reflection on top of ToT's tree structure |
| [ReAct (Yao, 2022)](../react-yao-2022/note.md) | LATS incorporates ReAct's (thought, action, observation) structure as the node representation in the tree |
| [Reflexion (Shinn, 2023)](../reflexion-shinn-2023/note.md) | LATS incorporates Reflexion's verbal reflection mechanism but applies it within a single run rather than across multiple episodes |
| [Chain-of-Thought (Wei, 2022)](../chain-of-thought-wei-2022/note.md) | CoT is the baseline that every node in the LATS tree builds on — the reasoning within each node is a CoT chain |
| [Self-Consistency (Wang, 2023)](../self-consistency-wang-2023/note.md) | Self-Consistency is flat sampling; LATS is guided sampling — the UCT formula replaces uniform random sampling |
| [AWM (2024)](../awm-2024/note.md) | AWM extends LATS-style search by persisting successful workflow patterns across runs, fixing the single-session limitation |

---

## Implementation Angles

1. **Strategy 4 in reasoning-evolution**: implement a simplified LATS — DFS with reflection instead of full MCTS — for the first run. Use a budget of 20 node expansions, branching factor k=3, and store up to 3 reflections. Measure whether reflections actually steer subsequent branches differently by logging which reflection text appears in expansion prompts and whether it changes the generated steps.

2. **Reflection quality audit**: after the experiment, manually review 5 reflections generated on failed attempts. Score each as: (a) correctly diagnosed the failure, (b) diagnosed the wrong cause, or (c) vague/generic. This is the key unknown about LATS — if reflection quality is poor, the mechanism is not working even when accuracy improves.

3. **Budget sensitivity**: run LATS at budgets of 5, 10, 20, 50 node expansions on the same 5 hard test cases. Plot accuracy vs. budget. The inflection point — where budget doubling no longer improves accuracy — is the practical budget ceiling for this task type.

---

## Open Questions

- For the paper synthesis tasks in reasoning-evolution, is the MCTS exploration actually finding better synthesis than ToT's BFS, or is the improvement from reflection alone? Ablating MCTS (keeping reflection, replacing UCT with random selection) would isolate the contribution.
- The paper uses a fixed exploration constant C=1.0. For tasks where the model's value estimates are unreliable (open-ended synthesis), should C be higher to force more exploration regardless of estimated values?

---

## Revision Notes

