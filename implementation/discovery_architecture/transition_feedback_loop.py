"""Trace a post-transition comparison back into DiscoveryConditions.

This does not claim to discover a new frame automatically. A fresh, external
recontact is explicitly supplied; the output is a *proposal* to change the
conditions of the next observation, not a new accepted evaluation criterion.
"""
from dataclasses import dataclass
from discovery_architecture import Record, ReviewStatus
from generation_conditions import (ConditionAxis, DiscoveryConditions,
                                   GenerationConditionChange)
from post_transition_reassessment import Reassessment, ReassessmentStatus


@dataclass(frozen=True)
class FeedbackResult:
    reassessment_status: ReassessmentStatus
    recontact_record_id: str
    condition_change_id: str
    candidate: GenerationConditionChange


def propose_followup(reassessment: Reassessment, *, discovery_bridge,
                     frame_proposal: Record, conditions: DiscoveryConditions,
                     external_evidence_ids: tuple[str, ...], observer: str,
                     authorization_refs: tuple[str, ...] = ()) -> FeedbackResult:
    """Create a traceable *next observation* proposal; never apply or adopt.

    Only evidence not used in the original reassessment counts as recontact.
    The caller remains responsible for evidence authenticity and semantics.
    """
    if conditions.cycle is not discovery_bridge.cycle:
        raise ValueError('DiscoveryConditions must share the discovery cycle')
    if frame_proposal.id not in discovery_bridge._geneses:
        raise ValueError('Proposal must originate from the discovery bridge')
    if not observer.strip() or not external_evidence_ids or any(not x.strip() for x in external_evidence_ids):
        raise ValueError('A named observer and external evidence references are required')
    if not set(external_evidence_ids).isdisjoint(reassessment.evidence_ids):
        raise ValueError('Recontact must not recycle reassessment evidence')
    if reassessment.old_frame_id != discovery_bridge.baseline_frame_id:
        raise ValueError('Old frame must match discovery baseline')
    if reassessment.new_frame_id not in discovery_bridge.registry.frames:
        raise ValueError('Reassessed new frame must be registered')

    # A regression is not proof that B is wrong. A compatible result is not
    # proof that B is universally better. All outcomes permit further inquiry.
    pending = sorted(reassessment.old_only | reassessment.unresolved)
    gained = sorted(reassessment.new_only)
    finding = (f'Post-transition {reassessment.status.value}; '
               f'old-only/unresolved={pending}; new-only={gained}; '
               'external recontact reported; causal meaning not established')
    record = discovery_bridge.recontact(
        frame_proposal, finding, evidence_ids=external_evidence_ids,
        observer=observer, judgment=ReviewStatus.INSUFFICIENT)
    change = GenerationConditionChange(
        axis=ConditionAxis.DISTINCTION_RULE,
        before=f'Comparison under {reassessment.old_frame_id} and {reassessment.new_frame_id}',
        after=f'Next observation explicitly contrasts preserved and emergent distinctions after {reassessment.new_frame_id}',
        rationale=f'Post-transition status={reassessment.status.value}; recontact record={record.id}',
        intended_observation='Test whether old-only, new-only and unresolved distinctions persist under fresh observations',
        possible_blind_spots=tuple(pending + gained) or ('Unobserved changes outside both frames',),
        comparison_condition=f'Repeat observations with both {reassessment.old_frame_id} and {reassessment.new_frame_id}; retain both outputs',
        authorization_refs=authorization_refs,
    )
    conditions.propose(change, based_on=record)
    return FeedbackResult(reassessment.status, record.id, change.id, change)
