"""Unit and deterministic regression tests for v1.3."""
import unittest
import numpy as np
from multiframe_relation_audit_v13 import generate, ordered, pair_bank, select_pairs, relation_features, main

class TestMultiFrame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=main()
    def test_order_direction(self):
        self.assertTrue(ordered(np.array([1,0,0]),1,np.array([0,4,0]),4))
        self.assertFalse(ordered(np.array([0,0,1]),1,np.array([4,0,0]),4))
    def test_absent_event(self):
        self.assertFalse(ordered(np.array([0,0]),1,np.array([4,4]),4))
    def test_deterministic_generator(self):
        a=generate(80,43);b=generate(80,43)
        for key in a: np.testing.assert_array_equal(a[key],b[key])
    def test_different_seeds(self):
        self.assertFalse(np.array_equal(generate(80,43)['events'],generate(80,44)['events']))
    def test_shapes(self):
        d=generate(60,50)
        self.assertEqual(d['events'].shape,(60,3,6))
        self.assertEqual(pair_bank(d)[0].shape,(60,36))
    def test_no_permission_implies_no_eligibility(self):
        d=generate(600,60)
        forbidden=(d['permissions'][:,0]==0)|(d['permissions'][:,1]==0)|(d['revoked']==1)
        self.assertTrue(np.all(d['eligible'][forbidden]==0))
    def test_no_exit_allows_mediated_link(self):
        d=generate(600,61)
        mask=(d['exit']==0)&(d['permissions'][:,0]==1)&(d['permissions'][:,1]==1)&(d['revoked']==0)
        self.assertTrue(np.all(d['eligible'][mask]==1))
    def test_exit_requires_transfer(self):
        d=generate(600,62)
        mask=(d['exit']==1)&(d['eligible']==1)
        self.assertTrue(np.all(d['latent_transfer'][mask]==1))
    def test_selection_training(self):
        d=generate(4200,111)
        self.assertEqual(select_pairs(d),(10,26))
    def test_relation_features(self):
        d=generate(80,70)
        self.assertEqual(relation_features(d,(10,26)).shape,(80,9))
    def test_bounds(self):
        d=generate(70,80,'changed');self.assertTrue(np.all(np.isin(d['y'],[0,1])))
    def test_main_reproducible(self):
        self.assertEqual(self.report['selected_pairs'],{'A_to_B':[1,4],'B_to_C':[4,2]})
    def test_baseline_performance(self):
        res=self.report['normal']
        self.assertLess(res['learned_relation_features']['brier'],res['current_only']['brier'])
    def test_fair_control(self):
        a=self.report['normal'];self.assertLess(abs(a['learned_relation_features']['brier']-a['standard_full_information_relation_baseline']['brier']),.015)

if __name__=='__main__':unittest.main()
