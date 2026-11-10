"""Synthetic regression tests for connection-continuity v0.3."""
import unittest
from connection_boundary_audit import make_world
from connection_boundary_comparative_v02 import UpdateOpportunity, Challenge, Response
from connection_continuity_v03 import (
    ConnectionContinuity, FrameInput, Difference, synthetic_lifecycle
)

ACTORS=('human','ai')
ACTIONS=('a','b')


def worlds(*, uncertain=False, conflict=False):
    first=make_world('w1',('same',),{'human':{'a'},'ai':{'b'} if conflict else {'a'}})
    if uncertain:
        second=make_world('w2',('same',),{'human':{'b'},'ai':{'b'}})
        return (first,second)
    return (first,)


def frame(t, worldset=None, *, choices=None, verification=None, paths=True,
          differences=(), reality=True, provenance='synthetic:fixture'):
    cs=choices or {'human':'adopt','ai':'adopt'}
    opp=tuple(UpdateOpportunity(i,f'old:{i}','new',True,True,cs.get(i,'adopt'),f'trace:{t}:{i}')
              for i in ACTORS) if paths else ()
    return FrameInput(t,'decision',ACTORS,('same',),worldset or worlds(),ACTIONS,cs,
                      verification if verification is not None else {i:True for i in ACTORS},
                      opp,differences,reality,provenance)


class ContinuityTests(unittest.TestCase):
    def test_connected_proxy(self):
        s=ConnectionContinuity().assess(frame(0))
        self.assertEqual(('GUARANTEED','CONNECTED_PROXY'),(s.feasibility,s.connection))

    def test_uncertainty_is_not_refusal(self):
        s=ConnectionContinuity().assess(frame(0,worlds(uncertain=True)))
        self.assertEqual('UNCERTAIN',s.connection)
        self.assertIn('OBSERVATIONAL_AMBIGUITY',s.reason_codes)
        self.assertNotIn('ACTOR_REJECTION',s.reason_codes)

    def test_impossibility_distinct_from_rejection(self):
        s=ConnectionContinuity().assess(frame(0,worlds(conflict=True)))
        self.assertEqual('INFEASIBLE',s.connection)
        self.assertIn('NO_JOINTLY_PERMITTED_ACTION',s.reason_codes)

    def test_refusal_while_feasible(self):
        s=ConnectionContinuity().assess(frame(0, choices={'human':'reject','ai':'adopt'}))
        self.assertEqual('GUARANTEED',s.feasibility)
        self.assertEqual('DECLINED',s.connection)
        self.assertIn('ACTOR_REJECTION',s.reason_codes)

    def test_hold_is_not_reject(self):
        s=ConnectionContinuity().assess(frame(0, choices={'human':'hold','ai':'adopt'}))
        self.assertEqual('DEFERRED',s.connection)
        self.assertNotIn('ACTOR_REJECTION',s.reason_codes)

    def test_missing_verification_is_conditional(self):
        s=ConnectionContinuity().assess(frame(0,verification={'human':False,'ai':True}))
        self.assertEqual('CONDITIONAL',s.connection)
        self.assertIn('VERIFICATION_PATH_INCOMPLETE',s.reason_codes)

    def test_missing_mutual_paths_is_conditional(self):
        s=ConnectionContinuity().assess(frame(0,paths=False))
        self.assertEqual('CONDITIONAL',s.connection)
        self.assertIn('MUTUAL_UPDATE_PATH_INCOMPLETE',s.reason_codes)

    def test_reality_unconfirmed_is_conditional(self):
        s=ConnectionContinuity().assess(frame(0,reality=False))
        self.assertEqual('CONDITIONAL',s.connection)
        self.assertIn('REALITY_CONTACT_UNCONFIRMED',s.reason_codes)

    def test_immutability_and_recheck(self):
        e=ConnectionContinuity()
        original=e.assess(frame(0,choices={'human':'reject','ai':'adopt'}))
        next_s=e.assess(frame(1),recheck_of=0)
        self.assertEqual('DECLINED',original.connection)
        self.assertEqual('CONNECTED_PROXY',next_s.connection)
        self.assertEqual('DECLINED',e.reopen(0)['historic_snapshot']['connection'])
        self.assertEqual(0,next_s.recheck_of)
        self.assertTrue(e.reopen(0)['later_events_excluded'])
        self.assertTrue(all(x['tick']==0 for x in e.reopen(0)['available_public_events']))

    def test_private_differences_are_not_disclosed(self):
        e=ConnectionContinuity()
        e.assess(frame(0,differences=(Difference('p1','SECRET CONTENT','human','private:source',False),)))
        self.assertNotIn('SECRET CONTENT',str(e.public_trace()))
        self.assertNotIn('p1',str(e.public_trace()))
        self.assertNotIn('p1',str(e.reopen(0)))
        self.assertNotIn('SECRET CONTENT',str(e.reopen(0)))
        self.assertEqual(1,e.reopen(0)['private_events_withheld'])

    def test_unresolved_differences_persist_then_resolution_attested(self):
        e=ConnectionContinuity()
        e.assess(frame(0,differences=(Difference('gap','difference','human','a:1'),)))
        self.assertIn('gap',e.assess(frame(1)).unresolved_differences)
        e.resolve_difference('gap',tick=1,evidence_provenance='a:review',actor='human')
        self.assertNotIn('gap',e.assess(frame(2)).unresolved_differences)
        self.assertIn('gap',e.reopen(0)['historic_snapshot']['unresolved_differences'])

    def test_reopening_cannot_backfill_unknown(self):
        e=ConnectionContinuity(); e.assess(frame(0)); e.assess(frame(1))
        self.assertEqual(0,e.reopen(0)['historic_snapshot']['tick'])
        self.assertNotIn('synthetic:fixture:future',str(e.reopen(0)))

    def test_verification_opportunity_proxy(self):
        e=ConnectionContinuity();e.assess(frame(0))
        ch=Challenge('human','ai','claim','frame',('public',),('public',))
        res=e.record_verification(0,ch,Response('ai',('public',),('public',),True,False),
                                  ('public',),provenance='a:challenge')
        self.assertTrue(res['challenge_addressed'])
        self.assertFalse(res['semantic_equivalence_verified'])
        self.assertTrue(any(x['kind']=='verification_opportunity' for x in e.public_trace()))

    def test_private_evidence_fails_challenge(self):
        e=ConnectionContinuity(); e.assess(frame(0))
        ch=Challenge('human','ai','claim','frame',('required',),('required',))
        res=e.record_verification(0,ch,Response('ai',('private',),('private',),True,True),
                                  ('required',),provenance='a:challenge')
        self.assertFalse(res['challenge_addressed'])

    def test_missing_actor_choice_rejected(self):
        with self.assertRaises(ValueError):
            ConnectionContinuity().assess(frame(0,choices={'human':'adopt'}))

    def test_no_rewrite_past(self):
        e=ConnectionContinuity(); e.assess(frame(0))
        with self.assertRaises(ValueError):e.assess(frame(0))

    def test_no_recheck_of_missing_tick(self):
        with self.assertRaises(ValueError):ConnectionContinuity().assess(frame(1),recheck_of=0)

    def test_duplicate_diff_id_prevented(self):
        e=ConnectionContinuity()
        d=Difference('gap','explanation','human','source')
        e.assess(frame(0,differences=(d,)))
        with self.assertRaises(ValueError):e.assess(frame(1,differences=(d,)))

    def test_synthetic_lifecycle(self):
        result=synthetic_lifecycle()
        self.assertEqual(['UNCERTAIN','DECLINED','CONNECTED_PROXY','CONNECTED_PROXY'],
                         [x['connection'] for x in result['transitions']])
        self.assertIn('meaning-gap',result['historic_reopening_before_resolution']['historic_snapshot']['unresolved_differences'])
        self.assertEqual((),tuple(result['transitions'][-1]['unresolved_differences']))


if __name__ == '__main__': unittest.main()

class BridgeIntegrationTests(unittest.TestCase):
    def _bridge(self):
        from social_connection import Actor
        from social_connection_v03_bridge import SocialConnectionV03
        b=SocialConnectionV03()
        b.register(Actor('human','human','frame_h',('a',)))
        b.register(Actor('ai','ai','frame_ai',('b',)))
        b.core.decide('human','a','hold',reason='needs time')
        b.core.decide('ai','a','adopt',reason='evidence')
        return b

    def test_actual_bridge_links_decisions(self):
        b=self._bridge()
        e=ConnectionContinuity()
        s=e.assess_from_bridge(b, frame(0,choices={'human':'hold','ai':'adopt'}))
        self.assertEqual('DEFERRED',s.connection)
        self.assertTrue(any(x['kind']=='linked_v03_bridge_records' for x in e.public_trace()))

    def test_bridge_cannot_fabricate_choice(self):
        b=self._bridge()
        with self.assertRaises(ValueError):
            ConnectionContinuity().assess_from_bridge(b,frame(0))

    def test_bridge_tick_mismatch_rejected(self):
        b=self._bridge()
        with self.assertRaises(ValueError):
            ConnectionContinuity().assess_from_bridge(b,frame(1,choices={'human':'hold','ai':'adopt'}))
