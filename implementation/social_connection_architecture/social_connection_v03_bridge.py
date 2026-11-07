"""IDOS Social Connection v0.3: actual adapters to the repository's existing modules.

NO external action is performed. The adapters deliberately do not claim semantic
understanding, causation, authenticated consent, or autonomous frame emergence.
Run the sample from the repository root or this directory.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import importlib.util
import sys

from social_connection import Actor, Evidence
from social_connection_v02 import SocialConnectionV02

IMPL = Path(__file__).resolve().parents[1]


def _existing_module(relative_file: str, unique_name: str):
    """Load actual sibling module by its checked-in file path, not a copied implementation."""
    location = (IMPL / relative_file).resolve()
    if not location.is_file() or not location.is_relative_to(IMPL):
        raise FileNotFoundError(f"Existing IDOS module unavailable: {relative_file}")
    if unique_name in sys.modules:
        return sys.modules[unique_name]
    spec = importlib.util.spec_from_file_location(unique_name, location)
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = module  # dataclasses and Enum depend on this registration
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(unique_name, None)
        raise
    return module


_interop = _existing_module('dynamic_interoperability/interoperability.py', 'idos_sca_existing_interoperability')
_discovery = _existing_module('discovery_architecture/discovery_architecture.py', 'idos_sca_existing_discovery')
_governance = _existing_module('coexistence_governance/governance.py', 'idos_sca_existing_governance')


@dataclass(frozen=True)
class BridgeLinks:
    """IDs of records that are actually present in the respective source modules."""
    exchange_id: str
    discovery_record_id: str | None = None
    governance_proposal_id: str | None = None


class SocialConnectionV03:
    """One social-connection session with live adapters to three pre-existing modules."""
    def __init__(self, core: SocialConnectionV02 | None = None):
        self.core = core if core is not None else SocialConnectionV02()
        self.exchange_ledger = _interop.Ledger()
        self.discovery_cycles: dict[str, Any] = {}
        self.governor: Any = None
        self.links: list[dict] = []
        self.bridge_events: list[dict] = []

    def register(self, actor: Actor):
        if self.governor is not None:
            raise RuntimeError('Register actors before starting governance')
        self.core.register(actor)

    def activate_governance(self):
        if not self.core.actors:
            raise ValueError('Register actors first')
        self.governor = _governance.CoexistenceGovernor([
            _governance.Actor(a.id, a.kind, a.native_frame, True)
            for a in self.core.actors.values()
        ])

    def _shared_evidence(self, actor_id: str, refs: tuple[str, ...]) -> None:
        if actor_id not in self.core.actors:
            raise ValueError('Unknown actor')
        if not self.core.actors[actor_id].can_share:
            raise PermissionError('Actor has not enabled sharing')
        if not refs:
            raise ValueError('At least one attributable shared source required')
        known = {e.source for e in self.core.evidence if e.actor_id == actor_id
                 and e.shared and e.tick == self.core.tick}
        if any(ref not in known for ref in refs):
            raise PermissionError('Evidence is not in current authorized shared records')

    def translate(self, source_id: str, target_id: str, *, message: str,
                  evidence_refs: tuple[str, ...], reviewer: str,
                  disposition: str = 'unresolved', review_evidence: str = '',
                  previous_exchange_id: str | None = None):
        """Perform a REAL Ledger.record; never infer semantic fidelity automatically.

        A reviewer may DECLARE a disposition with a written basis. This declaration
        is not a proof of correct translation or equal understanding.
        """
        self._shared_evidence(source_id, evidence_refs)
        if target_id not in self.core.actors or reviewer not in self.core.actors:
            raise ValueError('Target and reviewer must be registered')
        if target_id == source_id:
            raise ValueError('Distinct actors required')
        state = _interop.Disposition(disposition)
        claim = _interop.Claim(f'{source_id}:{self.core.tick}:{len(self.exchange_ledger.exchanges)}',
                               message, source_id, self.core.actors[source_id].native_frame)
        if state in (_interop.Disposition.PRESERVED, _interop.Disposition.ALTERED,
                     _interop.Disposition.OMITTED) and not review_evidence.strip():
            raise ValueError('Determinate assessments need an explicit review basis')
        assessment = _interop.Assessment(claim.id, state, review_evidence,
                                         reviewer if review_evidence.strip() else '')
        previous = next((e for e in self.exchange_ledger.exchanges if e.id == previous_exchange_id), None)
        if previous_exchange_id and (previous is None or previous.source_id != source_id
                                     or previous.target_id != target_id):
            raise ValueError('Previous exchange must have the same direction')
        item = self.exchange_ledger.record(
            round=self.core.tick + 1, source_id=source_id, target_id=target_id,
            source_frame=self.core.actors[source_id].native_frame,
            target_frame=self.core.actors[target_id].native_frame,
            source_trajectory=f'{source_id}:t{self.core.tick}',
            target_trajectory=f'{target_id}:t{self.core.tick}',
            original=[claim], translated=message,
            assessments=[assessment], cdp_quality='structural_adapter_only',
            cdp_residual='semantic fidelity not verified by this adapter',
            declared_by=reviewer, previous_exchange_id=previous_exchange_id)
        self.links.append({'type':'exchange','id':item.id,'shared_refs':list(evidence_refs),
                           'source':source_id,'target':target_id,'tick':self.core.tick})
        self.bridge_events.append({'event':'interop_exchange','id':item.id,
                                   'assessment':state.value})
        return item

    def begin_discovery(self, cycle_id: str, *, question: str, baseline_frame_id: str):
        if cycle_id in self.discovery_cycles:
            raise ValueError('Duplicate discovery ID')
        cycle = _discovery.DiscoveryCycle(question=question,
                    relation_trajectory_id=cycle_id, baseline_frame_id=baseline_frame_id)
        self.discovery_cycles[cycle_id] = cycle
        self.bridge_events.append({'event':'discovery_opened','id':cycle_id})
        return cycle

    def propose_after_observed_change(self, cycle_id: str, *, actor_id: str,
                                      intervention: str, observation: str,
                                      evidence_refs: tuple[str, ...],
                                      candidate_id: str, reason: str):
        """Records an externally attested *performed* action, NOT execution by IDOS.

        Caller attests that the intervention took place; provenance is retained.
        This prototype cannot independently authenticate the attestation.
        """
        self._shared_evidence(actor_id, evidence_refs)
        if candidate_id not in self.core.candidates:
            raise ValueError('Proposal must refer to a core candidate')
        if not self.core.candidates[candidate_id].validation:
            raise ValueError('Core candidate has not been evaluated')
        cycle = self.discovery_cycles[cycle_id]
        performed = cycle.intervene(intervention, evidence_ids=evidence_refs, performed=True)
        difference = cycle.difference(observation, after=performed,
                     evidence_ids=evidence_refs, status=_discovery.EvidenceStatus.OBSERVED)
        proposed = cycle.propose_frame(candidate_id, reason, based_on=difference)
        self.links.append({'type':'discovery_proposal','id':proposed.id,
                           'candidate_id':candidate_id,'cycle_id':cycle_id,
                           'evidence_refs':list(evidence_refs),'tick':self.core.tick})
        self.bridge_events.append({'event':'discovery_proposal','id':proposed.id,
                                   'candidate_id':candidate_id})
        return performed, difference, proposed

    def assess_governance(self, proposal_id: str, *, proposer_id: str,
                          affected: tuple[str, ...], action: str,
                          approvals: tuple[str, ...] = (), risk: str = 'unknown',
                          reversible: bool = True, evidence_refs: tuple[str, ...] = (),
                          possible_losses: tuple[str,...] = ()):
        if self.governor is None:
            raise RuntimeError('Activate governance first')
        if any(ref not in {e.source for e in self.core.evidence if e.shared
                           and e.tick == self.core.tick} for ref in evidence_refs):
            raise PermissionError('Unknown or non-shared evidence source')
        proposal = _governance.Proposal(proposal_id,proposer_id,affected,
                        'social_connection',action,reversible,risk,
                        evidence_refs,(), possible_losses)
        result = self.governor.assess(proposal,approvals=approvals)
        self.links.append({'type':'governance','id':proposal_id,'decision':result.decision.value,
                           'tick':self.core.tick,'evidence_refs':list(evidence_refs)})
        self.bridge_events.append({'event':'governance_assessment','proposal_id':proposal_id,
                                   'decision':result.decision.value,
                                   'no_execution':True})
        return result

    def recontact(self, cycle_id: str, frame_proposal_record: Any, *,
                  finding: str, evidence_refs: tuple[str, ...],
                  actor_id: str, review: str = 'insufficient'):
        self._shared_evidence(actor_id, evidence_refs)
        cycle = self.discovery_cycles[cycle_id]
        result = cycle.recontact(frame_proposal_record, finding, evidence_ids=evidence_refs,
                                 judgment=_discovery.ReviewStatus(review))
        self.links.append({'type':'discovery_recontact','id':result.id,
                           'cycle_id':cycle_id,'evidence_refs':list(evidence_refs),
                           'tick':self.core.tick})
        return result

    def snapshot(self) -> dict:
        result=self.core.snapshot()
        # expose ONLY permitted exchange content and IDs, not private observations
        result['ExternalModuleIntegration'] = {
            'dynamic_interoperability': self.exchange_ledger.snapshot(),
            'discovery_architecture': {key:{'question':cycle.question,
                'baseline_frame_id':cycle.baseline_frame_id,
                'records':[{'id':r.id,'kind':r.kind,'statement':r.statement,
                            'source_ids':r.source_ids,'evidence_ids':r.evidence_ids}
                           for r in cycle.records],
                'candidate_frames':list(cycle.candidate_frame_ids),
                'reviews':{k:v.value for k,v in cycle.reviews.items()}}
                for key,cycle in self.discovery_cycles.items()},
            'coexistence_governance': {'assessments':list(self.governor.audit)
                                         if self.governor else []},
            'links':list(self.links),'bridge_events':list(self.bridge_events),
            'limitations':['No external actions executed',
             'Caller-supplied approvals and attestation are not authenticated',
             'Reviewer-declared translation assessment is not semantic truth',
             'Proposals and governance eligibility do not force actor adoption']}
        return result


def integrated_demo() -> dict:
    s=SocialConnectionV03()
    s.register(Actor('human','human','growth_and_employment',('growth','people')))
    s.register(Actor('ai','ai','uncertainty_and_experimentation',('uncertainty',)))
    s.register(Actor('org','organization','cash_continuity',('cash',)))
    s.activate_governance()
    c=s.core
    c.observe(Evidence('human',0,'growth',.8,'human:market',True))
    c.observe(Evidence('org',0,'cash',10.,'org:ledger',True))
    c.observe(Evidence('org',0,'burn',2.5,'org:forecast',True))
    c.observe(Evidence('org',0,'private',77.,'org:private',False))
    c.decide('human','expand','adopt',reason='growth')
    c.decide('ai','experiment','hold',reason='uncertainty')
    c.decide('org','expand','reject',reason='liquidity')
    exchange=s.translate('org','human',message='Cash runway risk is significant',
        evidence_refs=('org:ledger','org:forecast'),reviewer='human',
        disposition='unresolved')
    c.record_relational_state()
    c.explore()
    c.evaluate_candidate('cash_runway')
    cycle=s.begin_discovery('relation_runway',question='How does cash risk change joint choices?',
                            baseline_frame_id='growth_only')
    _,_,frame=s.propose_after_observed_change('relation_runway',actor_id='org',
                intervention='Reported forecasting review by organization',
                observation='Runway constraint became visible to participants',
                evidence_refs=('org:ledger','org:forecast'),
                candidate_id='cash_runway',reason='Cross-frame cash continuity reference')
    # All affected approvals; high/unknown risk still goes to REVIEW, not ALLOW.
    assessment=s.assess_governance('g1',proposer_id='ai',
                  affected=('human','org'),action='propose external pilot',
                  risk='unknown',approvals=('human','org'),
                  evidence_refs=('org:forecast',))
    c.present_options('human',['cash_runway'])
    c.update_actor('human','cash_runway',actor_approved=False)
    c.update_actor('ai','cash_runway',actor_approved=True)
    c.update_actor('org','cash_runway',actor_approved=True)
    c.next_round()
    c.observe(Evidence('org',1,'cash',7.,'org:ledger:t1',True))
    c.observe(Evidence('org',1,'burn',3.5,'org:forecast:t1',True))
    # New evidence must be real to the simulation's tick; old data not backfilled.
    again=s.recontact('relation_runway',frame,
                    finding='Runway declined in the following period',
                    evidence_refs=('org:ledger:t1','org:forecast:t1'),actor_id='org',
                    review='supported')
    return {'version':'v0.3 bridged integration','exchange_id':exchange.id,
            'governance':assessment.decision.value,
            'discovery_recontact_id':again.id,
            'adopted_frames':{a.id:list(a.adopted_frames) for a in c.actors.values()},
            'interface':s.snapshot()}

if __name__ == '__main__':
    import json
    print(json.dumps(integrated_demo(),ensure_ascii=False,indent=2))
