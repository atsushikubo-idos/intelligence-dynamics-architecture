"""Reproduce the physics validation and create data/plots (run from any cwd)."""
import csv
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from quantum_hydrogen import solve_h2, solve_h2plus, BOHR_PER_ANGSTROM,HARTREE_TO_EV

ROOT=Path(__file__).resolve().parent

def main():
    grid=np.linspace(.45,3.20,90)
    h2=np.array([solve_h2(float(r))['energy_hartree'] for r in grid])
    h2p=np.array([solve_h2plus(float(r))['energy_hartree'] for r in grid])
    best_h2=minimize_scalar(lambda r:solve_h2(float(r))['energy_hartree'],bounds=(.55,1.0),method='bounded',options={'xatol':1e-8})
    best_h2p=minimize_scalar(lambda r:solve_h2plus(float(r))['energy_hartree'],bounds=(.7,1.6),method='bounded',options={'xatol':1e-8})
    rows=[{'distance_angstrom':round(float(r),8),'h2_rhf_hartree':round(float(e),10),'h2plus_one_electron_hartree':round(float(ep),10)} for r,e,ep in zip(grid,h2,h2p)]
    with (ROOT/'energy_curve.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    # two unambiguous plots; they are not a time-dependent chemical reaction simulation.
    for key,energies,rmin,label in [('H2_RHF',h2,best_h2.x,'H2 (RHF / STO-3G)'),('H2plus',h2p,best_h2p.x,'H2+ (one-electron / STO-3G)')]:
        fig,ax=plt.subplots(figsize=(7,4.6))
        ax.plot(grid,energies,label=label)
        ax.axvline(rmin,ls='--',alpha=.6,label=f'Minimum ~ {rmin:.3f} Å')
        ax.set_xlabel('Internuclear distance (Å)');ax.set_ylabel('Total Born–Oppenheimer energy (Hartree)')
        ax.set_title('Electronic-structure energy curve (not reaction kinetics)')
        ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(ROOT/f'{key}_energy_curve.png',dpi=170);plt.close(fig)
    atom_sto3g=-0.466581849557275
    results={
      'method':'H2: restricted Hartree-Fock / H2+: exact one-electron diagonalization in minimal STO-3G basis',
      'units':{'distance':'angstrom','energy':'hartree'},
      'h2_minimum':{'distance_angstrom':float(best_h2.x),'energy_hartree':float(best_h2.fun)},
      'h2plus_minimum':{'distance_angstrom':float(best_h2p.x),'energy_hartree':float(best_h2p.fun)},
      'h2_at_0_74A_hartree':solve_h2(.74)['energy_hartree'],
      'minimal_basis_H_atom_energy_hartree':atom_sto3g,
      'h2plus_basis_separation_reference_hartree':atom_sto3g,
      'h2_rhf_warning':'Restricted HF yields qualitatively incorrect dissociation for H2 due to static correlation; this is not bond-formation kinetics.',
      'limitations':['Born-Oppenheimer nuclei fixed for each distance','Minimal STO-3G basis, no electron correlation in H2','No time evolution, collision, radiation, third body or energy dissipation','Does not establish a chemical reaction rate or spontaneous bond formation','No IDOS-specific empirical advantage tested']
    }
    (ROOT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(results,indent=2))
    return results
if __name__=='__main__': main()
