# CASE_V004_ANTHROPIC_MULTI_AGENT_RESEARCH_SYSTEM_v0.1

## Status

Frozen Case Analysis  
Project: **What IDOS Makes Visible**  
Case ID: **V004**  
Regime: **Agentic / Multi-Agent**  
Protocol: `WHAT_IDOS_MAKES_VISIBLE_PROTOCOL_v0.1`  
Sampling source: `CASE_POOL_FREEZE_v0.1`

---

# 1. Case Title

**Anthropic Multi-Agent Research System**

---

# 2. Regime Classification

$$
\boxed{V004 = Agentic / Multi\text{-}Agent}
$$

V004 represents a system in which a Lead Agent delegates tasks to multiple Subagents, each agent operates with its own context and trajectory, and the final output emerges from distributed exploration, synthesis, and verification.

The main structural shift is:

$$
Human
\rightarrow
AI
$$

from V003 becoming:

$$
Human
\rightarrow
Lead\ Agent
\rightarrow
Subagents
\rightarrow
Lead
\rightarrow
Citation\ Agent
$$

Thus delegation becomes recursive, system state becomes distributed, and update relations become networked.

---

# 3. Evidence Base

Primary source:

1. **Anthropic Engineering — How we built our multi-agent research system**
   - https://www.anthropic.com/engineering/multi-agent-research-system

Additional source:

2. **Anthropic Research — Multi-agent systems**
   - https://www.anthropic.com/research/multiagent-systems

The evidence base is dominated by Anthropic’s own engineering and research reporting. Performance claims are therefore treated as company-reported unless independently established.

---

# 4. Stage 1 — Raw Reconstruction

## 4.1 System structure

Anthropic’s Research system uses a Lead Agent that decomposes a research task and delegates parts of the task to multiple Subagents.

Conceptually:

$$
User\ Query
\rightarrow
Lead\ Agent
\rightarrow
Subagent_1,\ Subagent_2,\ldots,Subagent_n
$$

followed by:

$$
Parallel\ Search
\rightarrow
Lead\ Synthesis
\rightarrow
Citation\ Agent
\rightarrow
Final\ Output
$$

The Lead Agent is not only a response generator. It functions as:

$$
\boxed{
Planner + Delegator + Integrator
}
$$

---

## 4.2 Subagent structure

Subagents perform separate research tasks with independent contexts and search trajectories.

Thus:

$$
Trajectory_{A_1}
\neq
Trajectory_{A_2}
\neq
Trajectory_{A_3}
$$

This allows the system to explore multiple paths in parallel rather than relying on one sequential search process.

---

## 4.3 Parallel exploration

The system shifts from:

$$
Sequential\ Search
$$

to:

$$
\boxed{
Parallel\ Exploration
}
$$

Multiple agents can pursue distinct lines of inquiry simultaneously.

This increases coverage but also introduces coordination cost.

---

## 4.4 Performance claims

Anthropic reported that a multi-agent configuration outperformed a single-agent baseline on an internal research evaluation.

However, Anthropic also noted that much of the improvement may come from:

$$
More\ Tokens + More\ Tool\ Calls
$$

Therefore the result is not treated as evidence of emergent collective intelligence by itself.

---

## 4.5 Coordination problems

Anthropic reports practical failure modes including:

- duplicated work;
- poor delegation;
- excessive agent spawning;
- runaway searching;
- coordination complexity;
- cascading failures.

Thus multi-agent structure introduces:

$$
Coordination\ Benefit
$$

and:

$$
Coordination\ Cost
$$

at the same time.

---

## 4.6 Error propagation

A local agent error may propagate into later system decisions.

Conceptually:

$$
Error_{A_i}
\rightarrow
Lead\ Interpretation
\rightarrow
Later\ Delegation
\rightarrow
Final\ Output
$$

The system is therefore path-dependent.

---

## 4.7 Independent context

Each Subagent may operate with its own context and evidence history.

Thus:

$$
State_{A_1}
\neq
State_{A_2}
\neq
State_{Lead}
$$

This enables independent search trajectories, but also means that no single local context necessarily contains the full system state.

---

## 4.8 Persistent process state

The Lead Agent may preserve plans or process state during long research tasks.

Thus the system behaves less like a one-shot prompt and more like a persistent process.

---

## 4.9 Citation Agent

A separate Citation Agent is used to verify and attach citations to the synthesized report.

This means that:

$$
Research
\neq
Citation\ Verification
$$

and these functions are distributed across agents.

---

## 4.10 Human involvement

The user provides the initial research goal.

After that, substantial parts of:

- task decomposition;
- delegation;
- search strategy;
- additional search;
- synthesis;

are performed within the agent system.

Thus:

$$
Human
\rightarrow
Goal
$$

followed by:

$$
Agent\ System
\rightarrow
Decomposition + Exploration + Coordination + Synthesis
$$

---

## 4.11 Recursive delegation

V003 mainly involved:

$$
Human
\rightarrow
Robot
$$

V004 involves:

$$
Human
\rightarrow
Lead
\rightarrow
Subagents
$$

Therefore:

$$
\boxed{
Delegation\ becomes\ recursive
}
$$

---

## 4.12 System boundary

The relevant components include:

- User;
- Lead Agent;
- multiple Subagents;
- search tools;
- external information sources;
- memory or process state;
- Citation Agent;
- synthesis process.

Because agents may be spawned dynamically, system membership can change during execution.

---

## 4.13 What is directly observed?

Public evidence supports:

- Lead Agent delegation;
- multiple Subagents;
- parallel search;
- separate contexts;
- synthesis by Lead Agent;
- separate citation verification;
- coordination failures;
- error propagation;
- increased resource usage.

---

## 4.14 What remains unknown?

Public evidence does not fully establish:

- the exact degree of direct Subagent-to-Subagent communication;
- detailed conflict-resolution mechanisms;
- how reliably the Lead detects incorrect Subagent results;
- how uncertainty is propagated;
- how much humans can intervene mid-process;
- whether long-term model-level mutual learning occurs;
- whether agent hierarchy itself is dynamically redesigned.

These remain open.

---

# 5. Stage 2 — Conventional Analysis

## 5.1 Strong conventional baseline

V004 is strongly explainable through:

- Multi-Agent Systems;
- Distributed Systems;
- Hierarchical Control;
- Task Allocation;
- Collective Intelligence;
- Distributed AI;
- Fault Propagation;
- Reliability Engineering;
- Organizational Theory.

Thus:

$$
\boxed{
Conventional\ analysis\ is\ still\ very\ strong
}
$$

---

## 5.2 Hierarchical control

The Lead Agent acts as a strategic coordinator.

Subagents perform delegated tasks.

This is a conventional hierarchy:

$$
Central\ Planner
\rightarrow
Distributed\ Workers
\rightarrow
Aggregation
$$

---

## 5.3 Distributed systems

Independent agent state creates classical distributed-system issues:

- asynchronous progress;
- partial information;
- duplicated work;
- inconsistent intermediate states;
- communication overhead;
- aggregation difficulty.

---

## 5.4 Parallel search

Parallel search already explains why multiple agents may cover more of a problem space than a single agent.

This does not by itself create IDOS-specific value.

---

## 5.5 Collective intelligence

The system may produce better results than one agent.

However, increased compute and tool usage provide a strong alternative explanation.

Therefore:

$$
Multi\text{-}Agent\ Performance\uparrow
$$

does not imply:

$$
Emergent\ Collective\ Intelligence
$$

---

## 5.6 Task allocation

Lead-to-Subagent delegation can be explained by conventional task allocation and orchestration theory.

---

## 5.7 Coordination cost

As the number of agents grows:

$$
Coordination\ Cost\uparrow
$$

This includes duplication, synthesis difficulty, resource usage, and task-allocation errors.

---

## 5.8 Fault propagation

Subagent mistakes can propagate through later system decisions.

This is explainable through reliability engineering and distributed-system fault propagation.

---

## 5.9 Organizational theory

The architecture can be interpreted as an artificial organization:

- Lead Agent = coordinator / manager;
- Subagents = specialized workers;
- Citation Agent = verification / quality-control function.

This is highly compatible with existing organizational theory.

---

## 5.10 Conventional blind spots

Despite the strong conventional baseline, several questions become harder:

### A. Where is the system state?

$$
State_{Lead}
\neq
State_{A_1}
\neq
State_{A_2}
$$

No single context necessarily contains the whole process state.

### B. What is the Updating Unit?

Possible units include:

- one Subagent;
- the Lead;
- the Lead plus Subagents;
- the entire research process.

### C. Verification becomes recursive

$$
Subagent
\rightarrow
Lead
\rightarrow
Citation\ Agent
\rightarrow
Human
$$

### D. No single actor necessarily observes the whole process

$$
\boxed{
No\ single\ actor\ necessarily\ observes\ the\ whole\ process
}
$$

### E. Delegation becomes recursive

$$
Delegation\ depth > 1
$$

### F. Error origin and observed error may be far apart

The final observed failure may originate from an early delegation or local search decision.

### G. Update becomes networked

Update relations are no longer purely dyadic.

### H. Temporal mismatch occurs between agents

$$
\tau_{A_1}
\neq
\tau_{A_2}
\neq
\tau_{Lead}
$$

---

# 6. Stage 3 — IDOS Analysis

## 6.1 Updating Unit

The strongest candidate is:

$$
\boxed{
U \approx Multi\text{-}Agent\ Research\ Process
}
$$

The system’s output emerges from a distributed process rather than one actor.

Thus:

$$
\boxed{
Updating\ Unit\ becomes\ distributed
}
$$

---

## 6.2 Dynamic Boundary

Agent spawning can change system membership during execution.

Thus:

$$
\boxed{
B_t \neq B_{t+1}
}
$$

V003 involved a moving role boundary.

V004 additionally involves changing system composition.

---

## 6.3 Trajectory

The system contains multiple local trajectories and one emergent system trajectory.

Thus:

$$
Trajectory_{A_1}
\neq
Trajectory_{A_2}
\neq
Trajectory_{Lead}
$$

and:

$$
\boxed{
Trajectory_{System}
\neq
\sum_i Trajectory_{A_i}
}
$$

The whole-system trajectory is not a simple sum of local trajectories.

---

## 6.4 Difference

Differences between agent findings can function as:

- conflict;
- redundancy;
- complementarity;
- new discovery.

Therefore:

$$
Difference
$$

may become a coordination resource rather than only an error signal.

---

## 6.5 Reference Frame

Each agent may have a distinct context and evidence history.

Thus:

$$
F_{A_1}
\neq
F_{A_2}
\neq
F_{Lead}
$$

The system therefore operates through distributed reference frames.

---

## 6.6 Measurement

Agent-level success does not imply system-level success.

Thus:

$$
\boxed{
Agent\ Performance
\neq
System\ Performance
}
$$

Measurement must distinguish local and system-level outcomes.

---

## 6.7 Provenance

Simple source citation is insufficient.

The relevant chain is:

$$
Source
\rightarrow
Subagent
\rightarrow
Interpretation
\rightarrow
Lead
\rightarrow
Synthesis
\rightarrow
Citation
$$

Thus:

$$
\boxed{
Distributed\ Process\ Provenance
}
$$

becomes important.

---

## 6.8 Future Updateability

The question shifts from changing one agent to redesigning the orchestration structure itself.

Thus:

$$
\boxed{
Can\ the\ system\ redesign\ its\ own\ delegation\ architecture?
}
$$

becomes a central second-order question.

---

## 6.9 CFV

Verification is relation-specific.

Examples include:

$$
CFV_{Lead,Subagent}
$$

$$
CFV_{Citation,Lead}
$$

$$
CFV_{Human,System}
$$

A key distinction is:

$$
\boxed{
CFV_{local}
\neq
CFV_{global}
}
$$

---

## 6.10 MU

Update relations form a network:

$$
MU_{Lead\rightarrow A_i}
$$

$$
MU_{A_i\rightarrow Lead}
$$

$$
MU_{Lead\rightarrow A_j}
$$

Thus:

$$
\boxed{
MU\ becomes\ networked
}
$$

---

## 6.11 Verification, influence, and update

The distinctions become:

$$
Verification
\neq
Influence
\neq
Operational\ Update
\neq
Structural\ Update
$$

---

## 6.12 Power

Multi-agent execution does not imply distributed authority.

The Lead may control:

- agent creation;
- task allocation;
- evidence selection;
- synthesis;
- termination.

Thus:

$$
\boxed{
Distributed\ Execution
\neq
Distributed\ Authority
}
$$

---

## 6.13 Temporal Compatibility

Each agent may operate on a different timescale:

$$
\tau_{A_1}
\neq
\tau_{A_2}
\neq
\tau_{Lead}
$$

Thus agent-to-agent temporal compatibility becomes relevant.

---

## 6.14 Reality Contact

The system’s contact with reality is mediated through documents, web content, and other representations.

Thus:

$$
\boxed{
Reality\ Contact\ is\ mediated
}
$$

---

## 6.15 Residual

Agent-to-agent disagreement can be represented as:

$$
Result_{A_1}
-
Result_{A_2}
$$

or:

$$
Lead\ Expectation
-
Subagent\ Finding
$$

This can be treated as:

$$
\boxed{
Cross\text{-}Agent\ Residual
}
$$

---

## 6.16 Holding

When agents disagree, the system may benefit from preserving disagreement rather than collapsing it immediately.

Thus:

$$
\boxed{
Hold\ the\ disagreement
}
$$

is analytically relevant.

However, this is not confirmed as an explicit Anthropic implementation mechanism.

---

## 6.17 Possibility Space

Parallel agents expand available search paths.

Thus:

$$
Possibility\ Space_{multi-agent}
>
Possibility\ Space_{single-agent}
$$

---

## 6.18 12PDM

V004 increases the importance of process sequencing across:

- Representation;
- Difference;
- Residual;
- Holding;
- Update;
- Trajectory;
- Reopening.

Thus 12PDM becomes a stronger candidate than in earlier cases.

---

# 7. Stage 4 — Incremental Visibility Test

## 7.1 Conventional View

Existing theory already explains:

- parallel search;
- coordination cost;
- hierarchical control;
- task allocation;
- fault propagation;
- asynchronous agents;
- distributed state.

These are not counted as IDOS-specific findings.

---

## 7.2 Y1 — Distributed Updating Unit

The update unit may be the whole research process rather than any single agent.

$$
\boxed{
U \approx Multi\text{-}Agent\ Research\ Process
}
$$

Classification:

$$
IV\text{-}2
$$

---

## 7.3 Y2 — Distributed System State

The system state is not located in one place.

$$
State_{Lead}
\neq
State_{A_1}
\neq
State_{A_2}
$$

This becomes visible as a relation among partial states.

Classification:

$$
IV\text{-}2
$$

---

## 7.4 Y3 — Recursive Delegation

Delegation becomes:

$$
Human
\rightarrow
Lead
\rightarrow
Subagent
$$

and may expand dynamically during execution.

Classification:

$$
IV\text{-}2
$$

---

## 7.5 Y4 — Networked Update

Update is no longer purely dyadic.

$$
\boxed{
Update\ is\ no\ longer\ dyadic
}
$$

Classification:

$$
IV\text{-}2
$$

---

## 7.6 Y5 — Local vs Global Verification

A local result may be verifiable while the adequacy of the overall search process remains unverifiable.

Thus:

$$
\boxed{
Local\ CFV
\neq
Global\ CFV
}
$$

Classification:

$$
IV\text{-}2
$$

---

## 7.7 Y6 — Process Provenance

V004 makes visible the distinction:

$$
\boxed{
Source\ Provenance
\neq
Process\ Provenance
}
$$

Source citation alone does not reconstruct the transformation path through the agent system.

Classification:

$$
IV\text{-}2
$$

---

## 7.8 Y7 — Global Output ≠ Global Observer

This is the strongest candidate in V004.

The system can generate:

$$
\boxed{
One\ Global\ Output
}
$$

without any one actor necessarily observing:

- all local states;
- all search paths;
- all intermediate interpretations;
- the complete provenance chain.

Thus:

$$
\boxed{
Global\ Output
\neq
Global\ Observer
}
$$

This means:

> 全体を直接把握する主体が存在しなくても、系全体として一つの判断・出力・更新が成立する。

Classification:

$$
\boxed{
IV\text{-}3\ candidate
}
$$

This is not yet confirmed as IV-3 because distributed cognition, organizational epistemology, and distributed systems may provide alternative explanations.

---

## 7.9 Y8 — Distributed Execution ≠ Distributed Authority

Multi-agent execution may be distributed while authority remains concentrated in the Lead.

Thus:

$$
\boxed{
Distributed\ Execution
\neq
Distributed\ Authority
}
$$

Classification:

$$
IV\text{-}2
$$

---

## 7.10 What does not count as incremental visibility

The following are excluded:

- multiple agents search in parallel;
- coordination cost increases;
- task allocation can fail;
- fault propagation occurs;
- context differs across agents;
- hierarchy exists.

These are already visible through established frameworks.

---

# 8. Stage 5 — Necessity Test

| IDOS Concept | V004 | 理由 |
|---|---:|---|
| Updating Unit | **N2** | Multi-Agent Research Process全体を更新単位として扱う必要 |
| Dynamic Boundary | **N2** | Agent生成によりsystem membership自体が変化 |
| Trajectory | **N2** | 再帰的委譲・誤り伝播を時間方向で追う |
| Difference | N1 | Agent間の不一致を明示 |
| Reference Frame | **N2** | 各Agentが異なる証拠履歴・contextを持つ |
| Measurement | **N2** | Agent性能とSystem性能を分離 |
| Provenance | **N2** | SourceではなくProcess Provenanceが必要 |
| Future Updateability | **N2** | Delegation Architecture自体の再設計可能性を見る |
| CFV | **N2** | Local verificationとGlobal verificationを分離 |
| MU | **N2** | 更新関係をnetworkとして扱う |
| Power | **N2** | Distributed executionとauthorityを分離 |
| Temporal Compatibility | **N2** | Agent間の非同期進行が統合に影響 |
| Reality Contact | N1 | 現実接触がrepresentation媒介になる |
| Residual | N1 | Cross-Agent Residualとして有用 |
| Holding | N1 | 不一致保持・追加探索に有用 |
| Possibility Space | N1 | 並列探索空間の拡大に有用 |
| 12PDM | **N2** | 複数Agent間のprocess sequencing記述に必要性が上昇 |

---

# 9. IV-3 Candidate Re-Test

The main candidate is:

$$
\boxed{
Global\ Output
\neq
Global\ Observer
}
$$

After concept removal tests, this structure still depends strongly on the combined use of:

- Updating Unit;
- Dynamic Boundary;
- Trajectory;
- Reference Frame;
- Provenance;
- CFV;
- MU.

The insight is therefore more than a simple terminology replacement.

However, established distributed-systems and distributed-cognition theories may still provide substantial alternative explanation.

Therefore:

$$
\boxed{
IV\text{-}3\ candidate\ retained
}
$$

but:

$$
\boxed{
IV\text{-}3\ not\ yet\ confirmed
}
$$

---

# 10. Cross-Case Comparison

| Concept | V001 | V002 | V003 | V004 |
|---|---:|---:|---:|---:|
| Updating Unit | N1 | N2 | N2 | **N2** |
| Dynamic Boundary | N0 | N1 | N2 | **N2** |
| Trajectory | N2 | N2 | N2 | **N2** |
| Reference Frame | N0 | N1 | N2 | **N2** |
| Measurement | N1 | N2 | N2 | **N2** |
| Provenance | N0 | N1 | N2 | **N2** |
| Future Updateability | N2 | N2 | N2 | **N2** |
| CFV | N0 | N1 | N2 | **N2** |
| MU | N1 | N2 | N2 | **N2** |
| Power | N0 | N1 | N2 | **N2** |
| Temporal Compatibility | N0 | N2 | N1 | **N2** |
| Reality Contact | N0 | N0 | N0 | N1 |
| Residual | N0 | N0 | N1 | N1 |
| Holding | N0 | N0 | N0 | N1 |
| Possibility Space | N0 | N1 | N1 | N1 |
| 12PDM | N0 | N0 | N1 | **N2** |

A notable change in V004 is that 12PDM becomes N2.

This suggests that once the system becomes multi-agent, the sequence of process transitions itself becomes more important than a static concept inventory.

---

# 11. Provisional Conclusion

V004 remains substantially explainable through established theory.

However, the following structure survives the Necessity Test:

$$
\boxed{
Global\ Output
\neq
Global\ Observer
}
$$

In Japanese:

> 誰もシステム全体の状態・履歴・判断過程を完全には持っていないにもかかわらず、系全体として一つの出力・判断・更新が成立する。

To describe this structure adequately, the following need to be considered together:

- Distributed State;
- Dynamic Boundary;
- Process Provenance;
- Local CFV vs Global CFV;
- Networked MU;
- Trajectory;
- Power.

Thus:

$$
\boxed{
Incremental\ Visibility_{V004}
=
High
}
$$

and:

$$
\boxed{
IV\text{-}3\ candidate\ retained
}
$$

However, IV-3 confirmation is deferred until V005 and the five-case cross-case synthesis.

---

# 12. Open Residuals

The following remain open:

1. Can a global system state be operationally reconstructed from distributed local states?
2. Under what conditions does local CFV fail to imply global CFV?
3. How should Process Provenance be represented in recursive delegation systems?
4. Can MU be represented as a dynamic network rather than a pairwise relation?
5. When does distributed execution become effectively autonomous from concentrated authority?
6. How should cross-agent disagreement be preserved without collapsing into premature consensus?
7. Does V005 produce a stronger form of system-level behavior in which even the delegation architecture becomes emergent?
8. Does the IV-3 candidate survive the Future Regime Proxy?

---

# 13. Cross-Case Carry-Forward Markers

Track the following in V005:

- `Updating Unit` — V004: N2
- `Dynamic Boundary` — V004: N2
- `Trajectory` — V004: N2
- `Reference Frame` — V004: N2
- `Measurement` — V004: N2
- `Provenance` — V004: N2
- `Future Updateability` — V004: N2
- `CFV` — V004: N2
- `MU` — V004: N2
- `Power` — V004: N2
- `Temporal Compatibility` — V004: N2
- `Reality Contact` — V004: N1
- `Residual` — V004: N1
- `Holding` — V004: N1
- `Possibility Space` — V004: N1
- `12PDM` — V004: N2
- `IV-3 candidate` — retained, not confirmed

These are case-specific classifications and should not be generalized before cross-case synthesis.

---

# 14. Freeze Rule

This V004 result is frozen for the five-case pilot.

It should not be revised merely because V005 produces stronger or weaker IDOS results.

Permissible later changes are limited to:

- factual correction;
- source correction;
- explicit methodological correction;
- clearly documented protocol-level revision after cross-case synthesis.

The analytical conclusion should otherwise remain fixed until the five-case synthesis.
