# IDOS Connection Continuity Architecture v0.3

**Research status:** Synthetic prototype; integration and formal-audit extension. Not empirical validation. 10 November 2026.

## Research question

How can a social-connection architecture preserve, across time, not only whether connection is feasible, but also **why it is not established**, **an actor's independent refusal or deferral**, **unresolved differences**, and **the conditions under which a new connection can be reconsidered**—without pretending to understand the actors' hidden internal states?

This is an orchestration/traceability design claim, **not** a novel mathematical theorem or proof of meaningful social connection.

## Inheritance: do not replace prior work

- `implementation/social_connection_architecture/social_connection.py` and `social_connection_v02.py`: actors, explicitly recorded individual decisions, public evidence, reference-frame history, residual/reopening.
- `social_connection_v03_bridge.py`: actual interoperability, discovery, and coexistence-governance adapters (existing v0.3).
- `connection_boundary_audit.py` (v0.1): robust common-action feasibility under finitely enumerated indistinguishable worlds; 3-actor illustrations.
- `connection_boundary_comparative_v02.py` (v0.2): full-history baseline, verification-opportunity and mutual-update-opportunity **proxies**.

`connection_continuity_v03.py` composes the existing **boundary** and **proxy** functions and can link an assessment to the real `SocialConnectionV03` instance. It does not copy those modules or modify frozen `MASTER_MAP v1.1` or the 13 research equations. It requires the prior v0.1 and v0.2 files in the same implementation directory.

## Explicit separation of decisions

A `Snapshot` has **two** different outputs:

1. `feasibility`: `GUARANTEED`, `POSSIBLE_NOT_GUARANTEED`, `IMPOSSIBLE` under declared world and permitted-action assumptions.
2. `connection`: `INFEASIBLE`, `UNCERTAIN`, `DECLINED`, `DEFERRED`, `CONDITIONAL`, or `CONNECTED_PROXY`.

An actor's `reject` is **not** a proof of mathematical impossibility. `hold` is not a rejection. `CONNECTED_PROXY` means only that the finite-world robust action, declared verification opportunity, per-actor update paths, and declared reality-contact freshness meet the chosen toy criteria; it is **not** actual mutual understanding, authentication, meaningful consent or mutual learning.

**Reason codes** are nonexclusive and retain ambiguity: `NO_JOINTLY_PERMITTED_ACTION`, `OBSERVATIONAL_AMBIGUITY`, `ACTOR_REJECTION`, `ACTOR_HOLD`, `VERIFICATION_PATH_INCOMPLETE`, `MUTUAL_UPDATE_PATH_INCOMPLETE`, `REALITY_CONTACT_UNCONFIRMED`. A world can also present multiple blockers. The explicit state is a simplified priority display, not an ontological classification.

The layer deliberately makes no prediction of a future reconnection probability. **Reconnection potential** means retained future opportunity for an actor-authorized recheck. New observations or permissions are an explicitly submitted new tick; they are never assumed or invented.

## Lifecycle

1. Explicitly declare actors, observation, hypothetical possible worlds, choices and provenance for a domain and tick.
2. Reuse `boundary()` to calculate feasibility without inferring anyone's hidden states.
3. Reuse `mutual_update_opportunity()` and optionally `verification_opportunity()` to record structural paths. **A caller declaration of verification is not inferred from mere evidence exchange.**
4. Record nonexclusive blocking reasons and current actor decisions separately.
5. Keep differences with IDs and provenance, including unresolved disagreements. Public trace does not publish private explanations or private difference IDs.
6. Reopen earlier public histories **as of their original time** without hindsight; do not rewrite prior snapshots.
7. Reassess at a new tick with fresh observed or declared inputs and an optional `recheck_of` link. No coercion or automatic resumption of contact occurs.
8. `assess_from_bridge` validates that a real `SocialConnectionV03` instance has the same actors, time, and recorded actor choices, and retains only public record IDs from its existing integration modules. It does not independently authenticate those records.

## Synthetic example

The deterministic test trajectory is:

| Tick | Feasibility | Connection proxy | Interpretation |
| --- | --- | --- | --- |
| 0 | `POSSIBLE_NOT_GUARANTEED` | `UNCERTAIN` | Same observation, incompatible world-dependent permitted actions; unresolved semantic difference held |
| 1 | `GUARANTEED` | `DECLINED` | Additional observation narrows worlds; human explicitly rejects |
| 2 | `GUARANTEED` | `CONNECTED_PROXY` | Synthetic independent actor choices now adopt; the prior difference is still held |
| 3 | `GUARANTEED` | `CONNECTED_PROXY` | A caller-attested difference resolution has been recorded; earlier snapshots remain unchanged |

These are **scenario assumptions**, not discoveries about humans, couples, children, organizations, or AI cognition. A different history or third actor can cause different results.

## Testing and negative results

- 22 new unit/integration checks cover all connection states, simultaneous blockers, rejection vs. feasibility, private redaction, refusal and deferment, historical reopening, recheck provenance, unresolved differences, real v0.3 decision alignment, and synthetic transitions.
- 75 pre-existing tests from social connection and boundary audits also pass, resulting in 97 passing tests across the six relevant suites in the working repository snapshot.
- The previous v0.2 benchmark established **equality** with the strong full-history baseline in 256 finite-world conditions. This result **continues to hold**; the present extension is not a new predictive-performance comparison.

## Known limitations and falsification targets

- All worlds, permissions, difference resolutions, evidence provenance and reality-contact flags are **caller-supplied**; no true human consent, reasoning, or semantic fidelity is authenticated.
- Finite exact-world enumeration is not a scalable representation of complex or unknown-unknown social states.
- The `assessment` event is a local append-only Python in-memory record, not a tamper-evident or distributed log. No cryptographic authorization, deletion policy, durable storage, concurrency, or remote execution is provided.
- Private data protection here is **output redaction in synthetic tests**, not end-to-end access security.
- A proxy may appear connected while human participants experience misunderstanding, harm, asymmetric influence, or coercion. Evaluate power and capacity preservation independently.
- `CONNECTED_PROXY` should never trigger automatic contact, action, treatment, intervention, or authorization.
- Existing event-sourced state machines and policy engines could reproduce these functions. A strong full-history, equally authorized and equally equipped baseline is required before claiming architectural superiority.

## Next empirical design

With independently running agents and consented participants, compare a conventional full-history event-sourced multi-agent baseline and this integrated trace design using the **same observations, permissions, evidence and governance rules**. Pre-register outcomes: reason-code accuracy against independent adjudication, missed consent withdrawals, preservation of unresolved differences, false claims of CFV/MU, ability to reconstruct decision-time evidence without hindsight, and quality of actor-authorized rechecks. Include refusal and irreversible nonconnection as valid outcomes.

## Running

```bash
cd implementation/social_connection_architecture
python -m unittest -v test_connection_continuity_v03.py
python connection_continuity_v03.py > connection_continuity_results_v03.json
```

The bridge integration needs the original sibling modules in the full repository (`dynamic_interoperability`, `discovery_architecture`, `coexistence_governance`). All files in this overlay are **additional**, not replacements.
