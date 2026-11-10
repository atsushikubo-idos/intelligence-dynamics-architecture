"""Minimal-basis ab initio Born-Oppenheimer curves for H2 and H2+.
Pure NumPy/SciPy, STO-3G contracted 1s Gaussian basis on H nuclei.
H2: restricted Hartree-Fock (RHF); H2+: one-electron generalized eigensolver.
Atomic units throughout internally.
"""
from __future__ import annotations
import math
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf

BOHR_PER_ANGSTROM = 1.8897261246257702
HARTREE_TO_EV = 27.211386245988
EXPONENTS = (3.42525091, 0.62391373, 0.16885540)
COEFFICIENTS = (0.15432897, 0.53532814, 0.44463454)


def boys0(t: float) -> float:
    if t < 1e-9:
        return 1 - t / 3 + t*t / 10
    return 0.5 * math.sqrt(math.pi / t) * float(erf(math.sqrt(t)))


def primitives(center):
    return [(a, c * (2*a/math.pi)**0.75, np.asarray(center, dtype=float))
            for a, c in zip(EXPONENTS, COEFFICIENTS)]


def pair(a, b):
    ea,ca,ra = a; eb,cb,rb = b
    p = ea+eb; mu=ea*eb/p; rab2=float(np.sum((ra-rb)**2))
    P=(ea*ra+eb*rb)/p
    return p,mu,rab2,P,ca*cb*math.exp(-mu*rab2)


def integrals(r_angstrom: float):
    R=r_angstrom*BOHR_PER_ANGSTROM
    nuclei=[np.array([0.,0.,-R/2]),np.array([0.,0.,R/2])]
    bas=[primitives(c) for c in nuclei]
    S=np.zeros((2,2)); T=np.zeros((2,2)); V=np.zeros((2,2)); eri=np.zeros((2,2,2,2))
    for i in range(2):
      for j in range(2):
        for aa in bas[i]:
          for bb in bas[j]:
            p,mu,rab2,P,pref=pair(aa,bb)
            norm= pref*(math.pi/p)**1.5
            S[i,j]+=norm
            T[i,j]+=mu*(3-2*mu*rab2)*norm
            for nuc in nuclei:
              V[i,j]+=-2*math.pi/p*pref*boys0(p*float(np.sum((P-nuc)**2)))
        for k in range(2):
          for l in range(2):
            for aa in bas[i]:
              for bb in bas[j]:
                p,mu,rab2,P,pref=pair(aa,bb)
                for cc in bas[k]:
                  for dd in bas[l]:
                    q,nu,rcd2,Q,pref2=pair(cc,dd)
                    t=p*q/(p+q)*float(np.sum((P-Q)**2))
                    eri[i,j,k,l] += pref*pref2*2*math.pi**2.5/(p*q*math.sqrt(p+q))*boys0(t)
    return S,T+V,eri,1/R


def solve_h2plus(r_angstrom: float):
    S,H,_,rep=integrals(r_angstrom)
    vals,vec=eigh(H,S)
    return {'energy_hartree':float(vals[0]+rep),'orbital_hartree':float(vals[0]),
            'coefficients':vec[:,0].tolist()}


def solve_h2(r_angstrom:float, max_iter=150, tol=1e-11):
    S,H,eri,rep=integrals(r_angstrom)
    evals,U=np.linalg.eigh(S)
    X=U@np.diag(evals**-0.5)@U.T
    # Symmetry-preserving initial guess: doubly occupied bonding MO.
    eps,Cp=np.linalg.eigh(X.T@H@X)
    C=X@Cp
    P=2*np.outer(C[:,0],C[:,0]); Eprev=None
    for iteration in range(1,max_iter+1):
        J=np.einsum('ls,mnls->mn',P,eri,optimize=True)
        K=np.einsum('ls,mlns->mn',P,eri,optimize=True)
        F=H+J-0.5*K
        eps,Cp=np.linalg.eigh(X.T@F@X)
        C=X@Cp
        new_P=2*np.outer(C[:,0],C[:,0])
        E=float(0.5*np.sum(new_P*(H+F))+rep)
        if Eprev is not None and abs(E-Eprev)<tol and np.max(abs(new_P-P))<tol:
            return {'energy_hartree':E,'iterations':iteration,'orbital_hartree':float(eps[0])}
        P=new_P; Eprev=E
    raise RuntimeError(f'SCF did not converge at {r_angstrom} A')


def scan(distances):
    return [{'distance_angstrom':float(r), 'h2_hartree':solve_h2(float(r))['energy_hartree'],
             'h2plus_hartree':solve_h2plus(float(r))['energy_hartree']}
            for r in distances]

if __name__ == '__main__':
    for r in [0.5,0.7,0.74,0.9,1.5,3.0]:
        print(r, solve_h2(r)['energy_hartree'],solve_h2plus(r)['energy_hartree'])
