"""Fast invariant checks of the recorded, reproducible v0.8 experiment."""
import json, unittest
from pathlib import Path
from h2_bath_sensitivity_v08 import configurations
ROOT=Path(__file__).resolve().parent

class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=json.loads((ROOT/'h2_bath_sensitivity_v08.json').read_text())['cases']
    def test_11_cases(self):self.assertEqual(len(self.cases),11)
    def test_configurations(self):self.assertEqual(set(configurations()),{x['scenario'] for x in self.cases})
    def test_fixed_initial_conditions(self):self.assertEqual(len({(x['omega_min'],x['omega_max']) for x in self.cases if x['scenario'].count('_')==1}),1)
    def test_equal_total_coupling_across_mode_counts(self):
        for c in (.01,.03,.08):self.assertEqual({x['modes'] for x in self.cases if x['lambda_total']==c and x['omega_min']==.005}, {1,4,24})
    def test_positive_spectral_frequencies(self):self.assertTrue(all(x['omega_min']>0 and x['omega_max']>=x['omega_min'] for x in self.cases))
    def test_energy_conservation(self):self.assertTrue(all(x['energy_max_drift_Ha']<1.e-4 for x in self.cases))
    def test_tail_fraction_bounds(self):self.assertTrue(all(0<=x['tail_fraction_r_below_2A']<=1 for x in self.cases))
    def test_backflow_nonnegative(self):self.assertTrue(all(x['backflow_from_peak_Ha']>=-1.e-10 for x in self.cases))
    def test_24_frequency_controls(self):self.assertEqual(len([x for x in self.cases if x['modes']==24 and x['lambda_total']==.03]),3)
    def test_distinct_retention_behavior(self):self.assertGreater(len(set(round(x['tail_fraction_r_below_2A'],2) for x in self.cases)),1)

if __name__=='__main__':unittest.main()
