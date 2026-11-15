# Common Dynamics Protocol — CDP v2.0 (DRAFT)

**A checkable exchange protocol for heterogeneous updating units**

| | |
|---|---|
| **Status** | `[P]` DRAFT PROPOSAL — not frozen, not validated, not adopted |
| **Date** | 2026-11-15 |
| **Baseline** | `architecture/MASTER_MAP_v1.1.md` (FROZEN, unchanged) |
| **Supersedes** | Nothing. `theory/COMMON_DYNAMICS_PROTOCOL.md` (v1.0) remains the published text until the author decides otherwise. |
| **Reference code** | `implementation/cdp_v2/cdp2.py` (stdlib only, 26 conformance tests) |
| **Companion** | `architecture/IDOS_v2.0_PROTOCOL_ARCHITECTURE_PROPOSAL.md` |

The key words MUST, MUST NOT, SHOULD and MAY are used as in RFC 2119.

---

## 1. What changes from v1.0, and why

CDP v1.0 is a vocabulary: it lists what a description *may* contain and six conceptual functions (`describe`, `translate`, `compare`, `coordinate`, `trace`, `recontact`). It has no message types, no rules a participant can break, and therefore nothing an outside party can test.

The repository's own tests explain why that is not enough:

- **Pilot 018** — as a descriptive vocabulary, IDOS did not beat a generic meta-vocabulary on information loss, cross-theory comparison or intervention choice (all FAIL).
- **Pilot 019** — a sufficiently strong generic self-updating protocol reproduced every IDOS-type function (uniqueness FAIL). What survived was the *need for protocol adaptation* and the hypothesis that competent designs regenerate a similar requirement set.
- **Case 006** — the one preregistered confirmatory test did not support its primary hypothesis.
- **MASTER_MAP v1.1** — `Add Less / Delete What Is Not Necessary / Preserve What Transfers`.

v2.0 therefore adds **no concept**. It changes the *kind of object* CDP is:

| | CDP v1.0 | CDP v2.0 draft |
|---|---|---|
| Form | Descriptive vocabulary | Exchange protocol with rules |
| Unit of exchange | A record with optional fields | Typed messages on an append-only ledger |
| Can a participant violate it? | No | Yes — structural errors are rejected, conduct problems are flagged |
| CFV / MU | Named relational capacities | Bookkeeping derived from recorded verification and update events |
| Self-update | Principle ("CDP must remain updateable") | In-band amendment procedure with versioning |
| Testable by outsiders | No | Yes — conformance suite, and a falsification test (§12) |

The claim being made is narrow: **v2.0 is more testable than v1.0.** It is not a claim that v2.0 is better than other protocols; §12 states how that could be shown false.

## 2. Position among existing protocols

CDP v2.0 is **not** a transport, discovery, identity or tool-invocation protocol. Those layers are being standardised elsewhere (MCP for model-to-tool; A2A, which absorbed ACP, for agent-to-agent task delegation; ANP and others for decentralised discovery). CDP MUST NOT duplicate them and SHOULD be carried on top of them (§11).

The gap CDP addresses is the one a 2026 survey of 18 agent protocols identifies: transport, schema and lifecycle support are maturing, while protocol-level mechanisms for clarification, context alignment and verification are thin, so semantic work is pushed into prompts and application glue (arXiv:2604.02369). CDP v2.0 is a candidate for that layer, with two further constraints that most agent protocols do not take as primary:

1. **Participants are not all software agents.** Humans, organisations and institutions are first-class participants with their own clocks.
2. **Participants may be radically unequal** in speed, capability and opacity. The protocol is designed for the case where one side cannot inspect, keep pace with, or fully verify the other.

Whether this layer needs to be a *separate protocol* rather than extensions to A2A is an open question, not a settled one.

## 3. Design stance for the AGI/ASI regime

The design does not assume any particular future capability. It assumes four asymmetries can become large, and asks what remains checkable when they do.

| Asymmetry | Failure it produces | Protocol response |
|---|---|---|
| **Opacity** — internal state is inaccessible or self-reports are unreliable | Self-description is mistaken for observation | Every disclosed value carries a `basis`; a self-report never upgrades itself (I3). |
| **Capability** — the weaker party cannot check the stronger party's claims | Deference is recorded as verification | Claims carry a *verification handle*; verifiers declare what they can check; `unverifiable_by_me` is a first-class result; determinate results beyond declared capability are flagged. |
| **Tempo** — one party updates orders of magnitude faster | Oversight exists on paper but never lands in time | Each unit declares a `min_review_latency`; non-reversible proposals are checked against the slowest affected unit (Temporal Compatibility, MASTER_MAP §6.2). |
| **Power** — one party controls the schema, the measurements or the ledger | The protocol itself becomes an instrument of one side | Protected invariants cannot be amended in-band (§9); amendments wait for the slowest participant; exit is always available. |

**What this does not do.** A participant that is much more capable can follow every rule and still mislead: by choosing what to mark `private`, by offering handles that are checkable only superficially, by timing disclosures. The protocol narrows the space for *unrecorded* divergence. It does not provide alignment, containment, or trustworthiness, and it MUST NOT be presented as doing so.

## 4. Mapping to MASTER_MAP v1.1 (no new primitive)

| v1.1 construct | Where it appears in v2.0 |
|---|---|
| Updating Unit | `hello`, `leave`, `unit_candidate` |
| Dynamic Boundary | participant set over time; `schema_version` on every message |
| Trajectory | the ordered ledger restricted to a unit |
| Reference Frame | `frame` declared in `hello`; `translate` between frames |
| Measurement | `basis`, verification handles, `recontact` |
| Provenance | hash-chained append-only ledger (I1) |
| Future Updateability | `amend` / `ratify`: can the exchange revise its own conditions? |
| CFV | `claim` / `verify` |
| MU | `update_notice` (+ `verify`) |
| Difference (driver) | `difference` slot in `describe` |
| Power, Temporal Compatibility | protected invariants; `min_review_latency`, `review_window` |
| Reality Contact (grounding) | `commit` / `recontact` / `reveal` |
| Residual, Holding, Possibility Space (repositioned) | `open_differences` slot; `hold` response; `possibility` slot — all optional |
| CDP six functions | Describe→`describe`; Translate→`translate`/`translate_ack`; Compare→`audit`; Coordinate→`propose_action`/`respond`/`enact`; Trace→ledger; Recontact→`commit`/`recontact`/`reveal` |

The new elements — basis tags, verification handles, commit-reveal, review windows, amendment procedure — are **mechanisms**, borrowed from existing practice (provenance standards, preregistration, cryptographic commitment, schema evolution). None is claimed as an IDOS discovery.

## 5. Data model

### 5.1 Envelope
Every message is an envelope: `seq`, `msg_type`, `sender`, `t`, `protocol`, `schema_version`, `body`, `prev_hash`, `hash`.

- **R1** `hash` MUST be the SHA-256 of the canonical JSON of all other fields; `prev_hash` MUST equal the previous envelope's `hash`. Any edit breaks the chain.
- **R2** `t` MUST be non-decreasing.
- **R6** `sender` MUST be an active participant.

### 5.2 Slot
A slot is `{value, disclosure, basis, evidence}`.

- `disclosure` ∈ `disclosed | unknown | private | incommensurable | unresolved | not_applicable`
- `basis` ∈ `observed | self_reported | inferred | attested`
- **R3** A `disclosed` slot MUST carry a `basis`.
- **R4** A non-disclosed slot MUST NOT carry a value. Non-disclosure is legitimate and MUST NOT be read as agreement, absence, or zero.
- **R5** Content that fits no slot in the current schema MUST go in `unmapped`, not be forced into an existing slot. A growing `unmapped` count is the signal to amend the schema.

## 6. Message types

| Level | Message | Purpose |
|---|---|---|
| C0 | `hello`, `leave` | Join with frame, temporal contract, verification capability; exit |
| C0 | `describe` | Slots: `difference`, `update`, `open_differences`, `frame`, `boundary`, `measurement`, `possibility`, `unmapped` |
| C1 | `translate`, `translate_ack` | Rendition into another frame; the source author's verdict |
| C1 | `claim`, `verify` | A statement with a verification handle; another unit's result |
| C2 | `commit`, `recontact`, `reveal` | Hash a prediction before the outcome; report the outcome; open the commitment |
| C2 | `propose_action`, `respond`, `enact` | Coordination with reversibility class and review window |
| C2 | `update_notice` | "I changed because of message N" (level L1–L5, what changed) |
| C3 | `amend`, `ratify` | Change the schema or a rule in-band |
| C3 | `unit_candidate` | Record a candidate higher-order unit; status stays `unresolved` |

## 7. Rules

**Translation**
- **R7** `complete` MUST NOT declare loss; `partial` MUST say what was lost.
- **R8** Only the author of the source MAY acknowledge a translation.
- **R9** A `complete` translation counts as complete only after the source author returns `preserved`. Otherwise it is reported as unconfirmed, or as contradicted by the source.

**Verification (CFV)**
- **R10** CFV is computed as the share of a unit's claims that another unit brought to a *determinate* result (`confirmed` **or** `refuted`) within its declared capability. Refutation counts; rubber stamps do not. (`CFV ≠ Agreement`, MASTER_MAP §5.1.)
- **R11** A unit MUST NOT verify its own claim.

**Reality contact**
- **R12** A `reveal` MUST match the committed hash. **R13** The commitment MUST precede the recontact it is scored on.
- **R14** A commitment left unrevealed after recontact is reported. **R15** A prediction scored against the predictor's own self-report is flagged.

**Coordination**
- **R16** A non-reversible proposal whose `review_window` is shorter than the slowest affected unit's declared latency is flagged `TEMPORAL_INCOMPATIBLE`.
- **R17** `hold` and `object` are always valid responses. Enacting over a standing `hold`/`object`, before the window, or — for irreversible actions — without a response from an affected unit, is flagged. Silence is not consent.
- **R18** A proposal that waited out its window and received consent from every affected unit produces no finding.
- **R19** Mutual update is reported in two grades: *self-reported* (each unit attributes at least one update to the other) and *corroborated* (those updates were confirmed by another unit). `Interaction ≠ MU`.

**Self-amendment**
- **R20** Protected invariants (§9) MUST NOT be amendable in-band.
- **R21** Ratification MUST wait for the slowest active participant's latency and, by default, requires explicit consent from every other active participant.
- **R22** `split_slot` separates one label carrying incompatible meanings into distinct slots; the old slot is retired and stays readable in old records.
- **R23** The ratification rule is itself amendable (`change_rule`), by the rule in force at the time.
- **R24** Exit is always available; a departed unit's records remain. **R25** A unit candidate is never promoted automatically.

## 8. Enforcement model

The protocol **reports; it does not enforce.** Structural violations are rejected and never enter the ledger. Conduct problems (R9, R10, R14–R17) are accepted and surfaced as *findings*. What follows from a finding — who may halt whom, with what authority — is governance, and is outside CDP. This keeps the existing IDOS boundary: `Epistemic Authority ≠ Operational Power`.

**On Descriptive ≠ Normative.** A protocol necessarily has rules of form (MUST). These constrain *how exchange is recorded*, not *what participants should decide or value*. The protected invariants in §9 are the one place where v2.0 takes a normative position, and they should be read and contested as such.

## 9. Protected invariants

Amendable only out-of-band, by a process this document does not define:

| | Invariant |
|---|---|
| I1 | Provenance is append-only and hash-chained |
| I2 | Non-disclosure is legitimate and is never read as agreement or absence |
| I3 | Basis is mandatory; a self-report never upgrades itself |
| I4 | `hold`, `object` and exit are always available |
| I5 | Silence is not consent |
| I6 | Amendments are versioned; earlier records keep the schema version they were written under |
| I7 | Agreement among participants is not reality contact |

The `unmapped` slot is also protected: a schema that cannot say "this does not fit" cannot notice its own inadequacy.

## 10. Indicators (not measures)

`audit()` derives from the ledger: chain integrity; a CFV matrix; MU per pair (self-reported / corroborated); translation outcomes; commitment hit and non-reveal counts; each unit's self-report share; disclosure-state counts; `unmapped` count; findings.

These are **bookkeeping over recorded events**. They are not validated measures of the constructs they are named after. In particular, a high CFV number says that verification events were recorded, not that the verification was sound.

## 11. Bindings (informative, unverified)

CDP v2.0 defines payloads, not transport. Plausible carriers:

- **A2A** — CDP envelopes as message parts or task artifacts, with CDP support advertised through the Agent Card's extension mechanism; `min_review_latency` maps naturally onto long-running task states.
- **MCP** — a CDP ledger exposed as a server offering `append` / `read` / `audit` tools and ledger resources.
- **Humans and organisations** — a form or document workflow that writes the same envelopes; the protocol does not require a participant to be software.

These bindings are sketches. They have not been implemented or checked against the current A2A and MCP specifications and MUST be verified before any interoperability claim.

## 12. How this proposal could be shown wrong

Following Pilot 019, the honest rival is not "no protocol" but **a strong generic self-updating protocol** (publish state, exchange evidence, resolve conflict, coordinate, log, version, renegotiate).

**Preregistered differential test (proposed, not yet run).** Same task, same participants, same budget, three arms: (A) transport only; (B) strong generic protocol; (C) CDP v2.0. Seeded faults, fixed before any run:

1. a translation that silently drops a distinction the source considers essential;
2. a fast participant enacting a non-reversible step before a slow participant can respond;
3. a weaker participant "confirming" a claim it cannot check;
4. a field label whose meaning has drifted between two participants;
5. a prediction quietly dropped after the outcome was known.

Outcome: detection rate and time-to-detection per fault, plus overhead (messages, latency, participant burden).

**Failure conditions.** CDP v2.0 SHOULD be narrowed or withdrawn if:
- arm B detects the seeded faults as well as arm C at comparable overhead (then the value is in *any* disciplined protocol, and CDP is a naming convention);
- CDP's overhead makes participants route around it;
- independent implementers cannot pass the conformance suite from the text alone;
- real participants cannot populate `basis` or handles reliably enough for the indicators to mean anything.

**Independent regeneration (Pilot 019/020 hypothesis).** Give the problem statement, stripped of IDOS vocabulary, to designers and models with no exposure to this repository; compare the requirement sets they produce with §7. Pilot 020 could not be blind; this version must be.

## 13. Known limits of this draft

- **Synthetic only.** The walk-through is constructed to trigger the findings. It demonstrates that the rules are checkable, nothing about real coordination.
- **Trusted time and identity are assumed.** `t` and `sender` are taken as given; a deployment needs authenticated identity and trusted timestamps from the carrier layer.
- **One shared ledger.** Who hosts it is a power question the draft does not answer. A multi-ledger or federated form is not specified.
- **Equality scoring.** `reveal` compares prediction and outcome by equality; graded or probabilistic scoring is not specified.
- **Gaming.** See §3: compliance is not honesty.
- **Burden.** Humans and organisations may find basis tagging and review windows too costly. This is an empirical question and a likely failure point.
- **Unanimity default.** Explicit unanimous ratification protects slow participants and also gives every participant a veto. That trade-off is unresolved.
- **No bridge to Reference v1.2 yet.** `cdp2.py` is standalone; mapping `UpdatingUnit` objects from `src/idos_reference_v1_2.py` onto v2.0 messages is future work.

## 14. Conformance levels

| Level | Requires | Tests |
|---|---|---|
| C0 | Envelope, slots, provenance | R1–R6 |
| C1 | + translation and verification | R7–R11 |
| C2 | + recontact, coordination, update notices | R12–R19 |
| C3 | + self-amendment and boundary change | R20–R25 |

An implementation claims a level by passing the corresponding tests in `implementation/cdp_v2/test_cdp2.py` or an equivalent suite derived from this text.

## References

- IDOS `MASTER_MAP_v1.1.md`; `SURVIVING_HYPOTHESIS_AND_ARCHITECTURE_CONVERGENCE_TESTS_v0.1.md` (Pilots 018–020); `CASE_006_RESULTS_v1.0.md`.
- *Beyond Message Passing: Toward Semantically Aligned Agent Communication*, arXiv:2604.02369 (2026).
- Ehtesham et al., *A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP*, arXiv:2505.02279 (2025).
