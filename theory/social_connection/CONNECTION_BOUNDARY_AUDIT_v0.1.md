# IDOS Social Connection: Connection-Boundary Audit v0.1

**Status:** Formal finite-world micro-audit / synthetic tests, NOT an additional IDOS law, engine, social experiment, or empirical claim. 10 November 2026.  
**Base:** Social Connection Architecture v0.3; MASTER_MAP v1.1 and the thirteen conceptual equations remain unchanged.

## 1. Research gap and prior negative result

Existing Inverse Architecture Audit studied ambiguous internal structures; Minimum-Structure Audit studied individual-history vs relation-state models; Dynamic Interoperability recorded directed claims and unresolved interpretation; Social Connection v0.3 joined the actual interoperability, discovery and coexistence-governance modules.

The earlier Minimum-Structure Audit v0.2 found that, in the tested synthetic setting, a sufficiently rich individual-history representation reconstructed relation state and matched relation-state prediction, while a strong adaptive baseline equaled or exceeded the alternative methods. Thus **a separate relational variable is not proven necessary or superior**. Do not reinterpret these experiments as validation of social connection or mutual understanding.

**New narrow focus:** in a *single, explicitly defined* finite-world model, test when partial observation permits a guaranteed joint action, when it does not, and how observation and permission changes alter this boundary. The contribution is a testable formalization and linkage of existing IDOS concerns, not a novel impossibility theorem.

## 2. Operational model

Fix domain d, participants I, action set A, hidden-world set W, public observation o, and per-world actor-specific allowed actions A_i^d(w). The uncertainty class is W(o) = {w ∈ W : O(w)=o}. A common allowed action in world w belongs to ∩_{i∈I} A_i^d(w).

A deterministic action chosen solely from observation o is **guaranteed admissible** over W(o) precisely when:

    ∃a ∈ A such that ∀w ∈ W(o), ∀i ∈ I, a ∈ A_i^d(w)

or, equivalently:

    ⋂_{w∈W(o)} ⋂_{i∈I} A_i^d(w) ≠ ∅.

*Proof.* If the intersection is non-empty, choose any member; the same action is permitted for every participant in every world consistent with the observation. Conversely, if an observation-based deterministic action is permitted for every participant in every consistent world, that action belongs to the intersection. QED.

**Caution:** this is an if-and-only-if characterization *under the definition of guaranteed common-action admissibility*. It is not a necessary-and-sufficient condition for psychological, semantic, or institutional social connection generally. A common action can be admissible yet ineffective, and a participant may decide not to act. Consent is represented solely by explicit, stipulated allowed-action sets; it is not authenticated or inferred.

Classifications per domain:
- `GUARANTEED`: nonempty robust intersection.
- `POSSIBLE_NOT_GUARANTEED`: some consistent world permits a joint action but no single action is admissible in all of them.
- `IMPOSSIBLE`: no consistent world permits any joint action within the specified action set.

For multiple preselected domains, `CONNECTED` means each has a robust action; `LIMITED` means at least one but not all domains do; `DISCONNECTED` means none do. These are declared test proxies, not universal ontology. In particular, `POSSIBLE_NOT_GUARANTEED` is **uncertainty**, not proof that actual-world connection fails. `IMPOSSIBLE` is relative to the enumerated action set, domain, and stated constraints; changing them may change the conclusion.

## 3. Indistinguishability witness

Two hidden worlds may induce the same public observations but permit disjoint joint action sets. Then no observation-only policy can guarantee success in both worlds. The test harness records a witness. A pair of disjoint sets is sufficient for failure, **not necessary**: three sets can intersect pairwise while having empty global intersection. A negative test checks this important distinction.

## 4. Temporal audit

The test sequence uses an initially ambiguous observation, a later discriminating observation, a withdrawal of permitted action by one participant, and subsequent restoration of permission. Expected robust statuses:

| Stage | Change | Robust status |
|---|---|---|
| t0 | Two indistinguishable worlds require incompatible actions | POSSIBLE_NOT_GUARANTEED |
| t1 | An observation distinguishes the worlds | GUARANTEED |
| t2 | Permission is withdrawn in the observed world | IMPOSSIBLE |
| t3 | Permission is restored | GUARANTEED |

The scenario is hand-constructed; it does not establish that real relationships typically change this way or that IDOS caused a re-connection.

## 5. Two versus three participants

An explicit third participant can make a previously jointly permitted action unavailable or restore availability when their action set changes. Separately, a conventional XOR example provides two joint distributions with identical pairwise marginals but different three-way dependence: `Z=X XOR Y` vs independent fair X, Y, Z. The corresponding even-parity probabilities are 1.0 and 0.5. **Full joint histories distinguish the distributions**; this does not show that a new relation state is necessary, as confirmed by the previous Minimum-Structure Audit.

## 6. Reproducibility and integration boundary

Files are an additive overlay, placed under the existing `implementation/social_connection_architecture/` directory and `theory/social_connection/`. They do not modify any prior source or require the v0.3 bridge to automatically exercise them.

From the existing repository checkout:

```sh
cd implementation/social_connection_architecture
python -m unittest -v test_connection_boundary_audit.py
python connection_boundary_audit.py > connection_boundary_results_v01.json
python -m unittest -v test_social_connection_legacy.py test_integration.py test_external_bridges.py test_connection_boundary_audit.py
```

The test workspace used Python standard library and synthetic finite-world fixtures. No external service is called.

## 7. Correspondence with existing IDOS functionality

| Formal audit construct | Existing research | Caveat |
|---|---|---|
| Partial observation and observational equivalence | Inverse Architecture Audit; observational equivalence research | Here hidden worlds are enumerated and public signals are stipulated |
| Rich histories versus explicit relation state | Minimum-Structure Audit v0.2 | No model superiority is established; full histories remain a strong baseline |
| Directional exchange, residual provenance | Dynamic Interoperability | This formal audit is not yet wired into its real exchange ledger |
| Actor-specific choices | Social Connection v0.2/v0.3 | Formal allowed-action sets are a test proxy, not authenticated consent |
| Governance / permission / refusal | Coexistence Governance | No external execution, legal permission, or secure access-control proof |
| CFV and MU | MASTER_MAP relational conditions | Meaningful verification or bilateral updateability is NOT measured by common action alone |
| Reopening / time / reality contact | Existing Social Connection & Discovery research | Time scenario re-evaluates declared options; it is not an agent learning from reality |

## 8. Remaining tests (T1–T6)

T1: identify robust conditions under incomplete versus full observation, including information-cost constraints.  
T2: test the effect of additional *credible* observations and whether they can shrink **or expand** the perceived admissible region.  
T3: vary participant reference frames and the permissions/safeguards independently, avoiding conflation.  
T4: distinguish pairwise marginals, full histories, and genuinely third-party constraints.  
T5: compare with a full-joint-history baseline and conventional partial-observation planning under identical evidence and action sets.  
T6: supply independently inspectable criteria for CFV, substantive MU, reopening, and later-world consequences.

**Do not claim novelty or deployment readiness before T5/T6 and relevant empirical evaluation.**
