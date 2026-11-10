import math, unittest
from physical_baselines import bond_probability, ising_exact, ising_energies, projected_transition_example, schlogl_dx, rk4

class PhysicalBaselinesTests(unittest.TestCase):
    def test_bond_monotonic(self):
        self.assertGreater(bond_probability(-4,1),bond_probability(0,1))
        self.assertGreater(bond_probability(0,1),bond_probability(4,1))
    def test_bond_midpoint(self): self.assertAlmostEqual(bond_probability(0,1),0.5)
    def test_bond_invalid_temperature(self):
        with self.assertRaises(ValueError): bond_probability(0,0)
    def test_ising_spin_flip_energy_invariance(self):
        x=[1,1,-1,1,-1,1,1,1,-1]
        self.assertEqual(ising_energies(x,3),ising_energies([-a for a in x],3))
    def test_ising_state_count(self): self.assertEqual(ising_exact(3,2)['states'],512)
    def test_ising_low_temperature_more_order(self):
        self.assertGreater(ising_exact(3,.8)['mean_abs_magnetization'], ising_exact(3,5.)['mean_abs_magnetization'])
    def test_ising_energy_low_temperature(self):
        self.assertLess(ising_exact(3,.8)['energy_per_site'],ising_exact(3,5)['energy_per_site'])
    def test_coarse_nonlumpable(self):
        r=projected_transition_example()
        self.assertTrue(r['same_current_macrostate'] and r['strong_lumpability_violated'])
        self.assertAlmostEqual(r['conditional_spread'],.8)
    def test_schlogl_fixed_points(self):
        for x in (1.,2.,4.): self.assertAlmostEqual(schlogl_dx(x),0)
    def test_schlogl_stable_endpoints(self):
        for x,y in ((0.5,1),(1.5,1),(2.5,4),(5.,4)):
            self.assertAlmostEqual(rk4(x),y,places=5)

if __name__=='__main__':unittest.main()
