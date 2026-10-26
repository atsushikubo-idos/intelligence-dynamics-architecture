"""Narrow CDP interoperability check for AI governance (not a second IDOS reference).

Optional: load the existing src/idos_reference_v1_2.py via normal Python import.
This adapter does not construct frames, translate values, or determine consent.
"""
from dataclasses import dataclass
from typing import Mapping, Tuple
from governance import CoexistenceGovernor, Proposal, Outcome, Decision

@dataclass(frozen=True)
class ConnectionEvidence:
    actor_ids: Tuple[str, ...]
    unit_ids: Tuple[str, ...]
    trajectory_ids: Tuple[str, ...]
    frames: Tuple[str, ...]
    translation_residuals: Tuple[str, ...]
    purpose: str


def describe_connection(actor_ids: Tuple[str, ...], units_by_actor: Mapping[str, object], purpose: str) -> ConnectionEvidence:
    """Use the real Reference v1.2 CDP for descriptions and directional translations.

    A description is NOT an active link or proof of semantic understanding.
    """
    from idos_reference_v1_2 import CommonDynamicsProtocol
    if len(actor_ids) < 2 or len(set(actor_ids)) != len(actor_ids):
        raise ValueError('two or more distinct actors are required')
    if any(a not in units_by_actor for a in actor_ids):
        raise ValueError('missing registered IDOS updating unit')
    cdp = CommonDynamicsProtocol()
    desc = [cdp.describe(units_by_actor[a]) for a in actor_ids]
    residuals = []
    for i, source in enumerate(desc):
        for j, target in enumerate(desc):
            if i != j:
                translation = cdp.translate(source, actor_ids[j])
                residuals.append(f'{actor_ids[i]} -> {actor_ids[j]}: {translation["translation_residual"]}')
    return ConnectionEvidence(actor_ids, tuple(d.unit_id for d in desc),
                              tuple(d.trajectory_id for d in desc),
                              tuple(d.frame_name for d in desc), tuple(residuals), purpose)


def assess_with_cdp(governor: CoexistenceGovernor, proposal: Proposal,
                    units_by_actor: Mapping[str, object], *, approvals: Tuple[str, ...] = ()) -> tuple[Outcome, ConnectionEvidence | None]:
    """Governance remains primary. Heterogeneous affected groups need a CDP description.

    Missing CDP evidence gives REVIEW, not automatic permission or an exception.
    """
    outcome = governor.assess(proposal, approvals=approvals)
    ids = tuple(dict.fromkeys((proposal.proposer_id,) + proposal.affected_actor_ids))
    kinds = {governor.actors[x].kind for x in ids}
    if len(kinds) < 2:
        return outcome, None
    try:
        evidence = describe_connection(ids, units_by_actor, proposal.purpose)
    except (ImportError, KeyError, ValueError, AttributeError, TypeError) as exc:
        if outcome.decision == Decision.ALLOW:
            outcome = Outcome(Decision.REVIEW, ('Heterogeneous connection not described by Reference CDP',),
                              outcome.objections, outcome.dissenting_frames,
                              'Provide Reference v1.2 CDP descriptions and retain translation limits')
        governor._record('cdp_description_unavailable', proposal_id=proposal.proposal_id, error_type=type(exc).__name__)
        return outcome, None
    governor._record('cdp_interoperability_checked', proposal_id=proposal.proposal_id,
                     actor_ids=list(ids), unit_ids=list(evidence.unit_ids),
                     translation_residuals=list(evidence.translation_residuals))
    return outcome, evidence
