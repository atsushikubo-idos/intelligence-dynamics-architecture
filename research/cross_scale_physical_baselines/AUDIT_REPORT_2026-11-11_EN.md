# Cross-Scale IDOS Research — Integration & Reproducibility Audit

**Date:** 2026-11-11  
**Status:** repository-ready candidate; GitHub remote publication is **not confirmed**.

## Basis of audit

The user-provided `intelligence-dynamics-architecture-main (23).zip` was used as the repository baseline, and the uploaded independent research overlay archives were checked and merged. This local ZIP is a snapshot, not a verified current remote HEAD. The candidate release is distributed as an **overlay** so newer changes on GitHub need not be overwritten.

## Verification actually performed

- Candidate overlays: 21 source ZIP archives including 2 connection-related archives. No conflicting same-path content was found against the supplied repository snapshot.
- Python source syntax parsing: passed for all Python files in the reconstructed candidate before packaging.
- `python -m pytest -q` in `research/cross_scale_physical_baselines`: **224 passed; 4 subtests passed**.
- `python -m pytest -q` in `implementation/social_connection_architecture`: **123 passed**, inclusive of 78 selected connection/cross-scale tests.
- These are **347 distinct pytest tests** across the two directories, plus 4 subtests. The 78 selected tests must not be double-counted.
- Tests ran in this session; source archive result files from earlier work were not numerically regenerated from scratch one by one.

## Scientific boundary and known limitations

| Area | Established computation | Not demonstrated |
|---|---|---|
| Quantum hydrogen | Approximate H2 and H2+ electronic structure; RHF/FCI within finite basis; FCI-derived nuclear/bath simulations | Accurate fully quantum time-dependent H2 formation kinetics, radiative stabilization, grain-surface chemistry |
| Statistical dynamics | Ising/Markov/coarse-graining toy baselines | New molecular law or proven predictive sufficiency in the real world |
| Social histories | Feature discovery/latent states/shift diagnostics on synthetic data | Discovery of causal social mechanisms in real people, AI, or organizations |
| Identifiability and observation | Explicit observational indistinguishability and pre-specified probes | Unrestricted self-invention of probes, reliable causal source attribution |
| Intervention | Synthetic information-versus-relationship-impact trade-off | Empirical interpersonal effects or demonstrated IDOS superiority over equivalent standard decision theory |

## Architectural findings

1. The physical and social branches remain **separate mathematical models**. The connection is an audit framework of structural distinctions, not a derivation from chemistry to intelligence.
2. Standard complete-history and standard ML / Bayesian baselines can reproduce the decisive predictions when given matching information. **Unique IDOS advantage is not established.**
3. Observation, consent, refusal, provenance, and uncertainty are meaningful requirements; this suite does **not** automatically integrate all historical IDOS CFV/MU operational semantics into every experiment.
4. Synthetic input generators may encode the very regularities being recovered; held-out samples drawn from the same generator do not constitute external validation.
5. The exact user GitHub HEAD, its branch protection, and any intervening remote changes have **not been checked**. Commit and push have not been performed.

## Publish procedure

Extract the accompanying release overlay directly over a **current local clone** using GitHub Desktop > Repository > Show in Explorer. Inspect changed files, then commit and push. The overlay contains no replacement repository-wide README, no changed MASTER_MAP, and no new root-level installation document. Do not replace the entire repository with the older archived snapshot.

Suggested commit title: `Add audited cross-scale physics and IDOS connection research`.
