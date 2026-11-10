import unittest
import numpy as np
from quantum_hydrogen import integrals,solve_h2,solve_h2plus,boys0

class QuantumHydrogenTests(unittest.TestCase):
    def test_boys_zero(self):self.assertAlmostEqual(boys0(0),1)
    def test_overlap_symmetric_normalized(self):
        s,h,eri,rep=integrals(.74)
        np.testing.assert_allclose(s,s.T,atol=1e-10)
        np.testing.assert_allclose(np.diag(s),np.ones(2),atol=3e-7)
    def test_eri_permutation(self):
        eri=integrals(.74)[2]
        np.testing.assert_allclose(eri,np.transpose(eri,(1,0,2,3)),atol=1e-12)
        np.testing.assert_allclose(eri,np.transpose(eri,(2,3,0,1)),atol=1e-12)
    def test_h2_known_minimal_basis_benchmark(self):
        self.assertAlmostEqual(solve_h2(.74)['energy_hartree'],-1.1167593,places=5)
    def test_h2_local_minimum(self):
        e=solve_h2(.73)['energy_hartree']
        self.assertLess(e,solve_h2(.5)['energy_hartree'])
        self.assertLess(e,solve_h2(1.2)['energy_hartree'])
    def test_h2plus_local_minimum(self):
        e=solve_h2plus(1.05)['energy_hartree']
        self.assertLess(e,solve_h2plus(.5)['energy_hartree'])
        self.assertLess(e,solve_h2plus(2.0)['energy_hartree'])
    def test_h2plus_below_separated_reference(self):
        self.assertLess(solve_h2plus(1.05)['energy_hartree'],-.46658)
    def test_h2plus_repulsion_at_short_distance(self):
        self.assertGreater(solve_h2plus(.3)['energy_hartree'],solve_h2plus(1.05)['energy_hartree'])
    def test_h2_rhf_dissociation_warning_observable(self):
        # RHF at large R is spuriously too HIGH (less negative) relative to two separated H atoms.
        self.assertGreater(solve_h2(3.0)['energy_hartree'],2*(-.46658185))
    def test_energy_finite(self):
        for r in [.4,.8,1.5,3.0]:
            self.assertTrue(np.isfinite(solve_h2(r)['energy_hartree']))
            self.assertTrue(np.isfinite(solve_h2plus(r)['energy_hartree']))
if __name__=='__main__':unittest.main()
