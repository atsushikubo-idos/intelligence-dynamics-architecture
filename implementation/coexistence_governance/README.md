# IDOS AI Coexistence Governance v0.3

**Scope: AI governance, not a second IDOS Reference.**

A compact, inspectable reference implementation for governing AI proposals and actions in heterogeneous human–AI–organization settings. It extends v0.2 with a conservative execution eligibility gate, externally reported collective-risk signals, and human-controlled slow review. The inherited `idos_bridge.py` uses the existing `idos_reference_v1_2.py` `CommonDynamicsProtocol` to describe heterogeneous actors without unifying their reference frames.

## Architecture

1. **Describe**: Optional existing IDOS CDP adapter describes actors and translation limits. No new reference-frame model is created.
2. **Review**: `CoexistenceGovernor` checks stakeholder approvals, objections, risk, reversibility, and recontact records.
3. **Fast gate**: `AIExecutionGate` denies missing/expired/mismatched capabilities, missing external invariant attestations, and active pauses. Unresolved collective signals require human review.
4. **Slow review**: Two distinct configured human/organizational reviewers may request policy review or release an incident gate lock, with evidence references. The AI **cannot** amend policy through these operations.
5. **Recontact**: Post-action outcomes are recorded for human interpretation; no automatic safety claim is produced.

Statuses: `eligible_for_external_enforcement`, `human_review_required`, `deny`, `paused`. **Eligible is not permission to execute and not proof of safety.** An external trusted tool gateway must authenticate principals, sign/verify credentials, bind scope to a resource, enforce time windows and rate limits, and independently perform the actual deny/stop.

### Key files

- `governance.py`: inherited v0.2 stakeholder governance and auditing.
- `idos_bridge.py`: inherited narrow CDP descriptive adapter; depends on `src/idos_reference_v1_2.py`.
- `execution_gate.py`: new v0.3 guard, collective signals, and slow-loop review requests.
- `example.py`, `example_cdp.py`, `example_gate.py`: illustrative usages; `example_gate.py` uses *mocked assertions*.
- `tests/`: behavior tests, **not** penetration or deployment tests.

### Test locally

From this folder:

```bash
python -m unittest discover -s tests -v
python example_gate.py
```

`example_cdp.py` requires the repository's `src` folder to be on `PYTHONPATH`.

## Safety and epistemic limits

- No agent or tool execution; no hardware root of trust, hardware cutoff, cryptographic capability issuance, sandbox, or actual emergency kill-switch.
- The `authenticated`, `scoped`, `cdp_ready`, and `external_invariants_ok` booleans are **assertions supplied by the caller**. If an attacker or AI controls them, this component provides no trustworthy execution boundary. A production integration must calculate them from trusted, independent enforcement systems—not model output.
- The collective-risk monitor accepts incident reports; it **does not detect emergent collusion, coordinated evasion, prompt injection, cascading failures, or deception** automatically. False negatives remain possible.
- Two-reviewer controls are configured actor IDs, **not identity verification**, organizational legitimacy, or legal authorization.
- Slow review records requests; it does not implement binding policy updates, democratic legitimacy, oversight institutions, or legal compliance.
- Reviewer approvals alone cannot compensate for failed external safety checks, and CDP can never overrule objections.
- Not a production safety system; not a claim of protection against loss of control or advanced autonomous AI.

## Origin and boundaries

Inspired by IDOS **ver.44** (multi-agent emergent risk, fast/slow governance, cross-scale observation) and **ver.15 extended** (execution gates, policy/invariant distinction, human override, fail-closed). The **real source diagrams remain richer than this prototype**. It does not implement hardware security or the full constitutional governance model proposed in those diagrams.

Install under `implementation/coexistence_governance/`. The authoritative CDP / dynamic ontology remain in `src/idos_reference_v1_2.py`. This prototype should be evaluated independently before any real deployment.
