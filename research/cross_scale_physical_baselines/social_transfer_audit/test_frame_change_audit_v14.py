"""Deterministic checks for v1.4 synthetic frame-change audit."""
import unittest
import numpy as np
from frame_change_audit_v14 import (generate, shift_data, blocks, fit_model,
    evaluate_run, diagnostics, adapt_and_score, run, WINDOW)
from multiframe_relation_audit_v13 import select_pairs

class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=generate(220,113)
        cls.train=generate(600,114)
        cls.selected=select_pairs(cls.train)
        cls.clf=fit_model(cls.train, cls.selected)

    def test_none_is_unchanged(self):
        d=shift_data(self.base,'none')
        self.assertTrue(np.array_equal(d['y'],self.base['y']))
        self.assertTrue(np.array_equal(d['events'],self.base['events']))

    def test_observer_preserves_truth(self):
        d=shift_data(self.base,'observer_A')
        self.assertTrue(np.array_equal(d['y'],self.base['y']))
        self.assertTrue(np.array_equal(d['events'][:,1:],self.base['events'][:,1:]))

    def test_observer_only_swaps_a_symbols(self):
        d=shift_data(self.base,'observer_A')
        a=self.base['events'][:,0]
        expected=np.where(a==1,5,np.where(a==5,1,a))
        self.assertTrue(np.array_equal(d['events'][:,0],expected))

    def test_relation_preserves_observations(self):
        d=shift_data(self.base,'relation')
        self.assertTrue(np.array_equal(d['events'],self.base['events']))

    def test_environment_preserves_observations(self):
        d=shift_data(self.base,'environment')
        self.assertTrue(np.array_equal(d['events'],self.base['events']))

    def test_invalid_shift(self):
        with self.assertRaises(ValueError):shift_data(self.base,'typo')

    def test_blocks_only_complete(self):
        self.assertEqual(blocks(np.arange(250)).tolist(),[49.5,149.5])

    def test_prediction_is_bounded(self):
        metric,p=evaluate_run(self.clf,self.selected,self.base,0.1)
        self.assertEqual(len(p),220)
        self.assertTrue(np.all((p>=0)&(p<=1)))
        self.assertGreaterEqual(metric['brier'],0)

    def test_diagnostics_are_observable(self):
        _,p=evaluate_run(self.clf,self.selected,self.base,0.1)
        d=diagnostics(self.train,self.base,self.selected,p)
        self.assertIn('residual_exit_permitted',d)
        self.assertGreaterEqual(d['A_symbol_total_variation'],0)

    def test_adaptation_no_future_labels(self):
        d=generate(420,199)
        r=adapt_and_score(self.train,d,self.selected,warmup=200)
        self.assertEqual(r['future_labels_used_to_refit'],0)

    def test_three_shifts_alert_in_this_run(self):
        r=run()['regimes']
        self.assertIsNone(r['none']['first_alert_observations'])
        for name in ('observer_A','relation','environment'):
            self.assertIsNotNone(r[name]['first_alert_observations'])

if __name__=='__main__': unittest.main()
