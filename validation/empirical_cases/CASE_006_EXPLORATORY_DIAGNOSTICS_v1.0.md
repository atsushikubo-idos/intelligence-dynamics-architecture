# Case 006 Exploratory Diagnostics v1.0

## Post-Hoc Failure Analysis and Measurement Revision

**Status:** POST-HOC / EXPLORATORY  
**Date:** 2026-10-01  
**Case:** 006 — Human Versus Artificial Intelligence Process Management Experiment

> This document does not modify, reinterpret, or rescue the preregistered Case 006 result.

The preregistered primary result remains:

\[
\boxed{\text{PRIMARY H1 NOT SUPPORTED}}
\]

Preregistration freeze commit:

`dae4b07`

Confirmatory results commit:

`0f790a2`

---

# 1. Purpose

Case 006 tested whether an observable Difference-conditioned response measure,

\[
G_i=P(U_{60s}=1\mid D_{failure}),
\]

provided additional out-of-sample predictive information about later adaptation beyond a simpler general behavioral-success baseline.

The preregistered comparison produced:

\[
RMSE_{BL}=1116.96
\]

\[
RMSE_{PM}=1218.79
\]

\[
\Delta RMSE=-101.82
\]

Therefore the preregistered hypothesis was not supported.

The purpose of this document is not to search for an alternative positive result.

Instead, it asks:

> What can the negative result teach us about the measurement architecture?

All analyses below were conducted after the confirmatory result was known.

They are therefore exploratory and hypothesis-generating only.

---

# 2. Diagnostic Question 1 — Was \(G\) simply non-discriminative?

No simple ceiling explanation was sufficient.

Among teams satisfying the preregistered denominator criterion, \(G\) showed substantial between-team variation.

Approximately:

\[
\min(G)\approx0
\]

\[
median(G)\approx0.76
\]

\[
\max(G)\approx0.98
\]

Thus the negative primary result cannot be explained simply by all teams having approximately identical values of \(G\).

However, \(G\) was substantially associated with the general route-success baseline \(B\):

\[
Corr(G,B)\approx0.62
\]

and was also associated with local behavioral dynamics.

This suggests that \(G\) may combine multiple components:

\[
G
\approx
GeneralBehavioralSuccess
+
LocalDynamics
+
DifferenceConditionedComponent.
\]

Therefore:

\[
\boxed{
G\neq B
}
\]

but also:

\[
\boxed{
G\text{ does not cleanly isolate Difference-specific Update.}
}
\]

**Diagnostic status:** plausible measurement limitation.

---

# 3. Diagnostic Question 2 — Was the POST outcome simply broken?

The preregistered outcome was:

\[
A_i=P_i^{late}-P_i^{early}.
\]

There was substantial between-team variation in \(A\), and the late-window formulation did not simply discard earlier best solutions.

However, further inspection showed an important limitation.

Because:

\[
A=L-E,
\]

the outcome is mechanically related to the starting level \(E\).

Exploratory analysis indicated a substantial negative association between early performance and measured improvement.

Therefore:

\[
\boxed{
PerformanceImprovement
\neq
Adaptation
}
\]

in the strong theoretical sense.

The preregistered outcome remains valid for the preregistered test, but future experiments should distinguish:

- initial performance,
- headroom for improvement,
- response latency,
- exploration,
- reconfiguration,
- recovery,
- and final performance.

**Diagnostic status:** the outcome is not invalid, but it is an incomplete measure of adaptation.

---

# 4. Diagnostic Question 3 — Would simpler behavioral predictors have solved the problem?

Exploratory comparisons considered simpler PRE-session predictors such as:

- activity,
- failure rate,
- general route-success rate,
- PRE performance,
- and local temporal dynamics.

None showed strong out-of-sample prediction of the preregistered POST improvement outcome.

A null model using no behavioral predictor performed competitively with, and in exploratory comparisons better than, several individual PRE behavioral measures.

Therefore the Case 006 failure cannot currently be reduced to:

> “The IDOS-derived measure failed because a simple conventional behavioral score was sufficient.”

A stronger competing explanation remains:

\[
\boxed{
PRE\ trait
\not\Rightarrow
POST\ adaptation
}
\]

or, more cautiously:

> Stable PRE-session behavioral summaries may contain limited information about the later adaptation outcome used in Case 006.

**Diagnostic status:** plausible competing explanation.

---

# 5. Diagnostic Question 4 — Is adaptation better represented as a trajectory?

Exploratory Session 2 analysis showed temporal differences in behavior associated with later performance improvement.

Some variation appeared in:

- early evaluation behavior,
- early reconfiguration,
- late reconfiguration,
- and the timing of behavioral changes.

This motivated the post-hoc hypothesis:

\[
\boxed{
Adaptation\ may\ emerge\ in\ the\ transition\ process
rather\ than\ exist\ as\ a\ stable\ pre-existing\ trait.
}
\]

However, this hypothesis was generated after inspecting the outcome.

It therefore receives no confirmatory evidential status from Case 006.

**Diagnostic status:** Candidate B — coherent and potentially testable, but unconfirmed.

---

# 6. Diagnostic Question 5 — Does a simple transition sequence explain adaptation?

A candidate sequence was examined:

\[
Evaluation
\rightarrow
Reconfiguration
\rightarrow
PerformanceChange.
\]

Evaluation was frequently followed by reconfiguration.

However, reconfiguration was also extremely frequent after non-evaluation events.

Exploratory estimates were approximately:

\[
P(R_{60}\mid Evaluation)\approx0.981
\]

\[
P(R_{60}\mid NonEvaluation)\approx0.986
\]

giving:

\[
\Delta P
=
P(R_{60}\mid Evaluation)
-
P(R_{60}\mid NonEvaluation)
\approx-0.005.
\]

Therefore the high absolute conditional probability did not identify an Evaluation-specific transition.

The simple three-stage trajectory explanation was not strongly supported.

**Diagnostic status:** weak / Candidate C for this specific operationalization.

---

# 7. Central Measurement Failure

The most important methodological result of the exploratory diagnostics is:

\[
\boxed{
P(U\mid D)
\neq
DifferenceSpecificUpdate
}
\]

in general.

A high conditional response probability is insufficient when the same response is already highly probable under other conditions.

For example:

\[
P(U\mid D)=0.95
\]

provides little evidence of Difference-specific responsiveness if:

\[
P(U\mid D_0)=0.94.
\]

Case 006 therefore reveals a discrimination problem in the original measurement logic.

The original measure:

\[
G=P(U\mid D)
\]

captures absolute conditional response frequency.

It does not necessarily isolate the component of Update attributable specifically to the Difference.

---

# 8. Measurement Revision

Future IDOS measurement should distinguish:

\[
\text{Absolute Conditional Response}
\]

from:

\[
\text{Difference-Specific Response}.
\]

A candidate differential measure is:

\[
\Gamma_i^{\Delta}
=
P(U\mid D,K,P,i)
-
P(U\mid D_0,K,P,i),
\]

where \(D_0\) is an appropriate matched or control condition.

Another candidate formulation is conditional information:

\[
\Gamma_i^{IG}
=
I(D;U\mid K,P,i).
\]

These formulations are NOT validated IDOS measures.

They are post-Case-006 candidate measurement revisions.

Their purpose is to prevent a generally high update rate from being misclassified as high Difference-specific responsiveness.

---

# 9. Revised Measurement Principle

Case 006 motivates the following provisional measurement principle:

\[
\boxed{
Conditional\ Frequency
\neq
Selective\ Update
}
\]

A stronger measurement design requires comparison against an appropriate alternative or matched condition:

\[
\boxed{
P(U\mid D)
\quad vs.\quad
P(U\mid D_0)
}
\]

rather than interpreting \(P(U\mid D)\) alone.

More generally:

\[
\boxed{
Observed\ co-occurrence
\neq
Difference-specific\ information.
}
\]

This is a measurement revision, not evidence that the broader IDOS architecture is correct.

---

# 10. What Case 006 Does Not Establish

Case 006 does NOT establish that:

- IDOS is empirically validated;
- the 12PDM is empirically validated;
- \(\Gamma^\Delta\) is the correct measure of selective update;
- trajectory-based measurement is superior;
- adaptation is necessarily generated rather than trait-like;
- Difference causes Update;
- relational Updating Units are required;
- Possibility Space is empirically necessary;
- Boundary, Frame, or Measurement-system updates are empirically demonstrated.

These remain separate hypotheses.

---

# 11. What Case 006 Does Establish Methodologically

Within the scope of this experiment:

1. The preregistered \(G\) measure did not improve primary out-of-sample prediction.

2. The negative result should not be rescued by selecting alternative outcomes or windows after inspection.

3. Absolute conditional response frequency does not by itself establish Difference-specific responsiveness.

4. High-frequency behavior requires an explicit comparison condition.

5. Static PRE summaries may be insufficient for predicting the selected POST adaptation outcome.

6. Dynamic transition hypotheses require direct transition-specific baselines rather than high absolute sequence frequencies.

7. Future measurement should separate:
   - general activity,
   - general success,
   - Difference-conditioned response,
   - Difference-specific incremental response,
   - and subsequent trajectory change.

---

# 12. Research Update

The measurement trajectory after Case 006 is therefore:

\[
\boxed{
P(U\mid D)
\rightarrow
MatchedDifferentialResponse
\rightarrow
TransitionSpecificity
\rightarrow
IndependentValidation
}
\]

rather than:

\[
\boxed{
NegativeResult
\rightarrow
MoreComplexIDOSExplanation.
}
\]

This distinction is essential.

The objective is not to preserve the theory.

The objective is to improve the measurement architecture under contact with negative evidence.

---

# 13. Implication for the Next Independent Test

A future independent test should preregister, before outcome inspection:

1. the Difference \(D\);
2. an explicit matched/control condition \(D_0\);
3. the observable Update \(U\);
4. the observation horizon;
5. the Updating Unit;
6. the context variables allowed in matching;
7. the differential measure;
8. the adaptation outcome;
9. the baseline models;
10. the falsification criterion.

A minimal candidate comparison is:

\[
\Gamma^\Delta
=
P(U\mid D)-P(U\mid D_0).
\]

The next experiment should test whether this differential quantity has incremental measurement or predictive value.

If it does not, the selective-update hypothesis should be weakened or revised rather than protected by additional conceptual complexity.

---

# 14. Frozen Conclusion

Case 006 remains a negative confirmatory result.

Its principal value is methodological.

The experiment exposed a weakness in the first operationalization of Difference-conditioned Update:

\[
\boxed{
P(U\mid D)
\text{ alone cannot distinguish selective responsiveness from generally frequent updating.}
}
\]

The resulting measurement revision is:

\[
\boxed{
Absolute\ Conditional\ Response
\rightarrow
Differential / Matched\ Response.
}
\]

This revision is a hypothesis generated by failure.

It requires independent preregistered validation.

---

**Status:** POST-HOC / EXPLORATORY — FROZEN AFTER CASE 006 CONFIRMATORY RESULT

**Case 006 confirmatory conclusion remains unchanged: PRIMARY H1 NOT SUPPORTED.**
