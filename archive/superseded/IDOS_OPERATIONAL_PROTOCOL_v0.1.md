# IDOS Operational Protocol v0.1

**Status:** Freeze Candidate  
**Scope:** Minimum operational use of IDOS  
**Dependency:** MASTER_MAP v1.1 / IDOS Purpose and Use — Canonical Definition  
**Constraint:** No new standalone concept or novelty claim.

---

## 1. Purpose

This protocol defines the minimum operational procedure required to use IDOS in a real evolving system.

Its purpose is not to implement the full MASTER_MAP.

Its purpose is to operationalize the canonical Q2:

\[
\boxed{
\textbf{
IDOS is an architecture for governing the conditions
under which evolving heterogeneous systems
remain able to update again.
}
}
\]

Japanese:

\[
\boxed{
\textbf{
IDOSは、変化し続ける異種知性系が
「次も変われる」ための条件を
継続的にGovernするArchitectureである。
}
}
\]

The protocol therefore asks:

\[
\boxed{
\textbf{
今回の変化によって、
次に変われる条件はどう変わったのか？
}
}
\]

---

## 2. Applicability

IDOS should be used when:

\[
Update_t
\rightarrow
\Delta Capacity(Update_{t+1})
\]

is potentially material.

Typical examples include systems in which an intervention may change:

- who can detect change,
- who can decide,
- who can override,
- who can update,
- how Human / AI / Organization are coupled,
- what is measured,
- where the system boundary lies,
- whether alternative update paths remain available.

IDOS is not required for every task.

If the intervention is simple, reversible, transparent, and does not materially affect future updating capability, IDOS may add little or no value.

---

## 3. Minimum Operational Loop

The minimum operational loop is:

\[
\boxed{
Detect
\rightarrow
Preserve
\rightarrow
Update
\rightarrow
Trace
\rightarrow
Recontact
\rightarrow
Reopen
}
\]

This is a compressed operational form of MASTER_MAP v1.1.

It does not replace MASTER_MAP.

---

## 4. Step 1 — Detect

### Question

\[
\boxed{
\textbf{
何を想定し、実際には何が起き、何が違ったか？
}
}
\]

Record:

\[
Expected_t
\]

\[
Observed_t
\]

\[
Difference_t
\]

Difference includes not only failure but also unexpected success.

A positive result may still contain important unexplained change.

### Minimum record

- Expected state
- Observed state
- Meaningful difference

### Pass condition

A meaningful Reality–Expectation difference can be identified and recorded.

---

## 5. Step 2 — Preserve

### Question

\[
\boxed{
\textbf{
まだ説明できないことは何か？
}
}
\]

Classify observed difference as:

\[
Explained
\]

\[
Partially\ Explained
\]

\[
Unresolved
\]

Unresolved difference must not automatically be:

- discarded,
- normalized,
- forced into an existing category,
- treated as noise without review.

Residual / Holding are operationalized here as:

\[
\boxed{
\textbf{
未解決のDifferenceを、未解決のまま残せること
}
}
\]

### Minimum record

- Explained items
- Partially explained items
- Unresolved residuals

### Pass condition

At least one mechanism exists for retaining unresolved observations for later review.

---

## 6. Step 3 — Update

### Question

\[
\boxed{
\textbf{
何を変えたのか？
}
}
\]

IDOS distinguishes output change from updating-structure change.

Possible update targets include:

\[
\{Frame,\ Rule/Role,\ Coupling,\ Boundary,\ Measurement\}
\]

Examples:

- changing the interpretation frame,
- changing decision authority,
- reallocating Human / AI roles,
- changing coupling between systems,
- changing what is considered inside or outside the system,
- changing what is measured and how.

### Minimum record

- Update performed
- Target of update
- Reason for update

### Pass condition

The intervention can be described in terms of what part of the updating structure was changed.

---

## 7. Step 4 — Trace

### Question

\[
\boxed{
\textbf{
その変更によって、
誰の「変われる能力」がどう変わったか？
}
}
\]

Track at least the relevant updating units.

Example:

| Updating Unit | Before | After |
|---|---|---|
| Human | Detection / Judgment / Override | Detection / Judgment / Override |
| AI | Detection / Recommendation / Execution | Detection / Recommendation / Execution |
| Organization | Memory / Coordination / Revision | Memory / Coordination / Revision |

Trace changes in:

- capability,
- authority,
- dependence,
- detection,
- override,
- fallback,
- reconfiguration.

The purpose is not to assume that capability transfer is bad.

The purpose is to make redistribution visible.

### Minimum record

- Which capability moved
- From whom / where
- To whom / where
- What fallback or override remains

### Pass condition

The intervention's effect on the distribution of updating capability can be traced.

---

## 8. Step 5 — Recontact

### Question

\[
\boxed{
\textbf{
変えたあと、Realityでは何が起きたか？
}
}
\]

IDOS must return to actual operation.

The protocol therefore requires:

\[
Update
\rightarrow
Enactment
\rightarrow
Reality'
\]

and then:

\[
Reality'
\rightarrow
Difference'
\]

### Minimum record

- What happened after enactment
- What differed from expectation
- What new evidence appeared

### Pass condition

The updated system is evaluated against external or operational reality rather than only internal consistency.

---

## 9. Step 6 — Reopen

### Question

\[
\boxed{
\textbf{
今回の変化によって、
次の未知の変化に対応する能力はどう変わったか？
}
}
\]

Minimum evaluation:

\[
Future\ Updateability:
\quad
\uparrow,\ \rightarrow,\ \downarrow,\ ?
\]

Assess at least:

1. Can new differences still be detected?
2. Can alternative interpretations still emerge?
3. Does any actor retain the ability to override or revise?
4. Has irreversible dependence materially increased?
5. Is there still a route back to Reality?
6. Can the updating structure itself still be changed?

### Pass condition

The intervention is evaluated not only by current performance but by its effect on the next update.

---

## 10. Minimum IDOS Record

A single operational cycle can be documented with the following six fields.

### 1. Reality / Difference

- What was expected?
- What occurred?
- What differed?

### 2. Residual

- What remains unexplained?
- What should not yet be closed?

### 3. Update

- What was changed?
- Frame / Rule-Role / Coupling / Boundary / Measurement?

### 4. Distribution Change

- Whose capability, authority, dependence, detection, or override changed?

### 5. Reality Recontact

- What happened after the intervention in real operation?

### 6. Next Updateability

\[
\uparrow,\ \rightarrow,\ \downarrow,\ ?
\]

with a short reason.

---

## 11. Core Decision Test

The minimum practical-value test is:

\[
\boxed{
\textbf{
Did IDOS alter the action in order to preserve future updateability?
}
}
\]

Possible outcomes:

### DV+

IDOS changes or adds an action because the intervention affects future updateability.

Example:

\[
Current\ Improvement
\]

becomes:

\[
Current\ Improvement
+
Exception\ Review
+
Override
+
Fallback
+
Reality\ Recontact
\]

### DV0

IDOS produces no materially different action because future updateability is already preserved or unaffected.

\[
Action_{existing}
=
Action_{IDOS}
\]

DV0 is a valid result.

---

## 12. Operational Warning Pattern

A recurring pattern to inspect is:

\[
Optimization
\rightarrow
Path\ Closure
\]

Examples include:

- automation reducing independent human judgment,
- standardization reducing exception detection,
- centralization removing fallback,
- AI recommendation reducing exploration,
- fixed measurement suppressing novelty detection,
- efficiency improvement creating irreversible dependency.

The protocol does not assume that optimization is bad.

It asks:

\[
\boxed{
\textbf{
Did the improvement close a path needed for the next update?
}
}
\]

---

## 13. Non-Goals

This protocol does not attempt to:

- create a universal Future Updateability score,
- fully operationalize every MASTER_MAP element,
- claim standalone novelty for each component,
- replace domain-specific governance,
- prescribe maximum flexibility,
- maximize updateability in all situations,
- define an implementation stack,
- define software architecture,
- define a PoC target.

Those belong to later stages only if required.

---

## 14. Minimum Completion Criteria

A case qualifies as having completed one Minimum IDOS cycle only if all of the following are recorded:

\[
\boxed{
Difference
}
\]

\[
\boxed{
Unresolved\ Residual
}
\]

\[
\boxed{
Updating\ Structure\ Change
}
\]

\[
\boxed{
Distribution\ Change
}
\]

\[
\boxed{
Reality\ Recontact
}
\]

\[
\boxed{
Next\ Updateability
}
\]

If the case stops at current performance or current success, the cycle is incomplete.

---

## 15. Freeze Rule

Until evidence requires revision:

1. This protocol remains subordinate to MASTER_MAP v1.1.
2. It should remain minimal.
3. New conceptual layers should not be added here.
4. Domain-specific details belong in later implementation documents.
5. DV0 and negative cases must be preserved.
6. The core question remains:

\[
\boxed{
\textbf{
変わった結果、次も変われるのか？
}
}
\]

7. The operational purpose remains:

\[
\boxed{
\textbf{
今回の変化によって、
次に変われる条件がどう変わったかを確認し、
必要ならActionを変える。
}
}
\]
