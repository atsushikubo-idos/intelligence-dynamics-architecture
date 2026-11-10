"""Reproducibility and boundary tests for the synthetic v1.6 audit."""
import unittest
from dataclasses import replace
from active_observation_design_v16 import (PROBES,Probe,entropy,info_gain,bayes_update,
                                           choose_probe,run_trial,evaluate)

ALL={'A':True,'B':True,'C':True}
NONE={'A':False,'B':False,'C':False}

class TestActiveObservation(unittest.TestCase):
    def test_entropy(self): self.assertAlmostEqual(entropy(.5),1.)
    def test_ig_high(self): self.assertAlmostEqual(info_gain(.5,PROBES[0]),.3901596952836)
    def test_ig_zero(self): self.assertAlmostEqual(info_gain(.5,PROBES[-1]),0.)
    def test_ig_nonnegative(self):
        for p in (.01,.1,.5,.9,.99):
            for q in PROBES: self.assertGreaterEqual(info_gain(p,q),-1e-10)
    def test_bayes_one(self): self.assertAlmostEqual(bayes_update(.5,PROBES[0],1),.85)
    def test_bayes_zero(self): self.assertAlmostEqual(bayes_update(.5,PROBES[0],0),.15)
    def test_no_consent(self):
        self.assertIsNone(choose_probe(.5,PROBES,NONE,6,3.5))
        for mode in ('constrained','information_only','standard_bayesian_design'):
            self.assertEqual(run_trial('A',1,mode,NONE)['count'],0)
    def test_denial_protected(self):
        consent={'A':False,'B':True,'C':True}
        for policy in ('constrained','information_only','standard_bayesian_design'):
            x=run_trial('B',1,policy,consent)
            self.assertNotIn('A',[e['owner'] for e in x['events']])
    def test_not_select_nonidentifying(self):
        q=choose_probe(.5,(PROBES[-1],),ALL,6,3.5)
        self.assertIsNone(q)
    def test_high_ig_baseline(self):
        self.assertEqual(choose_probe(.5,PROBES,ALL,6,3.5,'information_only').key,'high_information')
    def test_standard_equal_constrained(self):
        for p in (.1,.2,.5,.8,.9):
            for permission in (ALL,NONE,{'A':False,'B':True,'C':True}):
                a=choose_probe(p,PROBES,permission,6,3.5,'constrained')
                b=choose_probe(p,PROBES,permission,6,3.5,'standard_bayesian_design')
                self.assertEqual(a,b)
    def test_cost_budget(self):
        for mode in ('information_only','constrained'):
            x=run_trial('A',9,mode,ALL,budget=2.0)
            self.assertLessEqual(x['cost'],2.0)
    def test_stop_does_not_force_attribution(self):
        x=run_trial('B',1,'constrained',NONE)
        self.assertEqual(x['decision'],'undetermined')
    def test_deterministic(self):
        self.assertEqual(run_trial('A',123,'information_only',ALL),run_trial('A',123,'information_only',ALL))
    def test_burden(self):
        x=run_trial('A',6,'information_only',ALL,burden_limit=.1)
        self.assertTrue(all(e['probe']=='low_burden' for e in x['events']))
    def test_noisy_probe_less_informative(self):
        self.assertLess(info_gain(.5,PROBES[2]),info_gain(.5,PROBES[1]))
    def test_result_reproducible(self):
        a=evaluate(reps=6,seed=12)
        self.assertEqual(a,evaluate(reps=6,seed=12))
        for sc in a['results'].values():
            self.assertEqual(sc['constrained'],sc['standard_bayesian_design'])
            self.assertEqual(sc['constrained']['permission_violations'],0)

if __name__=='__main__':unittest.main()
