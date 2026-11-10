import unittest
from observation_changes_relation_v17 import ACTIONS, entropy,info_gain,update,choose,simulate_episode,compare
import random

class ExperimentTests(unittest.TestCase):
    def test_entropy(self): self.assertAlmostEqual(entropy(.5),1.)
    def test_zero_entropy(self): self.assertEqual(entropy(0),0.)
    def test_information_ranking(self):
        x=[info_gain(.5,a) for a in ACTIONS]
        self.assertTrue(x[0]<x[1]<x[2])
    def test_bayes_positive(self): self.assertAlmostEqual(update(.5,ACTIONS[2],True),.93)
    def test_bayes_negative(self): self.assertAlmostEqual(update(.5,ACTIONS[2],False),.07)
    def test_best_information(self): self.assertEqual(choose(.5,'information_only').name,'strong_probe')
    def test_best_risk_aware(self): self.assertEqual(choose(.5,'risk_aware').name,'gentle_probe')
    def test_consent_enforced_information(self): self.assertEqual(choose(.5,'information_only',False).name,'passive')
    def test_consent_enforced_risk(self): self.assertEqual(choose(.5,'risk_aware',False).name,'passive')
    def test_passive_cannot_dissolve(self):
        x=simulate_episode(True,'passive_only',random.Random(42))
        self.assertTrue(x['survives'])
    def test_refusal_recorded(self):
        x=simulate_episode(True,'information_only',random.Random(42),False)
        self.assertTrue(all(row['action']=='passive' and not row['consent'] for row in x['trace']))
    def test_reproducible(self): self.assertEqual(compare(100,44),compare(100,44))
    def test_survival_cost(self):
        z=compare(3000,44)
        self.assertGreater(z['risk_aware']['survival_rate'],z['information_only']['survival_rate'])
    def test_accuracy_tradeoff(self):
        z=compare(3000,44)
        self.assertLess(z['information_only']['mean_brier'],z['passive_only']['mean_brier'])

if __name__=='__main__': unittest.main()
