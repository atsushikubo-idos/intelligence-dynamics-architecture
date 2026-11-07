# IDOS Social Connection Architecture v0.3 — Repository Module Integration

**Status:** experimental prototype; 7 November 2026.

This release **connects the actual existing source modules**, rather than reproducing their logic in a new stand-alone experiment. It extends v0.2 without rewriting MASTER_MAP v1.1 or the 13 equations. The repository's existing three module directories are **required**.

## Live dependency edges

| Social connection event | Directly invoked, existing repository API | Preservation constraint |
| --- | --- | --- |
| Actor-to-actor statement | `implementation/dynamic_interoperability/interoperability.py`: `Ledger.record`, `Claim`, `Assessment` | Source and target frames, direction, trajectories and unresolved translation residuals |
| Potential reference-frame update | `implementation/discovery_architecture/discovery_architecture.py`: `DiscoveryCycle.intervene`, `.difference`, `.propose_frame`, `.recontact` | A frame proposal is linked to a documented, **reported** performed action and observation; not a proof of causality |
| Permission / intervention assessment | `implementation/coexistence_governance/governance.py`: `CoexistenceGovernor.assess`, `.object` | Proposals are reviewed, blocked, paused or deemed eligible; no automatic action, no override of actor choices |
| Shared evidence, distribution, frame reopening, independent actor adoption | Existing `social_connection.py` and `social_connection_v02.py` | Use of verified shared evidence, residuals, hypothesis distribution, holding and recovery |

The bridge uses `importlib.util.spec_from_file_location` to load those **actual Python files by repository path**. This avoids module-name clashes with `social_connection.py` and preserves the original implementations and tests. It does not replace the deeper CDP reference implementation; the interoperability ledger's `cdp_quality='structural_adapter_only'` is an explicit limitation.

## End-to-end demonstration

Three simulated actors—human, AI and organization—retain distinct reference frames and choices.

1. The organization shares cash and cash-burn evidence; a private datum remains unshared.
2. An attributed message is recorded with **unresolved** semantic assessment by the original dynamic interoperability ledger.
3. The social-connection core records differing choices, generates its limited `cash_runway` candidate and evaluates it.
4. A separate externally reported review is entered into the existing `DiscoveryCycle` with traceable evidence; the resulting reference-frame proposal is an auditable record, **not** auto-adoption.
5. The existing governance module assesses an AI-proposed pilot with unknown risk as `review`, even with caller-supplied affected-party approvals. No tool execution occurs.
6. The human declines the frame and the AI and organization adopt it. These are explicitly supplied simulated decisions.
7. At the next time step new authorized evidence triggers a Discovery recontact linked to the original proposal; past records are not rewritten.

## Run from the repository checkout

```bash
cd implementation/social_connection_architecture
python social_connection_v03_bridge.py > results_v03.json
python -m unittest -v test_social_connection_legacy.py test_integration.py test_external_bridges.py
```

The new suite adds 17 adapter/negative tests; together with the 28 pre-existing social-connection tests, **45 passed** in the development environment. Unmodified module tests also passed when invoked with their respective import paths: 15 (dynamic interoperability), 73 (discovery architecture), and 21 (coexistence governance).

```bash
# From the repository root:
(cd implementation/dynamic_interoperability && python -m unittest discover -p 'test_*.py')
(cd implementation/discovery_architecture && PYTHONPATH="../../src:." python -m unittest discover -p 'test_*.py')
(cd implementation/coexistence_governance && PYTHONPATH="../../src:." python -m unittest discover -s tests -p 'test_*.py')
```

The example commands above use bash-style environment variables. On Windows, run tests from your Python IDE or set `PYTHONPATH` in PowerShell as appropriate. The primary 45 integration tests do not require environment-variable configuration when run from the social-connection directory.

## What this **does not** prove

- The simulated actors are not independently deployed services, and caller-provided consent or intervention evidence is **not authenticated**.
- Passing the governance assessment does not execute or authorize a real external action. The execution gate remains a separate module and is **not connected** here.
- The textual message exchange is not automatic semantic translation. Declared reviewer assessments may be incorrect.
- `cash_runway` is a pre-programmed formula, not autonomous discovery of an unknown social reference frame.
- Distribution estimates are illustrative and have not been calibrated on social-world interactions.
- Relationship distributions, cross-frame verification under extreme capability gaps, MU in the substantive sense, and recursive renewal of the exploration space remain major open empirical questions.
- A secure access control, data segregation, or tamper-resistant provenance implementation is not provided.

**Design aim:** A single auditable social-connection workflow that does not collapse the agents' identities or determine one globally optimal choice. The research objective remains the emergence of relational distributions and renewal of their exploration possibilities, not algorithm count or synthetic benchmark speed.
