"""Run: python -m unittest test_h2_explicit_bath_v07.py"""
import unittest
import numpy as np
from run_explicit_bath_v07 import build_potential
from h2_explicit_bath_v07 import BathConfig,simulate,coupling_profile
from h2_nuclear_dynamics_v06 import DISSOCIATION_HARTREE

class ExplicitBathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=build_potential()
        cls.cases={
          'isolated':simulate(cls.p,BathConfig(duration_fs=180)),
          'single_weak':simulate(cls.p,BathConfig(modes=1,lambda_total=.01,duration_fs=180)),
          'single_strong':simulate(cls.p,BathConfig(modes=1,lambda_total=.08,duration_fs=180)),
          'distributed_24':simulate(cls.p,BathConfig(modes=24,lambda_total=.03,duration_fs=180)),
        }
    def test_profile_center(self):
        f,fp=coupling_profile(2,2,2.2);self.assertAlmostEqual(f,0);self.assertAlmostEqual(fp,1)
    def test_profile_odd(self):
        self.assertAlmostEqual(coupling_profile(2.6,2,2.2)[0],-coupling_profile(1.4,2,2.2)[0])
    def test_nonzero_coupling_requires_modes(self):
        with self.assertRaises(ValueError):simulate(self.p,BathConfig(lambda_total=.01,duration_fs=1))
    def test_negative_coupling(self):
        with self.assertRaises(ValueError):simulate(self.p,BathConfig(modes=1,lambda_total=-1,duration_fs=1))
    def test_zero_oscillators(self):self.assertEqual(self.cases['isolated']['modes'],0)
    def test_total_energy_conserved(self):
        for k,v in self.cases.items():
            with self.subTest(case=k):self.assertLess(v['maximum_recorded_energy_drift'],1.e-5)
    def test_bath_initially_at_rest(self):
        for k,v in self.cases.items():
            if k!='isolated':self.assertAlmostEqual(v['trajectory'][0,3],0.)
    def test_isolated_unbound(self):self.assertFalse(self.cases['isolated']['finite_window_retention'])
    def test_isolated_escapes(self):self.assertEqual(self.cases['isolated']['stop_reason'],'outer_boundary')
    def test_single_weak_escapes(self):self.assertEqual(self.cases['single_weak']['stop_reason'],'outer_boundary')
    def test_distributed_remains_finite_window(self):self.assertTrue(self.cases['distributed_24']['finite_window_retention'])
    def test_retained_has_below_dissociation_energy(self):
        self.assertLess(self.cases['distributed_24']['trajectory'][-1,2],DISSOCIATION_HARTREE)
    def test_explicit_bath_takes_energy(self):
        self.assertGreater(self.cases['distributed_24']['max_oscillator_energy'],.05)
    def test_energy_backflow_exists(self):
        self.assertTrue(self.cases['single_strong']['oscillator_energy_falls_at_some_point'])
    def test_bath_dimensions(self):
        self.assertEqual(len(self.cases['distributed_24']['frequency_au']),24)
    def test_comparative_controls(self):
        self.assertGreater(self.cases['isolated']['last_distance_angstrom'],7.9)
        self.assertLess(self.cases['distributed_24']['last_distance_angstrom'],2.)
    def test_finite_window_not_automatic(self):
        self.assertFalse(self.cases['single_strong']['finite_window_retention'])

if __name__=='__main__':unittest.main()
