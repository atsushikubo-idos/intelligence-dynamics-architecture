"""IDOS relational value delta: bounded evidence of added value, not discovery proof.

Compare pre-registered baseline and composed candidates on identical held-out cases.
Keep distinct reference frames, relation history, losses, and rejected explanations.
No model calls or real-world interventions are performed.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Sequence
from math import isfinite


@dataclass(frozen=True)
class Case:
    case_id: str
    truth: float
    predictions: Mapping[str, float]
    relation_phase: str
    relation_ref: str
    evidence_ref: str
    def __post_init__(self):
        if not self.case_id or not self.relation_ref or not self.evidence_ref:
            raise ValueError('Case must have stable identity, relation and evidence reference')
        if not isfinite(self.truth) or any(not isfinite(p) for p in self.predictions.values()):
            raise ValueError('Case numbers must be finite')


@dataclass(frozen=True)
class RegisteredComparison:
    baseline_ids: tuple[str, ...]
    composition_id: str
    frame_ref: str
    metric: str = 'absolute_error'
    min_cases: int = 4
    min_gain: float = 0.0
    relation_change_label: str = 'after'
    def __post_init__(self):
        if not self.baseline_ids or self.composition_id in self.baseline_ids:
            raise ValueError('Distinct baseline(s) and composition required')
        if self.metric != 'absolute_error' or self.min_cases < 2 or self.min_gain < 0:
            raise ValueError('Unsupported metric or threshold')
        if not self.frame_ref:
            raise ValueError('Reference frame required')


@dataclass(frozen=True)
class DecisionEffect:
    """Precomputed paired outcomes for a prespecified, identical decision policy.

    Each value is an observed or simulated utility; the caller must qualify it.
    """
    case_id: str
    baseline_utility: float
    composition_utility: float
    evidence_ref: str


@dataclass(frozen=True)
class DeltaReport:
    status: str
    count: int
    baseline_mean_error: float | None
    composed_mean_error: float | None
    gain: float | None
    baseline_winner: str | None
    ablation_gains: Mapping[str, float]
    before_gain: float | None
    after_gain: float | None
    decision_delta: float | None
    decision_evidence: str
    unresolved: tuple[str, ...]
    old_frame_losses: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    statement: str


def evaluate(comparison: RegisteredComparison, cases: Sequence[Case], *,
             losses: Sequence[str] = (), decisions: Sequence[DecisionEffect] = (),
             decision_evidence: str = 'not_assessed') -> DeltaReport:
    """Analyze paired observations; no causal discovery or semantic novelty claim.

    Ablation gains report composition improvement over each single comparator.
    The best baseline (lowest MAE) is chosen on *these same cases*, which is
    descriptive and optimistic for selection; external confirmation is needed.
    """
    ids = [c.case_id for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate case IDs')
    required = set(comparison.baseline_ids) | {comparison.composition_id}
    for c in cases:
        if not required.issubset(c.predictions):
            raise ValueError(f'Missing paired predictions: {c.case_id}')
    if decision_evidence not in {'not_assessed', 'simulation', 'observed'}:
        raise ValueError('Invalid decision evidence status')
    if decisions and {d.case_id for d in decisions} != set(ids):
        raise ValueError('Decision effects must cover exactly the same cases')
    if len({d.case_id for d in decisions}) != len(decisions):
        raise ValueError('Duplicate decision effects')
    if any(not all(isfinite(v) for v in (d.baseline_utility,d.composition_utility)) or not d.evidence_ref for d in decisions):
        raise ValueError('Invalid decision effect')
    if decisions and decision_evidence == 'not_assessed':
        raise ValueError('Qualify decision evidence as simulation or observed')
    unresolved: list[str] = []
    if len(cases) < comparison.min_cases:
        unresolved.append('insufficient_paired_cases')
    if len({c.relation_ref for c in cases}) < 1:
        unresolved.append('relation_history_unavailable')
    mae = lambda model, subset: sum(abs(c.predictions[model]-c.truth) for c in subset)/len(subset)
    if not cases:
        return DeltaReport('insufficient_evidence',0,None,None,None,None,{},None,None,None,decision_evidence,
                           tuple(unresolved),tuple(losses),(), 'No paired evidence; no delta established.')
    errors = {m: mae(m,cases) for m in required}
    winner = min(comparison.baseline_ids,key=lambda m:errors[m])
    gain = errors[winner]-errors[comparison.composition_id]
    ablations = {m: errors[m]-errors[comparison.composition_id] for m in comparison.baseline_ids}
    before = [c for c in cases if c.relation_phase != comparison.relation_change_label]
    after = [c for c in cases if c.relation_phase == comparison.relation_change_label]
    if not before or not after:
        unresolved.append('missing_before_or_after_relation_phase')
    gain_phase = lambda group: mae(winner,group)-mae(comparison.composition_id,group) if group else None
    before_gain, after_gain = gain_phase(before), gain_phase(after)
    if gain <= comparison.min_gain:
        unresolved.append('no_positive_incremental_predictive_gain')
    if not all(v > comparison.min_gain for v in ablations.values()):
        unresolved.append('does_not_outperform_every_registered_baseline')
    if not decisions:
        unresolved.append('decision_value_not_tested')
    if decision_evidence == 'simulation':
        unresolved.append('decision_effect_only_simulated')
    unresolved += ['causality_not_identified','semantic_novelty_not_established',
                   'external_generalization_not_established']
    dd = (sum(d.composition_utility-d.baseline_utility for d in decisions)/len(decisions)) if decisions else None
    status = ('incremental_gain_observed_on_cases' if gain > comparison.min_gain and
              len(cases)>=comparison.min_cases and all(v>comparison.min_gain for v in ablations.values())
              else 'not_established')
    return DeltaReport(status,len(cases),errors[winner],errors[comparison.composition_id],gain,winner,
                       ablations,before_gain,after_gain,dd,decision_evidence,
                       tuple(unresolved),tuple(losses),
                       tuple(sorted({c.evidence_ref for c in cases}|{d.evidence_ref for d in decisions})),
                       'A paired descriptive comparison; neither relational causation nor novel discovery is demonstrated.')
