"""Conservative, executable bridge to IDOS Reference v1.1.

Run from repository root, or with repository root on PYTHONPATH.
No equivalence of domain concepts is asserted by this projection.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))
import idos_reference_v1_1 as core
from enterprise_trajectory_reference_v0_1 import EnterpriseTrajectoryModel

@dataclass
class BridgeResult:
    unit: core.UpdatingUnit
    source_to_core: dict[str, str] = field(default_factory=dict)
    caveats: list[str] = field(default_factory=list)


def bridge_enterprise(model: EnterpriseTrajectoryModel) -> BridgeResult:
    """Project explicit enterprise records onto IDOS core structures.

    The bridge deliberately does not infer Residuals, causal coupling, agency,
    future updateability, or completed Reopening from a textual event label.
    """
    first_frame = next(iter(model.frames.values()), None)
    frame = core.ReferenceFrame(
        name=first_frame.name if first_frame else 'Unspecified enterprise frame',
        assumptions=list(first_frame.assumptions) if first_frame else [],
        categories=list(first_frame.criteria) if first_frame else [],
    )
    unit = core.UpdatingUnit(
        name=model.label, unit_type='enterprise_observation', frame=frame,
        boundary=core.Boundary(included=['enterprise'], excluded=[]),
        possibility_space=core.PossibilitySpace(
            actions=[p for future in model.futures.values() for p in future.possibilities]
        ), trajectory=core.Trajectory(label=model.label),
    )
    out = BridgeResult(unit=unit, caveats=[
        'Projection, not proof of conceptual equivalence or scientific validity.',
        'Relation revisions are recorded as provenance, not inferred as Coupling or Agency.',
        'Reopening event labels are not a completed Q2 reopening assessment.',
        'Future candidates are not predictions or ranked alternatives.',
        'Explicit enterprise residuals map to diagnostic core Residuals; no automatic classification.',
    ])
    if first_frame:
        out.source_to_core[first_frame.id] = frame.id
    previous_frame = first_frame
    for next_frame in list(model.frames.values())[1:]:
        if previous_frame and next_frame.previous_id != previous_frame.id:
            raise ValueError('Nonlinear reference-frame history cannot be projected as a single revision chain')
        frame = frame.revise(
            name=next_frame.name,
            add_assumptions=[x for x in next_frame.assumptions if x not in frame.assumptions],
            remove_assumptions=[x for x in frame.assumptions if x not in next_frame.assumptions],
            add_categories=[x for x in next_frame.criteria if x not in frame.categories],
            remove_categories=[x for x in frame.categories if x not in next_frame.criteria],
        )
        out.source_to_core[next_frame.id] = frame.id
        previous_frame = next_frame
    if frame.id != unit.frame.id:
        unit.update(core.UpdateLevel.L3, 'Explicit enterprise reference-frame revision', new_frame=frame)
    for rel in model.relations.values():
        unit.trajectory.provenance.append(core.ProvenanceEvent(
            event_type='enterprise_relation_revision',
            description=f'{rel.kind}: {rel.description}',
            source_ids=[rel.id] + ([rel.previous_id] if rel.previous_id else []) + list(rel.evidence_ids),
        ))
    for ev in model.events:
        if ev.process in ('Reality', 'Reality Prime'):
            contact = core.RealityContact(
                source='enterprise_record:' + ev.id, observation=ev.description,
                mode='documented_observation',
            )
            unit.contact_reality(contact)
            out.source_to_core[ev.id] = contact.id
        elif ev.process == 'Difference':
            diff = core.Difference(description=ev.description)
            out.source_to_core[ev.id] = diff.id
            unit.trajectory.provenance.append(core.ProvenanceEvent(
                event_type='enterprise_difference_unclassified',
                description=ev.description, source_ids=[ev.id, diff.id] + list(ev.evidence_ids),
            ))
        elif ev.process == 'Residual':
            if not ev.explicit_residual:
                raise ValueError('Residual classification must be explicit')
            diff = core.Difference(description=f'Enterprise-classified source difference: {ev.description}')
            residual = core.Residual(description=ev.description, difference=diff)
            unit.residuals[residual.id] = residual
            out.source_to_core[ev.id] = residual.id
            unit.trajectory.provenance.append(core.ProvenanceEvent(
                event_type='enterprise_explicit_residual', description=ev.description,
                source_ids=[ev.id, residual.id] + list(ev.evidence_ids),
            ))
        else:
            unit.trajectory.provenance.append(core.ProvenanceEvent(
                event_type='enterprise_' + ev.process.lower().replace(' ', '_'),
                description=ev.description, source_ids=[ev.id] + list(ev.evidence_ids),
            ))
    for source_residual, reason in model.holdings.items():
        core_id = out.source_to_core.get(source_residual)
        if core_id is None or core_id not in unit.residuals:
            raise ValueError('Holding references unmapped residual')
        unit.hold([unit.residuals[core_id]], reason=reason)
    for decision in model.decisions:
        unit.trajectory.provenance.append(core.ProvenanceEvent(
            event_type='enterprise_governance_' + decision.action,
            description=f'{decision.actor}: {decision.rationale}',
            source_ids=[decision.id] + list(decision.evidence_ids),
        ))
    return out


def complete_reopening_after_recontact(result: BridgeResult, *, source: str,
    observation: str, assessment: core.FutureUpdateabilityAssessment,
    action: core.ReopeningAction, basis: str, decision_rule_reopened: str):
    """Explicit caller-supplied Q2 decision, never inferred from event labels."""
    result.unit.recontact(core.RealityContact(source=source, observation=observation))
    return result.unit.reopen(assessment=assessment, action=action, basis=basis,
        decision_rule_reopened=decision_rule_reopened)
