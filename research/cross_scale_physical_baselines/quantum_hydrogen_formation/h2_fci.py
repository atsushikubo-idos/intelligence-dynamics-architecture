"""H2 full configuration interaction in STO-3G, reusing v0.4 AO integrals.

The 2-electron, 4-spin-orbital determinant basis has six states. Hamiltonian
is constructed directly in second quantization. Fixed nuclei, Born-Oppenheimer.
"""
from __future__ import annotations
from itertools import combinations
import numpy as np
from quantum_hydrogen import integrals

DETERMINANTS = tuple(sum(1 << i for i in occupied) for occupied in combinations(range(4),2))

def annihilate(det, orbital):
    if not (det >> orbital) & 1: return None
    parity = (det & ((1 << orbital) - 1)).bit_count()
    return det ^ (1 << orbital), (-1)**parity

def create(det, orbital):
    if (det >> orbital) & 1: return None
    parity = (det & ((1 << orbital) - 1)).bit_count()
    return det | (1 << orbital), (-1)**parity

def apply(det, ops):
    sign=1
    for kind,orb in ops: # executed right to left, listed in execution order
        result=annihilate(det,orb) if kind=='a' else create(det,orb)
        if result is None:return None
        det,s=result;sign*=s
    return det,sign

def hamiltonian(distance_angstrom):
    S,h,eri,rep=integrals(distance_angstrom)
    eig,U=np.linalg.eigh(S)
    X=U@np.diag(eig**-0.5)@U.T
    hm=X.T@h@X
    # chemist two-electron integrals (i j | k l) -> orthogonalized basis
    g=np.einsum('ai,bj,ck,dl,abcd->ijkl',X,X,X,X,eri,optimize=True)
    N=4;idx={det:i for i,det in enumerate(DETERMINANTS)}
    H=np.zeros((6,6))
    # spin-orbital id: spatial*2 + spin (0 alpha,1 beta)
    for j,det in enumerate(DETERMINANTS):
        for p in range(N):
            for q in range(N):
                if p%2 != q%2:continue
                term=apply(det,[('a',q),('c',p)])
                if term is not None:
                    d,s=term;H[idx[d],j]+=hm[p//2,q//2]*s
        for p in range(N):
            for q in range(N):
                if p%2 != q%2:continue
                for r in range(N):
                    for s in range(N):
                        if r%2 != s%2:continue
                        # (pq|rs) a†_p a†_r a_s a_q
                        term=apply(det,[('a',q),('a',s),('c',r),('c',p)])
                        if term is not None:
                            d,sgn=term;H[idx[d],j]+=0.5*g[p//2,q//2,r//2,s//2]*sgn
    H=(H+H.T)/2
    return H,rep

def solve_fci(distance_angstrom):
    H,rep=hamiltonian(distance_angstrom)
    w,v=np.linalg.eigh(H)
    return {'energy_hartree':float(w[0]+rep),'electronic_energy_hartree':float(w[0]),'determinant_weights':{format(d,'04b'):float(v[i,0]**2) for i,d in enumerate(DETERMINANTS)},'spectrum_hartree':[float(x+rep) for x in w]}
