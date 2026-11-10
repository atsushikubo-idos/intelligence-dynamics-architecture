import unittest
from connection_boundary_comparative_v02 import *

class ControlledComparison(unittest.TestCase):
    def test_full_history_equal_all_cases(self):
        self.assertEqual(len(comparison_scenarios()),4)
        self.assertTrue(all(x['full_history_equal'] for x in comparison_scenarios()))
    def test_limited_history_is_not_equivalent(self):
        self.assertTrue(any(x['lossy_disagrees'] for x in comparison_scenarios()))
    def test_conflict_is_not_guarantee(self):
        self.assertEqual(comparison_scenarios()[0]['idos_status'],'POSSIBLE_NOT_GUARANTEED')
    def test_refusal_is_not_conflated_with_unknown(self):
        self.assertEqual(comparison_scenarios()[-1]['idos_status'],'IMPOSSIBLE')

class ObservableProxyChecks(unittest.TestCase):
    def setUp(self):
        self.c=Challenge('human','ai','claim','f',('public',),('public',))
    def test_challenge_supported_by_disclosed_authorized_evidence(self):
        out=verification_opportunity(self.c,Response('ai',('public',),('public',),True,False),('public',))
        self.assertTrue(out['challenge_addressed'])
        self.assertFalse(out['semantic_equivalence_verified'])
    def test_challenge_fails_for_private_or_missing_evidence(self):
        out=verification_opportunity(self.c,Response('ai',('private',),('private',),True,True),('public',))
        self.assertFalse(out['challenge_addressed'])
    def test_wrong_respondent_cannot_satisfy_challenge(self):
        out=verification_opportunity(self.c,Response('other',('public',),('public',),True,True),('public',))
        self.assertFalse(out['challenge_addressed'])
    def test_claimed_resolution_does_not_prove_semantics(self):
        out=verification_opportunity(self.c,Response('ai',('public',),('public',),True,True),('public',))
        self.assertFalse(out['semantic_equivalence_verified'])
    def test_mutual_update_paths_allow_asymmetric_choices(self):
        paths=(UpdateOpportunity('human','old','new',True,True,'reject','h'),UpdateOpportunity('ai','old','new',True,True,'adopt','a'))
        result=mutual_update_opportunity(paths,('human','ai'))
        self.assertTrue(result['bilateral_paths_preserved'])
        self.assertFalse(result['substantive_mutual_learning_proven'])
    def test_missing_path_is_not_mutual(self):
        paths=(UpdateOpportunity('human','old','new',True,True,'adopt','h'),)
        self.assertFalse(mutual_update_opportunity(paths,('human','ai'))['bilateral_paths_preserved'])
    def test_forced_path_fails_mutuality_proxy(self):
        paths=(UpdateOpportunity('human','old','new',True,False,'adopt','h'),UpdateOpportunity('ai','old','new',True,True,'adopt','a'))
        self.assertFalse(mutual_update_opportunity(paths,('human','ai'))['bilateral_paths_preserved'])
    def test_hold_is_valid_actor_choice(self):
        paths=(UpdateOpportunity('human','old','new',True,True,'hold','h'),UpdateOpportunity('ai','old','new',True,True,'reject','a'))
        self.assertTrue(mutual_update_opportunity(paths,('human','ai'))['bilateral_paths_preserved'])
    def test_reopening_has_no_private_or_future_hindsight(self):
        records=(AuditRecord(0,('a',),'h','reason','dissent',True,'p0'), AuditRecord(0,('a',),'h','secret','hidden',False,'p1'),AuditRecord(1,('b',),'a','future','yes',True,'p2'))
        result=reopen_history(records,0,('reason','secret','future'))
        self.assertEqual(result['available'],{'reason':'dissent'})
        self.assertEqual(result['missing'],['future','secret'])
    def test_reopening_requires_provenance(self):
        records=(AuditRecord(0,('a',),'h','reason','value',True,''),)
        self.assertEqual(reopen_history(records,0,('reason',))['available'],{})

if __name__=='__main__':unittest.main()

class ExhaustiveInformationParity(unittest.TestCase):
    def test_all_two_world_two_actor_action_sets(self):
        from itertools import product
        possibilities=[set(),{'plan_a'},{'plan_b'},{'plan_a','plan_b'}]
        actors=('human','ai'); actions=('plan_a','plan_b')
        count=0
        for choices in product(range(4), repeat=4):
            worlds=tuple(make_world('w'+str(k),('same',),
                           {a:possibilities[choices[k*2+i]] for i,a in enumerate(actors)})
                         for k in range(2))
            observed=boundary(worlds,'decision',actors,('same',),actions)
            reference=independent_full_information_baseline(worlds,'decision',actors,('same',),actions)
            self.assertEqual((observed.status,observed.guaranteed_actions),reference)
            count+=1
        self.assertEqual(count,256)
