# IDOS Cross-Scale Predictive Sufficiency Audit v0.2

Date: 2026-11-11. Status: **synthetic, exact-probability research control, no IDOS-specific advantage demonstrated**.

## Aim

Test whether a coarse relational summary can discard next-step predictive information, and whether a *specified* compact refinement can retain the same future-prediction information as a full microstate in a finite first-order Markov system. This extends the independent physical-baseline v0.1 coarse-graining example with an exact quantitative comparison, rather than treating physical analogies as IDOS laws.

**Neither atoms nor real interpersonal relationships are simulated.** `refined` is an **oracle partition constructed from transition probabilities**; it is not a validated operational measure of provenance, consent, autonomy, CFV or MU.

## Model and protocol

- Six microstates (`a1, a2, b1, b2, c1, c2`) with an explicit stochastic transition matrix P recorded in the JSON results; all rows sum to 1.
- Macro reference frame: `X={a1,a2,b1,b2}`, `Y={c1,c2}` (2 groups).
- Refined *proxy* reference frame: `A={a1,a2}`, `B={b1,b2}`, `Y={c1,c2}` (3 groups).
- Full observed microstate: six groups (6 groups). Under first-order Markov dynamics, complete *observed microstate history* cannot beat the current full microstate for future prediction.
- The probability of moving to Y in one time step equals .90 from A, .10 from B, and .50 from Y. Each individual microstate has different within-group transition allocations; nevertheless the refined partition is **strongly lumpable** under the classic Kemeny-Snell criterion. The coarse macro partition is **not** strongly lumpable.
- An exact stationary distribution is computed, then the Bayes-optimal conditional probability forecast `P(Z_{t+n}=Y | representation at t)` is evaluated at horizons n=1,2,3. No fitted prediction rules or sampling fluctuations.
- Report the expected Brier score (lower is better); `H(Z_{t+n}|representation)` in bits (lower is better); and representation entropy `H(representation)` in bits (a complexity proxy, **not** an implementation bit cost).
- Additional baseline: one previous observed macrostate plus current macrostate; forecasts are computed using the exact stationary joint distribution.

## Reproducible results

| Representation | States | H(rep), bits | n=1 Brier score | H(next Y\|rep), bits |
|---|---:|---:|---:|---:|
| Macro only | 2 | 0.9024 | 0.20152 | 0.8526 |
| Macro history (previous + current) | 4 possible observed pairs | n/a | 0.18676 | not reported |
| Refined oracle proxy | 3 | 1.3456 | 0.14091 | 0.6380 |
| Full observed microstate | 6 | 2.3456 | 0.14091 | 0.6380 |

One-step predictive information lost by the 2-state macro representation compared with the full microstate (conditional-entropy difference): **0.21462 bits**. The refined proxy retains full one-step predictive information about the binary *macro outcome* and remains equally accurate for horizons 2 and 3 because the refined partition is strongly lumpable.

The macro-history forecast improves the macro-only forecast but remains worse than the refined/oracle baseline. This tests a **finite observed macro-history** of length two, not every possible infinite observed history or an optimally learned predictive state.

**Control:** a full observed microstate history, or any standard algorithm recovering the same sufficient-state partition, would match the full-microstate forecast. The IDOS vocabulary does not supply a statistical advantage here.

## Interpretation and falsifiability

1. **Positive control:** exact prediction can survive nontrivial coarse-graining when the partition is a sufficient predictive state. Keeping *every* distinction is unnecessary.
2. **Negative control:** a crude macro-frame may lose information relevant to future change even if its present-state description appears adequate.
3. **Direct bridge to IDOS:** audit whether observational Reference Frames and any selected relationship/provenance summary preserve probabilities of future **connection / refusal / reopening** events. However, this experiment models only an abstract Y/non-Y future outcome, not those events themselves.
4. **Strong null possibility:** an ordinary learned predictive state, finite-state HMM belief, or full-history baseline may perform as well as, or better than, an IDOS-designed representation. Any future IDOS benefit must be compared against those controls at matched observations and evaluation budget.
5. **Unresolved central question:** can IDOS operational variables such as CFV/MU/provenance be measured from partially observed behavior to create a sufficient (or approximately sufficient) predictive representation with defensible compression and out-of-sample performance? **Not tested here.**

## Assumptions and weaknesses

- Designed example, so improvement of the 3-state label is guaranteed by construction and not a discovery by the model.
- Synthetic stationary Markov chain; no learning, distribution shifts, intervention, endogenous rule generation, or real social data.
- The refined proxy's identity is *revealed to the observer*. Discovering it under partial observation is a distinct task.
- Information-theoretic storage entropy is not physical thermodynamic entropy nor true model description length.
- The outcome is a single binary future macro-event. Sufficiency for this event is not sufficiency for all micro-observables.
- No experimental evidence here for autonomous emergence of a new Reference Frame, physical phase transitions, molecular chemistry, or IDOS originality.

## Reproduction

From this directory:

```bash
python predictive_sufficiency_v02.py > predictive_sufficiency_results_v02.json
python -m unittest discover -s . -p 'test_predictive_sufficiency_v02.py' -v
```

The current overlay only **adds** files beneath `research/cross_scale_physical_baselines/`. It does not overwrite earlier v0.1 files, the root, MASTER_MAP, 12CDP, or the Social Connection implementation. Python standard library only.

## Established research context

- J. G. Kemeny and J. L. Snell, *Finite Markov Chains*, ch. 6: strong lumpability criterion. https://math.pku.edu.cn/teachers/yaoy/Fall2011/Kemeny-Snell_Chapter6.3-4.pdf
- C. R. Shalizi and J. P. Crutchfield, *Computational Mechanics: Pattern and Prediction, Structure and Simplicity* (2001): predictive causal states, minimal sufficient representations. https://csc.ucdavis.edu/~cmg/papers/cmppss.pdf
- J. P. Crutchfield and C. R. Shalizi, *Thermodynamic Depth of Causal States* (1999), Phys. Rev. E 59, 275. https://doi.org/10.1103/PhysRevE.59.275

These references identify prior methods; they are not offered as independent validation of the synthetic numerical choices in this audit.
