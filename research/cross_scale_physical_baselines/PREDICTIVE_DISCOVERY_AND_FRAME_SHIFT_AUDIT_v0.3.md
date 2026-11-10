# IDOS Cross-Scale Predictive Discovery and Frame-Shift Audit v0.3

## Status and scope

Synthetic **methodological control**, not an IDOS-specific algorithm, quantum-chemical simulation, empirical social-science result, or an implemented CFV/MU metric. It extends the direction of the existing v0.1 physical baselines and v0.2 predictive sufficiency audit without modifying them.

**Question:** Can prediction-relevant distinctions be learned from partial observations, and do learned distinctions remain trustworthy if the observation semantics change?

## Mechanistic generator

Three latent blocks A, B, Y reproduce the block transitions of the v0.2 six-microstate baseline: A→(A,B,Y)=(.05,.05,.90), B→(.05,.85,.10), Y→(.25,.25,.50). An observable macro label is X for latent A/B and Y for latent Y. A noisy observable, *provenance-like* tag, signals `a` or `b` with 80% accuracy conditional on A/B; in Y it is `N`. The actual latent block and true rates are **not used in model fitting**. The experimenter nonetheless specifies the generator in advance; this is not discovery of unknown chemistry.

Train, validation, test and shift datasets are independently generated trajectories with separate fixed random seeds (16,000, 5,000, 7,000 and 7,000 observations). Features at time t use only time t and t−1 observations; target is whether the macro observation at t+1 equals Y. Train data only determine model parameters; validation chooses the clustering radius; test is held out. All scores are one-step binary Brier scores, lower is better.

## Conventional, information-matched controls

- Current macro category only.
- Current and previous macro categories.
- Current macro and noisy observable tag.
- Full available observable context: current/previous macro and current/previous tag.
- Predictive clustering of those same full observable contexts: cluster empirical one-step probability estimates, with clustering radius selected on validation (0, .015, .03, .06, .1, .2, .4, 1.0). This is **not** causal-state reconstruction or proof of minimal sufficient representation.
- Existing online count-model baseline over full observed context with a trailing 600-observation window, updating only after each target becomes available. It receives the same feature information. Evaluation is prequential: predict, then observe, then update.

The optional latent oracle reference uses hidden labels and known generator probabilities, and is not treated as a fair model comparison.

## Results (seed 2026; Brier ↓)

| Observational method | In-distribution test | Shifted tag semantics test |
| --- | ---: | ---: |
| Current macro | 0.2014868 | 0.2050068 |
| Macro + previous macro | 0.1883406 | 0.1900648 |
| Current macro + tag | 0.1884218 | 0.2597029 |
| Full observed current + history + tag | 0.1766102 | 0.2325830 |
| Learned one-step predictive grouping (same inputs) | 0.1765504 | 0.2333060 |
| Online recent-window full observed model | 0.1794777 | 0.1831213 |

Learned groups select radius 0.015 on validation, yielding **6 clusters from 9 observed contexts**; observed class entropy on the training sample is 2.21751 bits. This is **not** an efficiency theorem: 9 contexts are already simple and the full-context baseline predicts almost identically (0.1766102 vs 0.1765504). The observed improvement is far too small to attribute distinctive value to the grouping.

Under shifted conditions the observation instrument's `a`/`b` meanings invert while latent dynamics remain the same. This is deliberately a severe sensor-semantics shift. Fixed tag-aware models degrade sharply; online retraining responds and achieves a lower shifted-test Brier. Unlike fixed predictors, the online evaluation is permitted to incorporate previous **test-period outcomes**; this is an explicitly different, streaming operational setting, not a head-to-head static held-out test. More formally matched online controls would be needed for claims of method superiority.

## What was learned

1. Additional observable context can improve future-event predictions under stable semantics; this is predicted by conventional information/statistical models.
2. A learned predictive grouping can compress empirical observation contexts **without being supplied the latent state partition**. It does not show recovery of *true* causal states.
3. A meaning shift of metadata can invalidate previously useful predictive representations.
4. Ordinary online recency-weighted adaptation can mitigate that shift. There is **no demonstrated IDOS advantage** and no uniquely IDOS-specific module in this audit.
5. The audit suggests a testable IDOS requirement: retain the provenance and version of reference frames, monitor predictive calibration under drift, and reopen a representation when performance deteriorates. Those functions are proposals for a later integration test, **not implementation claims**.

## Explicit nonclaims

- No real atoms, molecules, quantum binding energies, or chemical laboratory data are simulated.
- `a` and `b` are noisy model-generated markers, not genuine documentary provenance or participant identities.
- No autonomous reference-frame creation, objective causal discovery, formal validation of future updateability, or consent/CFV/MU mechanism was tested.
- This is one toy generator and one evaluation seed. No statistical confidence intervals or robustness across several generator families yet.
- A full-history comparator can always match the prediction from a deterministic summary if it has the same information, adequate model capacity, and data; compression offers potential resource or interpretability gains, not fundamental information advantage.

## Reproduction

No third-party dependencies. From repository root:

```bash
python research/cross_scale_physical_baselines/predictive_discovery_v03.py
python -m unittest discover -s research/cross_scale_physical_baselines -p 'test_predictive_discovery_v03.py' -v
```

The checked-in `predictive_discovery_results_v03.json` is generated by the script with defaults and is intended to be compared with its printed JSON. Existing v0.1/v0.2 files are untouched. The repository root receives no additional module-specific instructions.

## Scientific lineage

- Shalizi and Crutchfield, *Computational Mechanics: Pattern and Prediction, Structure and Simplicity* (2001). https://csc.ucdavis.edu/~cmg/papers/cmppss.pdf
- MacDonald, *A coarse-grained Markov chain is a hidden Markov model* (2020). https://www.sciencedirect.com/science/article/pii/S0378437119320424
- Buchholz, *Exact and ordinary lumpability in finite Markov chains* (1994). https://doi.org/10.2307/3215235

The cited theory predates IDOS and is not claimed as its original mathematical discovery.
