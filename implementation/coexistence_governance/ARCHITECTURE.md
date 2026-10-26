# AI Governance Boundary — v0.3

## Purpose

Preserve heterogeneity while governing **AI-initiated actions**. The IDOS CDP is an optional descriptive input, not an authorization mechanism. Reference v1.2 retains ownership of trajectories, frames, and relations.

## Mapping from the source diagrams

| Source idea | Minimal implementation | Not implemented |
|---|---|---|
| ver.44 collective emergent risk | externally reported `CollectiveSignal`; unresolved signals trigger review | automated multi-agent trajectory anomaly detection |
| ver.44 fast/slow governance | `gate()` versus human `propose_policy_revision()` | real-time middleware, legal deliberation |
| ver.15 capability-bound action | expiry, actor/action/resource, external verification assertions | cryptographic token verification, trusted identity |
| ver.15 invariant vs updateable policy | no ordinary policy change in fast loop; explicit external invariant check | trusted invariant engine or constitution amendment process |
| both: stop and accountability | incident lock, objection checks, audit | physical cutoff, enforceable kill-switch |
| IDOS CDP | reuse `idos_bridge.py` and Reference v1.2 descriptions | universal translation or meaning unification |

## Boundaries

This code makes a **policy recommendation** and records it; the secure execution gateway must enforce actions. It is intentionally small and dependent on outside verification. In particular, `eligible_for_external_enforcement` must not be interpreted as an authorization token.

For a real deployment, add independent identity and capability verification, allowlisted tool/resource policy, out-of-band human oversight, monitoring feeds, audit immutability, interruption controls, adversarial tests, incident handling, and regulatory review. These are missing capabilities, not minor production toggles.
