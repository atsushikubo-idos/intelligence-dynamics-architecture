import unittest
import numpy as np
from pipeline import run,main
from eventlog_validation import synthesize, make_cases

class IntegrationPilotTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.all=main()
 def test_three_way_split(self):
  d=self.all['stable']['n'];self.assertEqual(sum(d.values()),360)
 def test_fitted_model_selected_without_test(self):
  d=self.all['stable']['model_selection']
  self.assertEqual(d['chosen'],min(d['calibration_mae'],key=d['calibration_mae'].get))
 def test_v07_training_likelihoods(self):
  x=self.all['stable']['observation_design']
  self.assertAlmostEqual(sum(x['training_class_prior']),1,places=8)
  self.assertIn(x['selected_observation'], ['pre_review_hours','queue_at_review','handoff_at_review','pre_review_rework'])
 def test_brier_and_baseline(self):
  x=self.all['stable']['observation_design']; self.assertGreaterEqual(x['heldout_brier'],0)
  self.assertGreaterEqual(x['heldout_prior_brier'],0)
 def test_stable_audit_not_rejected(self):self.assertEqual(self.all['stable']['family_audit']['result']['status'],'compatible_not_proven')
 def test_shifted_audit_rejected(self):self.assertEqual(self.all['shifted_holdout']['family_audit']['result']['status'],'family_rejected')
 def test_no_auto_frame_update(self):
  for k in ('stable','shifted_holdout'):
   self.assertFalse(self.all[k]['family_audit']['next']['update_reference_frame'])
 def test_candidate_is_not_causal(self):
  self.assertIn('NOT causal',self.all['stable']['observation_design']['hypotheses'])
 def test_insufficient_cases(self):
  with self.assertRaises(ValueError):run(synthesize(30))
 def test_reproducibility(self):
  first=self.all['stable'];other=run(synthesize(360,seed=71))
  self.assertEqual(first['model_selection'],other['model_selection'])
  self.assertEqual(first['family_audit']['result']['monte_carlo_p'],other['family_audit']['result']['monte_carlo_p'])

if __name__=='__main__':unittest.main()
