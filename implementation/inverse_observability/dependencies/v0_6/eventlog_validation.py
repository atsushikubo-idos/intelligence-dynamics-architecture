"""IDOS Inverse Observability v0.6: event-log hypothesis comparison.

The model uses only information available at the first REVIEW event to predict
remaining time to RESOLUTION. Diagnostic, not causal / latent-variable proof.
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
import numpy as np

FIELDS = ('case_id', 'activity', 'timestamp', 'resource')
REVIEW = 'REVIEW'
START = 'SUBMIT'
TERMINAL = {'APPROVE', 'REJECT'}

def parse_timestamp(value: str) -> datetime:
    value = value.strip()
    if value.endswith('Z'):
        value = value[:-1] + '+00:00'
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError('timestamp must include a timezone offset: '+value)
    return dt.astimezone(timezone.utc)

def read_csv(path: str | Path) -> list[dict]:
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not set(FIELDS).issubset(reader.fieldnames or []):
            raise ValueError('CSV requires columns '+', '.join(FIELDS))
        rows=[]
        for n, row in enumerate(reader, 2):
            if not all(row.get(k) for k in FIELDS):
                raise ValueError(f'missing required field at line {n}')
            rows.append({**{k:row[k].strip() for k in FIELDS},'timestamp':parse_timestamp(row['timestamp'])})
    return rows

def make_cases(events: list[dict]) -> tuple[list[dict],dict]:
    """As-of cutoff for each case: first review; feature based only on history."""
    events=sorted(events,key=lambda e:(e['timestamp'],e['case_id'],e['activity']))
    bycase={}
    for e in events: bycase.setdefault(e['case_id'],[]).append(e)
    starts=[]; reviews=[]; resolved=[]; discarded=Counter()
    for case_id, items in bycase.items():
        first_start=next((e for e in items if e['activity']==START),None)
        first_review=next((e for e in items if e['activity']==REVIEW),None)
        terminal=next((e for e in items if e['activity'] in TERMINAL and first_review and e['timestamp']>=first_review['timestamp']),None)
        if first_start:starts.append((first_start['timestamp'],case_id))
        if terminal:resolved.append((terminal['timestamp'],case_id))
        if not(first_start and first_review and terminal):
            discarded['missing_start_review_or_terminal']+=1;continue
        if not(first_start['timestamp']<first_review['timestamp']<terminal['timestamp']):
            discarded['invalid_event_order']+=1;continue
        reviews.append((case_id,first_start,first_review,terminal,items))
    cases=[]
    for cid,start,rev,terminal,items in reviews:
        # Historical concurrent unresolved cases: uses only submissions/resolutions
        # stamped strictly before this review; never future information.
        active = sum(1 for ts,c in starts if c!=cid and ts<rev['timestamp']) - sum(1 for ts,c in resolved if c!=cid and ts<rev['timestamp'])
        # Cases lacking a terminal remain conservatively in the queue proxy.
        active=max(0,active)
        prior=[e for e in items if e['timestamp']<=rev['timestamp']]
        handoff=int(start['resource']!=rev['resource'])
        cases.append({'case_id':cid, 'start':start['timestamp'], 'landmark':rev['timestamp'],
             'duration_hours':(terminal['timestamp']-rev['timestamp']).total_seconds()/3600,
             'pre_review_hours':(rev['timestamp']-start['timestamp']).total_seconds()/3600,
             'queue_at_review':active,'handoff_at_review':handoff,
             'pre_review_rework':sum(e['activity']=='REWORK' for e in prior),
             'reviewer':rev['resource'], 'outcome':terminal['activity']})
    return sorted(cases,key=lambda e:(e['start'],e['case_id'])),{'input_events':len(events),'input_cases':len(bycase),'included_cases':len(cases),'excluded':dict(discarded)}

def _features(cases:list[dict], names:list[str]):
    return np.asarray([[1.0]+[float(c[n]) for n in names] for c in cases])

def _fit_predict(train,test,names):
    X=_features(train,names);Y=np.log1p([c['duration_hours'] for c in train])
    # Ridge with regularization fixed before validation; intercept unpenalized.
    means=X[:,1:].mean(axis=0);stds=X[:,1:].std(axis=0)
    stds[stds<1e-12]=1
    X[:,1:]=(X[:,1:]-means)/stds
    z=_features(test,names)
    z[:,1:]=(z[:,1:]-means)/stds
    p=np.eye(X.shape[1])*1.0;p[0,0]=0
    beta=np.linalg.solve(X.T@X+p,X.T@Y)
    return z@beta

def evaluate(cases:list[dict],train_fraction:float=.7):
    if len(cases)<35: raise ValueError('at least 35 complete cases needed for holdout')
    split=int(len(cases)*train_fraction)
    train,test=cases[:split],cases[split:]
    baseline=['pre_review_hours']
    candidates={'baseline':baseline,'queue':baseline+['queue_at_review'],
                'handoff':baseline+['handoff_at_review'],
                'rework':baseline+['pre_review_rework']}
    truth=np.log1p([c['duration_hours'] for c in test])
    results={}
    for name,features in candidates.items():
        prediction=_fit_predict(train,test,features)
        results[name]={'features':features,'holdout_log_mse':float(np.mean((truth-prediction)**2)),
                       'holdout_log_mae':float(np.mean(np.abs(truth-prediction)))}
    base=results['baseline']['holdout_log_mse']
    for v in results.values():v['improvement_pct']=float(100*(base-v['holdout_log_mse'])/base) if base>0 else None
    # No selection using test data: these are separate pre-registered comparisons.
    return {'n_train':len(train),'n_test':len(test),'split_at_first_submission':test[0]['start'].isoformat(),
            'model':'ridge alpha=1 on log(1+remaining hours), train-standardized predictors',
            'metric':'log-duration MSE (not hours MSE)', 'hypotheses':results,
            'best_on_holdout_for_description_only':min(results,key=lambda k:results[k]['holdout_log_mse']),
            'warning':'Out-of-sample associations, not causal identification; do not optimize model using test rankings.'}

def synthesize(n=320,seed=71):
    rng=np.random.default_rng(seed);origin=datetime(2024,1,1,tzinfo=timezone.utc)
    events=[]
    for i in range(n):
        # Synthetic case sequence, not real corporate events.
        t=origin+timedelta(hours=i*1.3)
        handoff=int(rng.random()<.43)
        reviewer='REVIEWER_B' if handoff else 'REVIEWER_A'
        w=max(1.,float(rng.lognormal(1.7,.6)))
        early_rework=int(rng.random()<.23)
        # Create case-level waiting-time differences by handoff and early rework.
        remaining=max(.2,float(np.exp(2.0+.65*handoff+.62*early_rework+.16*rng.normal())-1))
        cid=f'C{i:05d}'
        def add(a,tt,r):events.append({'case_id':cid,'activity':a,'timestamp':tt,'resource':r})
        add('SUBMIT',t,'REVIEWER_A')
        if early_rework:add('REWORK',t+timedelta(hours=w*.6),'REVIEWER_A')
        add('REVIEW',t+timedelta(hours=w),reviewer)
        add('APPROVE' if rng.random()<.8 else 'REJECT',t+timedelta(hours=w+remaining),reviewer)
    return events

def save_csv(path,events):
    with open(path,'w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows([{**e,'timestamp':e['timestamp'].isoformat() if isinstance(e['timestamp'],datetime) else e['timestamp']} for e in events])

def run(path,output):
    cases,meta=make_cases(read_csv(path))
    result={'version':'0.6','dataset_path':str(path),'metadata':meta,'evaluation':evaluate(cases),
      'status':'event-log evidence only, 12PDM is not directly measured'}
    Path(output).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--csv');p.add_argument('--output',default='eventlog_results.json');p.add_argument('--synthetic',action='store_true')
    args=p.parse_args()
    if args.synthetic:
        path=Path('synthetic_event_log.csv');save_csv(path,synthesize());print('Synthetic input:',path)
    elif args.csv:path=Path(args.csv)
    else:p.error('supply --csv PATH or --synthetic')
    print(json.dumps(run(path,args.output),indent=2,ensure_ascii=False))
