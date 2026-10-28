"""Optional live proposal source: requires caller-provided OPENAI_API_KEY.
The model can propose arithmetic metric formulas, never executable code.
"""
import json,os,urllib.request
from composed_cycle import GeneratedCandidate

class LiveComposedSource:
    def __init__(self,model,endpoint='https://api.openai.com/v1/chat/completions'):
        if endpoint!='https://api.openai.com/v1/chat/completions':raise ValueError('Only the fixed endpoint is allowed')
        self.model=model;self.endpoint=endpoint;self.audit=[]
    def propose(self,*,history,frame,visible_observations):
        key=os.environ.get('OPENAI_API_KEY')
        if not key:raise RuntimeError('Missing OPENAI_API_KEY: no real model call was made')
        instruction=('Propose a potentially overlooked measurable distinction in the simulated world, without predetermined answer. '
          'Return JSON object ONLY with idea,expression,maximize,action,rationale or null. '
          'expression is arithmetic using only wealth,energy,output,capacity; operators + - * /, parentheses and constants <=100. '
          'Available actions: inspect,subsidize,expand_energy,boost_output. '
          'You propose; a separate program checks measurement and authority. Novelty is not established by proposing.')
        context={'frame':{'id':frame.id,'metric':frame.metric},'observation':visible_observations,
          'history':[{'action':x['action'],'world_after':x['world_after'],'metric_after':x['metric_after']} for x in history]}
        req=urllib.request.Request(self.endpoint, json.dumps({'model':self.model,'messages':[{'role':'system','content':instruction},{'role':'user','content':json.dumps(context)}],'temperature':0}).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=35) as resp:result=json.load(resp)
        raw=result['choices'][0]['message']['content']
        try:
            obj=json.loads(raw)
            if obj is None:return None
            if not isinstance(obj,dict) or set(obj)!={'idea','expression','maximize','action','rationale'}:raise ValueError('schema')
            if type(obj['maximize']) is not bool or any(not isinstance(obj[k],str) for k in ('idea','expression','action','rationale')):raise ValueError('types')
            self.audit.append({'raw':raw,'accepted_schema':True});return GeneratedCandidate(**obj)
        except (ValueError,TypeError) as exc:
            self.audit.append({'raw':raw[:1000],'accepted_schema':False,'reason':str(exc)})
            return None
