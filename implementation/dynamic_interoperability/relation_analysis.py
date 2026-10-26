"""Directional, evidence-bounded analysis of exchange trajectories.

This tracks *observed exchanges*, not the full ontological relation trajectory.
It does not infer intention, causality, convergence or agency.
"""
from dataclasses import dataclass
from collections import defaultdict
from interoperability import Ledger, Disposition


@dataclass(frozen=True)
class DirectionReport:
    source_id: str
    target_id: str
    exchanges: int
    claim_count: int
    preserved: int
    open_count: int
    tentative_count: int
    retention_rate: float | None
    trajectory_steps: tuple[tuple[int, int, int], ...]


def analyze(ledger: Ledger) -> list[DirectionReport]:
    pairs = defaultdict(list)
    for exchange in ledger.exchanges:
        pairs[(exchange.source_id, exchange.target_id)].append(exchange)
    results = []
    for (source, target), events in sorted(pairs.items()):
        events.sort(key=lambda e: (e.round, next(i for i,x in enumerate(ledger.exchanges) if x.id == e.id)))
        preserved = unresolved = claims_total = 0
        steps = []
        for e in events:
            claims_total += len(e.original)
            preserved += sum(a.disposition == Disposition.PRESERVED for a in e.assessments)
            unresolved += sum(a.disposition == Disposition.UNRESOLVED for a in e.assessments)
            steps.append((e.round, preserved, unresolved))
        results.append(DirectionReport(source, target, len(events), claims_total,
                                       preserved, claims_total - preserved, unresolved,
                                       preserved / claims_total if claims_total else None,
                                       tuple(steps)))
    return results


def compare_directions(ledger: Ledger) -> list[dict]:
    reports = {(r.source_id, r.target_id): r for r in analyze(ledger)}
    result = []
    for (a,b), forward in sorted(reports.items()):
        if (b,a) in reports and a < b:
            reverse = reports[b,a]
            result.append({"a_to_b": forward, "b_to_a": reverse,
                           "asymmetry": (forward.retention_rate - reverse.retention_rate)
                           if forward.retention_rate is not None and reverse.retention_rate is not None else None})
    return result
