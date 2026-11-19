
/* IDOS V0.37 experimental unified transition kernel. Noncanonical. Pure model and audit. */
(function(root){'use strict';
const copy=x=>JSON.parse(JSON.stringify(x));
const clamp=x=>Math.max(0,Math.min(1,x));
const ids=['asi','ai','corp','mgr','observer'];
const defs=[['asi','ASI',[.92,.88,.95,.96,.55,.90],[.85,.92,.88]],['ai','AI',[.85,.62,.78,.70,.48,.55],[.62,.78,.60]],['corp','Organization',[.88,.72,.42,.35,.62,.48],[.55,.38,.42]],['mgr','Human decision-maker',[.72,.58,.52,.66,.74,.70],[.58,.52,.55]],['observer','External observer',[.45,.88,.71,.83,.59,.80],[.46,.72,.79]]];
const validId=x=>ids.includes(x);
const relationKey=(a,b)=>[a,b].sort().join(':');
function initial(){return {time:0,actors:defs.map(d=>({id:d[0],name:d[1],ref:d[2].slice(),rule:{decision:d[3][0],learning:d[3][1],frame:d[3][2]}})),relations:{},requests:{},audit:[]};}
function actor(s,id){return s.actors.find(x=>x.id===id);}
function checkEvent(e){if(!e||!['observe','propose','decide','contact'].includes(e.kind))throw Error('Unsupported event kind');if(!validId(e.from)||!validId(e.to)||e.from===e.to)throw Error('Invalid actors');if(e.kind==='observe'&&!['partial','withheld','declared'].includes(e.disclosure))throw Error('Invalid disclosure');if(e.kind==='propose'&&(!e.request_id||!['dialogue','collab','conflict','learn'].includes(e.mode)))throw Error('Invalid proposal');if(['decide','contact'].includes(e.kind)&&!e.request_id)throw Error('Missing request id');if(e.kind==='decide'&&!['approve','reject','hold'].includes(e.decision))throw Error('Invalid decision');}
function transition(input,event){checkEvent(event);const s=copy(input),e=copy(event);s.time++;const before={actors:copy(s.actors),relations:copy(s.relations)};
 let outcome='recorded',residuals=[],changed=false;const a=actor(s,e.from),b=actor(s,e.to);let request=null;
 if(e.kind==='observe'){
  outcome=e.disclosure==='withheld'?'withheld':'read_only';
  residuals.push(e.disclosure==='withheld'?'Reference-frame basis withheld':'Observation interpretation and external Reality correspondence unverified');
 } else if(e.kind==='propose'){
  if(s.requests[e.request_id])throw Error('Duplicate request id');
  s.requests[e.request_id]={from:e.from,to:e.to,mode:e.mode,decision_a:'approve',decision_b:'pending',executed:false};
  outcome='pending';residuals.push('Recipient decision pending');
 }else{
  request=s.requests[e.request_id];if(!request||request.from!==e.from||request.to!==e.to)throw Error('Unknown/mismatched request');
  if(e.kind==='decide'){
   if(request.executed)throw Error('Request already executed');
   request.decision_b=e.decision;
   outcome=e.decision; if(e.decision!=='approve')residuals.push(e.decision==='reject'?'Recipient rejected contact':'Recipient approval on hold');
  }else{
   if(request.executed)throw Error('Repeated contact');
   if(request.decision_a!=='approve'||request.decision_b!=='approve'){
    outcome='blocked';residuals.push('No bilateral approval; no state update');
   }else{
    const sign=request.mode==='conflict'?-1:1;
    const weight=request.mode==='learn'?.045:.028;
    const deltaA=a.ref.map((v,i)=>sign*(b.ref[i]-v)*weight*a.rule.learning);
    const deltaB=b.ref.map((v,i)=>sign*(a.ref[i]-v)*weight*b.rule.learning);
    a.ref=a.ref.map((v,i)=>clamp(v+deltaA[i]));b.ref=b.ref.map((v,i)=>clamp(v+deltaB[i]));
    a.rule.frame=clamp(a.rule.frame+.004);b.rule.frame=clamp(b.rule.frame+.004);
    const key=relationKey(e.from,e.to),rel=s.relations[key]||{contacts:0,strength:.5,history:[]};
    rel.contacts++;rel.strength=clamp(rel.strength+(sign>0?.015:-.015));rel.history.push({t:s.time,mode:request.mode});s.relations[key]=rel;
    changed=true;outcome='applied';request.executed=true;
    residuals.push('Semantic residual is not quantified');
   }
  }
 }
 const after={actors:copy(s.actors),relations:copy(s.relations)};
 const record={sequence:s.audit.length+1,t:s.time,event:e,outcome,changed,provenance:{type:'synthetic',external_reality_contact:false},before,after,residuals,checks:{bilateral_consent_required:true,observation_read_only:e.kind==='observe',future_updateability:'unmeasured'}};
 s.audit.push(record);return s;
}
function replay(events){let s=initial();for(const e of events)s=transition(s,e);return s;}
const scenarios={
 cooperation:[{kind:'observe',from:'observer',to:'mgr',disclosure:'partial'},{kind:'propose',request_id:'r1',from:'mgr',to:'ai',mode:'collab'},{kind:'decide',request_id:'r1',from:'mgr',to:'ai',decision:'approve'},{kind:'contact',request_id:'r1',from:'mgr',to:'ai'},{kind:'observe',from:'corp',to:'observer',disclosure:'declared'}],
 refusal:[{kind:'propose',request_id:'r1',from:'asi',to:'corp',mode:'collab'},{kind:'decide',request_id:'r1',from:'asi',to:'corp',decision:'reject'},{kind:'contact',request_id:'r1',from:'asi',to:'corp'},{kind:'observe',from:'observer',to:'asi',disclosure:'withheld'},{kind:'propose',request_id:'r2',from:'mgr',to:'ai',mode:'dialogue'},{kind:'decide',request_id:'r2',from:'mgr',to:'ai',decision:'hold'},{kind:'contact',request_id:'r2',from:'mgr',to:'ai'}],
 contested:[{kind:'observe',from:'ai',to:'mgr',disclosure:'partial'},{kind:'propose',request_id:'r1',from:'ai',to:'mgr',mode:'conflict'},{kind:'decide',request_id:'r1',from:'ai',to:'mgr',decision:'approve'},{kind:'contact',request_id:'r1',from:'ai',to:'mgr'},{kind:'propose',request_id:'r2',from:'corp',to:'observer',mode:'learn'},{kind:'decide',request_id:'r2',from:'corp',to:'observer',decision:'approve'},{kind:'contact',request_id:'r2',from:'corp',to:'observer'}]
};
function checks(events,state){const results=[];const add=(name,passed)=>results.push({name,passed:!!passed});
 add('Deterministic replay',JSON.stringify(state)===JSON.stringify(replay(events)));
 add('Five unique agents',state.actors.length===5&&new Set(state.actors.map(a=>a.id)).size===5);
 add('Audit aligned with events',state.audit.length===events.length);
 add('No agent updates without approved contact',state.audit.filter(a=>!a.changed).every(a=>JSON.stringify(a.before)===JSON.stringify(a.after)));
 add('Only approved contacts update agents',state.audit.filter(a=>a.changed).every(a=>a.event.kind==='contact'&&a.outcome==='applied'));
 add('Synthetic provenance distinguished from Reality',state.audit.every(a=>a.provenance.type==='synthetic'&&a.provenance.external_reality_contact===false));
 add('Retain residual records',state.audit.every(a=>Array.isArray(a.residuals)));
 add('Reference axis range preserved',state.actors.every(a=>a.ref.length===6&&a.ref.every(v=>v>=0&&v<=1)));
 add('Input remains immutable',(()=>{const old=initial(),snapshot=JSON.stringify(old);transition(old,{kind:'observe',from:'observer',to:'ai',disclosure:'partial'});return JSON.stringify(old)===snapshot;})());
 return results;
}
const api={initial,transition,replay,checks,scenarios:copy(scenarios)};root.IDOSV037=api;
if(typeof module==='object'&&module.exports)module.exports=api;
})(typeof window!=='undefined'?window:globalThis);



/* IDOS V0.38: integrated experimental extension of the V0.37 transition kernel.
   Synthetic and noncanonical. Explicit approval, provenance, audit. */
(function(root){'use strict';
const base=root.IDOSV037;if(!base)throw Error('V0.37 kernel is missing');
const cp=o=>JSON.parse(JSON.stringify(o)), clamp=x=>Math.min(1,Math.max(0,x)), ids=['asi','ai','corp','mgr','observer'];
const key=(a,b)=>[a,b].sort().join(':');
function init(){const s=base.initial();s.boundaries={};s.observations={};return s;}
function actor(s,id){return s.actors.find(x=>x.id===id);}
function validActor(id){return ids.includes(id);}
function ensurePair(e){if(!validActor(e.from)||!validActor(e.to)||e.from===e.to)throw Error('Invalid actor pair');}
function append(s,e,outcome,changed,before,residuals,extra={}){
 const after={actors:cp(s.actors),relations:cp(s.relations),boundaries:cp(s.boundaries)};
 s.audit.push({sequence:s.audit.length+1,t:s.time,event:cp(e),outcome,changed,before,after,residuals,provenance:{type:'synthetic_test_data',external_reality_contact:false},experimental_extension:extra,checks:{future_updateability:'unmeasured',real_reality_recontact:false}});return s;
}
function transit(input,e,feedback=true){if(!e||typeof e!=='object')throw Error('Invalid event format');const s=cp(input);
 if(['observe','propose','decide','contact'].includes(e.kind)){
  ensurePair(e);
  if(e.kind==='contact'){
   const req=s.requests[e.request_id];if(!req||req.from!==e.from||req.to!==e.to)throw Error('Matching proposal not found');
   const boundary=s.boundaries[key(e.from,e.to)]||'open';
   if(boundary==='closed'){
    if(req.executed)throw Error('Contact already executed');
    s.time++;const before={actors:cp(s.actors),relations:cp(s.relations),boundaries:cp(s.boundaries)};
    return append(s,e,'blocked_boundary',false,before,['Closed boundary blocks contact despite approval'],{boundary});
   }
  }
  // The V0.37 kernel is used without changing its algorithm. Extend only after accepted contacts.
  const preRel=e.kind==='contact' ? (s.relations[key(e.from,e.to)]?.contacts||0):0;
  const previousAuditCount=s.audit.length;
  const next=base.transition(s,e);
  if(e.kind==='contact'&&next.audit.at(-1).changed&&feedback&&preRel>0){
   const a=actor(next,e.from),b=actor(next,e.to);
   const beforeRule=[a.rule.learning,b.rule.learning];
   const intensity=Math.min(preRel,5)*0.006;
   a.rule.learning=clamp(a.rule.learning+intensity);
   b.rule.learning=clamp(b.rule.learning+intensity);
   const rec=next.audit.at(-1);
   rec.after.actors=cp(next.actors);
   rec.experimental_extension={relation_feedback:true,prior_contacts:preRel,learning_rules_before:beforeRule,learning_rules_after:[a.rule.learning,b.rule.learning]};
  }else{next.audit.at(-1).experimental_extension={relation_feedback:false,prior_contacts:preRel};}
  next.audit.at(-1).provenance={type:'synthetic_test_data',external_reality_contact:false};
  next.audit.at(-1).checks.future_updateability='unmeasured';
  return next;
 }
 if(e.kind==='boundary'){
  ensurePair(e);if(!['open','closed'].includes(e.value)||e.consent_from!=='approve'||e.consent_to!=='approve')throw Error('Boundary change requires bilateral approval and valid value');
  s.time++;const before={actors:cp(s.actors),relations:cp(s.relations),boundaries:cp(s.boundaries)};
  s.boundaries[key(e.from,e.to)]=e.value;
  return append(s,e,'boundary_changed',true,before,['Boundary change changes contact permissions, not actor references'],{boundary_change:true});
 }
 if(e.kind==='external_observation'){
  if(!validActor(e.target)||!e.observation_id||s.observations[e.observation_id]||!['declared','withheld'].includes(e.disclosure))throw Error('Invalid observation ID or disclosure');
  if(e.disclosure==='declared'&&(!Number.isInteger(e.axis)||e.axis<0||e.axis>5||typeof e.value!=='number'||e.value<0||e.value>1))throw Error('Invalid declared observation value');
  s.time++;const before={actors:cp(s.actors),relations:cp(s.relations),boundaries:cp(s.boundaries)};
  s.observations[e.observation_id]={target:e.target,axis:e.axis??null,value:e.disclosure==='declared'?e.value:null,disclosure:e.disclosure,source:e.source||'synthetic-source',used:false};
  return append(s,e,e.disclosure==='withheld'?'withheld':'observation_recorded',false,before,[e.disclosure==='withheld'?'Observation content withheld':'External series is synthetic data, not real ground truth'],{observation_only:true});
 }
 if(e.kind==='recontact'){
  if(!validActor(e.target)||!e.observation_id||!s.observations[e.observation_id])throw Error('Invalid recontact target or observation ID');
  const obs=s.observations[e.observation_id];if(obs.target!==e.target)throw Error('Observation target mismatch');
  if(obs.used)throw Error('Observation already used for recontact');
  if(!['approve','reject','hold'].includes(e.consent))throw Error('Invalid consent state');
  s.time++;const before={actors:cp(s.actors),relations:cp(s.relations),boundaries:cp(s.boundaries)};
  if(e.consent!=='approve'||obs.disclosure!=='declared')return append(s,e,'no_update',false,before,['No adjustment due to rejection, hold, or withholding'],{observation_id:e.observation_id});
  const a=actor(s,e.target),old=a.ref[obs.axis],newValue=clamp(old+(obs.value-old)*0.12);
  a.ref[obs.axis]=newValue;obs.used=true;
  return append(s,e,'synthetic_adjustment',newValue!==old,before,['Experimental adjustment based on synthetic observation; not real Reality recontact'],{observation_id:e.observation_id,axis:obs.axis,old,newValue});
 }
 throw Error('Unknown event kind');
}
function replay(events,feedback=true){let s=init();for(const e of events)s=transit(s,e,feedback);return s;}
const contact=(id,a,b,mode)=>[{kind:'propose',request_id:id,from:a,to:b,mode},{kind:'decide',request_id:id,from:a,to:b,decision:'approve'},{kind:'contact',request_id:id,from:a,to:b}];
const presets={
 adaptive:[...contact('a','mgr','ai','dialogue'),...contact('b','mgr','ai','learn'),{kind:'external_observation',observation_id:'o1',target:'mgr',axis:2,value:.22,disclosure:'declared',source:'synthetic-test-series'},{kind:'recontact',observation_id:'o1',target:'mgr',consent:'approve'},...contact('c','mgr','ai','collab')],
 closed:[{kind:'boundary',from:'ai',to:'corp',value:'closed',consent_from:'approve',consent_to:'approve'},...contact('a','ai','corp','collab'),{kind:'boundary',from:'ai',to:'corp',value:'open',consent_from:'approve',consent_to:'approve'},...contact('b','ai','corp','collab')],
 withheld:[{kind:'external_observation',observation_id:'o1',target:'asi',disclosure:'withheld',source:'synthetic-test-series'},{kind:'recontact',observation_id:'o1',target:'asi',consent:'approve'},{kind:'external_observation',observation_id:'o2',target:'ai',axis:0,value:.2,disclosure:'declared',source:'synthetic-test-series'},{kind:'recontact',observation_id:'o2',target:'ai',consent:'reject'}, {kind:'observe',from:'observer',to:'mgr',disclosure:'partial'}]
};
function checks(events,s,feedback){let rerun=replay(events,feedback),p=[];const add=(name,v)=>p.push({name,passed:!!v});
 add('Deterministic replay',JSON.stringify(s)===JSON.stringify(rerun));
 add('Five unique actors',s.actors.length===5&&new Set(s.actors.map(a=>a.id)).size===5);
 add('One audit event per input event',s.audit.length===events.length);
 add('Observation, rejection, and hold preserve actor states',s.audit.filter(a=>['observe','external_observation'].includes(a.event.kind)||a.outcome==='no_update'||a.outcome==='blocked_boundary').every(a=>JSON.stringify(a.before.actors)===JSON.stringify(a.after.actors)));
 add('Closed boundaries block contact',s.audit.filter(a=>a.outcome==='blocked_boundary').every(a=>!a.changed&&JSON.stringify(a.before.actors)===JSON.stringify(a.after.actors)));
 add('Contact requires bilateral approval',s.audit.filter(a=>a.event.kind==='contact'&&a.changed).every(a=>{const r=s.requests[a.event.request_id];return r?.decision_a==='approve'&&r?.decision_b==='approve';}));
 add('No real-world Reality connection claimed',s.audit.every(a=>a.provenance.external_reality_contact===false));
 add('Residual and provenance auditability',s.audit.every(a=>Array.isArray(a.residuals)&&a.provenance?.type==='synthetic_test_data'));
 add('Reference axes within [0,1]',s.actors.every(a=>a.ref.length===6&&a.ref.every(v=>v>=0&&v<=1)));
 add('Future Updateability marked unmeasured',s.audit.every(a=>a.checks?.future_updateability==='unmeasured'));
 add('Rejected boundary change fails',(()=>{try{transit(init(),{kind:'boundary',from:'ai',to:'corp',value:'closed',consent_from:'approve',consent_to:'reject'});return false}catch{return true}})());
 return p;
}
function experiment(name,feedback=true){if(!Object.hasOwn(presets,name))throw Error('Invalid experiment preset');const events=cp(presets[name]),result=replay(events,feedback),tests=checks(events,result,feedback);return {schema:'idos.v038.integration',status:'synthetic_noncanonical',scenario:name,feedback,events,result,tests,limitations:['Not real Reality data','Not an empirical validation','CDP v1.0 conformance not tested','Future Updateability unmeasured','Legacy panels remain separate']};}
root.IDOSV038={initial:init,transition:transit,replay,checks,experiment,presets:cp(presets)};
if(typeof module==='object'&&module.exports)module.exports=root.IDOSV038;
})(typeof window!=='undefined'?window:globalThis);
