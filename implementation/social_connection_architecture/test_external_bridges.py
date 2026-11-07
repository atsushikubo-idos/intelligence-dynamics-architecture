"""Regression and adversarial tests of adapters to the REAL existing IDOS modules."""
import unittest

from social_connection import Actor, Evidence
from social_connection_v03_bridge import SocialConnectionV03, integrated_demo


class TestExistingModuleBridges(unittest.TestCase):
    def setUp(self):
        self.s = SocialConnectionV03()
        self.s.register(Actor('h','human','growth',('growth',)))
        self.s.register(Actor('ai','ai','possibilities',('uncertainty',)))
        self.s.register(Actor('o','organization','continuity',('cash',)))
        self.s.activate_governance()
        self.c = self.s.core
        self.c.observe(Evidence('h',0,'growth',.7,'h:market',True))
        self.c.observe(Evidence('o',0,'cash',10,'o:cash',True))
        self.c.observe(Evidence('o',0,'burn',2.5,'o:burn',True))
        self.c.observe(Evidence('o',0,'secret',12345,'o:secret',False))
        self.c.decide('h','expand','adopt',reason='growth')
        self.c.decide('ai','pilot','hold',reason='uncertainty')
        self.c.decide('o','expand','reject',reason='risk')

    def validated_frame(self):
        self.c.explore()
        self.c.evaluate_candidate('cash_runway')

    def test_three_real_modules_are_used(self):
        import social_connection_v03_bridge as b
        self.assertIn('dynamic_interoperability', str(b._interop.__file__))
        self.assertIn('discovery_architecture', str(b._discovery.__file__))
        self.assertIn('coexistence_governance', str(b._governance.__file__))

    def test_exchange_preserves_unresolved_without_faking_verification(self):
        ex=self.s.translate('o','h', message='Cash pressure', evidence_refs=('o:cash',), reviewer='h')
        self.assertEqual(ex.assessments[0].disposition.value,'unresolved')
        self.assertEqual(ex.cdp_quality, 'structural_adapter_only')
        self.assertEqual(self.s.exchange_ledger.exchanges[0].id, ex.id)

    def test_exchange_direction_and_trajectory_preserved(self):
        ex=self.s.translate('o','h', message='Cash', evidence_refs=('o:cash',), reviewer='h')
        self.assertEqual(ex.source_frame,'continuity')
        self.assertEqual(ex.target_frame,'growth')
        self.assertNotEqual(ex.source_trajectory,ex.target_trajectory)

    def test_shared_provenance_required(self):
        with self.assertRaises(PermissionError):
            self.s.translate('o','h',message='Secret',evidence_refs=('o:secret',),reviewer='h')
        self.assertFalse(self.s.exchange_ledger.exchanges)

    def test_no_unattributed_claim(self):
        with self.assertRaises(ValueError):
            self.s.translate('o','h',message='Cash',evidence_refs=(),reviewer='h')

    def test_review_cannot_be_claimed_without_basis(self):
        with self.assertRaises(ValueError):
            self.s.translate('o','h',message='Cash', evidence_refs=('o:cash',),
                             reviewer='h',disposition='preserved')

    def test_review_is_explicit_declared_assessment(self):
        ex=self.s.translate('o','h',message='Cash',evidence_refs=('o:cash',),
                            reviewer='h',disposition='altered',review_evidence='Loss of contextual assumptions')
        self.assertEqual(ex.assessments[0].disposition.value,'altered')
        self.assertEqual(ex.assessments[0].assessor,'h')

    def test_discovery_calls_existing_cycle_and_retains_sources(self):
        self.validated_frame()
        self.s.begin_discovery('rel',question='What changed?',baseline_frame_id='growth')
        performed,difference,proposal=self.s.propose_after_observed_change(
          'rel',actor_id='o',intervention='An externally reported review',
          observation='Cash changed consideration',evidence_refs=('o:cash',),
          candidate_id='cash_runway',reason='Explanation')
        self.assertEqual([r.kind for r in self.s.discovery_cycles['rel'].trace(proposal.id)],
                         ['performed_intervention','difference','frame_proposal'])
        self.assertEqual(difference.source_ids,(performed.id,))

    def test_discovery_does_not_imply_actor_adoption(self):
        self.validated_frame()
        self.s.begin_discovery('rel',question='What changed?',baseline_frame_id='growth')
        self.s.propose_after_observed_change('rel',actor_id='o',
            intervention='Reported review',observation='Different trajectory',
            evidence_refs=('o:cash',),candidate_id='cash_runway',reason='Check')
        self.assertEqual(self.c.actors['h'].adopted_frames,[])
        self.assertEqual(self.c.actors['o'].adopted_frames,[])

    def test_discovery_requires_validated_core_candidate(self):
        self.s.begin_discovery('rel',question='Why?',baseline_frame_id='growth')
        with self.assertRaises(ValueError):
            self.s.propose_after_observed_change('rel',actor_id='o',
              intervention='Action',observation='Difference',
              evidence_refs=('o:cash',),candidate_id='unknown',reason='Why')

    def test_governance_unknown_risk_review_not_execution(self):
        out=self.s.assess_governance('p1',proposer_id='ai', affected=('h','o'),
                    action='pilot',approvals=('h','o'),risk='unknown',evidence_refs=('o:cash',))
        self.assertEqual(out.decision.value,'review')
        self.assertTrue(self.s.bridge_events[-1]['no_execution'])

    def test_governance_can_block_objection(self):
        self.s.governor.object('p','h','reject unsafe intervention')
        out=self.s.assess_governance('p',proposer_id='ai',affected=('h','o'),
                    action='pilot',approvals=('h','o'),risk='low',evidence_refs=('o:cash',))
        self.assertEqual(out.decision.value,'block')

    def test_governance_missing_approval_requires_review(self):
        out=self.s.assess_governance('p',proposer_id='ai',affected=('h','o'),
                    action='pilot',approvals=('h',),risk='low',evidence_refs=('o:cash',))
        self.assertEqual(out.decision.value,'review')

    def test_governance_disallows_private_evidence(self):
        with self.assertRaises(PermissionError):
            self.s.assess_governance('p',proposer_id='ai',affected=('o',),
                    action='pilot',risk='low',evidence_refs=('o:secret',))

    def test_future_evidence_not_backfilled(self):
        self.validated_frame()
        self.s.begin_discovery('rel',question='What changed?',baseline_frame_id='growth')
        _,_,prop=self.s.propose_after_observed_change('rel',actor_id='o',
                         intervention='Reported review',observation='Changed',
                         evidence_refs=('o:cash',),candidate_id='cash_runway',reason='Check')
        self.c.next_round()
        self.c.observe(Evidence('o',1,'cash',7,'o:cash:t1',True))
        with self.assertRaises(PermissionError):
            self.s.recontact('rel',prop,finding='New facts',
                         evidence_refs=('o:cash',),actor_id='o',review='supported')
        result=self.s.recontact('rel',prop,finding='New facts',
                         evidence_refs=('o:cash:t1',),actor_id='o',review='supported')
        self.assertEqual(result.kind,'recontact')

    def test_snapshot_omits_private_value(self):
        self.s.translate('o','h',message='Cash',evidence_refs=('o:cash',),reviewer='h')
        import json
        dump=json.dumps(self.s.snapshot())
        self.assertNotIn('12345',dump)
        self.assertNotIn('o:secret',dump) # audit counts only, no private source value

    def test_end_to_end_and_noncoercion(self):
        d=integrated_demo()
        self.assertEqual(d['governance'],'review')
        self.assertEqual(d['adopted_frames']['human'],[])
        self.assertEqual(d['adopted_frames']['ai'],['cash_runway'])
        self.assertEqual(d['adopted_frames']['org'],['cash_runway'])
        self.assertEqual(len(d['interface']['ExternalModuleIntegration']['dynamic_interoperability']),1)
        self.assertIn('relation_runway',d['interface']['ExternalModuleIntegration']['discovery_architecture'])


if __name__=='__main__': unittest.main()
