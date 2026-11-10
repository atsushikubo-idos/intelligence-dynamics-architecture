import unittest
import numpy as np
from h2_fci import solve_fci,hamiltonian,DETERMINANTS,apply
from quantum_hydrogen import solve_h2

class FCITests(unittest.TestCase):
    def test_six_determinants(self): self.assertEqual(len(DETERMINANTS),6)
    def test_fermion_anticommutation(self):
        self.assertIsNone(apply(0,[('a',0)]))
        self.assertEqual(apply(0,[('c',0),('c',1)]),(3,-1))
        self.assertEqual(apply(0,[('c',1),('c',0)]),(3,1))
    def test_hermitian(self):
        H,_=hamiltonian(.74)
        np.testing.assert_allclose(H,H.T,atol=1e-12)
    def test_reference_equilibrium(self): self.assertAlmostEqual(solve_fci(.74)['energy_hartree'],-1.1372838,places=6)
    def test_fci_variational_lower(self):
        for r in [.65,.74,1,1.5,2,3]:
            self.assertLessEqual(solve_fci(r)['energy_hartree'],solve_h2(r)['energy_hartree']+1e-9)
    def test_dissociation_to_2h(self):
        self.assertAlmostEqual(solve_fci(8)['energy_hartree'],2*(-.466581849557275),places=6)
    def test_rhf_incorrect_at_stretch(self):
        self.assertGreater(solve_h2(3)['energy_hartree']-solve_fci(3)['energy_hartree'],0.25)
    def test_nonzero_correlation_at_equilibrium(self):
        self.assertGreater(solve_h2(.74)['energy_hartree']-solve_fci(.74)['energy_hartree'],0.02)
    def test_stretch_correlation_greater(self):
        self.assertGreater(solve_h2(2)['energy_hartree']-solve_fci(2)['energy_hartree'],solve_h2(.74)['energy_hartree']-solve_fci(.74)['energy_hartree'])
    def test_spectrum_ordered(self):
        spectrum=solve_fci(.74)['spectrum_hartree']
        self.assertEqual(len(spectrum),6)
        self.assertTrue(all(a<=b for a,b in zip(spectrum,spectrum[1:])))
    def test_ground_state_normalized(self):
        weights=solve_fci(.74)['determinant_weights']
        self.assertAlmostEqual(sum(weights.values()),1,places=10)
    def test_two_hydrogen_ref(self):
        self.assertLess(abs(solve_fci(5)['energy_hartree']+0.93316369911455),1e-5)

if __name__=='__main__':unittest.main()
