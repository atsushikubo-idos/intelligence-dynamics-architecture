import argparse,json
from pathlib import Path
from composed_cycle import ComposedCycle,GeneratedCandidate
from dynamic_cycle import ReplaySource
from live_composed import LiveComposedSource
p=argparse.ArgumentParser();p.add_argument('--mode',choices=('replay','live'),required=True);p.add_argument('--model',default='gpt-4.1-mini');p.add_argument('--cycles',type=int,default=3);p.add_argument('--approve-sandbox',action='store_true');p.add_argument('--out',default='v04_output.json');a=p.parse_args()
if a.mode=='live': source=LiveComposedSource(a.model)
else: source=ReplaySource([GeneratedCandidate('Supply bottleneck','capacity-output',False,'expand_energy','test fixture'),GeneratedCandidate('Energy productivity','output/energy',True,'boost_output','test fixture'),None])
cycle=ComposedCycle(source);events=cycle.run(a.cycles,approve_frame=a.approve_sandbox)
record={'mode':a.mode,'real_ai_queried':a.mode=='live','fixture_only':a.mode=='replay','events':events,'source_audit':getattr(source,'audit',[])}
Path(a.out).write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'mode':a.mode,'frames':[e['frame_after'] for e in events],'actions':[e['action'] for e in events],'output':a.out}))
