"""v0.8 controlled finite-bath sensitivity experiment; requires v0.5-v0.7 modules."""
from pathlib import Path
import csv, json
import numpy as np
from run_explicit_bath_v07 import build_potential
from h2_explicit_bath_v07 import BathConfig, simulate

HERE=Path(__file__).resolve().parent

def configurations():
    cases={}
    for n in (1, 4, 24):
        for coupling in (.01,.03,.08):
            cases[f'N{n}_L{coupling:.2f}']=dict(modes=n,lambda_total=coupling,omega_min=.005,omega_max=.027)
    cases['N24_L0.03_narrow']=dict(modes=24,lambda_total=.03,omega_min=.012,omega_max=.014)
    cases['N24_L0.03_high']=dict(modes=24,lambda_total=.03,omega_min=.025,omega_max=.047)
    return cases

def describe(potential, cfg):
    r=simulate(potential,cfg)
    t=r['trajectory']
    tail=t[t[:,0]>=135.]
    bath=t[:,3]+t[:,4]
    return {'stop_reason':r['stop_reason'], 'last_time_fs':r['last_recorded_time_fs'],
            'last_distance_angstrom':r['last_distance_angstrom'],
            'retention_v07':bool(r['finite_window_retention']),
            'tail_fraction_r_below_2A':float(np.mean(tail[:,1]<2.)) if len(tail) else 0.,
            'energy_max_drift_Ha':r['maximum_recorded_energy_drift'],
            'max_bath_plus_interaction_Ha':float(np.max(bath)),
            'backflow_from_peak_Ha':float(np.max(bath)-bath[-1]),
            'terminal_bath_plus_interaction_Ha':float(bath[-1]),
            'trajectory':t}

def run(save=True,duration_fs=180.,dt_au=.12):
    potential=build_potential()
    out=[]
    for label,pars in configurations().items():
        result=describe(potential,BathConfig(**pars,duration_fs=duration_fs,dt_au=dt_au,stride=100))
        out.append({'scenario':label,**pars,**{k:v for k,v in result.items() if k!='trajectory'}})
    if save:
        (HERE/'h2_bath_sensitivity_v08.json').write_text(json.dumps({'protocol':'one-at-a-time parameter controls, zero-temperature finite classical oscillator bath; no claims of irreversible chemical yield','cases':out},indent=2),encoding='utf8')
        with (HERE/'h2_bath_sensitivity_v08.csv').open('w',newline='',encoding='utf8') as f:
            w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    return out

if __name__=='__main__':
    for case in run():print(case['scenario'],case['tail_fraction_r_below_2A'],case['energy_max_drift_Ha'])
