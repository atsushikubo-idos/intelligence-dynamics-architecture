"""Optional live model source. Does not execute generated code or grant permissions."""
import json, os, urllib.request
from dynamic_cycle import Candidate, SENSORS, ACTIONS

class LiveSource:
    def __init__(self, model, endpoint='https://api.openai.com/v1/chat/completions'):
        if not endpoint.startswith('https://'): raise ValueError('HTTPS required')
        self.model=model; self.endpoint=endpoint; self.audit=[]
    def propose(self, *, history, frame, visible_observations):
        key=os.environ.get('OPENAI_API_KEY')
        if not key: raise RuntimeError('OPENAI_API_KEY unavailable: live mode not executed')
        # Groundable interface only: existing simulated sensors/actions are specified.
        context={'frame':{'id':frame.id,'metric':frame.metric}, 'observation':visible_observations,
                 'prior_results':[{'frame_after':h['frame_after'],'action':h['action'],
                                   'score_after_on_new_frame':h['score_after_on_new_frame'],
                                   'world_after':h['world_after']} for h in history]}
        prompt=('Propose one testable alternative way of observing a simulated economy and a matching intervention. '
                'Do not assume the candidate is correct, new or useful. The old frame must remain available. '
                'Return JSON with exactly idea,metric,maximize,proposed_action,rationale. '
                'For this sandbox only, available computed metrics: '+', '.join(SENSORS)+'. '
                'Allowed actions: '+', '.join(sorted(ACTIONS))+'. '
                'You may output null if evidence is insufficient. Do not claim real-world validity.')
        body={'model':self.model,'messages':[{'role':'system','content':prompt},
                                             {'role':'user','content':json.dumps(context)}],
              'temperature':0}
        req=urllib.request.Request(self.endpoint,json.dumps(body).encode(),
          headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=30) as res: data=json.load(res)
        raw=data['choices'][0]['message']['content']
        try:
            d=json.loads(raw)
            if d is None: return None
            if not isinstance(d,dict) or set(d)!={'idea','metric','maximize','proposed_action','rationale'}: raise ValueError('schema')
            if not all(isinstance(d[k],str) for k in ('idea','metric','proposed_action','rationale')) or type(d['maximize']) is not bool: raise ValueError('type')
            if d['metric'] not in SENSORS or d['proposed_action'] not in ACTIONS: raise ValueError('unavailable capability')
            if any(len(d[k])>500 or not d[k].strip() for k in ('idea','rationale')): raise ValueError('length')
            self.audit.append({'valid':True,'proposal':d})
            return Candidate(**d)
        except (ValueError,TypeError) as exc:
            self.audit.append({'valid':False,'reason':str(exc),'raw':raw[:1000]})
            return None
