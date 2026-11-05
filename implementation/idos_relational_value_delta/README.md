# IDOS — Relational Value Delta (prototype v0.2)

**Purpose:** Ask whether combining independently developed models reveals an incrementally useful difference, beyond the best prespecified standalone model, without mistaking a descriptive improvement for causal emergence.

This module is deliberately **not** another reference-frame generator. It evaluates externally supplied candidates on identical cases and preserves relation-trajectory references, evidence references, losses and unresolved claims.

## Input / output

- Input: registered baselines, candidate composition, shared evaluation frame, paired held-out case predictions, relation phase and trace, evidence pointers, optional matched decision utilities.
- Output: best-baseline versus composed model error, per-baseline ablation comparison, before/after relation-phase descriptive deltas, optional decision utility delta, retained losses and explicitly unresolved interpretations.
- Outcome label `incremental_gain_observed_on_cases` indicates **only** a positive within-case predictive delta against each supplied baseline. It is not proof of a novel metric, discovery, causal relational effect, or generalization.

## Run

`python -m unittest discover -s . -p 'test_*.py' -v`

## Intended connection to existing IDOS

- `implementation/discovery_architecture/emergent_engine`: supplies proposed metrics or candidate observations, not proof of novelty.
- `implementation/discovery_architecture/idos_bridge.py`: supplies traceable relation IDs and frame IDs; adaptation must be done explicitly (not silently assumed).
- `src/idos_reference_v1_2.py`: remains unmodified.
- Future independent evaluator: register split and criteria *before* seeing test observations; use holdout or prospective data; randomize or control interventions where possible; report uncertainty and costs; require external human authorization.

## Boundaries

The prototype does **not** invent a composition, detect semantic novelty, learn a relation trajectory, perform actions, estimate uncertainty, establish causal influence, or outperform the global research frontier. A phase comparison can reflect selection bias or confounding. A single benchmark may hide subgroup harms. Model-selection on the evaluated cases is optimistic. For a genuine “+α” result, independently confirm the comparison on newly collected cases, including decision quality, costs and old-frame losses.

## v0.2 — explicit Discovery boundary

`discovery_adapter.py` adds a **non-invasive**, trace-linked connection from
`implementation/discovery_architecture/emergent_engine/composed_cycle.py`
(`ComposedCycle.step()` events) to the independent evaluator.

1. Extract event provenance using `provenance_from_events(events, relation_ref=..., evidence_ref=...)`.
2. Independently prepare paired `EvaluatedObservation` records, containing observed
   truth and all preregistered model predictions, plus an exact Discovery `record_hash`.
3. Call `evaluate_discovery_delta(comparison, provenance, observations, losses=...)`.

The adapter **refuses** unlinked evaluation records and unapproved/rejected candidate
frames. It never turns an engine's self-reported sensor value into ground truth.
An approved frame means *authorized for a local cycle*, not scientifically valid.
No action is executed by the adapter. Source modules remain unchanged.

### Integration location

Place this folder at `implementation/relational_value_delta/` in the IDOS repo.
The adapter imports only its sibling evaluator; the Discovery engine's existing
JSON-like event schema is consumed at the boundary (no dependency or import-cycle).

### Validation caveat

The predictive baseline winner is selected on the supplied cases, so selection
bias remains. Phase gains are descriptive and not causal; prospective holdouts,
uncertainty, subgroup harm, costs, and policy counterfactuals remain future work.
