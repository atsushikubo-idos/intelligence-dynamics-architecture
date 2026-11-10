# IDOS Cross-Scale: Unsupervised Latent-State Predictive Audit v1.2

## Scope and scientific status
This **synthetic baseline experiment** extends sequence-pattern selection in v1.1. It does not reproduce chemical formation and does not establish a new IDOS theorem, predictive edge, interpretability, causality, or real-world social connection. It examines whether statistical hidden-state estimation from anonymous event streams can retain information useful for predicting a subsequent outcome.

## Experiment
- A three-state categorical hidden Markov process generates sequences of 12 anonymous observations (six symbols) and a binary next-step relationship-retention proxy. The ground-truth hidden state and its semantics are **not** supplied to fitting code.
- The model fits candidate categorical HMMs with K=2, 3, 4 hidden states using expectation-maximization; K is selected exclusively by validation **observation likelihood**, not test outcomes. Each candidate uses two random restarts and 32 EM iterations. Ground-truth K=3 is not required as an input to the learner.
- A supervised classifier then uses the HMM's filtered end-of-sequence posterior to predict the outcome; this is **not fully unsupervised outcome prediction**. The HMM is unsupervised, its outcome calibration is supervised.
- Standard logistic baselines see the same observations, including last event, frequency counts, last three events, and combined features. This is a baseline-method audit, **not an IDOS versus non-IDOS trial**.
- Training: 1,200 episodes; validation: 400; independent held-out test: 400. A second synthetic regime changes only the mapping from hidden state to outcome: 180 labeled episodes calibrate classifiers; a separate 620 episodes measure performance. The same labeled calibration budget is used for each method.
- The unknown latent state oracle is printed only as an unattainable reference.

## Results (Brier score; lower is better)
| Representation | Held-out normal | Changed regime, frozen | Changed regime, recalibrated (180 labels) |
|---|---:|---:|---:|
| Last symbol | 0.184378 | 0.397652 | 0.224359 |
| Bag/counts | 0.231437 | 0.301807 | 0.252296 |
| Last 3 symbols | 0.177916 | 0.427044 | 0.227654 |
| Counts + last 3 | 0.179101 | 0.425978 | 0.230944 |
| Unsupervised HMM filter + logistic calibration | **0.172864** | **0.429819** | **0.216308** |

Validation log likelihood per sequence: K=2: -19.857078; K=3: -19.592442; K=4: -19.593462. This particular sample selects K=3, but state-count selection is unstable in general and K is not uniquely identifiable. Unattainable true-hidden-state oracle Brier score: 0.127150. Shuffling symbol order destroys much of the HMM's predictive signal (Brier 0.259257 versus 0.172864), which is consistent with useful temporal structure in this constructed data.

## Interpretation and limitations
1. The synthetic generator is itself an HMM. This favors a correctly specified HMM baseline and cannot be generalized to arbitrary human/AI/organizational event streams.
2. The fitted hidden-state labels are not necessarily the generator's original labels, much less provenance, meaningful agreements, consent, or refusal. State-label permutation and model non-identifiability matter.
3. A meaningful predictive state can be learned without semantic event annotations **under the assumptions of this experiment**, but it does not establish causal state discovery or novel reference-frame construction.
4. Under regime shift, the fixed posterior-outcome mapping becomes unreliable. Recalibration improves outcomes but uses new **labeled** data and does **not** automatically detect the change or rediscover the representation.
5. Retaining all raw history is not needed by the fitted HMM for its prediction; this follows from its Markov assumptions, and is not a universal claim about real-life provenance preservation.
6. Comparisons are deterministic on a chosen simulation seed. Broader statistical confidence intervals, non-HMM generators, regime changes in observation emissions, intervention evaluation, and multiple independent populations remain needed.

## Connection to IDOS (hypotheses, not results)
The filtered posterior is a candidate operational analogue of a compact predictive reference state, rather than a representation of autonomy or the 12CDP framework. Additional experiments must ask whether agency-specific frames, consent/refusal, CFV/MU, provenance, and Reopening improve decision quality or future updateability **relative to fair full-history and adaptive baselines**. No IDOS-specific benefit has been demonstrated.

## Reproduce
From this directory with NumPy, SciPy, scikit-learn installed:

```bash
OPENBLAS_NUM_THREADS=1 python latent_state_audit_v12.py > results_v12.json
OPENBLAS_NUM_THREADS=1 python -m unittest -q test_latent_state_audit_v12.py
```

The code uses fixed seeds and no real personal or organizational data. The model does not import or change the production Social Connection Architecture. It adds files alongside v0.9–v1.1, without any repository-root file.
