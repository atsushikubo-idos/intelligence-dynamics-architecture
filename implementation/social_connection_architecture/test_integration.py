import unittest
from social_connection import Actor, Evidence
from social_connection_v02 import SocialConnectionV02, ExternalOffer, integrated_demo

class IntegratedArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.s=SocialConnectionV02()
        for id,kind,frame in [('A','human','people'),('B','ai','uncertainty'),('C','organization','liquidity')]:
            self.s.register(Actor(id,kind,frame,(frame,)))

    def shared(self):
        self.s.observe(Evidence('A',0,'growth',.7,'A:opinion',True))
        self.s.observe(Evidence('C',0,'cash',12,'C:ledger',True))
        self.s.observe(Evidence('C',0,'burn',3,'C:forecast',True))

    def test_old_projections_fail_after_frame_change(self):
        self.shared()
        v=self.s.capture_frame('runway_only')
        self.assertTrue(v.valid)
        self.assertEqual(v.values,{'cash_runway':4.})
        check=self.s.check_equivalence(v,'runway_and_growth')
        self.assertFalse(check['equivalent'])
        self.assertEqual(check['missing_in_projection'],['growth'])
        self.assertEqual(self.s.reopen_frame(0,'runway_and_growth').values,{'cash_runway':4.,'growth':.7})

    def test_private_evidence_never_becomes_shared_on_reopen(self):
        self.shared()
        self.s.observe(Evidence('A',0,'handoff_risk',999,'private_source',False))
        v=self.s.reopen_frame(0,'expanded_external')
        self.assertFalse(v.valid)
        self.assertIn('handoff_risk',v.missing)
        import json
        self.assertNotIn('999',json.dumps(self.s.snapshot(),default=str))

    def test_conflicting_claims_not_silently_overwritten(self):
        self.shared()
        self.s.observe(Evidence('A',0,'cash',80,'A:conflict',True))
        self.assertNotIn('cash',self.s.verified_shared_values())
        self.assertFalse(self.s.capture_frame('runway_only').valid)
        state=self.s.record_relational_state()
        self.assertIn('cash',state['conflicted_keys'])

    def test_distributions_separated(self):
        self.shared()
        self.s.decide('A','grow','adopt',reason='a')
        self.s.decide('B','wait','hold',reason='b')
        r=self.s.record_relational_state()
        prior=dict(self.s.hypothesis_weights)
        self.assertAlmostEqual(r['choice_distribution']['adopt'],.5)
        self.s.update_hypotheses()
        self.assertEqual(self.s.distribution_history[0]['choice_distribution']['adopt'],.5)
        self.assertNotEqual(self.s.hypothesis_weights,prior)
        self.assertNotEqual(r['choice_distribution'],self.s.hypothesis_weights)

    def test_validation_snapshots_not_overwritten(self):
        self.shared()
        self.s.decide('A','grow','adopt',reason='a')
        self.s.decide('C','grow','reject',reason='c')
        self.s.explore()
        self.s.evaluate_candidate('cash_runway')
        self.s.next_round()
        self.s.observe(Evidence('C',1,'cash',4,'C:newledger',True))
        self.s.observe(Evidence('C',1,'burn',2,'C:newforecast',True))
        self.s.decide('A','grow','hold',reason='a')
        self.s.decide('C','grow','reject',reason='c')
        self.s.explore()
        self.s.evaluate_candidate('cash_runway')
        self.assertEqual([e['evaluation']['runway_months'] for e in self.s.candidate_history],[4.,2.])

    def test_offer_rejected_without_all_required_approvals(self):
        self.s.offer_external(ExternalOffer('o',0,'C','handoff_risk',.2,'external'))
        self.s.authorize_offer('o','A',True)
        self.s.authorize_offer('o','B',False)
        self.assertFalse(self.s.accept_offer('o',('A','B','C')))
        self.assertNotIn('handoff_risk',self.s.verified_shared_values())

    def test_offer_only_admitted_after_consent(self):
        self.s.offer_external(ExternalOffer('o',0,'C','handoff_risk',.2,'external'))
        for a in ('A','B','C'): self.s.authorize_offer('o',a,True)
        self.assertTrue(self.s.accept_offer('o',('A','B','C')))
        self.assertEqual(self.s.verified_shared_values()['handoff_risk'],.2)
        with self.assertRaises(ValueError): self.s.accept_offer('o',('A','B','C'))

    def test_no_hindsight_when_reopening(self):
        self.shared()
        self.s.next_round()
        self.s.observe(Evidence('C',1,'handoff_risk',.2,'C:later',True))
        self.assertIn('handoff_risk',self.s.reopen_frame(0,'expanded_external').missing)

    def test_presentation_cannot_choose_for_actor(self):
        self.shared()
        self.s.decide('A','grow','adopt',reason='a')
        self.s.decide('C','grow','reject',reason='c')
        self.s.explore()
        before=list(self.s.actors['B'].decision_history)
        self.s.present_options('B',['cash_runway'])
        self.assertEqual(self.s.actors['B'].decision_history,before)
        self.assertFalse(self.s.update_actor('A','cash_runway',actor_approved=False))

    def test_question_not_claimed_as_autonomous_discovery(self):
        q=self.s.formulate_question(reason='disagreement')
        self.assertIn('independently checkable',q.text)
        self.assertEqual(q.status,'open')
        self.assertNotIn('discovered_new_ontology',self.s.snapshot()['Limit'])

    def test_legacy_12cdp_mapping_retained(self):
        from social_connection import CDP_FIELDS
        self.assertEqual(tuple(self.s.snapshot()), CDP_FIELDS)

    def test_demo(self):
        out=integrated_demo()
        self.assertFalse(out['equivalence_break']['equivalent'])
        self.assertTrue(out['reopen_historical_success'])
        self.assertEqual(out['old_external_field_missing'],['handoff_risk'])
        self.assertEqual(out['agent_frames']['human'],[])
        self.assertTrue(out['external_accepted'])
        self.assertTrue(out['new_frame_valid'])

if __name__=='__main__': unittest.main()
