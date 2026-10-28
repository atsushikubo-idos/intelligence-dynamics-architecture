"""v0.4: executable, bounded, model-proposed compositional measurements.
A generated expression is *data* parsed through an allowlisted arithmetic grammar,
not arbitrary code. The action space remains fixed and explicitly authorized.
"""
from __future__ import annotations
import ast, hashlib, json, math
from dataclasses import dataclass, asdict
from dynamic_cycle import DynamicCycle, FrameSpec, SENSORS, ACTIONS
from reference_transition import FrameSnapshot, review_transition, Decision

BASE = frozenset(('wealth','energy','output','capacity'))
OPERATORS = (ast.Add,ast.Sub,ast.Mult,ast.Div)

class InvalidMetric(ValueError): pass

def compile_metric(expression: str):
    if not isinstance(expression,str) or len(expression)>140: raise InvalidMetric('invalid expression length')
    try: root=ast.parse(expression,mode='eval')
    except SyntaxError as ex: raise InvalidMetric('syntax') from ex
    if sum(1 for _ in ast.walk(root))>25: raise InvalidMetric('too complex')
    def evaluate(node, values):
        if isinstance(node,ast.Expression):return evaluate(node.body,values)
        if isinstance(node,ast.Name) and node.id in BASE: return float(values[node.id])
        if isinstance(node,ast.Constant) and type(node.value) in (int,float) and abs(node.value)<=100: return float(node.value)
        if isinstance(node,ast.BinOp) and isinstance(node.op,OPERATORS):
            l=evaluate(node.left,values);r=evaluate(node.right,values)
            if isinstance(node.op,ast.Add):v=l+r
            elif isinstance(node.op,ast.Sub):v=l-r
            elif isinstance(node.op,ast.Mult):v=l*r
            else:
                if abs(r)<1e-9:raise InvalidMetric('division by zero')
                v=l/r
            if not math.isfinite(v) or abs(v)>1e9:raise InvalidMetric('nonfinite / unbounded result')
            return v
        raise InvalidMetric('disallowed syntax or observable')
    # Validate AST before use even on paths not exercised in a specific world.
    for node in ast.walk(root):
        if isinstance(node,(ast.Call,ast.Attribute,ast.Subscript,ast.IfExp,ast.Compare,ast.BoolOp,ast.Lambda,ast.ListComp,ast.Pow,ast.Mod,ast.FloorDiv,ast.UnaryOp)):
            raise InvalidMetric('disallowed syntax')
        if isinstance(node,ast.Name) and node.id not in BASE:raise InvalidMetric('unknown observable')
    def measure(values): return evaluate(root,values)
    measure({'wealth':50.,'energy':4.,'output':6.,'capacity':9.})
    return measure

@dataclass(frozen=True)
class GeneratedCandidate:
    idea: str
    expression: str
    maximize: bool
    action: str
    rationale: str

class ComposedCycle(DynamicCycle):
    def __init__(self,generator,**kwargs):
        super().__init__(generator,**kwargs)
        self.computed=dict(SENSORS)
        self.proposal_audit=[]
    def measure(self,frame,raw): return self.computed[frame.metric](raw)
    def step(self,*,approve_frame=False):
        before=self.world.measure(); prior=self.frame
        source_visible={'current_metric':prior.metric,'current_value':self.measure(prior,before),
          'raw_observation':before,'history_count':len(self.history)}
        candidate=self.generator.propose(history=list(self.history),frame=prior,visible_observations=source_visible)
        review_status='no_candidate'; reason=None; proposed_metric=None
        if candidate is not None:
            if not isinstance(candidate,GeneratedCandidate) or type(candidate.maximize) is not bool or candidate.action not in ACTIONS or not candidate.idea or len(candidate.idea)>300 or len(candidate.rationale)>600:
                review_status='rejected';reason='invalid candidate'
            else:
                try:
                    sensor=compile_metric(candidate.expression)
                    proposed_metric='generated:'+hashlib.sha256(candidate.expression.encode()).hexdigest()[:12]
                    if proposed_metric==prior.metric:raise InvalidMetric('unchanged frame')
                    # Deliberately preserve original prior metric in registered frame lineage.
                    next_frame=FrameSpec('F'+str(len(self.frames)),proposed_metric,candidate.maximize,(candidate.action,'inspect'))
                    assessment=review_transition(
                      FrameSnapshot(prior.id,frozenset((prior.metric,)),frozenset(('trace:'+prior.id,))),
                      FrameSnapshot(next_frame.id,frozenset((prior.metric,proposed_metric)),frozenset(('candidate:'+next_frame.id,))),
                      independent_evidence=frozenset(('sandbox-sensor-evaluation',)),
                      authorization_id='local_sandbox_operator' if approve_frame else None)
                    review_status=assessment.decision.value
                    if assessment.decision is Decision.AUTHORIZED:
                        self.computed[proposed_metric]=sensor
                        self.frame=next_frame;self.frames[next_frame.id]=next_frame
                except InvalidMetric as ex:
                    review_status='rejected';reason=str(ex)
        eligible=self._eligible(self.frame,before)
        action=eligible[0] if eligible else 'inspect'
        outcome=self.world.apply(action);after=self.world.measure()
        event={'cycle':len(self.history)+1,'frame_before':prior.id,'frame_after':self.frame.id,
          'metric_before':prior.metric,'metric_after':self.frame.metric,
          'generated_expression':candidate.expression if isinstance(candidate,GeneratedCandidate) else None,
          'candidate':asdict(candidate) if isinstance(candidate,GeneratedCandidate) else None,
          'review_status':review_status,'rejection':reason,'possible_metric_id':proposed_metric,
          'before_old':self.measure(prior,before),'after_old':self.measure(prior,after),
          'before_new':self.measure(self.frame,before),'after_new':self.measure(self.frame,after),
          'eligible_before':self._eligible(prior,before),'eligible_after':eligible,
          'action':action,'world_before':before,'world_after':after,
          'source_type':'unverified_generator'}
        event['record_hash']=hashlib.sha256(json.dumps(event,sort_keys=True).encode()).hexdigest()
        self.history.append(event)
        return event
