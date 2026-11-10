"""Reproduce the v0.7 explicit-environment study using v0.5 and v0.6 files."""
from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from h2_fci import solve_fci
from h2_nuclear_dynamics_v06 import Potential, DISSOCIATION_HARTREE
from h2_explicit_bath_v07 import BathConfig,simulate
HERE=Path(__file__).resolve().parent

def build_potential():
    # Same additional grid used in v0.6, explicitly regenerated from v0.5 FCI.
    tail=[(float(r),solve_fci(float(r))['energy_hartree']) for r in
        [0.20,0.25,0.30,0.35,0.40,0.45,0.48,0.60,0.66,0.68,0.70,0.72,0.74,0.76,0.78,0.80]+list(np.linspace(3.2,8.,25))]
    return Potential(HERE/'h2_fci_comparison.csv',tail)

def run_all(duration_fs=180,dt_au=.12):
    p=build_potential()
    cases={
       'isolated':BathConfig(duration_fs=duration_fs,dt_au=dt_au),
       'single_weak':BathConfig(modes=1,lambda_total=.01,duration_fs=duration_fs,dt_au=dt_au),
       'single_strong':BathConfig(modes=1,lambda_total=.08,duration_fs=duration_fs,dt_au=dt_au),
       'distributed_24':BathConfig(modes=24,lambda_total=.03,duration_fs=duration_fs,dt_au=dt_au),
    }
    results={k:simulate(p,v) for k,v in cases.items()}
    if duration_fs==180 and dt_au==.12:
        with (HERE/'h2_explicit_bath_v07.csv').open('w',newline='',encoding='utf8') as f:
            w=csv.writer(f);w.writerow(['scenario','time_fs','r_angstrom','H2_energy_hartree',
                         'bath_oscillator_energy_hartree','interaction_energy_hartree','total_energy_hartree'])
            for label,res in results.items():
                for row in res['trajectory']:w.writerow([label,*[float(y) for y in row]])
        report={'name':'Explicit finite harmonic bath coupled to H2 FCI BO potential, v0.7',
                'potential':'v0.5 STO-3G FCI curve using v0.6 spline extension',
                'model':'classical nuclei + classical finite harmonic oscillator environment with completed-square coupling counterterm',
                'energy_conservation':'total molecular + bare oscillators + interaction',
                'retention_definition':'r < 2 A and molecular energy below isolated dissociation reference for every sampled point of last quarter of a finite run; only a proxy',
                'limitations':['not quantum H2 formation kinetics','one-dimensional zero-angular-momentum encounter',
                'finite bath may return energy to molecule','counterterm and oscillator couplings are phenomenological',
                'no radiative transitions, grain lattice, temperature ensemble or formation rate'],
                'scenarios':{k:{kk:vv for kk,vv in res.items() if kk not in ('trajectory','initial_state','final_state')}
                             for k,res in results.items()}}
        (HERE/'h2_explicit_bath_results_v07.json').write_text(json.dumps(report,indent=2),encoding='utf8')
        fig,axs=plt.subplots(2,1,figsize=(9,7.2),sharex=True)
        for label,res in results.items():
            a=res['trajectory'];axs[0].plot(a[:,0],a[:,1],lw=1.2,label=label)
            if label!='isolated':axs[1].plot(a[:,0],a[:,3]+a[:,4],lw=1.1,label=label)
        axs[0].axhline(p.equilibrium()[0],color='gray',ls=':',label='FCI energy minimum')
        axs[0].set_ylabel('H–H internuclear distance (Å)');axs[0].set_ylim(.4,8.1)
        axs[0].legend(fontsize=8,ncol=2)
        axs[1].set_xlabel('Time (fs)');axs[1].set_ylabel('Bath + interaction energy (Ha)')
        axs[1].legend(fontsize=8)
        fig.suptitle('H₂ nuclear motion with an explicit finite harmonic environment (energy conserving)')
        fig.tight_layout();fig.savefig(HERE/'H2_explicit_bath_v07.png',dpi=180);plt.close(fig)
    return results
if __name__=='__main__':
    r=run_all()
    for name,s in r.items():
        print(name, 'distance',round(s['last_distance_angstrom'],3),'molecule E above diss.',
              round(s['final_molecular_energy_above_dissociation'],5), 'retained',s['finite_window_retention'],
              'energy drift',s['maximum_recorded_energy_drift'],'stopped',s['stop_reason'])
