"""Run with PYTHONPATH including the Reference v1.1 and standalone prototype folders."""
from idos_reference_v1_1 import make_unit
from value_recognition import Observation, ReferenceFrame
from reference_adapter import ValueRecognitionAdapter

unit = make_unit('M&A team', 'organization', 'Short-term returns')
adapter = ValueRecognitionAdapter(unit)
adapter.register_frame(ReferenceFrame('value-1', 't1', {'short_term_profit': 1.0}), unit.frame)
adapter.observe(Observation('event-1', 'M&A', 't1', {'knowledge_sharing': 0.9},
                            'Unexpected knowledge sharing across merged teams'))
first = adapter.evaluate('event-1', 'value-1')
assert first.status == 'unassessable'
adapter.hold_unassessed('event-1', 'Insufficient data for initial criterion; preserve for later inquiry')
new_frame = unit.frame.revise(name='Knowledge integration', add_categories=['knowledge_sharing'])
adapter.revise_frame(new_idos_frame=new_frame,
                     new_value_frame=ReferenceFrame('value-2', 't2', {'knowledge_sharing': 1.0}),
                     description='Hypothetical M&A objective shift')
result = adapter.reevaluate('event-1', 'value-2')
assert result['recognition_transition'] == 'unassessable -> assessed'
assert result['current']['score'] == 0.9
print(result)
print('Provenance events:', len(unit.trajectory.provenance))
