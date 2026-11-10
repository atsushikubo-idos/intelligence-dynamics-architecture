"""Reproduce v0.6 dynamics using prior v0.5 FCI CSV and new FCI tail points."""
from pathlib import Path
import csv, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from h2_fci import solve_fci
from h2_nuclear_dynamics_v06 import Potential,run_trajectory, DISSOCIATION_HARTREE

HERE=Path(__file__).resolve().parent

def build():
    tail=[(float(r),solve_fci(float(r))['energy_hartree']) for r in [0.20,0.25,0.30,0.35,0.40,0.45,0.48,0.60,0.66,0.68,0.70,0.72,0.74,0.76,0.78,0.80]+list(np.linspace(3.2,8.0,25))]
    potential=Potential(HERE/'h2_fci_comparison.csv',tail)
    systems={'isolated':0.0,'weak_damping':0.0002,'moderate_damping':0.001}
    runs={k:run_trajectory(potential,gamma_per_au=g) for k,g in systems.items()}
    with open(HERE/'h2_nuclear_dynamics_v06.csv','w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['scenario','time_fs','distance_angstrom','mechanical_energy_hartree','cumulative_heat_hartree'])
        for name,run in runs.items():
            for values in zip(run['time_fs'],run['r_angstrom'],run['energy_hartree'],run['heat_hartree']):
                w.writerow([name,*map(lambda x:float(x),values)])
    eq_r, eq_e=potential.equilibrium()
    report={'model':'classical 1D zero-impact-parameter nuclear motion on H2 FCI/STO-3G Born-Oppenheimer ground-state curve',
            'electronic_energies':'v0.5 FCI CSV, plus FCI-computed short-range points (0.20–0.48 A), refined well (0.60–0.80 A), and long-range tail (3.2–8.0 A)',
            'dissociation_reference_hartree':DISSOCIATION_HARTREE,
            'equilibrium_angstrom':eq_r,'equilibrium_hartree':eq_e,
            'capture_definition':'mechanical energy below dissociation reference at the end; no statement of quantum reaction rates',
            'limitations':['classical nuclei','zero angular momentum','ground-state BO curve','minimal STO-3G basis','phenomenological damping, not microscopic photon or grain coupling','no statistical collision ensemble'],
            'scenarios':{k:{key:val for key,val in run.items() if not isinstance(val,np.ndarray)} for k,run in runs.items()}}
    (HERE/'h2_nuclear_results_v06.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    fig,ax=plt.subplots(figsize=(8,4.8))
    for k,r in runs.items():ax.plot(r['time_fs'],r['r_angstrom'],label=f'{k} ({r["outcome"]})',lw=1.4)
    ax.axhline(eq_r,color='0.5',ls=':',label='FCI equilibrium')
    ax.set_xlabel('Time (fs)');ax.set_ylabel('H–H internuclear distance (Å)');ax.set_title('Classical nuclear motion on H₂ STO-3G FCI potential')
    ax.legend(fontsize=7);fig.tight_layout();fig.savefig(HERE/'H2_nuclear_dynamics_v06.png',dpi=180);plt.close(fig)
    return report

if __name__=='__main__':
    report=build()
    print(json.dumps(report,indent=2))
