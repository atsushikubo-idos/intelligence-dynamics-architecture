# IDOS ver.84 — Cross-domain Trajectory Observation (prototype v0.2)

## Purpose
An **experimental, descriptive application-layer prototype** for observing changes in expectations, options, commitments, reference frames, Holding, and Residual across **M&A and hiring** cases. All bundled examples are synthetic.

This is **not** a validated decision-support instrument, an M&A valuation tool, or a predictive model. It does not infer private mental states, establish causality, measure Future Updateability directly, or demonstrate superiority over existing methods.

## Relationship to the IDOS architecture

- The frozen `MASTER_MAP v1.1` and `src/idos_reference_v1_1.py` remain unchanged.
- This prototype uses IDOS-inspired labels for a common **event-recording and comparison schema**; it does **not** implement or mathematically integrate the reference architecture.
- Cross-domain compatibility shown by synthetic examples is a software demonstration, **not** proof of scientific construct validity or practical improvement.
- `ver.84` refers to the associated application/communication context, **not** a new version of `MASTER_MAP`.

## Files

- `idos_ver84_application_v0_2.py` — standard-library Python adapter and synthetic M&A/hiring examples
- `idos_ver84_cross_domain_demo_v0_2.json` — generated synthetic demonstration report
- `test_idos_ver84_v0_2.py` — seven automated unit tests

## Run

Python 3.9+; no third-party packages required. Run commands from this directory:

```bash
python idos_ver84_application_v0_2.py --demo --output demo.json
python -m unittest -v test_idos_ver84_v0_2.py
```

For your own case input, provide JSON with `case_id`, `domain` (`M&A` or `hiring`), and an `events` array. Each event requires `date`, `actor`, `kind`, `topic`, `value`, `evidence`, and `visibility`. Run:

```bash
python idos_ver84_application_v0_2.py --input case.json --output report.json
```

## Governance and data limitations

- Bundled examples contain **no real client data**.
- Records marked `restricted` are excluded from normal analysis outputs. **This is not encryption, access control, anonymization, or a security guarantee.** The input file still contains these records.
- Do not upload confidential, personal, or client information to a public repository.
- Holding status is a deadline flag, not an autonomous recommendation to delay or proceed.
- Recorded changes are descriptive and do not establish causal relationships.

## Status

Experimental prototype v0.2; seven local unit tests pass. No independent validation or deployment. Kept separate from the frozen research baseline.
