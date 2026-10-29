"""Explicit boundary between Discovery traces and independently evaluated value deltas.

Nothing here manufactures truth labels, predictions, decisions, or causal claims.
The adapter consumes immutable, audited Discovery cycle events and separately
provided matched evaluation observations. No changes to Reference/Discovery code.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Sequence
from relational_value_delta import Case, RegisteredComparison, DecisionEffect, DeltaReport, evaluate


@dataclass(frozen=True)
class DiscoveryProvenance:
    event_hash: str
    cycle: int
    frame_before: str
    frame_after: str
    candidate_expression: str
    review_status: str
    source_type: str
    relation_ref: str
    evidence_ref: str


@dataclass(frozen=True)
class EvaluatedObservation:
    case_id: str
    truth: float
    predictions: Mapping[str, float]
    relation_phase: str
    discovery_event_hash: str
    evidence_ref: str


def provenance_from_events(events: Sequence[Mapping], *, relation_ref: str,
                           evidence_ref: str) -> tuple[DiscoveryProvenance, ...]:
    """Extract trace pointers, without treating any generated frame as validated."""
    if not relation_ref or not evidence_ref:
        raise ValueError('Relation and evidence IDs required')
    seen = set()
    result = []
    for e in events:
        fields = ('record_hash', 'cycle', 'frame_before', 'frame_after', 'review_status', 'source_type')
        if any(k not in e for k in fields):
            raise ValueError('Incomplete discovery event')
        h = e['record_hash']
        if not isinstance(h, str) or not h or h in seen:
            raise ValueError('Missing or duplicate record hash')
        seen.add(h)
        result.append(DiscoveryProvenance(
            h, e['cycle'], e['frame_before'], e['frame_after'],
            e.get('generated_expression') or '', e['review_status'],
            e['source_type'], relation_ref, evidence_ref))
    return tuple(result)


def evaluate_discovery_delta(comparison: RegisteredComparison,
                             provenance: Sequence[DiscoveryProvenance],
                             observations: Sequence[EvaluatedObservation], *,
                             losses: Sequence[str] = (),
                             decisions: Sequence[DecisionEffect] = (),
                             decision_evidence: str = 'not_assessed') -> DeltaReport:
    """Evaluate externally supplied paired evidence linked to Discovery traces.

    Reject missing provenance and unreviewed candidates. 'authorized' is only
    evidence of local authorization, NOT correctness or novel value.
    """
    traces = {p.event_hash: p for p in provenance}
    if len(traces) != len(provenance):
        raise ValueError('Duplicate provenance hash')
    for obs in observations:
        p = traces.get(obs.discovery_event_hash)
        if p is None:
            raise ValueError(f'Unlinked evaluation observation: {obs.case_id}')
        if p.review_status not in ('authorized', 'approved'):
            raise ValueError(f'Non-authorized discovery candidate: {obs.case_id}')
    cases = [Case(o.case_id, o.truth, o.predictions, o.relation_phase,
                  traces[o.discovery_event_hash].relation_ref, o.evidence_ref)
             for o in observations]
    report = evaluate(comparison, cases, losses=losses, decisions=decisions,
                      decision_evidence=decision_evidence)
    # Preserve all original cautions and indicate the provenance source.
    from dataclasses import replace
    return replace(report, unresolved=tuple(dict.fromkeys((*report.unresolved,
        'discovery_candidate_not_proof_of_new_value',
        'trace_link_does_not_establish_relational_causation'))),
        evidence_refs=tuple(sorted(set(report.evidence_refs) |
            {p.evidence_ref for p in provenance if any(o.discovery_event_hash == p.event_hash for o in observations)})))
