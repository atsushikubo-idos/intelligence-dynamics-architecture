"""IDOS experimental connection-continuity layer (v0.3).

Pure, event-sourced orchestration over existing connection-boundary v0.1/v0.2.
No authentication, semantic understanding, learning, agent execution, or
validated CFV/MU is implied. All scenario assertions are caller-supplied.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Mapping, Sequence
from connection_boundary_audit import World, boundary
from connection_boundary_comparative_v02 import (
    Challenge, Response, verification_opportunity,
    UpdateOpportunity, mutual_update_opportunity,
)

CHOICES = frozenset({'adopt', 'hold', 'reject'})


@dataclass(frozen=True)
class Difference:
    difference_id: str
    explanation: str
    actor: str
    provenance: str
    shared: bool = True


@dataclass(frozen=True)
class FrameInput:
    """A snapshot of declared inputs, not a discovered real-world truth."""
    tick: int
    domain: str
    actors: tuple[str, ...]
    observation: tuple[str, ...]
    worlds: tuple[World, ...]
    actions: tuple[str, ...]
    choices: Mapping[str, str]
    verification: Mapping[str, bool]  # auditable verification opportunities only
    update_paths: tuple[UpdateOpportunity, ...]
    differences: tuple[Difference, ...] = ()
    reality_contact: bool = True  # caller-attested freshness, never independently established
    provenance: str = ''


@dataclass(frozen=True)
class Event:
    event_id: str
    tick: int
    kind: str
    detail: Mapping[str, object]
    provenance: str
    shared: bool


@dataclass(frozen=True)
class Snapshot:
    tick: int
    domain: str
    feasibility: str
    guaranteed_actions: tuple[str, ...]
    connection: str
    reason_codes: tuple[str, ...]
    choice_by_actor: Mapping[str, str]
    unresolved_differences: tuple[str, ...]
    recheck_of: int | None
    reality_contact_declared: bool
    verification_paths_declared: bool
    mutual_paths_recorded: bool


class ConnectionContinuity:
    """Append-only decision history; caller-controlled events, no side effects.

    A snapshot is the declared, domain-scoped assessment at one tick. The
    ``reopen`` operation NEVER recalculates old snapshots with later evidence.
    New observations or permissions only appear in a new tick via ``assess``.
    """

    def __init__(self):
        self._events: list[Event] = []
        self._snapshots: list[Snapshot] = []
        self._unresolved: dict[str, Difference] = {}
        self._private_difference_ids: set[str] = set()
        self._next_id = 1
        self._last_tick = -1

    def _record(self, tick: int, kind: str, detail: Mapping[str, object],
                provenance: str, shared: bool = True) -> None:
        eid = f'continuity:{self._next_id:04d}'
        self._next_id += 1
        self._events.append(Event(eid, tick, kind, dict(detail), provenance, shared))

    def assess(self, inp: FrameInput, *, recheck_of: int | None = None) -> Snapshot:
        if inp.tick <= self._last_tick:
            raise ValueError('Ticks must be strictly increasing; past snapshots are immutable')
        if not inp.provenance.strip():
            raise ValueError('Declared input provenance required')
        if not inp.actors or len(set(inp.actors)) != len(inp.actors):
            raise ValueError('Nonempty distinct actors required')
        if not inp.domain or not inp.actions or not inp.worlds:
            raise ValueError('Domain, actions and world assumptions required')
        if set(inp.choices) != set(inp.actors) or any(c not in CHOICES for c in inp.choices.values()):
            raise ValueError('Explicit adopt/hold/reject choice required from every actor')
        if set(inp.verification) != set(inp.actors):
            raise ValueError('Explicit verification opportunity assertion required for every actor')
        if recheck_of is not None and not any(s.tick == recheck_of for s in self._snapshots):
            raise ValueError('Recheck must point to a preceding snapshot')
        diff_ids = [d.difference_id for d in inp.differences]
        if len(set(diff_ids)) != len(diff_ids) or any(not d.difference_id or not d.provenance for d in inp.differences):
            raise ValueError('Differences require unique IDs and provenance')
        if any(d.difference_id in self._unresolved or any(
            e.kind == 'difference_declared' and e.detail.get('difference_id') == d.difference_id
            for e in self._events) for d in inp.differences):
            raise ValueError('Difference IDs may not be reused')

        b = boundary(inp.worlds, inp.domain, inp.actors, inp.observation, inp.actions)
        mu = mutual_update_opportunity(inp.update_paths, inp.actors)
        all_verify = all(inp.verification.values())
        any_reject = any(choice == 'reject' for choice in inp.choices.values())
        any_hold = any(choice == 'hold' for choice in inp.choices.values())
        reasons = []
        if b.status == 'IMPOSSIBLE':
            reasons.append('NO_JOINTLY_PERMITTED_ACTION')
        elif b.status == 'POSSIBLE_NOT_GUARANTEED':
            reasons.append('OBSERVATIONAL_AMBIGUITY')
        if any_reject:
            reasons.append('ACTOR_REJECTION')
        if any_hold:
            reasons.append('ACTOR_HOLD')
        if not all_verify:
            reasons.append('VERIFICATION_PATH_INCOMPLETE')
        if not mu['bilateral_paths_preserved']:
            reasons.append('MUTUAL_UPDATE_PATH_INCOMPLETE')
        if not inp.reality_contact:
            reasons.append('REALITY_CONTACT_UNCONFIRMED')

        # Deliberately separate robust feasibility from the actors' choice.
        # No mandatory adoption, and a hold is NOT conflated with a rejection.
        if b.status == 'IMPOSSIBLE':
            state = 'INFEASIBLE'
        elif b.status == 'POSSIBLE_NOT_GUARANTEED':
            state = 'UNCERTAIN'
        elif any_reject:
            state = 'DECLINED'
        elif any_hold:
            state = 'DEFERRED'
        elif not all_verify or not mu['bilateral_paths_preserved'] or not inp.reality_contact:
            state = 'CONDITIONAL'
        else:
            state = 'CONNECTED_PROXY'

        for d in inp.differences:
            self._unresolved[d.difference_id] = d
            if not d.shared:
                self._private_difference_ids.add(d.difference_id)
            self._record(inp.tick, 'difference_declared', {
                'difference_id': d.difference_id,
                # Private explanations must not enter the public event record.
                'explanation': d.explanation if d.shared else '[withheld]',
                'actor': d.actor}, d.provenance, d.shared)
        snap = Snapshot(inp.tick, inp.domain, b.status, b.guaranteed_actions,
                        state, tuple(reasons), dict(inp.choices),
                        tuple(self._unresolved), recheck_of, inp.reality_contact,
                        all_verify, mu['bilateral_paths_preserved'])
        self._snapshots.append(snap)
        self._last_tick = inp.tick
        self._record(inp.tick, 'assessment', {
            'domain': inp.domain, 'feasibility': b.status, 'connection': state,
            'reason_codes': list(reasons), 'recheck_of': recheck_of,
            'unresolved_ids': [k for k in self._unresolved if k not in self._private_difference_ids],
            'private_unresolved_count': sum(k in self._private_difference_ids for k in self._unresolved)},
            inp.provenance)
        return snap

    def assess_from_bridge(self, bridge: object, inp: FrameInput,
                           *, recheck_of: int | None = None) -> Snapshot:
        """Attach an assessment to the actual SocialConnectionV03 instance.

        Require recorded actor decisions and a matching round; use original
        v0.3 records instead of reproducing their implementation. A verification
        flag supplied in FrameInput remains an *assertion*, not a bridge proof.
        """
        from social_connection_v03_bridge import SocialConnectionV03
        if not isinstance(bridge, SocialConnectionV03):
            raise TypeError('Expected an actual SocialConnectionV03 bridge')
        if bridge.core.tick != inp.tick:
            raise ValueError('Bridge and boundary audit must share the same tick')
        if set(inp.actors) != set(bridge.core.actors):
            raise ValueError('All registered bridge actors must be accounted for')
        for actor in inp.actors:
            decisions = [d for d in bridge.core.actors[actor].decision_history
                         if d['tick'] == inp.tick]
            if not decisions or decisions[-1]['disposition'] != inp.choices.get(actor):
                raise ValueError(f'Actor choice not consistent with bridge history: {actor}')
        snap = self.assess(inp, recheck_of=recheck_of)
        public_links = [{'type': item['type'], 'id': item['id']}
                        for item in bridge.links if item.get('tick') == inp.tick]
        self._record(inp.tick, 'linked_v03_bridge_records',
                     {'linked_record_ids': public_links,
                      'source_is_actual_v03_bridge': True,
                      'bridge_approvals_and_evidence_not_authenticated': True},
                     inp.provenance)
        return snap

    def record_verification(self, tick: int, challenge: Challenge, response: Response,
                            public_evidence: Sequence[str], *, provenance: str) -> Mapping[str, object]:
        if tick != self._last_tick or not provenance:
            raise ValueError('Verification must reference current tick and provenance')
        result = verification_opportunity(challenge, response, public_evidence)
        # The result is an opportunity proxy. Do not equate to semantic truth.
        self._record(tick, 'verification_opportunity', {
            'challenger': challenge.challenger, 'respondent': challenge.respondent,
            'claim': challenge.claim, 'challenge_addressed': result['challenge_addressed'],
            'missing_public_evidence': result['missing_public_evidence'],
            'semantic_equivalence_verified': False}, provenance)
        return result

    def resolve_difference(self, difference_id: str, *, tick: int,
                           evidence_provenance: str, actor: str) -> None:
        if tick != self._last_tick or not evidence_provenance or not actor:
            raise ValueError('Resolution requires current tick and attributable evidence')
        d = self._unresolved.pop(difference_id, None)
        if d is None:
            raise KeyError('Unknown or already resolved difference')
        self._record(tick, 'difference_resolution_attested', {
            'difference_id': difference_id, 'actor': actor,
            'resolution_is_caller_attested': True}, evidence_provenance, d.shared)
        # Existing snapshot is immutable. Next assessment reflects this change.

    @property
    def history(self) -> tuple[Snapshot, ...]:
        return tuple(self._snapshots)

    def reopen(self, tick: int, *, include_private: bool = False) -> Mapping[str, object]:
        matches = [s for s in self._snapshots if s.tick == tick]
        if not matches:
            raise KeyError('Unknown historical tick')
        # include_private never releases private content; this argument is
        # intentionally not an authorization mechanism.
        events = [asdict(e) for e in self._events if e.tick <= tick and e.shared]
        snapshot = asdict(matches[0])
        snapshot['unresolved_differences'] = [k for k in snapshot['unresolved_differences']
                                             if k not in self._private_difference_ids]
        snapshot['private_differences_withheld'] = True
        return {'historic_snapshot': snapshot, 'available_public_events': events,
                'private_events_withheld': sum(1 for e in self._events if e.tick <= tick and not e.shared),
                'later_events_excluded': True, 'authorization_to_reveal_private': False}

    def public_trace(self) -> list[dict]:
        return [asdict(e) for e in self._events if e.shared]


def synthetic_lifecycle() -> Mapping[str, object]:
    """One synthetic trajectory across uncertain, refusal, and reconnectable states."""
    from connection_boundary_audit import make_world
    actors = ('human', 'ai', 'organization')
    actions = ('plan_a', 'plan_b')
    def world(key, obs, a, b, c):
        return make_world(key, obs, {'human': a, 'ai': b, 'organization': c})
    ambiguous = (world('w1', ('same',), {'plan_a'}, {'plan_a'}, {'plan_a'}),
                 world('w2', ('same',), {'plan_b'}, {'plan_b'}, {'plan_b'}))
    known = (world('w1', ('known_a',), {'plan_a'}, {'plan_a'}, {'plan_a'}),)
    def paths(h='adopt', a='adopt', o='adopt'):
        return tuple(UpdateOpportunity(actor, f'frame_{actor}', 'candidate', True, True, choice,
                                        f'trace:{actor}:{choice}')
                     for actor, choice in zip(actors, (h,a,o)))
    def inp(tick, obs, worlds, choices, diffs=()):
        return FrameInput(tick, 'decision', actors, obs, worlds, actions,
                          choices, {i: True for i in actors},
                          paths(*[choices[i] for i in actors]), diffs,
                          True, f'synthetic:scenario:{tick}')
    engine = ConnectionContinuity()
    engine.assess(inp(0, ('same',), ambiguous, {i: 'hold' for i in actors},
                      (Difference('meaning-gap', 'Interpretations differ', 'human', 'synthetic:human'),)))
    engine.assess(inp(1, ('known_a',), known, {'human':'reject', 'ai':'adopt', 'organization':'adopt'}), recheck_of=0)
    engine.assess(inp(2, ('known_a',), known, {i: 'adopt' for i in actors}), recheck_of=1)
    reopened_before = engine.reopen(0)
    engine.resolve_difference('meaning-gap', tick=2, actor='human', evidence_provenance='synthetic:review')
    engine.assess(inp(3, ('known_a',), known, {i: 'adopt' for i in actors}), recheck_of=2)
    return {'research_status':'synthetic scenario / architecture trace only',
            'transitions': [asdict(s) for s in engine.history],
            'historic_reopening_before_resolution': reopened_before,
            'public_events': engine.public_trace(),
            'claim':'No tested superiority over full-history baselines and no real agent connection.'}


if __name__ == '__main__':
    import json
    print(json.dumps(synthetic_lifecycle(), indent=2, ensure_ascii=False))
