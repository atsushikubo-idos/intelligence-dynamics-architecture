# IDOS Connection Boundary Comparative Audit v0.2

**Status:** Experimental / synthetic / not peer-reviewed  
**Target:** Social Connection Architecture v0.3, extending Connection Boundary Audit v0.1.  
**Scope:** T5 (fair information-matched baseline comparison) and T6 (observable CFV/MU pathways and Reopening).  
**No changes** to MASTER_MAP v1.1, the 12CDP vocabulary, or the thirteen conceptual equations.

## 1. Research question

Can heterogeneous actors that do not fully observe each other's internal states maintain an auditable and permission-respecting route to connection, challenge, independent choice and future reopening? If so, does IDOS offer any demonstrated advantage over an ordinary baseline with identical full historical information?

The finite-world model's notion of connection is **joint permissibility of an action across worlds observationally consistent with a shared observation**. It is not human mutual understanding, trust, actual collaboration, or proof of CFV/MU in lived social relations.

## 2. Existing results retained

Connection Boundary Audit v0.1 defines `GUARANTEED`, `POSSIBLE_NOT_GUARANTEED`, and `IMPOSSIBLE`; demonstrates temporal changes from more observation to an actor's refusal and later restored permission; and constructs the XOR vs independent triple-distribution counterexample. These are established mathematical examples and controlled synthetic behaviors, not novel theorems.

## 3. T5: Independent fair baseline

`independent_full_information_baseline` reconstructs the robust joint action set directly from exactly the **same** finite worlds, observation, actors and permitted action sets as `connection_boundary_audit.boundary`. It does not call `boundary` internally. It is a full-information reference and should be expected to equal the IDOS-style decision. The tests verify this in four documented scenarios and **all 256** possible two-world/two-actor/two-action acceptance profiles (each actor's acceptance set being one of four subsets).

**Observed result:** full-information reference and IDOS boundary classifications and guaranteed actions agree in all four named cases and all 256 enumerated configurations. There is **no performance or prediction advantage established** for IDOS.

The `recency_only_baseline` intentionally drops all but the last compatible world and incorrectly labels an ambiguity scenario `GUARANTEED`. This illustrates information loss. **It is not a strong conventional baseline and does not demonstrate IDOS superiority.**

The comparison is finite, deterministic and correctness-oriented; it does not benchmark latency, resource use, semantic adequacy or a state-of-the-art multi-agent orchestration system.

## 4. T6: Operational traces, not semantic verification

- **CFV-related test proxy:** an actor can issue an addressed challenge and another actor can return explicitly disclosed, authorized public evidence with a recorded acknowledgment. Missing/private evidence and the wrong respondent fail. A positive outcome means only that the evidence request was addressed; it does not prove claim truth, frame equivalence or understanding.
- **MU-related test proxy:** each actor must have an independently recorded, permissioned, traceable path to choose adopt / hold / reject. A forced or missing actor pathway fails. A human can reject while an AI adopts and the system retains both traces. This is not demonstrated substantive bilateral learning.
- **Reopening:** reconstruction of a past requested field uses only the public, provenance-bearing records available at the requested historic tick. Private values and evidence recorded at later ticks remain missing; no hindsight reconstruction.

The audit uses caller-provided assertions and synthetic records. Authentication, actual mental states, causal influence, and real consent have not been demonstrated.

## 5. Exact reproduction

From `implementation/social_connection_architecture/` in a complete repository checkout:

```bash
python -m unittest -q test_connection_boundary_audit test_connection_boundary_comparative_v02 test_social_connection_legacy test_integration test_external_bridges
python connection_boundary_comparative_v02.py > connection_boundary_results_v02.json
```

In the reconstructed repository workspace tested on 2026-11-10, **75 tests passed**, comprising 15 v0.1 tests, 15 v0.2 tests, and 45 existing Social Connection v0.3 tests. The old three-module regression suites (109 tests) are not part of this 75-test invocation. The exhaustive 256-configuration parity check is one of the 15 new v0.2 test methods, not 256 additional counted unittest cases.

`connection_boundary_results_v02.json` holds the deterministic example results. Run tests from the code directory and retain the checked-in adjacent `implementation/` source dependencies for the v0.3 integration tests.

## 6. Interpretation / novelty restraint

**Established in this audit:** a tractable and reproducible way to distinguish robust task-specific joint permission, incomplete information, dissent, historical reinspection and independently recorded update opportunities.

**Not established:** mathematical novelty, that a relation-state variable is indispensable, improved prediction versus an equally informed baseline, actual CFV, actual MU, social emergence, autonomous discovery of new reference frames, safe real-world governance, or the claim that three agents are universally minimal.

**Next falsifiable step:** independent human/AI/organization actors; authenticated and scoped permissions; a pre-registered outcome measure of independently useful challenges; longitudinal actual frame changes; equivalent-information event-sourced multi-agent baseline; blinded evaluation of failures and downstream reconfiguration. Compare architectural auditability and recovery while holding evidence, authority and observation windows constant.

## 7. Relation to core IDOS

The Social Connection application layer is distinct from the IDOS Core, consistent with MASTER_MAP v1.1. The Core is not revised. CFV, MU, effective influence, reconfiguration capacity, exit/recovery and reality contact remain requirements to be operationalized rather than quantities proven by the current test suite. Refusal or non-connection may be a legitimate autonomy-preserving outcome, not an error to optimize away.
