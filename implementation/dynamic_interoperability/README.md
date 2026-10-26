# IDOS Dynamic Interoperability — Difference Preservation v0.2

A minimal IDOS application that records heterogeneous, directional information exchange and **proposes** possible meaning changes automatically. It reuses `src/idos_reference_v1_2.py` `CommonDynamicsProtocol` through `idos_bridge.py`; it does not recreate CDP or Reference.

## Two additions

- **Automatic candidate detection:** `semantic_detection.py` provides deterministic indicators for possible omissions, negation mismatches, numeric changes and lexical overlap. For actual model-based inference, pass a user-provided `AIProvider` callable to `detect`; it must return `(Disposition, rationale)`. No external AI service is secretly called. Both rule-based and AI-generated results remain **UNRESOLVED** when entered in the ledger until independently assessed.
- **Observed relation trajectory analysis:** `relation_analysis.py` groups exchanges by direction, reports time-ordered retained/unresolved counts, and identifies asymmetries where reverse exchanges exist. It does not claim to model unobserved interactions or establish causality.

## Usage from repository root

```bash
PYTHONPATH=src:implementation/dynamic_interoperability python implementation/dynamic_interoperability/example.py
PYTHONPATH=src:implementation/dynamic_interoperability python -m unittest discover -s implementation/dynamic_interoperability -p 'test_*.py' -v
```

## Boundaries

1. Lexical heuristics are **not semantic equivalence detectors**: negation, paraphrase, implicature, multilingual content and tacit knowledge can be missed or misclassified. Candidate confidence is not calibrated probability.
2. The AI provider is a configurable integration point, not a bundled trained model. Model assertions never become verified facts by default.
3. `retention_rate` measures **reviewer-attested preserved claims**, not total meaning retained. Unreviewed candidates count as unresolved.
4. CDP structural translation is not natural-language translation. Text is provided by the caller.
5. The trajectory reports are observational audit summaries, not independent verification of relation formation or future updateability.
6. Nothing herein provides network security, consent, AI governance, or validated superiority over existing audit tools.

## Files

- `interoperability.py`: claim-level ledger
- `idos_bridge.py`: thin CDP adapter
- `semantic_detection.py`: automatic tentative candidate detection and pluggable AI assessor
- `relation_analysis.py`: directional observed trajectory summaries
- `example.py`: deterministic example
- `test_interoperability.py`: unit and CDP integration tests
