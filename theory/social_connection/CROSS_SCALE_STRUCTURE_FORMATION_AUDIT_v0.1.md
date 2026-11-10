# IDOS Cross-Scale Structure-Formation Audit v0.1

**Status:** synthetic, reproducible minimal test; no empirical evidence of physical or social emergence; no IDOS-specific superiority established.

## Question
Can interactions and constraints among partially observed agents explain the creation, absence, and revision of relationally admissible opportunities, without reconstructing all agent internals?

## Prior basis and distinctions
- IDOS Connection Boundary Audit v0.1 supplies a finite-world, all-worlds permitted-action predicate. This note reuses it rather than introducing an independent social engine.
- Chemical reaction network theory relates graph/stoichiometric structure to constraints on dynamics **under explicit kinetic assumptions**. Its theorems are not imported as laws governing persons or institutions.
- Computational mechanics studies minimal predictive representations. Compression is not automatically justified by the mere existence of relational statistics.
- Higher-order information theory shows that three-way dependencies may not be determined by pairwise margins; this does not imply relational variables necessarily outperform a complete-history baseline.

## Minimal model
Let `W(o)` be all states compatible with an observation `o`. Let `A_i(w; R, B)` be actions allowed by actor `i` in world `w`, given relational protocol `R` and boundaries/consent `B`.

`G(o,R,B) = intersection over w in W(o), i in actors of A_i(w;R,B)`.

`G != empty` is **robust joint-action feasibility in the declared domain**, not proof of trust, mutual understanding, CFV, MU, or real-world connection.

Two hidden worlds have distinct required coordination actions (`left` and `right`) but the same public observation. An optional third actor `C` can offer a **predefined** mediated protocol; this protocol is jointly admissible only if C exists and both participating actors permit the option. Explicit public observation and explicit refusal are separately manipulated.

## Results from executed script

| Scenario | Robustly admissible actions | Conclusion within model |
| --- | --- | --- |
| Opaque pair; no mediator | none | possible in individual worlds, but no guarantee |
| Additional public observation | `left` | observation refines the world set |
| Third actor added without a protocol | none | topology alone is insufficient |
| Third actor + proposed protocol + consent | `mediated` | a relational protocol expands feasible actions |
| Same three-actor topology, protocol declined | none | permissions, not graph topology alone, determine feasibility |
| Protocol flag without mediator | none | institutional condition remains unsatisfied |

Ten unit tests passed; an exhaustive ordinary full-information planner produced **identical decisions in all 16 Boolean combinations** of signal, mediator, protocol and consent. The test is deterministic and synthetic; the generated action is explicitly coded, not autonomously discovered.

## Counterexample and interpretable proposition
Two networks can have the same graph structure yet different robust feasible action sets because consent/permission differs. Therefore, in this class of systems, a graph topology by itself is insufficient for determining social connection feasibility. This is a **model-specific counterexample**, not a newly discovered universal law.

## Causal caveats
- Adding a mediator and adding the protocol are not separable in the 'mediated' outcome unless the protocol is experimentally controlled. The ablation explicitly checks mediator-only and protocol-without-mediator conditions.
- The action set is externally enlarged; this does not establish spontaneous emergence, self-organization, chemical-style autocatalysis, or second-order generation-method evolution.
- A refusal may be legitimate even when a common feasible action exists; a feasibility guarantee does not compel adoption.
- No agent is independently running; the consent assertions are user-defined model inputs.
- A strong standard multi-agent planner with the same history and action space matches the IDOS predicate.

## Scientific next test (not yet conducted)
1. Test **predictive sufficiency under coarse-graining**: compare full event histories, pairwise summaries, hyperedge summaries, and IDOS provenance/residual/consent-aware summaries, all with equal training data; evaluate future connection-state forecasts out of sample.
2. Construct an independent three-agent simulator with asymmetric private observations, genuine local decision policies, and explicit opt-outs; disallow caller-declared successful updates.
3. Observe whether new actions are proposed endogenously, and preregister criteria distinguishing new feasible moves from recombinations of a fixed action menu.
4. Quantify relational changes in the *future reachable action set*, not simply connection status. Preserve the right to refuse and condition on the actor/authority boundary.
5. Compare with event sourcing + ordinary state-machine / multi-agent orchestration. Report ties as ties.

## Reproduction
Place `cross_scale_audit_v01.py` and `test_cross_scale_audit_v01.py` in `implementation/social_connection_architecture/` alongside the **existing** `connection_boundary_audit.py` from IDOS v0.1. Run:

```sh
python -m unittest -v test_cross_scale_audit_v01.py
python cross_scale_audit_v01.py > cross_scale_results_v01.json
```

Python standard library only. The data are synthetic. No change to MASTER_MAP v1.1, 12CDP or the thirteen conceptual equations is proposed.
