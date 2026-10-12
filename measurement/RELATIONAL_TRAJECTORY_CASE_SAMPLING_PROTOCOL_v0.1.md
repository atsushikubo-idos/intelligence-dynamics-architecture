# RELATIONAL_TRAJECTORY_CASE_SAMPLING_PROTOCOL_v0.1

**Status:** Freeze Candidate  
**Date:** 2026-10-06  
**Measurement Reference:** RELATIONAL_TRAJECTORY_MEASUREMENT_PROTOCOL_v0.1  
**Architecture Reference:** IDOS MASTER_MAP v1.1  
**Purpose:** Predefine case eligibility and mechanical selection for the first Relational Trajectory measurement case.

## 1. Principle

Case selection must not depend on whether a study is expected to support IDOS, produce RT-3/RT-4, demonstrate novelty, or generate positive social value.

A null or negative case is valid.

## 2. Discovery Domain

Initial discovery domain:

> Empirical Human–AI / Human–Robot / Human–Adaptive-Machine studies involving repeated interaction between a human and an artificial adaptive unit.

This first pool is a **web-accessible discovery pool**, not a claim of exhaustive systematic-review coverage.

## 3. Inclusion Criteria

A study enters the frozen candidate pool only if all are satisfied:

I1. Empirical study with human participants.  
I2. Human and artificial unit interact repeatedly rather than once.  
I3. Artificial unit changes action, policy, belief, learning state, or other adaptive variable during or across interaction.  
I4. Human behavior across interaction is observable.  
I5. Artificial-unit behavior/adaptation across interaction is observable.  
I6. Temporal ordering of repeated interaction can be reconstructed.  
I7. Sufficient full-text methodological/results information is publicly inspectable for protocol application.

## 4. Exclusion Criteria

Exclude:

E1. Pure simulation with no human participant.  
E2. One-shot interaction.  
E3. Artificial system is entirely fixed and no adaptive variable changes.  
E4. Only final performance is reported, preventing reconstruction of interaction dynamics.  
E5. Review/theory paper without an empirical interaction study.  
E6. Insufficient accessible methodological evidence.

## 5. Criteria Explicitly Forbidden for Selection

Do **not** select based on:

- apparent IDOS fit;
- expected Update-Mechanism Change;
- expected Future Updateability;
- presence of a different Task₂;
- expected RT-3/RT-4 result;
- expected differential value;
- expected novelty;
- conceptual attractiveness.

Task₂ is a measurement advantage, not an inclusion requirement.

## 6. Frozen Initial Candidate Pool

**RT-C001**  
Nikolaidis, Hsu & Srinivasa (2017), *Human-robot mutual adaptation in collaborative tasks: Models and experiments.*

**RT-C002**  
van Zoelen et al. (2021), *Becoming Team Members: Identifying Interaction Patterns of Mutual Adaptation for Human-Robot Co-Learning.*

**RT-C003**  
Chasnov, Ratliff & Burden (2025), *Human adaptation to adaptive machines converges to game-theoretic equilibria.*

The pool is frozen before applying the IDOS RT measurement outcome classification.

## 7. Mechanical Selection Rule

Seed:

`RTM-v0.1-20261006`

For every candidate, calculate:

`SHA256(seed + "|" + candidate_id + "|" + canonical_title)`

Select the candidate with the lexicographically smallest SHA-256 hexadecimal digest.

No reroll is permitted because the selected case appears inconvenient, negative, weak, or difficult.

## 8. Frozen Hash Results

RT-C001  
`eef2f60a19324033505775e13f7891464ff6f27988511a3ad260957f21b06362`

RT-C002  
`8a0748b6eb3c8afaeb0dc1ee92f9b7c7d3d881cb7a6ec6144331ea580e21b58d`

RT-C003  
`9c8b9bcc07e16db3384572e187f7a81135d3a3507f0a4b1a5d9d79a5fc4a3ea8`

Lexicographically smallest:

\[
\boxed{RT-C002}
\]

Therefore:

\[
\boxed{RT-001 = van\ Zoelen\ et\ al.\ (2021)}
\]

## 9. Selection Interpretation

RT-001 was **not selected because it is expected to validate IDOS**.

It was selected by a deterministic rule from the frozen eligible pool.

The selected study may produce:

- RT-0,
- RT-1,
- RT-2,
- RT-3,
- RT-4,
- or Indeterminate.

All are valid results.

## 10. Anti-Cherry-Picking Rule

After RT-001 selection:

1. Do not replace the case.
2. Do not alter L1–L4 definitions.
3. Do not redefine G to fit observed results.
4. Do not weaken evidence thresholds.
5. Do not reinterpret missing evidence as positive evidence.
6. Preserve negative and indeterminate findings.
7. Separate Measurement, Differential Value, Social Value, and Novelty.

## 11. Next Step

Apply `RELATIONAL_TRAJECTORY_MEASUREMENT_PROTOCOL_v0.1` to RT-001.

Before outcome interpretation, reconstruct and freeze:

- Unit A / Unit B;
- T0–T4;
- Task₁ / Task₂;
- baseline G_A / G_B;
- candidate L3 subfunctions;
- predicted direction where justified;
- alternative explanations.

Only after that freeze should RT-001 outcome classification begin.

**Status: FREEZE CANDIDATE**
