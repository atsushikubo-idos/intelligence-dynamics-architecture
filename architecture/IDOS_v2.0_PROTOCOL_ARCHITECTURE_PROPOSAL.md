# IDOS v2.0 — Protocol Architecture Proposal

| | |
|---|---|
| **Status** | `[P]` PROPOSAL for the author's decision. Not frozen. Does not replace `MASTER_MAP_v1.1.md`. |
| **Date** | 2026-11-15 |
| **Purpose** | Re-centre IDOS on its stated aim — a common dynamics protocol for heterogeneous intelligences — in a form that can be implemented, broken and compared. |

---

## 1. The move

MASTER_MAP v1.1 moved IDOS from *process-centred* to *updateability-centred*. This proposal makes one further move and no other:

```
Vocabulary-centred  →  Protocol-centred
```

The seven v1.1 primitives, the two relational capacities, the cross-cutting conditions and the three design principles are kept exactly as frozen. What changes is where the architecture's weight sits: from *what can be said about* heterogeneous updating to *what participants must exchange, and what can be checked about that exchange*.

Reason: the repository's own reductions (Pilots 018–019, POST-RT §15–18) located the surviving value at "architecture level … describing, translating, comparing, tracing and reconnecting heterogeneous updating systems", while showing that as a vocabulary this does not beat a strong generic alternative. An architecture whose value is interoperability has to be stated as something two unlike parties can run.

## 2. Layered architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│ L5  META        amend / ratify            Future Updateability        │  can the exchange
│                 protected invariants      Power                       │  revise its own terms?
├───────────────────────────────────────────────────────────────────────┤
│ L4  GROUNDING   commit / recontact /      Reality Contact             │  did reality agree?
│                 reveal                                                │
├───────────────────────────────────────────────────────────────────────┤
│ L3  COORDINATION propose / respond /      MU, Temporal Compatibility  │  who changed, and
│                 enact, update_notice                                  │  was there time?
├───────────────────────────────────────────────────────────────────────┤
│ L2  CROSS-FRAME translate / ack,          Reference Frame, CFV        │  what survived the
│                 claim / verify                                        │  crossing; what was checked?
├───────────────────────────────────────────────────────────────────────┤
│ L1  RECORD      describe, slots,          Updating Unit, Boundary,    │  what changed, on
│                 basis, disclosure         Trajectory, Measurement,    │  what basis?
│                 hash-chained ledger       Provenance, Difference      │
├───────────────────────────────────────────────────────────────────────┤
│ L0  CARRIER     transport, identity,      (outside IDOS: A2A, MCP,    │
│                 discovery, time           DID, human workflow)        │
└───────────────────────────────────────────────────────────────────────┘
```

L1–L5 are CDP v2.0 (`theory/COMMON_DYNAMICS_PROTOCOL_v2.0_DRAFT.md`). L0 is deliberately not IDOS.

## 3. What is kept, moved, and not added

| | |
|---|---|
| **Kept as frozen** | Updating Unit, Dynamic Boundary, Trajectory, Reference Frame, Measurement, Provenance, Future Updateability; CFV, MU; Power, Temporal Compatibility; Reality Contact; the three design principles |
| **Kept as repositioned in v1.1** | Residual, Holding, Possibility Space, 12PDM — optional slots / responses, never required |
| **Moved** | CDP: from "relational/application interoperability layer" to the organising spine of the architecture |
| **Operationalised (not redefined)** | CFV and MU become bookkeeping over recorded events; Future Updateability becomes the observable question "has this exchange amended its own schema or rules, and could it?" |
| **Not added** | No new primitive, layer of ontology, or theoretical construct. New items are mechanisms from existing practice. |

One consequence should be stated plainly: operationalising CFV, MU and Future Updateability this way is *narrower* than their v1.1 definitions. The protocol sees only what participants record. The latent capacities remain unmeasured, as v1.1 already says.

## 4. Requirements for the AGI/ASI regime

The Future-Regime cases (F001–F010) repeatedly produced the same pressures. Stated as protocol requirements:

| # | Requirement | From | Met in v2.0 by |
|---|---|---|---|
| Q1 | Self-report must stay distinguishable from observation | F001, F010 | `basis` (I3) |
| Q2 | "I cannot verify this" must be sayable without penalty and visible afterwards | F002, F009 | `unverifiable_by_me`; capability declaration |
| Q3 | Nominal oversight that cannot land in time must be detectable | F006, F007 | `min_review_latency`, `review_window` |
| Q4 | Internal consensus must not count as external grounding | F004, F008 | commit / recontact (I7) |
| Q5 | The terms of exchange must be revisable without the fast or strong party rewriting them alone | F003, F009 | amendment procedure, protected invariants |
| Q6 | Participants and boundaries change mid-exchange | F005, F007 | `hello` / `leave` / `unit_candidate`, per-message schema version |
| Q7 | Non-disclosure must be possible without being read as assent | all | disclosure states (I2), I5 |
| Q8 | What the schema cannot express must not be silently compressed | Pilot 019 Event 1 | `unmapped` |

These requirements are derived from scenario stress tests, which are not observations of the future.

## 5. Honest assessment of "world-leading"

What can be said:

- The target — a verification/alignment layer above transport, built for unequal and non-software participants — is one that current surveys describe as underdeveloped. The proposal is aimed at an open problem, not a solved one.
- Taking tempo asymmetry, verifier capability and protocol self-amendment as *first-class protocol rules with tests* is uncommon in the agent-protocol specifications reviewed.

What cannot be said:

- That it is the most advanced architecture in the world. No comparison has been run. Pilot 019 predicts a strong generic protocol can match it functionally; §12 of the spec is the test of that.
- That any component is novel. Each mechanism exists elsewhere.
- That it works with real humans, organisations or advanced AI systems. Everything here is synthetic.

A defensible external sentence: *"IDOS proposes a draft exchange protocol for heterogeneous updating units, with an executable conformance suite and a stated falsification test against a generic baseline."*

## 6. Decisions for the author

1. **Adopt, shelve, or cut down?** Nothing in the frozen baseline has been touched. This can be adopted as the v2.0 line, kept as a research branch, or reduced to its C0–C1 core.
2. **Normative content.** §9 of the spec (protected invariants) is a normative position inside a framework that has kept `Descriptive ≠ Normative`. Either accept that a protocol needs a small explicit normative core, or move the invariants out to the governance layer and leave CDP purely formal.
3. **Separate protocol or A2A extension?** If the differential test shows the value is real, the lower-cost path to adoption may be an A2A/MCP extension profile rather than a standalone protocol.
4. **Next research gate.** The cross-scale synthesis already calls for one preregistered benchmark and a freeze on new synthetic examples. The differential test in spec §12 is a candidate for that single benchmark.

## 7. Files in this proposal

| File | Content |
|---|---|
| `architecture/IDOS_v2.0_PROTOCOL_ARCHITECTURE_PROPOSAL.md` | this document |
| `theory/COMMON_DYNAMICS_PROTOCOL_v2.0_DRAFT.md` | protocol specification |
| `implementation/cdp_v2/cdp2.py` | reference implementation |
| `implementation/cdp_v2/test_cdp2.py` | 26 conformance tests (R1–R25 + walk-through) |
| `implementation/cdp_v2/example.py` | deterministic three-unit walk-through |
| `implementation/cdp_v2/cdp2.schema.json` | JSON Schema for envelope and slot |
| `implementation/cdp_v2/README.md` | usage and boundaries |

This package adds files only. Existing `README.md`, `DOCUMENT_INDEX.md`, and the frozen MASTER_MAP v1.1 remain unchanged. The Japanese overview is maintained separately outside the GitHub package.
