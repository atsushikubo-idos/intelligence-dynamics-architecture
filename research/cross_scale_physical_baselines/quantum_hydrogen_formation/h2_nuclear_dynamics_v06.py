"""v0.6: classical zero-angular-momentum nuclear motion on the H2 STO-3G FCI BO curve.

IMPORTANT: phenomenological velocity drag is NOT radiative or grain-surface
chemistry, and no formation rate, quantum nuclear dynamics or actual H2 reaction
mechanism is inferred here. Zero impact parameter is imposed; capture is defined
relative to the finite-basis two-H dissociation asymptote.
"""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

ANGSTROM_PER_BOHR = 0.529177210903
ATOMIC_TIME_FS = 0.02418884326505
HYDROGEN_NUCLEAR_MASS_ME = 1836.15267343  # approximate proton mass; BO nuclei
REDUCED_MASS = HYDROGEN_NUCLEAR_MASS_ME / 2
DISSOCIATION_HARTREE = -0.93316369911455  # TWO isolated H atoms in STO-3G

class Potential:
    def __init__(self, csv_path: str | Path, tail_points: list[tuple[float, float]]):
        with open(csv_path, newline='', encoding='utf8') as f:
            rows = list(csv.DictReader(f))
        a = [(float(r['distance_angstrom']), float(r['fci_hartree'])) for r in rows]
        a += tail_points
        a.sort()
        distances, energies = np.asarray(a).T
        if not np.all(np.diff(distances) > 0):
            raise ValueError('distance must be strictly increasing')
        self.min_angstrom, self.max_angstrom = distances[0], distances[-1]
        self.interpolation = PchipInterpolator(distances / ANGSTROM_PER_BOHR, energies, extrapolate=False)
        self.derivative = self.interpolation.derivative()

    def energy(self, r_bohr):
        val = self.interpolation(r_bohr)
        return float(val) if np.ndim(val)==0 else val

    def force(self, r_bohr):
        val = -self.derivative(r_bohr)
        return float(val) if np.ndim(val)==0 else val

    def equilibrium(self):
        from scipy.optimize import minimize_scalar
        result = minimize_scalar(self.energy, bounds=(0.57 / ANGSTROM_PER_BOHR, 1.0 / ANGSTROM_PER_BOHR), method='bounded')
        return float(result.x * ANGSTROM_PER_BOHR), float(result.fun)


def run_trajectory(potential: Potential, collision_energy_hartree: float=0.008,
                   gamma_per_au: float=0.0, start_angstrom: float=4.0,
                   duration_fs: float=160., n_samples: int=2001):
    if collision_energy_hartree <= 0 or gamma_per_au < 0:
        raise ValueError('positive collision energy and nonnegative friction required')
    r0 = start_angstrom / ANGSTROM_PER_BOHR
    kinetic0 = DISSOCIATION_HARTREE + collision_energy_hartree - potential.energy(r0)
    if kinetic0 <= 0:
        raise ValueError('initial kinetic energy nonpositive')
    v0 = -np.sqrt(2 * kinetic0 / REDUCED_MASS)
    time_max = duration_fs / ATOMIC_TIME_FS
    rmin = potential.min_angstrom / ANGSTROM_PER_BOHR + 1e-7
    rmax = potential.max_angstrom / ANGSTROM_PER_BOHR - 1e-7

    def f(t, x):
        r, v, heat = x
        # Damping force proportional to v. Integrated 'heat' is energy released.
        return [v, potential.force(r)/REDUCED_MASS-gamma_per_au*v,
                gamma_per_au*REDUCED_MASS*v*v]

    def escape(t, x): return x[0]-rmax
    escape.terminal = True
    escape.direction = 1
    def beyond_inner(t,x):return x[0]-rmin
    beyond_inner.terminal = True
    beyond_inner.direction = -1
    ts=np.linspace(0,time_max,n_samples)
    sol=solve_ivp(f,(0,time_max),[r0,v0,0.],rtol=1e-10,atol=1e-12,
                  max_step=1.,dense_output=True,events=[escape,beyond_inner])
    ts=ts[ts <= sol.t[-1]]
    if ts[-1] < sol.t[-1]:ts=np.r_[ts,sol.t[-1]]
    r,v,heat=sol.sol(ts)
    potential_e=potential.energy(r)
    kinetic=.5*REDUCED_MASS*v*v
    energy=kinetic+potential_e
    initial_energy=.5*REDUCED_MASS*v0*v0+potential.energy(r0)
    balance_error=np.max(np.abs(energy+heat-initial_energy))
    if sol.t_events[0].size:outcome='outgoing_escape_from_curve'
    elif sol.t_events[1].size:outcome='hit_inner_boundary'
    elif energy[-1] < DISSOCIATION_HARTREE:outcome='energetically_bound_at_end'
    else:outcome='still_unbound_at_end'
    return {'time_fs':ts*ATOMIC_TIME_FS,'r_angstrom':r*ANGSTROM_PER_BOHR,
            'v_bohr_per_au':v,'energy_hartree':energy,'heat_hartree':heat,
            'initial_energy_hartree':initial_energy,'energy_balance_max_error_hartree':float(balance_error),
            'final_energy_relative_dissociation_hartree':float(energy[-1]-DISSOCIATION_HARTREE),
            'outcome':outcome,'gamma_per_au':gamma_per_au,
            'final_time_fs':float(ts[-1]*ATOMIC_TIME_FS),
            'minimum_r_angstrom':float(np.min(r*ANGSTROM_PER_BOHR)),
            'initial_collision_energy_hartree':collision_energy_hartree}
