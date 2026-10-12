# Case 006 Results v1.0

## Difference-Conditioned Update Did Not Improve Primary Out-of-Sample Prediction of Adaptation

**Research program:** Intelligence Dynamics Architecture / IDOS  
**Case:** 006  
**Version:** 1.0  
**Date:** 2026-10-01  
**Status:** CONFIRMATORY RESULT — PRIMARY HYPOTHESIS NOT SUPPORTED  
**Preregistration:** `CASE_006_PREREGISTRATION_v1.0.md`  
**Preregistration freeze commit:** `dae4b07`

---

## 1. Purpose

This document reports the confirmatory result of Case 006.

The analysis was conducted after freezing the Case 006 preregistration and before making any changes to the preregistered primary definitions.

The purpose of Case 006 was deliberately narrow.

It did not test IDOS as a whole.

It did not test the full Provisional 12-Process Dynamics Model (12PDM).

It did not assume that the operational measure used here was equivalent to the broader IDOS construct Γ.

The preregistered question was:

> Does an observable measure of update following a specific difference provide additional out-of-sample predictive information about later adaptation, beyond a simpler measure of general behavioral success?

The tested measurement hypothesis can be summarized as:

\[
P(U \mid D)
\]

versus a simpler baseline related to general behavioral tendency.

---

## 2. Preregistration Boundary

The confirmatory analysis was frozen before inspection of the team-level POST outcome used in Case 006.

The preregistration was committed as:

`dae4b07`

with the status:

**FROZEN BEFORE TEAM-LEVEL POST-OUTCOME ANALYSIS**

The following primary elements were therefore fixed before POST evaluation:

1. observational unit;
2. PRE / POST boundary;
3. Difference definition;
4. Update definition;
5. 60-second response window;
6. minimum-denominator rule;
7. primary predictor;
8. baseline;
9. POST adaptation outcome;
10. predictive models;
11. Leave-One-Team-Out evaluation;
12. RMSE metric;
13. interpretation rule.

No primary definition was changed after observing the confirmatory POST result.

---

## 3. Primary Measurement

### 3.1 Difference

The preregistered observable Difference was a failed route-addition attempt:

- `ManualPathAdded;RangeTooLong`
- `ManualPathAdded;PayloadConstraint`

This was denoted:

\[
D_{failure}
\]

No subjective belief, intention, Residual, Frame, or internal cognitive state was inferred.

---

### 3.2 Update

An observable correction was defined as a successful `ManualPathAdded` event occurring within 60 seconds after the failed attempt.

\[
U_{60s}=1
\]

if such an event occurred during:

\[
(t,t+60s]
\]

Otherwise:

\[
U_{60s}=0
\]

---

### 3.3 Difference-conditioned measure

For team \(i\):

\[
G_i=
P(U_{60s}=1 \mid D_{failure})
\]

operationalized as:

\[
G_i=
\frac{
N(\text{failed attempts followed by successful correction within 60s})
}{
N(\text{failed route attempts})
}
\]

The preregistered minimum-denominator rule was:

\[
N(D_{failure})\ge10
\]

---

## 4. Baseline

The primary baseline measured general route-success tendency:

\[
B_i=
\frac{
N(\text{successful route additions})
}{
N(\text{all route-addition attempts})
}
\]

The confirmatory question was therefore not whether \(G_i\) correlated with later performance in isolation.

It was whether \(G_i\) added predictive information beyond \(B_i\).

---

## 5. POST Adaptation Outcome

The preregistered POST outcome was:

\[
A_i=P_i^{late}-P_i^{early}
\]

where:

\[
P_i^{early}
=
\max Profit_{i,t},
\quad
t\in[0,5min)
\]

and:

\[
P_i^{late}
=
\max Profit_{i,t},
\quad
t\in[15,20min]
\]

Thus, the outcome measured improvement within the changed POST environment rather than absolute final performance alone.

---

## 6. Final Primary Sample

The preregistered data-quality and eligibility rules were applied before primary modeling.

The expected maximum primary cohort after PRE-side eligibility filtering was approximately:

\[
N=21
\]

One additional team, `Team_AI_11`, had no valid Profit observation in the preregistered Late POST window.

Under the preregistered missing-outcome rule, that team was excluded from the primary analysis.

The final confirmatory sample was therefore:

\[
\boxed{N=20}
\]

No outcome window was extended and no missing value was imputed.

---

## 7. Confirmatory Models

The preregistered baseline model was:

\[
BL:
A_i=
\beta_0+\beta_1B_i+\epsilon_i
\]

The preregistered candidate model was:

\[
PM:
A_i=
\beta_0+\beta_1B_i+\beta_2G_i+\epsilon_i
\]

Both models were evaluated using:

**Leave-One-Team-Out cross-validation (LOTO).**

The primary metric was:

\[
RMSE=
\sqrt{
\frac{1}{N}
\sum_i
(A_i-\widehat A_i)^2
}
\]

The preregistered primary contrast was:

\[
\Delta RMSE
=
RMSE_{BL}-RMSE_{PM}
\]

A positive value would indicate improved out-of-sample prediction after adding \(G_i\).

---

## 8. Primary Result

The baseline model produced:

\[
\boxed{
RMSE_{BL}=1116.96
}
\]

The candidate model including the difference-conditioned measure produced:

\[
\boxed{
RMSE_{PM}=1218.79
}
\]

Therefore:

\[
\Delta RMSE
=
1116.96-1218.79
\]

\[
\boxed{
\Delta RMSE=-101.82
}
\]

Adding \(G_i\) increased rather than reduced out-of-sample prediction error.

Under the preregistered interpretation rule:

\[
\Delta RMSE\le0
\]

is classified as:

\[
\boxed{\text{No predictive support}}
\]

Accordingly:

> **The primary hypothesis of Case 006 was not supported.**

---

## 9. Confirmatory Interpretation

Within this dataset, operationalization, outcome definition, and prediction setting, the difference-conditioned update measure:

\[
P(U_{60s}\mid D_{failure})
\]

did not provide incremental out-of-sample predictive value beyond general route-success tendency.

The result therefore does not support the specific Case 006 measurement hypothesis that this operationalization of Difference-conditioned Update improves prediction of subsequent adaptation.

The result is not reinterpreted as confirmatory success using alternative windows, outcomes, Difference classes, or exploratory variables.

---

## 10. Strong Matched Sensitivity Analysis

The preregistration also specified a stronger temporal sensitivity baseline:

\[
M_i=
P(
SuccessfulRouteAddition_{(t,t+60s]}
\mid
SuccessfulRouteAddition_t
)
\]

This controls, in part, for local 60-second temporal clustering of route activity.

One additional team lacked the events required to define \(M_i\), resulting in:

\[
N=19
\]

for this sensitivity analysis.

The matched baseline model:

\[
BL_M:
A_i\sim B_i+M_i
\]

produced:

\[
RMSE_{BL_M}=1343.61
\]

The matched candidate model:

\[
PM_M:
A_i\sim B_i+M_i+G_i
\]

produced:

\[
RMSE_{PM_M}=1306.34
\]

Therefore:

\[
\boxed{
\Delta RMSE_{matched}
=
1343.61-1306.34
=
+37.27
}
\]

This is a positive sensitivity signal.

However, it does **not** alter the preregistered confirmatory conclusion.

The primary result remains:

\[
\boxed{
\Delta RMSE=-101.82
}
\]

and therefore:

\[
\boxed{\text{Primary H1 not supported}}
\]

The matched result is retained as a secondary robustness / sensitivity observation requiring independent follow-up.

---

## 11. What Failed

The result does not imply that adaptation is unrelated to prior behavior.

More specifically, it shows that the tested operationalization:

\[
G_i=P(U_{60s}\mid D_{failure})
\]

did not improve primary out-of-sample prediction beyond the preregistered baseline.

Thus, the following narrower claim did not receive predictive support:

> Measuring whether a team corrects a failed route attempt within 60 seconds provides incremental predictive information about its later adaptation beyond its general route-success tendency.

This is the claim that Case 006 was designed to expose to failure.

It failed that test.

---

## 12. What Did Not Fail

The negative result does not by itself falsify:

- IDOS as a whole;
- the Provisional 12-Process Dynamics Model;
- the existence of selective updating;
- the broader concept of Γ;
- dynamic measurement of intelligence;
- relational Updating Units;
- Possibility Space;
- Trajectory;
- cross-unit propagation;
- changing Boundary, Frame, or Measurement systems.

Those constructs were not the confirmatory target of Case 006.

They therefore cannot be claimed as supported or refuted by this result.

---

## 13. Implication for Γ

Case 006 deliberately avoided assuming:

\[
G=\Gamma
\]

The negative result reinforces the importance of maintaining that distinction.

The tested quantity was a one-dimensional conditional behavioral rate:

\[
P(U\mid D)
\]

whereas the broader candidate selective-update formulation in IDOS may depend on additional state and context:

\[
\Gamma_i(D_t,K_t,P_t)
\]

Case 006 does not establish that a richer Γ formulation would perform better.

That possibility is a new hypothesis and must not be used to rescue Case 006 retrospectively.

If investigated, it must be tested prospectively or pseudo-prospectively in a subsequent case.

---

## 14. Methodological Lesson

Case 006 provides an important methodological constraint for the IDOS measurement program.

A conceptually plausible mapping:

\[
Difference
\rightarrow
Update
\rightarrow
Adaptation
\]

is not sufficient.

Even when Difference and Update can be operationalized directly from behavioral logs, the resulting measurement must demonstrate incremental value against simpler baselines.

In this case, it did not.

This supports a stricter development rule:

\[
\boxed{
Conceptual\ coherence
\neq
Measurement\ value
\neq
Predictive\ value
}
\]

These levels must remain separate.

---

## 15. Status of Case 006

The confirmatory status of Case 006 is:

\[
\boxed{\text{NEGATIVE}}
\]

More precisely:

**The preregistered primary hypothesis was not supported.**

The result is retained as part of the IDOS research trajectory rather than removed, reframed, or optimized away.

Any subsequent analysis of:

- alternative response windows;
- alternative Difference classes;
- alternative adaptation outcomes;
- process-manager interventions;
- Human versus AI management;
- communication dynamics;
- Possibility Space;
- Trajectory;
- cross-unit propagation;
- richer Γ representations;

will be explicitly labeled:

\[
\boxed{\text{POST-HOC / EXPLORATORY}}
\]

and will not alter the Case 006 confirmatory result.

---

## 16. Next Research Step

Case 006 closes the first preregistered predictive test with a negative primary result.

The next step is not to modify Case 006 until it becomes positive.

Instead, the result creates a new research question:

> Is a one-dimensional Difference-conditioned response rate too compressed to capture the selective-update structure relevant to future adaptation?

One possible future formulation is:

\[
\Gamma_i(D_t,K_t,P_t)
\]

rather than:

\[
P(U\mid D)
\]

However, this remains a hypothesis generated after Case 006.

It must therefore be evaluated in a separate preregistered test.

---

## 17. Research Trajectory

Case 006 represents the following transition:

\[
Conceptual\ Architecture
\rightarrow
Operationalization
\rightarrow
Preregistration
\rightarrow
Prediction
\rightarrow
Reality
\rightarrow
Negative\ Result
\rightarrow
Model\ Revision
\]

The negative result is therefore not removed from the research trajectory.

It becomes part of the evidence constraining the next version of the measurement architecture.

---

**Final Case 006 confirmatory status:**  
**PRIMARY HYPOTHESIS NOT SUPPORTED**

**Primary result:**  
\(RMSE_{BL}=1116.96\)  
\(RMSE_{PM}=1218.79\)  
\(\Delta RMSE=-101.82\)

**Preregistration freeze:** `dae4b07`

**No confirmatory specification was changed after POST outcome inspection.**
