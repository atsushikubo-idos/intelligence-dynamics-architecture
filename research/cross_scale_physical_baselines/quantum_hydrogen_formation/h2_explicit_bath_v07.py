"""Explicit finite harmonic environment coupled to H2 FCI Born–Oppenheimer stretch.

Toy Hamiltonian, atomic units:
 H = p_r²/(2 μ) + V_FCI(r) + sum_j [p_j²/2 + (ω_j²/2)(q_j - c_j*f(r)/ω_j²)²].
 V_FCI is a spline from v0.5–v0.6. The completed square is a
 Caldeira–Leggett-style counterterm and preserves the relaxed BO potential.
 Integrate all degrees of freedom with velocity Verlet, NO drag/thermostat.
 This is not microscopic H2 formation, quantum nuclear motion or radiation.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from h2_nuclear_dynamics_v06 import (ANGSTROM_PER_BOHR, ATOMIC_TIME_FS,
                                        REDUCED_MASS, DISSOCIATION_HARTREE)

@dataclass(frozen=True)
class BathConfig:
    modes: int = 0
    lambda_total: float = 0.0  # total sum c_j^2/omega_j^2, Ha/bohr^2
    omega_min: float = .005    # atomic frequency units
    omega_max: float = .027
    width_bohr: float = 2.2
    collision_energy: float = .008
    start_angstrom: float = 4.0
    duration_fs: float = 180.
    dt_au: float = .12
    stride: int = 40


def coupling_profile(r, equilibrium_bohr, width_bohr):
    delta = r - equilibrium_bohr
    z = delta / width_bohr
    e = np.exp(-.5*z*z)
    return delta*e, e*(1-z*z)


def simulate(potential, cfg: BathConfig):
    if cfg.modes < 0 or cfg.lambda_total < 0 or cfg.duration_fs <= 0 or cfg.dt_au <= 0 or cfg.stride <= 0:
        raise ValueError('invalid bath or integration parameters')
    if cfg.modes == 0 and cfg.lambda_total != 0:
        raise ValueError('nonzero coupling with no modes')
    if cfg.modes and cfg.omega_min <= 0:
        raise ValueError('frequencies must be positive')
    re_angstrom,_ = potential.equilibrium()
    re = re_angstrom / ANGSTROM_PER_BOHR
    n = cfg.modes
    omega = np.linspace(cfg.omega_min,cfg.omega_max,n) if n else np.zeros(0)
    lam = np.full(n,cfg.lambda_total/n) if n else np.zeros(0)
    c=omega*np.sqrt(lam)
    r0=cfg.start_angstrom / ANGSTROM_PER_BOHR
    kinetic0=DISSOCIATION_HARTREE+cfg.collision_energy-potential.energy(r0)
    if kinetic0 <= 0: raise ValueError('initial kinetic energy not positive')
    x=np.zeros(2+2*n)
    x[0]=r0;x[1]=-np.sqrt(2*kinetic0/REDUCED_MASS)
    initial=x.copy()
    def parts(y):
        r,v=y[:2];q=y[2:2+n];vq=y[2+n:]
        f,_=coupling_profile(r,re,cfg.width_bohr)
        molecule=.5*REDUCED_MASS*v*v+potential.energy(r)
        oscillator=.5*np.sum(vq*vq+(omega*q)**2)
        interaction=-f*np.dot(c,q)+.5*f*f*np.sum(lam)
        return molecule,oscillator,interaction
    def forces(y):
        r=y[0];q=y[2:2+n]
        f,fp=coupling_profile(r,re,cfg.width_bohr)
        force_r=potential.force(r)+fp*(np.dot(c,q)-f*np.sum(lam))
        force_q=-(omega*omega)*q+c*f
        return force_r,force_q
    H0=sum(parts(x))
    # Avoid extrapolation outside the tabulated FCI potential.
    r_max=(potential.max_angstrom-1.e-4)/ANGSTROM_PER_BOHR
    r_min=(potential.min_angstrom+1.e-4)/ANGSTROM_PER_BOHR
    rows=[]
    max_drift=0.
    steps=int(cfg.duration_fs / ATOMIC_TIME_FS / cfg.dt_au)
    stop='time_limit'
    dt=cfg.dt_au
    for k in range(steps+1):
        if k%cfg.stride==0 or k==steps:
            Em,Eb,Ei=parts(x);total=Em+Eb+Ei
            max_drift=max(max_drift,abs(total-H0))
            rows.append([k*dt*ATOMIC_TIME_FS,x[0]*ANGSTROM_PER_BOHR,Em,Eb,Ei,total])
        if k==steps:break
        fr,fq=forces(x)
        vhalf=x[1]+.5*dt*fr/REDUCED_MASS
        vqhalf=x[2+n:]+.5*dt*fq
        x[0]+=dt*vhalf
        x[2:2+n]+=dt*vqhalf
        if x[0]>=r_max or x[0]<=r_min:
            stop='outer_boundary' if x[0]>=r_max else 'inner_boundary'
            # stop without evaluating the inaccessible potential or reporting
            # an incorrect final energy (last valid saved sample is retained).
            break
        fr,fq=forces(x)
        x[1]=vhalf+.5*dt*fr/REDUCED_MASS
        x[2+n:]=vqhalf+.5*dt*fq
    arr=np.asarray(rows,float)
    tail=arr[int(len(arr)*.75):]
    # Operational finite-window retention only, not asymptotic capture.
    retained=bool(stop=='time_limit' and np.all(tail[:,1] < 2.)
                  and np.all(tail[:,2] < DISSOCIATION_HARTREE))
    return {'trajectory':arr, 'initial_state':initial,'final_state':x,
            'initial_total_energy':float(H0),'maximum_recorded_energy_drift':float(max_drift),
            'stop_reason':stop,'last_recorded_time_fs':float(arr[-1,0]),
            'last_distance_angstrom':float(arr[-1,1]),
            'final_molecular_energy_above_dissociation':float(arr[-1,2]-DISSOCIATION_HARTREE),
            'finite_window_retention':retained, 'modes':n,
            'coupling_lambda_total':cfg.lambda_total,'frequency_au':omega.tolist(),
            'c_j':c.tolist(), 'number_samples':int(len(arr)),
            'min_distance_angstrom':float(np.min(arr[:,1])),
            'max_distance_angstrom':float(np.max(arr[:,1])),
            'max_oscillator_energy':float(np.max(arr[:,3])),
            'oscillator_energy_falls_at_some_point':bool(np.any(np.diff(arr[:,3]) < -1.e-6))}
