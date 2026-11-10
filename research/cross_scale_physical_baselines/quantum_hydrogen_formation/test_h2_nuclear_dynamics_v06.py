"""Regression tests for classical 1D trajectory audit v0.6."""
import unittest
from pathlib import Path
import numpy as np
from h2_fci import solve_fci
from h2_nuclear_dynamics_v06 import Potential,run_trajectory,DISSOCIATION_HARTREE

HERE=Path(__file__).resolve().parent

class DynamicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tail=[(float(r),solve_fci(float(r))['energy_hartree']) for r in [0.20,0.25,0.30,0.35,0.40,0.45,0.48,0.60,0.66,0.68,0.70,0.72,0.74,0.76,0.78,0.80]+list(np.linspace(3.2,8.,25))]
        cls.p=Potential(HERE/'h2_fci_comparison.csv',tail)
        cls.iso=run_trajectory(cls.p,gamma_per_au=0)
        cls.weak=run_trajectory(cls.p,gamma_per_au=.0002)
        cls.mod=run_trajectory(cls.p,gamma_per_au=.001)

    def test_well_near_experimental_distance_not_fit_to_experiment(self):
        r,E=self.p.equilibrium();self.assertTrue(.68<r<.82)
    def test_well_below_atomic_limit(self):
        self.assertLess(self.p.equilibrium()[1],DISSOCIATION_HARTREE-.15)
    def test_initial_energy_positive_relative_to_dissociation(self):
        self.assertAlmostEqual(self.iso['initial_energy_hartree']-DISSOCIATION_HARTREE,.008,places=8)
    def test_isolated_escapes(self):
        self.assertEqual(self.iso['outcome'],'outgoing_escape_from_curve')
    def test_isolated_energy_conserved(self):
        self.assertLess(self.iso['energy_balance_max_error_hartree'],1e-6)
    def test_isolated_has_no_energy_release(self):
        self.assertEqual(float(self.iso['heat_hartree'][-1]),0)
    def test_damping_weak_captures(self):
        self.assertEqual(self.weak['outcome'],'energetically_bound_at_end')
    def test_damping_moderate_captures(self):
        self.assertEqual(self.mod['outcome'],'energetically_bound_at_end')
    def test_dissipation_monotonic(self):
        for trajectory in (self.weak,self.mod):
            self.assertGreater(float(trajectory['heat_hartree'][-1]),0.)
            self.assertGreaterEqual(float(np.min(np.diff(trajectory['heat_hartree']))),-1e-12)
    def test_total_energy_accounting(self):
        for run in (self.iso,self.weak,self.mod):
            self.assertLess(run['energy_balance_max_error_hartree'],1e-6)
    def test_stronger_damping_more_release(self):
        self.assertGreater(float(self.mod['heat_hartree'][-1]),float(self.weak['heat_hartree'][-1]))
    def test_close_approach_not_always_bonding(self):
        self.assertLess(self.iso['minimum_r_angstrom'],.5)
        self.assertEqual(self.iso['outcome'],'outgoing_escape_from_curve')
    def test_bad_friction_rejected(self):
        with self.assertRaises(ValueError):run_trajectory(self.p,gamma_per_au=-.01)
    def test_bad_collision_energy_rejected(self):
        with self.assertRaises(ValueError):run_trajectory(self.p,collision_energy_hartree=-.01)
    def test_initial_conditions_identical(self):
        self.assertAlmostEqual(self.iso['initial_energy_hartree'],self.weak['initial_energy_hartree'])
        self.assertAlmostEqual(self.iso['initial_energy_hartree'],self.mod['initial_energy_hartree'])

if __name__=='__main__': unittest.main()
