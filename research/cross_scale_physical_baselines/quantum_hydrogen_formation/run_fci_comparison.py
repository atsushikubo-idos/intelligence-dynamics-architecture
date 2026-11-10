"""Run v0.5 FCI/STO-3G vs v0.4 RHF/STO-3G with same AO integrals."""
from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from h2_fci import solve_fci
from quantum_hydrogen import solve_h2, HARTREE_TO_EV
ROOT=Path(__file__).resolve().parent

def main():
    # Restricted HF can exhibit convergence issues at long bond lengths;
    # keep fair RHF/FCI comparison up to 3A, FCI-only dissociation reference beyond.
    grid=np.linspace(.5,3,38)
    rows=[]
    for r in grid:
        rf=solve_h2(float(r))['energy_hartree']
        fc=solve_fci(float(r))['energy_hartree']
        rows.append({'distance_angstrom':round(float(r),7),'rhf_hartree':rf,'fci_hartree':fc,'correlation_hartree':rf-fc})
    with (ROOT/'h2_fci_comparison.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
    dissoc=2*(-.466581849557275)
    fig,ax=plt.subplots(figsize=(7.6,4.9))
    ax.plot(grid,[r['rhf_hartree'] for r in rows],label='Restricted Hartree–Fock (STO-3G)')
    ax.plot(grid,[r['fci_hartree'] for r in rows],label='Full configuration interaction (STO-3G)')
    ax.axhline(dissoc,ls=':',label='Separated H atoms (STO-3G)')
    ax.set(xlabel='H–H internuclear distance (Å)',ylabel='Total Born–Oppenheimer energy (Hartree)',title='H₂: electronic correlation and dissociation')
    ax.legend(fontsize=8);ax.grid(alpha=.15);fig.tight_layout()
    fig.savefig(ROOT/'H2_RHF_vs_FCI_v05.png',dpi=160);plt.close(fig)
    selected=[]
    for r in [.74,1,2,3]:
        rhf=solve_h2(r)['energy_hartree'];fci=solve_fci(r)['energy_hartree']
        selected.append({'distance_angstrom':r,'rhf_hartree':rhf,'fci_hartree':fci,'correlation_gap_hartree':rhf-fci,'correlation_gap_ev':(rhf-fci)*HARTREE_TO_EV})
    result={
        'version':'v0.5', 'description':'H2 STO-3G fixed-nuclei ab initio electronic-structure; 6-determinant FCI vs restricted Hartree-Fock',
        'selected_distances':selected,'fci_at_8_angstrom_hartree':solve_fci(8)['energy_hartree'],
        'two_isolated_h_atoms_sto3g_hartree':dissoc,
        'limits':['Not collision or bond formation in real time','No nuclear dynamics or dissipation','FCI exact only within STO-3G finite basis','RHF reference model may have stretched bond SCF failures; avoid unverified convergence','No IDOS-specific advantage or social inference established']}
    (ROOT/'h2_fci_results_v05.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
