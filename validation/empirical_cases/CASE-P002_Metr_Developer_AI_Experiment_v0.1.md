# CASE-P002 — Software Developer AI Experiment
## Theory-Neutral Reconstruction, Master Map Mapping, Red Team, and Revision Pressure Test

**Case ID:** CASE-P002  
**Study:** *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*  
**Source:** METR  
**Study type:** Randomized Controlled Trial  
**Sampling Protocol:** CASE_SAMPLING_PROTOCOL_v0.1  
**Master Map Baseline:** MASTER_MAP_v1.0 — FROZEN  
**IDOS Analysis Status at Selection:** NOT STARTED  
**Record Version:** v0.1  
**Date:** 2026-10-02

---

## 0. Selection Record

CASE-P002 was not selected because it appeared favorable, interesting, or compatible with IDOS.

The case was selected by continuing the same seeded pseudorandom sequence used for CASE-P001, without replacement, from the original frozen candidate pool.

```yaml
CASE-P002

Case:
Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity

Source:
METR

Sampling Protocol:
CASE_SAMPLING_PROTOCOL_v0.1

Candidate Pool:
Original frozen pool from CASE-P001 selection

Selection Rule:
Continue the original seeded pseudorandom sequence without replacement

Original Candidate Index:
6

Random Seed:
20261002

Master Map Baseline:
MASTER_MAP_v1.0 — FROZEN

IDOS Analysis Status:
NOT STARTED AT TIME OF SELECTION
```

This case therefore enters the evaluation sequence prospectively under the frozen protocol.

---

# Stage A — Theory-Neutral Reconstruction

## A1. Study Setting

METR studied experienced open-source software developers working on real tasks in repositories with which they were already highly familiar.

The study included:

- 16 experienced OSS developers;
- 246 real software-development tasks;
- task-level randomized assignment to AI-allowed or AI-disallowed conditions;
- mature repositories in which participants had substantial prior experience;
- early-2025 AI tools, primarily Cursor Pro and Claude 3.5 / 3.7 Sonnet.

The primary observed outcome was task implementation time.

The study should therefore be interpreted as evidence about this specific population and setting, not about software development or AI productivity in general.

---

## A2. Primary Result

The central experimental result was:

\[
\boxed{
T_{\mathrm{AI}}
>
T_{\mathrm{NoAI}}
}
\]

with an estimated effect of approximately:

\[
\boxed{
\text{AI allowed}
\rightarrow
19\% \text{ longer implementation time}
}
\]

Thus, under the studied conditions, AI availability was associated with a measurable productivity slowdown rather than a speedup.

---

## A3. Expected, Observed, and Perceived Effects

Before performing the tasks, developers expected AI to improve speed by approximately:

\[
\boxed{
24\% \text{ speedup expected}
}
\]

The experimentally observed effect was:

\[
\boxed{
19\% \text{ slowdown observed}
}
\]

After the study, developers still estimated that AI had made them approximately:

\[
\boxed{
20\% \text{ faster}
}
\]

Therefore, three empirically distinct quantities existed:

\[
\boxed{
\text{Expected Effect}
\neq
\text{Observed Effect}
\neq
\text{Perceived Effect}
}
\]

More specifically:

\[
Expected=-24\% \text{ time}
\]

\[
Observed=+19\% \text{ time}
\]

\[
Perceived=-20\% \text{ time}
\]

This distinction exists prior to any IDOS interpretation.

---

## A4. Minimal Theory-Neutral Reconstruction

The minimal event structure is:

\[
\boxed{
\text{Experienced Developer}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{Real OSS Task}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{Random Assignment: AI Allowed / AI Disallowed}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{Task Execution}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{Measured Completion Time}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{AI Allowed}
\rightarrow
19\% \text{ Longer}
}
\]

In parallel:

\[
\boxed{
\text{Expected Speedup}=24\%
}
\]

and:

\[
\boxed{
\text{Post-hoc Perceived Speedup}=20\%
}
\]

No IDOS-specific process is required to state these facts.

---

# Stage B — Mapping to MASTER_MAP_v1.0

## B1. Mapping Discipline

Mapping is not validation.

\[
\boxed{
\text{Mapping}
\neq
\text{Validation}
}
\]

The following labels are used:

- **O — Observed:** directly supported by the study;
- **I — Inferred:** plausible but not directly observed;
- **U — Unobservable:** cannot be determined from the available design;
- **N — Not required / No evidence:** not needed or unsupported in this case.

---

## B2. Master Map Mapping Table

| Master Map Construct | CASE-P002 Status | Classification |
|---|---|---|
| Reality Contact | Real OSS tasks in familiar repositories | O |
| Observation | Completion time and participant estimates | O |
| Reference Frame | Related to prediction/perception but internal frame not directly observed | I / U |
| Difference | AI vs non-AI time difference; forecast vs observed difference | O candidate |
| Representation | Implied by forecasts and retrospective estimates | I |
| Residual | Cannot be equated with discrepancy alone | I / U |
| Holding | Not measured | U |
| Selection / Γ | Not measured | U |
| Transformation | Work process changed under AI availability | O / I |
| Update | Insufficient evidence | U |
| Possibility Space | AI availability changes available actions | I |
| Trajectory | Longitudinal structure insufficiently measured | I / U |
| Limit | Not measured | U |
| Enactment | Actual coding activity is a candidate | O / I |
| Reopening | Not measured | U |
| Updating Unit | Cannot be uniquely identified | U |
| Relational Update | Interaction exists; relational change not directly measured | I / U |
| System Update | Cannot be operationally established | U |
| Measurement System | Multiple measurement modes produce divergent results | O |
| Forward vs Inverse Measurement | Distinction is directly relevant | O |
| Evaluation / Improvement | Completion-time effect directly measurable | O |
| Governance | Outside study scope | N |
| CDP | Not tested | U / N |
| Translation Residual | Not tested | U |
| DO / CFV / MU | Not tested | U |

---

## B3. Main Stage B Result

The case does not reproduce the full IDOS process structure.

The strongest directly observable structure is:

\[
\boxed{
\text{Reality Contact}
\rightarrow
\text{Measurement}
\rightarrow
\text{Observed Difference}
}
\]

By contrast, much of the proposed internal update chain remains unobserved:

\[
\boxed{
Residual
\rightarrow
Holding
\rightarrow
Selection
\rightarrow
Update
\rightarrow
Possibility\ Space
\rightarrow
Trajectory
}
\]

cannot be reconstructed from this study without adding unobserved assumptions.

This is an important negative constraint.

---

# Stage C — Red Team / Incremental Explanatory Value Test

## C1. Core Question

The central Red Team question is:

\[
\boxed{
\text{Does IDOS explain anything here that simpler existing explanations do not?}
}
\]

The answer from CASE-P002 is currently:

\[
\boxed{
\text{Not yet, for most of the observed result.}
}
\]

---

## C2. Alternative Explanations

The main observed findings can plausibly be explained using existing frameworks without invoking IDOS.

### Cognitive and Perceptual Explanations

The divergence between measured and perceived productivity may reflect ordinary cognitive or perceptual effects.

Therefore:

\[
\boxed{
Observed
\neq
Perceived
}
\]

does not by itself establish the need for IDOS.

### Measurement Theory

Differences among benchmark results, field experiments, forecasts, and self-reports can be addressed through existing concepts such as:

- construct validity;
- ecological validity;
- measurement error;
- instrument dependence.

Thus:

\[
\boxed{
M_1(R)
\neq
M_2(R)
}
\]

does not by itself establish IDOS-specific explanatory value.

### Human-Computer Interaction

The slowdown may also be explained through ordinary interaction costs:

\[
\boxed{
\text{Net Benefit}
=
\text{AI Assistance}
-
\text{Coordination / Verification Cost}
}
\]

No new Updating Unit or system-level theory is required to state this possibility.

### Context-Specific Expertise

The participants were experienced developers working in familiar repositories.

Therefore:

\[
\boxed{
\text{High Human Baseline}
+
\text{AI Interaction Cost}
}
\]

may be sufficient to explain the observed slowdown.

---

## C3. Concepts Under Strong Red Team Pressure

### Residual

A measured discrepancy cannot automatically be labeled Residual.

Otherwise:

\[
Residual
=
\text{Unexplained Difference}
\]

would become merely a relabeling.

**Assessment:** B / C

### Holding

No independent evidence of Holding exists in this case.

**Assessment:** C

### Selection

The experimental assignment of AI availability is not IDOS Selection.

\[
\boxed{
\text{Experimental Assignment}
\neq
\text{Selection}
}
\]

**Assessment:** C

### Relational Updating Unit

Human + AI interaction does not by itself establish:

\[
U_{HA}
\]

as a distinct Updating Unit.

**Assessment:** C

### System Update

A change in task performance does not establish System Update.

\[
\boxed{
\text{Performance Difference}
\neq
\text{System Update}
}
\]

**Assessment:** C

---

## C4. What Remains Potentially Distinctive

After removing explanations already available through measurement theory, cognitive science, and HCI, one potentially useful IDOS-level question remains:

\[
\boxed{
\text{How does a detected Difference propagate across observation, recognition, response, and later updating?}
}
\]

CASE-P002 directly observes an external discrepancy:

\[
D_{\mathrm{external}}
=
T_{\mathrm{AI}}
-
T_{\mathrm{NoAI}}
\]

but the relationship between that discrepancy and participant recognition or later updating is not directly measured.

Thus:

\[
\boxed{
D_{\mathrm{external}}
\not\Rightarrow
D_{\mathrm{recognized}}
}
\]

and potentially:

\[
\boxed{
D_{\mathrm{external}}
\not\Rightarrow
Update
}
\]

The second statement remains unobserved and must not be treated as a result.

The research implication is that future tests must directly measure the propagation path rather than infer it.

---

## C5. Stage C A/B/C Classification

| Construct | Assessment |
|---|---|
| Reality Contact | A |
| Difference | A |
| Reference Frame | B |
| Measurement System | A |
| Forward vs Inverse Measurement | A |
| Residual | B / C |
| Holding | C |
| Selection | C |
| Transformation | B |
| Update | B / C |
| Possibility Space | B |
| Trajectory | C |
| Relational Update | B / C |
| Relational Updating Unit | C |
| System Update | C |
| CDP | C / N |
| Translation Residual | C / N |
| DO / CFV / MU | C / N |

The case therefore does not validate IDOS.

\[
\boxed{
\text{CASE-P002 does NOT validate IDOS}
}
\]

and:

\[
\boxed{
\text{Most of CASE-P002 can currently be explained without IDOS}
}
\]

---

# Stage D — Master Map Revision Pressure Test

## D1. Revision Decision

The case does not currently justify revision of MASTER_MAP_v1.0.

\[
\boxed{
\text{Architectural Revision}
=
0
}
\]

However:

\[
\boxed{
\text{Measurement Pressure}
\uparrow
}
\]

The case mainly changes empirical priorities rather than the frozen architecture.

---

## D2. Construct-Level Revision Pressure

| Construct | Stage D Decision |
|---|---|
| Reality Contact | KEEP |
| Difference | KEEP |
| Reference Frame | KEEP + OPERATIONALIZE |
| Measurement Architecture | KEEP |
| Forward / Inverse Measurement | KEEP |
| Residual | DEMOTE + OPERATIONALIZE |
| Holding | DEMOTE |
| Selection Problem | KEEP |
| Γ Mechanism | DEMOTE / OPERATIONALIZE |
| Transformation | KEEP |
| Update | KEEP + HIGH-PRIORITY OPERATIONALIZATION |
| Possibility Space | KEEP PROVISIONAL |
| Trajectory | NOT TESTED |
| Relational Update | KEEP PROVISIONAL |
| Relational Updating Unit | KEEP OPEN |
| System Update | KEEP OPEN + OPERATIONALIZE |
| CDP | NOT TESTED |
| DO / CFV / MU | NOT TESTED |
| Difference-Update Trace | EMPIRICAL PRIORITY ↑ |

---

## D3. Main Revision Pressure

CASE-P002 makes one problem especially clear:

\[
\boxed{
\text{Difference observed}
\not\Rightarrow
\text{Update observed}
}
\]

The current architecture can survive this result because MASTER_MAP_v1.0 does not require every provisional mechanism to be present in every case.

But future empirical work must distinguish at least:

\[
\boxed{
\text{Difference}
\rightarrow
\text{Recognition}
\rightarrow
\text{Response}
\rightarrow
\text{Transformation}
\rightarrow
\text{Reality Recontact}
}
\]

without assuming that each transition occurred.

This creates a direct empirical priority for the Difference-Update Trace.

---

# Final CASE-P002 Result

CASE-P002 does not provide positive validation of IDOS.

It also does not produce an architectural contradiction strong enough to revise MASTER_MAP_v1.0.

Instead, it exposes a major observational gap:

\[
\boxed{
\textbf{Detected Difference}
\quad
\not\Rightarrow
\quad
\textbf{Demonstrable Update}
}
\]

The architecture therefore survives, but only at a relatively abstract level.

The case places substantial pressure on the empirical program to directly observe the intermediate path between Difference and Update rather than reconstruct it retrospectively using theoretical language.

The most defensible summary is:

\[
\boxed{
\textbf{CASE-P002 preserved the architectural skeleton, but exposed a large observational gap between detected Difference and demonstrable Update.}
}
\]

This result should not be interpreted as support for all IDOS mechanisms.

Rather, it narrows the next empirical task:

\[
\boxed{
\textbf{Measure the Difference-Update Trace directly.}
}
\]

---

# Research Implication

CASE-P002 suggests that future prospective cases should prioritize datasets or study designs capable of separately observing:

1. an externally detectable Difference;
2. whether the Difference was recognized;
3. the response or non-response to that Difference;
4. any subsequent transformation;
5. whether continuity is sufficient to call the transformation an Update;
6. Reality Recontact;
7. whether the resulting outcome generates a new Difference.

The objective is not to make every case fit the architecture.

The objective is to determine which parts of the architecture remain necessary when observation is strict enough to permit failure.

---

## Sources

- METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*
- METR study summary and methodological discussion, 2025-07-10
- MASTER_MAP_v1.0 — FROZEN, 2026-10-02
- CASE_SAMPLING_PROTOCOL_v0.1
