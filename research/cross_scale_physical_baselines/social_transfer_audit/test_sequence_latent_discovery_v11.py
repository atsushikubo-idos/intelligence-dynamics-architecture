"""Run: python -m unittest discover -s research/cross_scale_physical_baselines/social_transfer_audit -p 'test_sequence_latent_discovery_v11.py'"""
import unittest
from sequence_latent_discovery_v11 import (ALPHABET, BetaRate, LogisticPairs, brier, discover,
    event_motif, evaluate, make_episodes, online_recalibration, split)

class SequenceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=make_episodes(1800,seed=117)
        cls.tr,cls.va,cls.te=split(cls.data)
    def test_deterministic_generation(self):
        self.assertEqual(self.data,make_episodes(1800,seed=117))
    def test_split_disjoint(self):
        self.assertFalse(set(map(id,self.tr)) & set(map(id,self.te)))
        self.assertEqual(len(self.tr)+len(self.va)+len(self.te),len(self.data))
    def test_no_semantic_inputs(self):
        self.assertEqual(len(self.tr[0].tokens)>=5,True)
        self.assertTrue(set(self.tr[0].tokens).issubset(set(ALPHABET)))
    def test_sequence_order_matters(self):
        self.assertEqual(event_motif('bxxe','b','e'),1)
        self.assertEqual(event_motif('exxb','b','e'),0)
    def test_learned_pair(self):
        pair,_,_,n=discover(self.tr,self.va)
        self.assertEqual(pair,('b','e'));self.assertEqual(n,30)
    def test_predict_probability(self):
        m=BetaRate(lambda seq:event_motif(seq,'b','e')).fit(self.tr)
        self.assertTrue(0<=m.predict(('a','b','e'))<=1)
    def test_holdout_improvement(self):
        _,_,m,_=discover(self.tr,self.va)
        base=BetaRate(lambda seq:1).fit(self.tr+self.va)
        self.assertLess(brier(m,self.te),brier(base,self.te))
    def test_standard_baseline_valid(self):
        m=LogisticPairs(steps=70).fit(self.tr)
        self.assertTrue(0<=m.predict(('b','e'))<=1)
    def test_rule_shift_hurts_fixed_model(self):
        _,_,m,_=discover(self.tr,self.va)
        shifted=make_episodes(400,seed=188,regime=1)
        self.assertGreater(brier(m,shifted),brier(m,self.te))
    def test_prequential_adaptation(self):
        pair,_,_,_=discover(self.tr,self.va)
        shifted=make_episodes(700,seed=166,regime=1)
        m=BetaRate(lambda seq:event_motif(seq,*pair)).fit(self.tr+self.va)
        fixed=brier(m,shifted)
        online,_=online_recalibration(BetaRate(lambda seq:event_motif(seq,*pair)).fit(self.tr+self.va),shifted)
        self.assertLess(online,fixed)
    def test_not_consistent_with_real_data_claim(self):
        result=evaluate()
        self.assertEqual(result['data'],'synthetic anonymous token sequences')
        self.assertIn('standard_logistic_all_pairs',result['heldout_brier'])

if __name__=='__main__':unittest.main()
