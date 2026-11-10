"""Tests for synthetic state-discovery v1.2. Run: python -m unittest test_latent_state_audit_v12.py"""
import unittest
import numpy as np
from latent_state_audit_v12 import (synthetic, fb, CategoricalHMM, simple_features,
                                    brier, run, SEQ_LEN, TRUE_A, TRUE_B, TRUE_PI)

class AuditTests(unittest.TestCase):
    def test_shapes(self):
        x,y,z=synthetic(20,12)
        self.assertEqual(x.shape,(20,SEQ_LEN))
        self.assertEqual(y.shape,(20,))
        self.assertEqual(z.shape,(20,SEQ_LEN))
    def test_deterministic_synthesis(self):
        self.assertTrue(all(np.array_equal(a,b) for a,b in zip(synthetic(10,19),synthetic(10,19))))
    def test_probability_matrices(self):
        for mat in (TRUE_A,TRUE_B):self.assertTrue(np.allclose(mat.sum(axis=1),1))
    def test_forward_backwards_normalized(self):
        x,_,_=synthetic(40,23)
        a,g,xi,ll=fb(x,TRUE_PI,TRUE_A,TRUE_B)
        self.assertTrue(np.allclose(a.sum(axis=2),1,atol=1e-8))
        self.assertTrue(np.allclose(g.sum(axis=2),1,atol=1e-8))
        self.assertTrue(np.isfinite(ll))
        self.assertTrue(np.all(xi>=0))
    def test_expected_transition_counts(self):
        x,_,_=synthetic(35,20)
        _,_,xi,_=fb(x,TRUE_PI,TRUE_A,TRUE_B)
        self.assertAlmostEqual(xi.sum(),35*(SEQ_LEN-1),places=4)
    def test_hmm_fit_probabilities(self):
        x,_,_=synthetic(140,40)
        hmm=CategoricalHMM(3,iterations=4,restarts=1).fit(x)
        self.assertTrue(np.isclose(hmm.pi.sum(),1))
        self.assertTrue(np.allclose(hmm.A.sum(axis=1),1))
        self.assertTrue(np.allclose(hmm.B.sum(axis=1),1))
    def test_hmm_output_dimension(self):
        x,_,_=synthetic(120,40)
        hmm=CategoricalHMM(2,iterations=3,restarts=1).fit(x)
        self.assertEqual(hmm.features(x).shape,(120,2))
    def test_feature_dimensions(self):
        x,_,_=synthetic(10,40)
        self.assertEqual(simple_features(x,'last').shape,(10,6))
        self.assertEqual(simple_features(x,'bag').shape,(10,6))
        self.assertEqual(simple_features(x,'last3').shape,(10,18))
        self.assertEqual(simple_features(x,'counts_last3').shape,(10,24))
    def test_bag_ignores_order(self):
        x,_,_=synthetic(10,47)
        self.assertTrue(np.array_equal(simple_features(x,'bag'),simple_features(x[:,::-1],'bag')))
    def test_brier_reference(self):
        self.assertAlmostEqual(brier(np.array([.2,.8]),np.array([0,1])),.04)
    def test_outcome_shift_does_not_change_event_process(self):
        x1,_,z1=synthetic(80,51,False)
        x2,_,z2=synthetic(80,51,True)
        self.assertTrue(np.array_equal(x1,x2))
        self.assertTrue(np.array_equal(z1,z2))
    def test_end_to_end_audit(self):
        result=run()
        self.assertEqual(result['selected_states'],3)
        self.assertLess(result['unseen_test']['hmm_unsupervised_filter']['brier'],result['unseen_test']['last']['brier'])
        self.assertLess(result['shift_after_equal_label_budget_brier']['hmm_unsupervised_filter'],result['shift_fixed_brier']['hmm_unsupervised_filter'])

if __name__=='__main__':unittest.main()
