# Case 006 Preregistration v1.0

## Difference-Conditioned Update as a Predictor of Adaptation Under Environmental Change

**Status:** FROZEN BEFORE TEAM-LEVEL POST-OUTCOME ANALYSIS  
**Research program:** Intelligence Dynamics Architecture / IDOS  
**Case:** 006  
**Version:** 1.0  
**Date:** 2026-10-01

---

## 1. Purpose

Case 006 is a deliberately narrow empirical test within the broader IDOS measurement program.

It does **not** test IDOS as a whole.

It does **not** test the full Provisional 12-Process Dynamics Model (12PDM).

It does **not** establish that the operational measure used below is equivalent to the IDOS construct Γ.

The confirmatory question is:

> Does an observable measure of update following a specific difference provide additional out-of-sample predictive information about later adaptation, beyond a simpler measure of general behavioral success?

Formally, the test concerns whether:

\[
P(U \mid D)
\]

contains predictive information beyond a simpler baseline related to:

\[
P(U)
\]

for subsequent adaptation under an environmental change.

---

## 2. Epistemic Status

This study is classified as:

**Pseudo-prospective / quasi-blind validation.**

The underlying experiment and aggregate findings have already been published.

Therefore, this is not a fully prospective experiment.

However, the present hypothesis, operational definitions, exclusion rules, prediction models, evaluation metric, and interpretation rules are frozen before analysis of the team-level POST outcome used in this test.

No claim of full prospective blindness is made.

---

## 3. Dataset

Case 006 uses behavioral data from the Human Versus Artificial Intelligence Process Management Experiment / HyForm engineering design dataset.

Primary behavioral source:

- `Experiment Log.csv`

Additional files may be used only for exploratory analyses unless explicitly specified otherwise.

Post-experiment questionnaires are not used in the confirmatory test.

The experiment contains two sessions:

\[
PRE = Session\ 1
\]

\[
POST = Session\ 2
\]

The transition between Session 1 and Session 2 is treated as the environmental-change boundary:

\[
t^*
\]

---

## 4. Primary Observational Unit

The primary observational unit is:

\[
\boxed{Team}
\]

Individual participants, roles, and process managers are not treated as independent primary observations.

A team is eligible only if the behavioral data required for both PRE and POST analysis are available.

Duplicate behavioral records are not treated as independent teams.

During PRE-analysis data-quality inspection, two team identifiers were found to represent behaviorally duplicated records after removal of identifier fields.

They are therefore treated as one observational unit using a deterministic identifier rule.

The initial data-quality sequence was:

\[
24\ PRE
\rightarrow
23\ PRE+POST
\rightarrow
22\ independent\ candidate\ teams
\]

A further measurement-availability rule described below reduces the expected maximum primary cohort to approximately:

\[
N=21
\]

before application of POST outcome-availability rules.

Final sample size and all exclusions will be reported.

---

## 5. Primary Difference

The primary Difference is an observable failed route-addition attempt.

\[
D_{failure}
\]

is defined only by raw system-recorded actions:

- `ManualPathAdded;RangeTooLong`
- `ManualPathAdded;PayloadConstraint`

No inference about subjective failure recognition, belief, intention, residual, or internal cognitive state is required.

Thus:

\[
D_{failure,t}=1
\]

when either predefined raw event occurs.

---

## 6. Primary Update

A successful route addition occurring within 60 seconds after a failed route attempt is treated as an observable correction.

\[
U_{60s}=1
\]

if a successful `ManualPathAdded` event occurs during:

\[
(t,t+60s]
\]

following \(D_{failure,t}\).

Otherwise:

\[
U_{60s}=0
\]

The primary response window is:

\[
\boxed{h=60\ seconds}
\]

This window was selected using PRE-only response-time structure before inspection of the confirmatory POST outcome.

Sensitivity windows are preregistered as:

\[
h=30s
\]

and

\[
h=120s
\]

These sensitivity analyses will not replace the primary 60-second result.

---

## 7. Difference-Conditioned Update Measure

For team \(i\), define:

\[
G_i=
\frac{
N(U_{60s}=1 \mid D_{failure})
}{
N(D_{failure})
}
\]

Equivalently:

\[
G_i=
P(U_{60s}=1 \mid D_{failure})
\]

at the team level.

A minimum denominator rule is imposed:

\[
\boxed{N(D_{failure})\ge10}
\]

Teams with fewer than 10 observed failed route attempts do not receive a primary \(G_i\) estimate.

This threshold is not claimed to be statistically optimal.

It is a preregistered measurement-quality rule intended to prevent highly unstable estimates such as:

\[
3/3=1.00
\]

from being treated as reliable team-level conditional response measures.

The threshold will not be changed after inspection of POST outcomes.

---

## 8. Relationship Between \(G\) and Γ

This preregistration does **not** assume:

\[
G=\Gamma
\]

The measure \(G\) is an observable difference-conditioned behavioral response measure.

Whether it is a valid operationalization of the broader IDOS selective-update construct Γ remains an open empirical and theoretical question.

A positive result therefore does not constitute validation of Γ.

---

## 9. Primary Baseline

The primary baseline measures general route-success tendency.

For team \(i\):

\[
B_i=
\frac{
N(SuccessfulRouteAddition)
}{
N(AllRouteAdditionAttempts)
}
\]

The central comparison is therefore between:

\[
G_i=P(U_{60s}\mid D_{failure})
\]

and a simpler general behavioral tendency:

\[
B_i
\]

The purpose is to test whether conditioning update behavior on an observable Difference adds predictive information beyond general route success.

---

## 10. Matched Temporal Sensitivity Baseline

A stronger preregistered sensitivity baseline controls for local 60-second behavioral dynamics.

Define:

\[
M_i=
P(
SuccessfulRouteAddition_{(t,t+60s]}
\mid
SuccessfulRouteAddition_t
)
\]

The anchor event itself is not counted as the subsequent successful event.

This measure tests whether any apparent predictive value of \(G_i\) can be explained by general local temporal clustering of route activity rather than by failure-conditioned response.

This is a strong sensitivity analysis and is not the primary success criterion.

---

## 11. POST Adaptation Outcome

The POST session is divided into two fixed windows:

\[
Early = 0-5\ minutes
\]

\[
Late = 15-20\ minutes
\]

For each team, the best observed valid numeric Profit state in each window is calculated:

\[
P_i^{early}
=
\max Profit_{i,t},
\quad
t\in[0,5min)
\]

\[
P_i^{late}
=
\max Profit_{i,t},
\quad
t\in[15,20min]
\]

The primary adaptation outcome is:

\[
\boxed{
A_i=P_i^{late}-P_i^{early}
}
\]

This measures within-POST performance improvement after entry into the changed environment.

If either the Early or Late window contains no valid numeric Profit observation, the primary outcome is considered unavailable for that team.

No zero imputation, window extension, or post-hoc replacement outcome will be used.

All such exclusions will be reported.

---

## 12. Confirmatory Hypothesis

The confirmatory hypothesis is:

\[
\boxed{
H_1:
G_i
\text{ adds out-of-sample predictive information about }
A_i
\text{ beyond }
B_i
}
\]

The baseline model is:

\[
BL:
A_i
=
\beta_0+\beta_1B_i+\epsilon_i
\]

The candidate model is:

\[
PM:
A_i
=
\beta_0+\beta_1B_i+\beta_2G_i+\epsilon_i
\]

No additional predictors will be added to the primary models after POST inspection.

---

## 13. Out-of-Sample Evaluation

Because the expected sample is small, the primary evaluation uses:

**Leave-One-Team-Out cross-validation (LOTO).**

For every eligible team \(i\):

\[
Train_{-i}
\rightarrow
\widehat{A}_i
\]

The primary prediction metric is:

\[
RMSE
=
\sqrt{
\frac{1}{N}
\sum_i
(A_i-\widehat{A}_i)^2
}
\]

Define:

\[
RMSE_{BL}
\]

for the baseline model and:

\[
RMSE_{PM}
\]

for the candidate model.

The primary contrast is:

\[
\boxed{
\Delta RMSE
=
RMSE_{BL}-RMSE_{PM}
}
\]

Therefore:

\[
\Delta RMSE>0
\]

means that adding \(G_i\) reduced out-of-sample prediction error.

---

## 14. Primary Interpretation Rule

Interpretation is frozen before POST outcome analysis.

### If:

\[
\Delta RMSE\le0
\]

the result will be reported as:

**No predictive support for H1 in Case 006.**

The difference-conditioned measure did not improve out-of-sample prediction beyond the primary baseline.

No post-hoc redefinition of \(D\), \(U\), \(G\), the time window, or the primary outcome will convert this result into confirmatory support.

### If:

\[
\Delta RMSE>0
\]

the result will initially be reported as:

**Positive predictive signal.**

This alone will not be described as validation of IDOS, Γ, or the broader measurement architecture.

---

## 15. Stability and Uncertainty

Because the expected sample size is small and LOTO folds have highly overlapping training sets, conventional independent-fold confidence-interval assumptions are not adopted.

Resampling analyses may be used to examine the stability of:

\[
\Delta RMSE
\]

across team compositions.

Such analyses will be explicitly reported as:

**stability / robustness analyses**

rather than treated as conventional independent-sample confidence intervals.

The sign of the preregistered primary:

\[
\Delta RMSE
\]

remains the primary result.

---

## 16. Strong Sensitivity Test

A stronger sensitivity comparison will evaluate:

\[
BL_M:
A_i
=
\beta_0+\beta_1B_i+\beta_2M_i+\epsilon_i
\]

against:

\[
PM_M:
A_i
=
\beta_0+\beta_1B_i+\beta_2M_i+\beta_3G_i+\epsilon_i
\]

Define:

\[
\Delta RMSE_{matched}
=
RMSE_{BL_M}-RMSE_{PM_M}
\]

If:

\[
\Delta RMSE>0
\]

but:

\[
\Delta RMSE_{matched}\le0
\]

the primary positive signal will be interpreted cautiously because local temporal activity dynamics remain a plausible alternative explanation.

If both are positive, the result provides stronger preliminary evidence that failure-conditioned response contains information beyond both general route-success tendency and matched local temporal dynamics.

---

## 17. Confirmatory / Exploratory Firewall

Only the following chain is confirmatory in Case 006:

\[
\boxed{
D_{failure}
\rightarrow
U_{60s}
\rightarrow
G
\rightarrow
A
}
\]

with the preregistered comparison:

\[
A\sim B
\]

versus:

\[
A\sim B+G
\]

The following are explicitly exploratory in Case 006:

- Process-manager interventions
- Human versus AI process-manager differences
- Communication dynamics
- Cross-unit propagation
- Possibility Space
- Trajectory structure
- Relational Updating Units
- Boundary change
- Frame change
- Measurement-system change
- Full 12PDM mapping
- Other Difference classes
- Other Update classes

Positive exploratory findings will not be used to relabel a negative primary result as confirmatory success.

---

## 18. Falsification Consequence

A negative Case 006 result does not falsify IDOS as a whole.

However, it does count against the specific measurement hypothesis tested here.

If:

\[
\Delta RMSE\le0
\]

then the claim that this operationalization of difference-conditioned update provides incremental predictive information must be downgraded.

The result will not be rescued by changing the operationalization after outcome inspection.

Possible future revisions must be tested on a separate case or dataset.

---

## 19. What Case 006 Cannot Establish

Even a positive result cannot establish that:

- IDOS is validated;
- the 12PDM is validated;
- \(G\) is identical to Γ;
- intelligence itself has been measured;
- difference-conditioned update is universally predictive;
- the result generalizes beyond this task or dataset;
- IDOS outperforms all alternative theories.

At most, a positive result can provide preliminary evidence that an observable difference-conditioned update measure contains incremental predictive information about adaptation in this specific environment.

---

## 20. Freeze Boundary

This document defines the confirmatory analysis before inspection of the team-level POST outcome used for Case 006.

After this document is frozen:

1. the primary Difference definition will not change;
2. the primary Update definition will not change;
3. the 60-second window will not change;
4. the minimum-denominator rule will not change;
5. the primary outcome will not change;
6. the primary baseline and candidate models will not change;
7. the primary evaluation metric will not change;
8. negative results will not be converted into confirmatory success through exploratory analyses.

Any subsequent deviation must be documented explicitly as a deviation from preregistration.

---

## 21. Research Logic

The intended sequence is:

\[
Raw\ Data
\rightarrow
Observable\ Difference
\rightarrow
Observable\ Update
\rightarrow
Conditional\ Measurement
\rightarrow
Frozen\ Prediction\ Rule
\rightarrow
Unseen\ POST\ Outcome
\rightarrow
Out\text{-}of\text{-}Sample\ Evaluation
\]

The purpose is not to make IDOS fit the dataset.

The purpose is to expose a small IDOS-derived measurement hypothesis to a result that can fail.

---

Freeze status: FROZEN before Case 006 team-level POST outcome analysis.
