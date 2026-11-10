"""Reproducible, dependency-free physical baselines; NOT a molecular simulation."""
from __future__ import annotations
import itertools, math, json
from dataclasses import dataclass


def bond_probability(delta_g: float, temperature: float) -> float:
    """Two-state equilibrium P(bound) for free-energy difference G_bound-G_unbound.

    Units: k_B=1. This is a toy *thermodynamic* two-state system, not quantum chemistry.
    """
    if temperature <= 0: raise ValueError('temperature must be positive')
    q = delta_g/temperature
    if q >= 0:
        z=math.exp(-q); return z/(1+z)
    z=math.exp(q); return 1/(1+z)


def ising_energies(spins, size: int, coupling: float=1.0):
    """Periodic square lattice, count right/down bonds once."""
    energy = 0.0
    for r in range(size):
        for c in range(size):
            spin = spins[r*size+c]
            energy -= coupling*spin*(spins[r*size+(c+1)%size] + spins[((r+1)%size)*size+c])
    return energy


def ising_exact(size: int, temperature: float):
    if size < 2 or size > 4 or temperature <= 0: raise ValueError('size 2..4 and positive T')
    n=size*size
    states=[]
    for spins in itertools.product((-1,1),repeat=n):
        en=ising_energies(spins,size)
        m=sum(spins)/n
        states.append((en,m))
    shift=min(e for e,_ in states)
    weights=[math.exp(-(en-shift)/temperature) for en,_ in states]
    z=sum(weights)
    e_avg=sum(w*en for w,(en,_) in zip(weights,states))/z/n
    abs_m=sum(w*abs(m) for w,(_,m) in zip(weights,states))/z
    m2=sum(w*m*m for w,(_,m) in zip(weights,states))/z
    return {'size':size,'temperature':temperature,'states':len(states),
            'mean_abs_magnetization':abs_m,'mean_magnetization_squared':m2,
            'energy_per_site':e_avg,
            'susceptibility_proxy': n*(m2-abs_m*abs_m)/temperature}


def projected_transition_example():
    """4-state micro-Markov chain; merge microstates (a,b) -> X, (c,d)->Y.
    From a, P(Y)=0.9, from b, P(Y)=0.1, so the projection is not strongly lumpable.
    """
    transition={
      'a':{'a':0.1,'c':0.9},
      'b':{'b':0.9,'c':0.1},
      'c':{'a':0.5,'d':0.5},
      'd':{'b':0.5,'d':0.5},
    }
    coarse={'a':'X','b':'X','c':'Y','d':'Y'}
    next_y={s:sum(p for dest,p in outs.items() if coarse[dest]=='Y') for s,outs in transition.items()}
    return {'p_next_Y_from_a':next_y['a'],'p_next_Y_from_b':next_y['b'],
      'same_current_macrostate':coarse['a']==coarse['b'],
      'strong_lumpability_violated':abs(next_y['a']-next_y['b'])>1e-12,
      'conditional_spread':abs(next_y['a']-next_y['b'])}


def schlogl_dx(x: float) -> float:
    """Mass-action chemostatted Schloegl-type model:
    A+2X -> 3X (7), 3X -> A+2X (1), B -> X (8), X -> B (14), A=B=1.
    dx/dt = 7*x*x - x**3 + 8 - 14*x = -(x-1)(x-2)(x-4).
    The parameters are selected to give exactly 3 steady states.
    """
    return 7*x*x - x*x*x + 8 - 14*x


def rk4(x0: float, dt:float=0.002, steps:int=20000) -> float:
    x=x0
    for _ in range(steps):
        k1=schlogl_dx(x)
        k2=schlogl_dx(x+dt*k1/2)
        k3=schlogl_dx(x+dt*k2/2)
        k4=schlogl_dx(x+dt*k3)
        x+=dt*(k1+2*k2+2*k3+k4)/6
    return x


def results():
    bonds={str(x):bond_probability(x,1.0) for x in (-4.,0.,4.)}
    temps=[0.8,2.0,5.0]
    ising=[ising_exact(3,T) for T in temps]
    coarse=projected_transition_example()
    starts={str(x):rk4(x) for x in (0.5,1.5,2.5,5.0)}
    return {'caveats': ['synthetic physical models; no atoms simulated',
      'finite 3x3 Ising lattice, not proof of a phase transition',
      'no IDOS-specific advantage tested'],
      'bond_two_state':{'temperature':1.0,'bound_probability_by_delta_g':bonds},
      'ising_exact_3x3':ising,
      'coarse_graining':coarse,
      'schlogl_mass_action':{'fixed_points':[1.,2.,4.],
         'stability':['stable','unstable','stable'],
         'endpoints_by_initial':starts}}

if __name__=='__main__':
    print(json.dumps(results(),indent=2,ensure_ascii=False))
