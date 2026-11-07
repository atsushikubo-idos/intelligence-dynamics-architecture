"""IDOS Social Connection Architecture v0.2.

Extension of v0.1: authorization, relational trajectory, frame-sensitive
minimal representations, external reopening, audit of presentation, and
multiple non-mandatory structural hypotheses. Standard library only.

All agents are simulated; scientific novelty and real-world CFV/MU are unproven.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from collections import Counter
from typing import Any
import math
import json
from social_connection import SocialConnection, Actor, Evidence, Candidate

@dataclass(frozen=True)
class AuditObservation:
    tick: int
    actor_id: str
    native_frame: str
    key: str
    value: float | None
    provenance: str
    permission: str

@dataclass(frozen=True)
class ContrastiveQuestion:
    id: str
    tick: int
    observed_keys: tuple[str, ...]
    disagreement: tuple[str, ...]
    text: str
    status: str = 'open'

@dataclass
class FrameView:
    name: str
    fields: tuple[str, ...]
    tick: int
    values: dict[str, float]
    source_ids: tuple[str, ...]
    valid: bool
    missing: tuple[str, ...] = ()

@dataclass
class ExternalOffer:
    id: str
    tick: int
    actor_id: str
    key: str
    value: float
    provenance: str
    approvals: dict[str, bool] = field(default_factory=dict)
    accepted: bool = False

class SocialConnectionV02(SocialConnection):
    def __init__(self):
        super().__init__()
        self.audit_observations: list[AuditObservation] = []
        self.frame_views: list[FrameView] = []
        self.questions: list[ContrastiveQuestion] = []
        self.offers: dict[str, ExternalOffer] = {}
        self.presentation_events: list[dict[str, Any]] = []
        self.candidate_history: list[dict[str, Any]] = []
        self.distribution_history: list[dict[str, Any]] = []
        self.frame_requirements: dict[str, tuple[str, ...]] = {
            'runway_only': ('cash_runway',),
            'runway_and_growth': ('cash_runway', 'growth'),
            'expanded_external': ('cash_runway', 'growth', 'handoff_risk'),
        }

    def observe(self, evidence: Evidence):
        super().observe(evidence)
        actor = self.actors[evidence.actor_id]
        # Never store private numeric data in audit or event log; original Evidence
        # stays in the actor-owned record store for consent-restricted retrieval.
        self.audit_observations.append(AuditObservation(
            evidence.tick, evidence.actor_id, actor.native_frame, evidence.key,
            evidence.value if evidence.shared else None, evidence.source,
            'shared' if evidence.shared else 'withheld'))

    def _conflicted_keys(self, tick: int) -> set[str]:
        seen: dict[str, float] = {}
        conflicts: set[str] = set()
        for e in self.evidence:
            if e.tick == tick and e.shared:
                if e.key in seen and not math.isclose(e.value, seen[e.key], abs_tol=1e-9):
                    conflicts.add(e.key)
                else:
                    seen.setdefault(e.key, e.value)
        return conflicts

    def verified_shared_values(self, tick: int | None = None) -> dict[str, float]:
        t = self.tick if tick is None else tick
        conflicts = self._conflicted_keys(t)
        vals: dict[str, float] = {}
        for e in self.evidence:
            if e.tick == t and e.shared and e.key not in conflicts:
                vals[e.key] = e.value
        return vals

    def record_relational_state(self) -> dict[str, Any]:
        """Empirical actor-by-decision distribution, not posterior over methods."""
        decisions = [(a.id, d) for a in self.actors.values() for d in a.decision_history
                     if d['tick'] == self.tick]
        n = len(decisions)
        counter = Counter(d['disposition'] for _,d in decisions)
        tick_dist = {x: counter[x] / n for x in ('adopt', 'hold', 'reject')} if n else {}
        pair_differences = []
        for k,(i,a) in enumerate(decisions):
            for j,b in decisions[k+1:]:
                if (a['option'],a['disposition']) != (b['option'],b['disposition']):
                    pair_differences.append([i,j])
        state = {'tick': self.tick, 'choice_distribution': tick_dist,
                 'disagreement_pairs': pair_differences,
                 'observation_keys': sorted(self.verified_shared_values()),
                 'conflicted_keys': sorted(self._conflicted_keys(self.tick)),
                 'note': 'empirical finite record; not metaphysical emergence'}
        self.distribution_history.append(state)
        self._log('relational_state_recorded', pairs=len(pair_differences))
        return state

    def evaluate_candidate(self, frame_id: str) -> dict[str,Any]:
        candidate = self.candidates[frame_id]
        current = dict(candidate.validation)
        if not current or current.get('tick') != self.tick:
            raise ValueError('Candidate not evaluated at current tick')
        event = {'tick': self.tick, 'frame_id': frame_id,
                 'evaluation': current.copy(), 'derived_from': list(candidate.derived_from)}
        # Record immutable snapshots; next round must not overwrite history.
        self.candidate_history.append(event)
        self._log('candidate_evaluation_archived', frame_id=frame_id)
        return event

    def capture_frame(self, name: str) -> FrameView:
        """Snapshot a compact, frame-dependent view; unknowns stay unknown."""
        if name not in self.frame_requirements:
            raise KeyError('Unknown observation frame')
        fields = self.frame_requirements[name]
        values = self.verified_shared_values()
        if 'cash_runway' in fields and 'cash' in values and values.get('burn',0)>0:
            values['cash_runway'] = values['cash'] / values['burn']
        vals = {k:values[k] for k in fields if k in values}
        missing = tuple(k for k in fields if k not in vals)
        sources = tuple(sorted({e.source for e in self.evidence if e.tick==self.tick and e.shared
                                and e.key in ('cash','burn') + fields}))
        view = FrameView(name, fields, self.tick, vals, sources, not missing, missing)
        self.frame_views.append(view)
        self._log('frame_projection', frame=name, valid=view.valid, missing=list(missing))
        return view

    def check_equivalence(self, old: FrameView, requested: str) -> dict[str,Any]:
        """Can old compact representation answer the NEW frame without archive?"""
        required = self.frame_requirements[requested]
        missing = [x for x in required if x not in old.values]
        result = {'old_frame':old.name, 'requested_frame':requested, 'tick':old.tick,
                  'equivalent':old.valid and not missing,
                  'missing_in_projection':missing, 'can_reopen_archive':True}
        self._log('equivalence_check', **result)
        return result

    def reopen_frame(self, old_tick: int, requested: str) -> FrameView:
        """Reconstruct solely from historic authorized shared evidence, no hindsight."""
        if requested not in self.frame_requirements:
            raise KeyError(requested)
        fields = self.frame_requirements[requested]
        data = self.verified_shared_values(old_tick)
        if 'cash_runway' in fields and 'cash' in data and data.get('burn',0)>0:
            data['cash_runway'] = data['cash']/data['burn']
        vals = {k:data[k] for k in fields if k in data}
        missing = tuple(k for k in fields if k not in vals)
        sources = tuple(sorted({e.source for e in self.evidence if e.tick==old_tick and e.shared
                                and e.key in ('cash','burn')+fields}))
        view = FrameView(requested,fields,old_tick,vals,sources,not missing,missing)
        self.frame_views.append(view)
        self.reopenings.append({'tick':self.tick, 'historic_tick':old_tick,
                                'reason':'observation_frame_changed',
                                'new_frame':requested,'missing':list(missing)})
        self._log('reopen_historical_frame', historic_tick=old_tick, new_frame=requested,
                  missing=list(missing))
        return view

    def formulate_question(self, *, reason: str) -> ContrastiveQuestion:
        missing = ['unknown_relation']
        if self._conflicted_keys(self.tick):
            missing = sorted(self._conflicted_keys(self.tick))
        dissenters = tuple(sorted(a.id for a in self.actors.values() if a.decision_history
                                 and a.decision_history[-1]['tick']==self.tick))
        q = ContrastiveQuestion(f'question_{self.tick}_{len(self.questions)}',self.tick,
                                tuple(sorted(self.verified_shared_values())), dissenters,
                                f'Which independently checkable and permitted observations '
                                f'could distinguish {reason}?')
        self.questions.append(q)
        self._log('question_formed', question=q.id, trigger=reason)
        return q

    def offer_external(self, offer: ExternalOffer):
        if offer.tick != self.tick: raise ValueError('Offer tick mismatch')
        if offer.actor_id not in self.actors: raise ValueError('Unknown external provider')
        if offer.id in self.offers: raise ValueError('Duplicate offer')
        self.offers[offer.id] = offer
        self._log('external_offer', id=offer.id, key=offer.key, provider=offer.actor_id,
                  provenance=offer.provenance, no_value_disclosed=True)

    def authorize_offer(self, offer_id: str, actor_id: str, approved: bool):
        if actor_id not in self.actors: raise KeyError(actor_id)
        offer = self.offers[offer_id]
        offer.approvals[actor_id] = approved
        self._log('offer_authorization', offer=offer_id, actor=actor_id, approved=approved)

    def accept_offer(self, offer_id: str, required: tuple[str,...]) -> bool:
        offer = self.offers[offer_id]
        if offer.accepted: raise ValueError('Offer already accepted')
        if not all(offer.approvals.get(a, False) for a in required):
            self._log('offer_withheld', offer=offer_id, reason='missing_approval')
            return False
        if not self.actors[offer.actor_id].can_share:
            self._log('offer_withheld', offer=offer_id, reason='provider_permission')
            return False
        self.observe(Evidence(offer.actor_id,self.tick,offer.key,offer.value,offer.provenance,True))
        offer.accepted = True
        self._log('external_observation_admitted', offer=offer_id, key=offer.key)
        return True

    def present_options(self, to_actor: str, ranking: list[str] | None = None):
        """Record presentation framing; return options but never call actor.decide()."""
        if to_actor not in self.actors: raise KeyError(to_actor)
        ranking = list(self.candidates) if ranking is None else ranking
        if not set(ranking).issubset(self.candidates): raise ValueError('Unknown frame')
        event = {'tick':self.tick,'actor':to_actor,'order':list(ranking),
                 'risk':'presentation may influence actor decision',
                 'no_automatic_selection':True}
        self.presentation_events.append(event)
        self._log('possibilities_presented', actor=to_actor, order=list(ranking))
        return event

    def snapshot(self) -> dict:
        d = super().snapshot()
        d['Representation']['current_relational_state'] = self.distribution_history[-1] if self.distribution_history else None
        d['Representation']['frame_projections'] = [asdict(v) for v in self.frame_views]
        d['Residual'] += [{'event':'conflicting_evidence','tick':self.tick,'keys':sorted(self._conflicted_keys(self.tick))}] if self._conflicted_keys(self.tick) else []
        d['Holding']['evaluated_candidate_history'] = list(self.candidate_history)
        d['Holding']['withheld_count'] = sum(o.permission=='withheld' for o in self.audit_observations)
        d['Possibility Space']['questions'] = [asdict(q) for q in self.questions]
        d['Possibility Space']['external_offers'] = [{'id':o.id,'key':o.key,'accepted':o.accepted,
                                                       'approvals':dict(o.approvals)} for o in self.offers.values()]
        d['Limit'].extend(['Observation frame reconstitution only from past shared evidence',
                           'Empirical relation frequencies != structural posterior',
                           'External observation does not imply autonomous invention',
                           'Ranking or presentation can influence actors'])
        return d


def integrated_demo() -> dict:
    s=SocialConnectionV02()
    s.register(Actor('human','human','growth_and_people',('growth','people')))
    s.register(Actor('ai','ai','uncertainty_and_options',('uncertainty',)))
    s.register(Actor('org','organization','cash_continuity',('cash',)))
    s.observe(Evidence('human',0,'growth',.8,'human:market',True))
    s.observe(Evidence('org',0,'cash',10.,'org:ledger',True))
    s.observe(Evidence('org',0,'burn',2.5,'org:forecast',True))
    s.observe(Evidence('human',0,'confidential',42.,'human:withheld',False))
    s.decide('human','expand','adopt',reason='jobs')
    s.decide('ai','pilot','hold',reason='risk')
    s.decide('org','expand','reject',reason='runway')
    relation0=s.record_relational_state()
    s.explore()
    s.evaluate_candidate('cash_runway')
    s.update_hypotheses()
    initial=s.capture_frame('runway_only')
    invalid=s.check_equivalence(initial,'runway_and_growth')
    reopened=s.reopen_frame(0,'runway_and_growth')
    cfv=s.cfv_review('ai',{'actor_id':'org','key':'cash','value':10.})
    s.present_options('human',['cash_runway'])
    s.update_actor('human','cash_runway',actor_approved=False)
    s.update_actor('ai','cash_runway',actor_approved=True)
    s.update_actor('org','cash_runway',actor_approved=True)
    s.contact_reality('unexpected',note='intervention-sensitive future assumptions')
    first=s.snapshot()
    s.next_round()
    s.observe(Evidence('human',1,'growth',.7,'human:revision',True))
    s.observe(Evidence('org',1,'cash',7.,'org:ledger',True))
    s.observe(Evidence('org',1,'burn',3.5,'org:forecast',True))
    s.decide('human','expand','hold',reason='wait')
    s.decide('ai','pilot','adopt',reason='reversible')
    s.decide('org','expand','reject',reason='cash')
    s.record_relational_state()
    q=s.formulate_question(reason='unexpected change in relationship and cash')
    s.offer_external(ExternalOffer('external_1',1,'org','handoff_risk',.4,'org:independent_review'))
    s.authorize_offer('external_1','human',True)
    s.authorize_offer('external_1','ai',True)
    s.authorize_offer('external_1','org',True)
    accepted=s.accept_offer('external_1',('human','ai','org'))
    s.explore()
    s.evaluate_candidate('cash_runway')
    new_view=s.capture_frame('expanded_external')
    # The old archive cannot retroactively invent the newly observed external field.
    old_reopened=s.reopen_frame(0,'expanded_external')
    return {'project':'IDOS Social Connection Architecture v0.2',
            'relational_distribution_t0':relation0,
            'posterior_t1':dict(s.hypothesis_weights),
            'equivalence_break':invalid,
            'reopen_historical_success':reopened.valid,
            'old_external_field_missing':list(old_reopened.missing),
            'cfv':cfv,'external_accepted':accepted,'new_frame_valid':new_view.valid,
            'agent_frames':{a.id:list(a.adopted_frames) for a in s.actors.values()},
            'questions':[asdict(q)],'round_0':first,'round_1':s.snapshot(),
            'events':s.events}

if __name__=='__main__':
    print(json.dumps(integrated_demo(),ensure_ascii=False,indent=2))
