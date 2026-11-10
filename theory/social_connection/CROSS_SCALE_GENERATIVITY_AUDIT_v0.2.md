# IDOS Cross-Scale Generativity Audit v0.2

**Status:** Experimental research note; synthetic, non-peer-reviewed. 2026-11-11.

## Research question
Can interaction between independently proposed, complementary capabilities form a new action-generation **rule**, and can a subsequent observed failure change that rule while preserving consent, refusal and provenance? Does a relational IDOS representation outperform a fully informed conventional baseline?

## Existing context and placement
This is an *incremental audit* over `cross_scale_audit_v01.py` (v0.1), not a new IDOS core or new law. It concerns the Social Connection application layer. It does not modify `MASTER_MAP v1.1`, 12CDP or the thirteen conceptual equations.

## Methods
Two distinct hidden worlds require mutually incompatible existing actions (`left`, `right`). The action `verified_mediation` is neither in the prior candidate set nor explicitly proposed by one actor. A independently offers a **verification capability** and B a **mediation capability**, each with a provenance string and explicit consent. A transparent, *pre-existing* composition grammar assembles these into the `composed_verify_then_mediate` rule. A robust cross-world action is available only if the complementary offers, positive consent and authorization are all present. Explicit veto, missing evidence and missing authorization block the action.

A deliberately simple deterministic second-stage feedback policy suspends a failing rule. A new, consented recovery capability offered by C permits the rule to be revised to `recovery_gated_mediation`, and the revision retains all evidence provenance. This **does not** autonomously discover the underlying composition grammar. It is an explicit, bounded, testable transition.

The comparison baseline gets **exactly the same** offers, constraints, compositional grammar and hidden-world conditions. It independently enumerates actions; it does not call the IDOS functions. All 16 combinations of proposal presence, B consent, and authorization are checked for agreement. This is not a statistical trial or evidence of superior performance.

## Results
- Previously, with old actions only, no single action was robust in both hidden worlds.
- Independent complementary proposals yielded the `verified_mediation` rule and one robust action under declared authorization.
- Neither proposal alone, an unrelated offer, a veto, missing evidence, missing authorization, nor B's refusal yielded a robust mediated action.
- A failed rule was suspended; a fresh consenting C recovery proposal generated a revision with retained A/B/C provenance.
- A same-information conventional baseline produced the identical robust-action set for **16/16** configurations.
- **26/26 unit tests passed** (10 v0.1 plus 16 v0.2), in the supplied test environment.

## Interpretation / falsification limits
A new *instantiated rule relative to the system's prior enacted repertoire* is not an unbounded novel principle or a newly discovered meta-rule. The allowed action symbols, proposal kinds, composition grammar and feedback-revision logic were all predefined by a programmer. These examples do **not** establish nontrivial self-generation of reference-frame generators, a new probability distribution over generators, real agent autonomy, substantial CFV/MU, or an emergent social ontology. The known full-history baseline is equally capable. The code contains no external observations, independently operating agents or scientific validation of generalized novelty.

## Next stringent experiment
Use independently operating participants with disjoint private information and explicit consent; give an equally resourced baseline identical messages and permissible tools. Separate novelty of **outcome**, **action rule**, and **generator of rules**. Measure out-of-sample transfer, failure/recovery, genuine choice and veto, unrepresented contingencies, provenance completeness and retained future update paths. Pre-register operational measures and negative controls. Never interpret the absence of a currently known representation as evidence of fundamentally unrepresentable possibilities.

## Run
From a directory containing `connection_boundary_audit.py`, `cross_scale_audit_v01.py`, `cross_scale_generativity_v02.py` and both corresponding tests:

```
python -m unittest -v test_cross_scale_audit_v01 test_cross_scale_generativity_v02
python cross_scale_generativity_v02.py > results_v02.json
```

This overlay uses existing v0.1 dependencies; it is not a self-contained reproduction of the full IDOS repository.
