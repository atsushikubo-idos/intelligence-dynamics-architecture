import unittest
from history_discovery_v10 import (FEATURES, make_episodes,split_by_group, select_history,
                                   HistogramPredictor, best_decision_stump, score, evaluate)

class HistoryDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=make_episodes(960)
        cls.train,cls.test=split_by_group(cls.data)

    def test_deterministic_generation(self):
        self.assertEqual(self.data,make_episodes(960))
    def test_episodes_unique(self):
        self.assertEqual(len({e.episode_id for e in self.data}),len(self.data))
    def test_train_test_separated(self):
        self.assertFalse(set(e.group for e in self.train)&set(e.group for e in self.test))
    def test_all_predeparture_connected(self):
        self.assertTrue(all(e.features[0] for e in self.data))
    def test_outcome_is_transfer(self):
        self.assertTrue(all(e.retained_after_departure==e.features[1] for e in self.data))
    def test_no_ground_truth_in_feature_names(self):
        self.assertNotIn('retained_after_departure',FEATURES)
    def test_selection_discovers_transfer(self):
        self.assertIn('verified_transfer_event',select_history(self.train)['selected_names'])
    def test_current_only_worse(self):
        discovered=select_history(self.train)['selected_indices']
        self.assertLess(score(HistogramPredictor(discovered).fit(self.train),self.test),
                        score(HistogramPredictor((0,)).fit(self.train),self.test))
    def test_standard_stump_equal(self):
        _, stump=best_decision_stump(self.train)
        discovered=HistogramPredictor(select_history(self.train)['selected_indices']).fit(self.train)
        self.assertAlmostEqual(score(stump,self.test),score(discovered,self.test),places=6)
    def test_decoy_not_selected(self):
        names=select_history(self.train)['selected_names']
        self.assertNotIn('unrelated_random_event',names)
    def test_shift_does_not_preserve_zero_error(self):
        report=evaluate()
        self.assertGreater(report['shifted_reliability_brier']['learned_history'],0.05)
    def test_results_stable(self):
        self.assertEqual(evaluate(),evaluate())

if __name__=='__main__':unittest.main()
