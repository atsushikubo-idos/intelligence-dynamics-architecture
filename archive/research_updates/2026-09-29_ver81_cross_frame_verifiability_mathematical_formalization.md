# IDOS Research Update — ver.81 / ver.81+

## Cross-Frame Verifiability, Mutual Updateability, and Mathematical Formalization

**Date:** 2026-09-29  
**Status:** Working Theory / Research Snapshot  
**Framework:** Intelligence Dynamics Operating System (IDOS)

---

## 1. Purpose of This Update

This update extends IDOS from a framework for describing intelligence dynamics toward an architecture for interaction among heterogeneous intelligences.

The central research question is:

> How can heterogeneous intelligences remain mutually verifiable and updateable when their frames of reference, boundaries, measurement systems, values, and verification criteria themselves continue to change?

The relevant intelligences may include:

- humans,
- AI systems,
- organizations,
- collective systems,
- and future AI / ASI systems.

The objective is not to force these intelligences into a shared ontology, representation, value system, measurement standard, or world model.

Instead, IDOS explores whether their **dynamics of updating** can provide a common interface for observation, challenge, verification, and continued revision.

This update develops that idea at two connected levels:

- **ver.81:** Social Connection Architecture
- **ver.81+:** Mathematical Formalization and Candidate Executable Toy Model

ver.81+ is treated here as a formal extension of ver.81 rather than as a separate conceptual revision.

---

## 2. Canonical Core: 12 Dynamic Processes

The canonical internal update dynamics remain unchanged:

1. Reality
2. Difference
3. Representation
4. Residual
5. Holding
6. Update
7. Possibility Space
8. Trajectory
9. Limit
10. Enactment
11. Reality'
12. Reopening

These twelve processes describe the internal dynamics through which an intelligence encounters difference, detects unresolved residuals, holds them, updates itself, generates possibilities, forms trajectories, acts, and recontacts reality.

The twelve processes should not be confused with the Common Dynamics Protocol.

---

## 3. Separation of the 12 Dynamic Processes and CDP

A major clarification in the current architecture is:

> **12 Dynamic Processes != Common Dynamics Protocol (CDP)**

The 12 Dynamic Processes describe **how an intelligence updates**.

CDP describes **how heterogeneous intelligences expose and connect aspects of their update dynamics across frames**.

The current CDP consists of six interoperability functions:

1. Describe
2. Translate
3. Compare
4. Coordinate
5. Trace
6. Recontact

Therefore:

**12 Dynamic Processes = internal update dynamics**

**CDP = cross-intelligence interoperability layer**

This distinction prevents the internal dynamics of intelligence from being conflated with the protocol used to connect heterogeneous intelligences.

---

## 4. Dynamic Measurement Configuration

For intelligence i, the current measurement configuration is represented as:

S_i(t) = {X_i(t), F_i(t), B_i(t), M_i(t), V_i(t), C_i(t), P_i(t)}

where:

- X = Reality / object of observation
- F = Frame
- B = Boundary
- M = Measurement
- V = Value
- C = Verification criteria
- P = Possibility Space

The important assumption is that these components may themselves change over time.

IDOS therefore does not only ask how to measure a changing world.

It asks:

> How can measurement remain meaningful when the measurement system itself is part of the dynamics?

This is the basis of Dynamic Measurement in the current IDOS architecture.

---

## 5. Cross-Frame Residual

For two intelligences i and j:

Residual(i <- j, t) = Delta_i(O_j(t), S_i(t))

Residual is defined relationally.

It represents the part of another intelligence's output, action, or observation that cannot be fully absorbed by the receiving intelligence's current configuration.

In general:

Residual(i <- j) != Residual(j <- i)

Residual is therefore not assumed to be symmetric.

The same interaction may produce different Residuals depending on the receiving intelligence's Frame, Boundary, Measurement, Value, Verification Criteria, and Possibility Space.

This makes Residual not merely an objective error signal, but a relation between observation and the current configuration of the receiving intelligence.

---

## 6. Translation Residual

Translation across heterogeneous intelligences is not assumed to preserve meaning perfectly.

> **Translation != Perfect Preservation**

Information may be lost, distorted, reconstructed, or remain unresolved when translated from one frame into another.

The current architecture provisionally represents this remainder as:

**Translation Residual**

Conceptually:

TR(i -> j, t) = Delta_j^Tr(O_i(t), T(i -> j)(O_i(t)))

The purpose is not to eliminate translation loss.

The purpose is to prevent translation loss from disappearing silently from the architecture.

What cannot be preserved through translation may itself become a source of future Residual and updating.

---

## 7. Common Dynamic Observability

IDOS does not require complete access to another intelligence's internal state.

Instead, it introduces the concept of:

**Common Dynamic Observability**

This refers to a limited but operationally useful capacity to observe aspects of another intelligence's update dynamics.

The goal is not:

- complete state reconstruction,
- identical representation,
- identical meaning,
- identical values,
- or identical verification criteria.

The goal is sufficient observability to support continued challenge and verification across heterogeneous frames.

In general:

DO_ij(t) < 1

Complete observability is not assumed.

The relevant question is whether enough of the update dynamics can become mutually visible to support cross-frame verification.

---

## 8. Dynamic Cross-Frame Verifiability

Common Dynamic Observability leads to a stronger research question:

> Can heterogeneous intelligences remain mutually verifiable even when their verification criteria themselves change?

This motivates the concept of:

**Dynamic Cross-Frame Verifiability**

A provisional representation is:

CFV_ij(t) = f(DO_ij(t), R_ij(t), TR_ij(t), Q_ij(t))

where:

- DO = Dynamic Observability
- R = Residual exchangeability
- TR = Translation Residual / translation fidelity
- Q = Challengeability

This equation is currently a research scaffold rather than a validated measurement function.

Its operational definition remains open.

The central shift is from requiring common verification criteria to asking whether verification can remain possible across changing frames.

---

## 9. Verifiability Is Not Updateability

A central distinction introduced in this update is:

> **Verifiability != Updateability**

An intelligence may be observable and challengeable without being meaningfully affected by that challenge.

Therefore:

CFV_ij > 0

does not necessarily imply:

MU_ij > 0

where MU represents Mutual Updateability.

A provisional representation is:

MU_ij(t) = g(CFV_ij(t), A_ij(t), G_ij(t), H_i(t), P_i(t))

where:

- A = access to Residual,
- G = governance / power / effective influence,
- H = Holding capacity,
- P = capacity to reopen Possibility Space.

This distinction makes power asymmetry an explicit boundary condition of cross-intelligence interaction.

Residual generation, Residual recognition, Residual verification, and Residual influence should not be treated as equivalent.

A weak actor may generate an important Residual while having little capacity to make that Residual influence the receiving system.

Similarly, an AI system may strongly influence human updating while the reverse path remains weak.

Interaction alone therefore does not imply Mutual Updateability.

---

## 10. Temporary Closure and Reopening

IDOS does not imply endless openness.

The canonical process already includes:

Possibility Space  
-> Limit  
-> Enactment  
-> Reality'  
-> Reopening

This introduces an important distinction:

> **Temporary Closure != Permanent Consensus**

A system may temporarily reduce possibilities in order to act.

The resulting Enactment changes reality.

That new Reality' provides a new point of contact from which Difference and Residual may emerge again.

The objective is therefore neither permanent openness nor permanent closure.

It is the capacity to close provisionally while retaining the possibility of reopening.

---

## 11. Descriptive Dynamics and Normative Deliberation

Another important boundary is:

> **Descriptive Dynamics != Normative Deliberation**

IDOS may describe:

- what produced a Residual,
- what was held,
- what changed,
- how a trajectory formed,
- and what was enacted.

This does not automatically determine whether the resulting update is ethically, politically, or socially desirable.

Normative judgment therefore remains distinct from the descriptive dynamics represented by IDOS.

The current architecture should not be interpreted as an automatic mechanism for deciding what ought to be valued or preserved.

---

## 12. Updating Unit, Subject, and Sovereignty

The following concepts must also remain distinct:

> **Updating Unit != Subject != Sovereign Subject**

The emergence of a relational Updating Unit does not automatically imply the emergence of a new subject.

Likewise, the emergence of a subject does not automatically establish sovereignty.

This distinction becomes increasingly important when considering Human-AI systems, organizations, collective intelligence, and future AI / ASI systems.

---

# Part II — ver.81+ Mathematical Formalization

## 13. Mathematical Status

The current mathematical development can be separated into three levels.

### Level 1 — Conceptual Architecture

Concepts such as:

- Residual
- Holding
- Dynamic Measurement
- CDP
- Cross-Frame Verifiability
- Mutual Updateability

### Level 2 — Typed Formal Model

State spaces, operators, domains, codomains, partial observation, and asymmetric Residual relations are explicitly distinguished.

### Level 3 — Executable Dynamical Model

Concrete update equations, parameters, simulations, and stability / viability tests are implemented and evaluated.

The current status is:

> Level 1 is conceptually developed.  
> Level 2 is under formalization.  
> A candidate minimal formulation for Level 3 is introduced below.

The current framework should therefore not be interpreted as a completed mathematical dynamical theory.

---

## 14. Typed State Space

For intelligence i:

S_i(t) belongs to S_i

with:

S_i = X_i x F_i x B_i x M_i x V_i x C_i x P_i

The Residual operator can be typed as:

Delta_i : O_j x S_i -> R_i

The internal update operator can be represented as:

Gamma_i^(12DP) : S_i x R_i -> S_i

The notation Gamma^(12DP) is intentionally used to distinguish the internal twelve-process update dynamics from CDP.

A future formalization may attempt to decompose Gamma^(12DP) into individual operators corresponding to the twelve Dynamic Processes.

However, simple sequential composition should not yet be assumed, because the processes may contain loops, recurrence, parallel interaction, or backtracking.

---

## 15. CDP as an Interoperability Layer

The current CDP is represented as:

CDP = {Describe, Translate, Compare, Coordinate, Trace, Recontact}

These functions should not all be assumed to have identical mathematical types.

In particular, Recontact has an inherently temporal character.

It connects previously observed or translated dynamics with later states and renewed contact with Reality.

This means that Recontact should eventually be formalized as a temporally indexed operation rather than as a static translation function.

The exact formal type remains open.

---

## 16. Candidate Two-Intelligence Toy Model

To move toward executable testing, a minimal system with two intelligences A and B can be introduced.

For initial exploration, each intelligence may be reduced to:

S_A(t) = (F_A(t), P_A(t))

S_B(t) = (F_B(t), P_B(t))

A simple candidate update structure is:

F_A(t+1) = F_A(t) + alpha_A * r_A(t)

P_A(t+1) = P_A(t) + beta_A * abs(r_A(t)) - lambda_A * P_A(t)

with analogous equations for B.

A Holding variable may also be introduced:

H_i(t+1) = rho * H_i(t) + abs(r_i(t))

with an update condition such as:

H_i(t) > theta_i

Different values of alpha_A and alpha_B can represent asymmetric sensitivity to Residual.

The candidate model could be used to explore regimes such as:

- Fixed Point
- Oscillation
- Runaway
- Deadlock
- Frame Lock
- Reopening
- Mutual Viability

However:

> **Executable != Validated**

At this stage, these equations constitute a candidate executable formulation.

They have not yet established empirical validity for IDOS.

Any observed regime would depend on model specification and parameterization.

Successful simulation would not by itself validate the broader IDOS architecture.

---

## 17. From Stability to Viability

A further hypothesis concerns the distinction between convergence and continued updateability.

Low Residual does not necessarily imply successful intelligence dynamics.

For example:

Residual -> 0

while:

Possibility Space -> 0

may represent Frame Lock rather than successful adaptation.

This suggests that convergence alone may be an insufficient criterion.

A possible alternative is to consider whether the system remains within a viable or admissible region:

S_i(t) belongs to A_i(t)

while maintaining conditions such as:

P_i(t) > P_min

and a Residual load that remains within a viable range.

This leads to an emerging hypothesis:

> Intelligence may depend not only on reaching stable states, but on preserving the capacity to remain updateable.

At the interaction level, this raises the possibility of:

**Mutually Viable Intelligence Dynamics**

in which directional updateability remains possible across heterogeneous intelligences without requiring convergence to a single frame.

This remains a hypothesis for simulation and empirical testing.

---

## 18. Recursive Revision of IDOS

The self-application principle requires IDOS itself to remain revisable.

However:

> **Recursive Revision != Unrestricted Self-Modification**

The twelve-process architecture and CDP should not change merely because an alternative formulation can be generated.

Revision should require persistent Residual, evidence, comparison, and testing.

Conceptually:

Current Architecture  
-> Residual  
-> Holding  
-> Alternative  
-> Test  
-> Revised Architecture

A provisional representation is:

12DP_(t+1) = Psi_12(12DP_t, Res_12(t), E_t)

CDP_(t+1) = Psi_CDP(CDP_t, Res_CDP(t), E_t)

Meta-level revision should require a higher evidential threshold than ordinary local updating.

Conceptually:

theta_meta > theta_local

This is treated as update governance rather than as a thirteenth canonical process.

---

## 19. Boundary Conditions and Open Problems

The current architecture explicitly recognizes several unresolved problems.

### Residual Overload

Continuous challenge may produce cognitive, computational, or organizational overload.

Limit and Enactment provide provisional closure, but the operational conditions governing appropriate closure remain unresolved.

### Operationalization Gap

X, F, B, M, V, C, and P are theoretical dimensions.

They should not be assumed to be directly or uniquely measurable.

Observable indicators, proxy variables, or latent-state estimation may be required.

### Power Asymmetry

Residual generation does not guarantee Residual recognition or influence.

The architecture must distinguish visibility from effective capacity to produce updating.

### Translation Loss

Cross-frame translation cannot be assumed to preserve semantic structure perfectly.

Translation Residual therefore requires explicit operationalization.

### Protocol Self-Revision

A revisable protocol requires governance conditions preventing arbitrary or unstable self-modification.

### Empirical Validation

The current architecture and candidate toy model remain unvalidated.

Simulation, comparative cases, adversarial testing, and empirical operationalization are required.

---

## 20. Current Research Proposition

The current research proposition of IDOS ver.81 / ver.81+ can be summarized as follows:

> Heterogeneous intelligences may not need to share the same representations, values, ontologies, measurement systems, or verification criteria in order to remain connected.

Instead, they may require a common way to:

- observe update dynamics,
- expose unresolved Residuals,
- preserve translation loss,
- challenge one another across frames,
- recontact Reality,
- and retain the capacity for continued updating.

The architectural shift is therefore:

> **From shared meaning to shared dynamics of update.**

More precisely:

> **Do not standardize meanings and values first. Make the dynamics of updating mutually observable, challengeable, and revisable.**

This suggests a possible architecture for an intelligence ecosystem in which heterogeneous intelligences do not need to become one world in order to remain connected.

---

## 21. Research Status

This document is a working research snapshot.

It does not claim:

- empirical validation,
- universal applicability of the twelve Dynamic Processes,
- completeness of the mathematical formalization,
- proof that the proposed architecture is uniquely necessary,
- or proof that viability is a better criterion than conventional stability.

The purpose of this update is to make the current theoretical structure explicit enough to be:

- criticized,
- compared with alternative theories,
- formalized,
- simulated,
- operationalized,
- falsified,
- and revised.

Future revisions should remain visible as part of the research trajectory rather than being hidden as corrections to a supposedly completed theory.
