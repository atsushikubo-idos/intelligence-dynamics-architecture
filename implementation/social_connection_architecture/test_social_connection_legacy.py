import unittest
from social_connection import SocialConnection, Actor, Evidence, demo, CDP_FIELDS

class TestArchitecture(unittest.TestCase):
    def setUp(self):
        self.s=SocialConnection()
        self.s.register(Actor('A','human','growth',('growth',)))
        self.s.register(Actor('B','ai','uncertainty',('uncertainty',)))
        self.s.register(Actor('C','organization','continuity',('cash',)))

    def add_shared(self):
        self.s.observe(Evidence('A',0,'growth',.9,'A:estimate',True))
        self.s.observe(Evidence('C',0,'cash',10.,'C:ledger',True))
        self.s.observe(Evidence('C',0,'burn',2.,'C:forecast',True))

    def test_registered_native_frames_distinct(self):
        self.assertEqual(len({a.native_frame for a in self.s.actors.values()}),3)

    def test_no_leak_from_private_evidence(self):
        self.s.observe(Evidence('A',0,'secret',999.,'private',False))
        self.assertNotIn('secret',self.s.shared_values())

    def test_sharing_permission(self):
        self.s.actors['C'].can_share=False
        with self.assertRaises(PermissionError):
            self.s.observe(Evidence('C',0,'cash',10.,'ledger',True))

    def test_cfv_validity(self):
        self.add_shared()
        self.assertEqual(self.s.cfv_review('B',{'actor_id':'C','key':'cash','value':10.})['status'],'supported')
        self.assertEqual(self.s.cfv_review('B',{'actor_id':'C','key':'cash','value':100.})['status'],'contradicted')
        self.assertEqual(self.s.cfv_review('B',{'actor_id':'A','key':'unknown','value':1.})['status'],'unverifiable')

    def test_choices_stay_independent(self):
        self.s.decide('A','expand','adopt',reason='growth')
        self.s.decide('C','expand','reject',reason='cash')
        self.assertEqual(self.s.actors['A'].decision_history[0]['disposition'],'adopt')
        self.assertEqual(self.s.actors['C'].decision_history[0]['disposition'],'reject')

    def test_frame_requires_disagreement(self):
        self.add_shared()
        self.assertEqual(self.s.explore(),[])

    def test_candidate_generated_by_cross_frame_difference(self):
        self.add_shared()
        self.s.decide('A','expand','adopt',reason='growth')
        self.s.decide('C','expand','reject',reason='cash')
        self.assertEqual(self.s.explore()[0].validation['runway_months'],5.)

    def test_no_candidate_with_missing_permission(self):
        self.s.observe(Evidence('C',0,'cash',10.,'ledger',True))
        self.s.observe(Evidence('C',0,'burn',2.,'private',False))
        self.s.decide('A','expand','adopt',reason='growth')
        self.s.decide('C','expand','reject',reason='cash')
        self.assertEqual(self.s.explore(),[])

    def test_candidate_does_not_force_adoption(self):
        self.add_shared()
        self.s.decide('A','expand','adopt',reason='growth')
        self.s.decide('C','expand','reject',reason='cash')
        self.s.explore()
        self.assertFalse(self.s.update_actor('A','cash_runway',actor_approved=False))
        self.assertEqual(self.s.actors['A'].adopted_frames,[])
        self.assertTrue(self.s.update_actor('C','cash_runway',actor_approved=True))

    def test_joint_distribution_not_confused_with_hypotheses(self):
        self.add_shared()
        self.s.decide('A','x','adopt',reason='x')
        self.s.decide('C','x','reject',reason='y')
        self.assertEqual(self.s.relationship_distribution()['adopt'],.5)
        self.assertEqual(self.s.hypothesis_weights['growth_only'],.5)
        self.s.update_hypotheses()
        self.assertNotEqual(self.s.hypothesis_weights['growth_only'],.5)
        self.assertEqual(self.s.relationship_distribution()['adopt'],.5)

    def test_no_evidence_no_inference(self):
        self.assertEqual(self.s.update_hypotheses(),{'growth_only':.5,'liquidity_sensitive':.5})

    def test_reopening_keeps_history(self):
        self.s.contact_reality('unexpected',note='new outcome')
        self.assertEqual(len(self.s.reopenings),1)
        self.assertTrue(any(e['event']=='reopening' for e in self.s.events))

    def test_12cdp_mapping(self):
        self.assertEqual(tuple(self.s.snapshot()),CDP_FIELDS)

    def test_no_central_best_action(self):
        self.assertFalse(hasattr(self.s,'choose_for_all'))
        self.assertEqual(len(self.s.actors['A'].decision_history),0)

    def test_rounds_and_trace(self):
        self.add_shared()
        self.s.next_round()
        with self.assertRaises(ValueError):
            self.s.observe(Evidence('C',0,'cash',1.,'late',True))
        self.assertTrue(any(e['event']=='next_round' for e in self.s.events))

    def test_demo_end_to_end(self):
        out=demo()
        self.assertEqual(out['candidate_ids'],['cash_runway'])
        self.assertEqual(out['round_0']['Update']['h'],[])
        self.assertEqual(out['round_0']['Update']['a'],['cash_runway'])
        self.assertEqual(out['round_1']['Possibility Space']['cash_runway']['validation']['runway_months'],2.)
        self.assertEqual(out['cfv_contradiction']['status'],'contradicted')

if __name__=='__main__': unittest.main()
