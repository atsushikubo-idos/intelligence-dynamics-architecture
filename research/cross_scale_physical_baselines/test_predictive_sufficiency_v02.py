"""Run with: python -m unittest discover -s research/cross_scale_physical_baselines -p 'test_predictive_sufficiency_v02.py' -v"""
import unittest
from predictive_sufficiency_v02 import (P,STATES,MACRO,REFINED,stationary,prob_future_Y,
    strong_lumpability,representation,forecast_stats,macro_history_brier,run)

class PredictiveSufficiencyAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pi=stationary()
        cls.result=run()

    def test_transition_rows_are_stochastic(self):
        for row in P.values():
            self.assertAlmostEqual(sum(row.values()),1)
            self.assertTrue(all(0 <= x <= 1 for x in row.values()))

    def test_stationary_is_normalized_and_invariant(self):
        self.assertAlmostEqual(sum(self.pi.values()),1)
        for dst in STATES:
            self.assertAlmostEqual(sum(self.pi[src]*P[src][dst] for src in STATES),self.pi[dst],places=12)

    def test_macro_fails_strong_lumpability(self):
        self.assertFalse(strong_lumpability(MACRO))

    def test_refined_satisfies_strong_lumpability(self):
        self.assertTrue(strong_lumpability(REFINED))

    def test_known_one_step_difference(self):
        q=prob_future_Y()
        self.assertAlmostEqual(q['a1'],.9)
        self.assertAlmostEqual(q['b1'],.1)
        self.assertEqual(MACRO['a1'],MACRO['b1'])

    def test_refined_equal_micro_brier_multiple_horizons(self):
        for k in ('1','2','3'):
            rs=self.result['forecast_horizons'][k]
            self.assertAlmostEqual(rs['refined']['expected_brier_score'],rs['micro']['expected_brier_score'],places=12)
            self.assertAlmostEqual(rs['refined']['predictive_entropy_bits'],rs['micro']['predictive_entropy_bits'],places=12)

    def test_refinement_beats_macro_for_all_horizons(self):
        for k in ('1','2','3'):
            rs=self.result['forecast_horizons'][k]
            self.assertLess(rs['refined']['expected_brier_score'],rs['macro']['expected_brier_score'])

    def test_refined_requires_less_storage_than_micro(self):
        rs=self.result['forecast_horizons']['1']
        self.assertLess(rs['refined']['storage_entropy_bits'],rs['micro']['storage_entropy_bits'])

    def test_history_improves_macro_forecast(self):
        macro=self.result['forecast_horizons']['1']['macro']['expected_brier_score']
        history=macro_history_brier(self.pi)['brier_macro_previous_and_current']
        self.assertLess(history,macro)

    def test_macro_history_still_behind_refined(self):
        self.assertGreater(macro_history_brier(self.pi)['brier_macro_previous_and_current'],
            self.result['forecast_horizons']['1']['refined']['expected_brier_score'])

    def test_expected_information_gap_positive(self):
        self.assertGreater(self.result['one_step_information_lost_by_macro_bits'],0)
        self.assertAlmostEqual(self.result['one_step_information_lost_by_macro_bits'],.21462365038324693,places=9)

    def test_microstate_is_oracle_baseline(self):
        for n in (1,2,3):
            target=prob_future_Y(n)
            z=forecast_stats(representation('micro'),target,self.pi)
            for s,p in z['predicted_p_future_Y'].items():self.assertAlmostEqual(p,target[s])

if __name__=='__main__':unittest.main()
