"""Reproducible offline tests. Run: python -m unittest discover -s research/cross_scale_physical_baselines -p 'test_predictive_discovery_v03.py'"""
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('audit',Path(__file__).with_name('predictive_discovery_v03.py'))
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

class PredictiveDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=audit.run()
    def test_reproducible(self):self.assertEqual(self.r, audit.run())
    def test_synthetic_flag(self):self.assertTrue(self.r['synthetic'])
    def test_no_oracle_used_for_fitting(self):self.assertFalse(self.r['oracle_partition_used_for_training'])
    def test_trajectory_split(self):self.assertIn('independent',self.r['train_test_split'])
    def test_sample_no_lookahead(self):
        x=[('X','a'),('X','b'),('Y','N'),('X','a')]
        self.assertEqual(audit.samples(x),[(('X','b','X','a'),1),(('Y','N','X','b'),0)])
    def test_markov_probabilities(self):
        self.assertTrue(all(abs(sum(r)-1)<1e-12 for r in audit.TRANS.values()))
    def test_dataset_lengths(self):
        self.assertEqual(self.r['models']['macro_current']['test']['n'],6998)
    def test_macro_history_improves_baseline(self):
        m=self.r['models'];self.assertLess(m['macro_history']['test']['brier'],m['macro_current']['test']['brier'])
    def test_tag_history_improves_in_distribution(self):
        m=self.r['models'];self.assertLess(m['macro_tag_history']['test']['brier'],m['macro_history']['test']['brier'])
    def test_semantic_shift_hurts_fixed_tags(self):
        m=self.r['models']['macro_tag_history'];self.assertGreater(m['shift_test']['brier'],m['test']['brier']+.03)
    def test_adaptation_mitigates_shift(self):
        m=self.r['models'];self.assertLess(m['adaptive_full_observed_context']['shift_test_prequential']['brier'],m['macro_tag_history']['shift_test']['brier'])
    def test_cluster_selected_on_validation(self):
        cl=self.r['models']['learned_predictive_groups'];self.assertEqual(cl['validation']['brier'],min(c['brier'] for c in cl['candidate_validation']))
    def test_cluster_is_not_oracle(self):self.assertLessEqual(self.r['models']['learned_predictive_groups']['discovered_predictive_classes'],self.r['models']['learned_predictive_groups']['full_observed_contexts'])
    def test_no_baseline_outperformance_claim(self):
        m=self.r['models']; self.assertLessEqual(abs(m['learned_predictive_groups']['test']['brier']-m['macro_tag_history']['test']['brier']),.005)

if __name__=='__main__':unittest.main()
