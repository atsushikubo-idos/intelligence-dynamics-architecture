# IDOS Social Connection Architecture v0.2 — selective integration

**Status:** executable synthetic integration prototype, 2026-11-07. Python 3.10+, standard library only.

This version **preserves v0.1** (`social_connection.py`, `test_social_connection_legacy.py`) and adds a social-connection integration layer (`social_connection_v02.py`). It selectively incorporates useful architectural lessons from Minimal Pilot v0.1–v1.4, Inverse Architecture Audit v0.1–v0.3, and Minimum-Structure Audit v0.1–v0.2. See [`SOCIAL_CONNECTION_ARCHITECTURE_v0.2.md`](../../theory/social_connection/SOCIAL_CONNECTION_ARCHITECTURE_v0.2.md) for the inclusion/exclusion matrix and architecture notes.

## Run

```bash
python -m unittest -v test_social_connection_legacy.py test_integration.py
python social_connection_v02.py > results.json
```

## Integration, not a model zoo

The protocol connects three *simulated* autonomous actors with different frames and independent choices, **without central optimization**. It supports:

- A provenance-labelled, permission-gated observation ledger and a 12CDP-shaped illustration.
- CFV as **checkability of an attributed shared statement** (not verification of minds or ground truth); MU as a *permission/choice pathway*, not proven beneficial mutual learning.
- Separate **empirical choice/relationship proxy distributions** and **illustrative structural hypothesis weights**, avoiding an invalid equation between empirical interaction patterns and Bayesian belief over models.
- Frame-specific minimal views, explicit observational-equivalence failures, archival reopening with no hindsight or private-source leakage.
- Preservation of historical candidate evaluations, without overwriting time-indexed old values.
- Contrastive inquiry from unexplained difference; external evidence offers that require all specified agents' consent; no automatic novel-sensor invention.
- A record of possibility presentation and its potential influence; the protocol does not choose for any actor.

## Key limitations

The empirical choice frequency is **only a narrow proxy** for relational distribution; full temporal relational dynamics and distribution-valued reference-frame exploration are not implemented. The candidate generator still contains a prewritten cash-runway composition rule. Bayes-like model weights are illustrative, not calibrated. No original mathematical discovery, self-modifying generation methods, complete 12CDP compliance, real-world governance, or empirical social validation is claimed. Do not treat this as secure production consent/privacy infrastructure.

## Files

- `social_connection.py`: unchanged v0.1 foundational protocol.
- `social_connection_v02.py`: optional v0.2 integrated social-connection facade and end-to-end demonstration.
- `test_social_connection_legacy.py`: original 16 tests.
- `test_integration.py`: 12 new integration and regression tests.
- `results.json`: end-to-end synthetic evidence and protocol snapshot.
- `../../theory/social_connection/SOCIAL_CONNECTION_ARCHITECTURE_v0.2.md`: architecture and selection audit (English).

## Design principles

Keep MASTER_MAP v1.1 and the 13 equations frozen. Agents have their own boundaries, histories, native reference frames and freedom to adopt/hold/reject. The shared protocol exposes **possibilities and evidence, not mandatory answers**. It may record multiple explanatory structures and limits; new observations are accepted with consent and provenance, and unsuccessful predictions can reopen frames. These are architecture-interface capabilities, not evidence that emergent social coordination has been achieved.

## Repository placement

Keep these five Python/JSON files and this README together under `implementation/social_connection_architecture/` because local module imports rely on that directory. Store the theory/audit document separately under `theory/social_connection/`. Run the commands above from the implementation directory.
