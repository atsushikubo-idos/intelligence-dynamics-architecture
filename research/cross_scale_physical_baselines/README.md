# Cross-Scale Baselines and IDOS Connection Research

**Research status:** exploratory, synthetic for social experiments; no established cross-domain law or unique IDOS predictive advantage. November 11, 2026.

## Research architecture

1. **Physical/statistical baselines** (`physical_baselines.py`, predictive sufficiency and discovery modules): existing statistical mechanics, Markov coarse-graining, and predictive-state methods.
2. **Quantum hydrogen** (`quantum_hydrogen_formation/`): finite-basis H2/H2+ electronic energies, RHF/FCI comparison, classical nuclear motion, simplified dissipative and finite-oscillator bath models. These do **not** constitute a realistic quantum molecular collision or interstellar-grain formation-rate simulation.
3. **Social transfer audits** (`social_transfer_audit/`): synthetic relation maintenance, event-history feature discovery, HMM latent states, multi-observer histories, shift detection, observational non-identifiability, active diagnostic selection, and intervention-related state change. Consent and refusal are modelled constraints, not empirical human behaviors.
4. **Connection boundary and generativity experiments** (`../../implementation/social_connection_architecture/` with notes under `../../theory/social_connection/`): connection possibility, continuity, and simple capability composition under supplied rules.

## Research logic

Established physics/chemistry -> independently reproducible baseline computation -> abstraction of testable structural distinctions (possibility / formation / persistence / observation / intervention) -> separate synthetic IDOS comparison -> real-world data validation **still required**.

No equivalence between electron correlation, physical energy dissipation and trust, consent, or interpersonal agency is asserted. Physical formulas are **not** imposed on social systems.

## Reproduce

Run from this repository's `research/cross_scale_physical_baselines` directory:

```bash
python -m pip install numpy scipy matplotlib pytest scikit-learn
python -m pytest -q
```

Run social connection tests from `implementation/social_connection_architecture`:

```bash
python -m pytest -q
```

The original numerical result CSV/JSON files are retained as provenance. Tests validate model behavior; they are not a substitute for independent physical or empirical validation. Some physical studies have simplified assumptions (minimal basis, classical nuclei, finite baths), and some social data generators bake in the target relation.

## Audit and publication status

See [`AUDIT_REPORT_2026-11-11_EN.md`](AUDIT_REPORT_2026-11-11_EN.md) and [`RELEASE_FILE_MANIFEST_2026-11-11.json`](RELEASE_FILE_MANIFEST_2026-11-11.json). This work is **not** an empirical validation of IDOS; all numerical claims should be interpreted within their specified models.
