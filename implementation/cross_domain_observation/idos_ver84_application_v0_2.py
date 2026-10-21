"""IDOS ver.84 cross-domain observation adapter v0.2.

Descriptive event-ledger for M&A and hiring, not IDOS reference mathematics.
No predictive scoring, autonomous decisions, or inference about private mental states.
Python 3.9+, standard library only.

python idos_ver84_application_v0_2.py --demo --output demo.json
python idos_ver84_application_v0_2.py --input case.json --output report.json
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

KINDS = {'imagined_future', 'feasible_option', 'observation', 'reference_frame',
         'commitment', 'decision', 'residual', 'holding', 'option_change', 'boundary_change'}
VISIBILITY = {'public', 'consented', 'restricted'}
REQUIRED = {'date', 'actor', 'kind', 'topic', 'value', 'evidence', 'visibility'}
DOMAINS = {'M&A', 'hiring', 'clinical'}


def validate(case):
    if not isinstance(case, dict) or not isinstance(case.get('case_id'), str) or not case['case_id']:
        raise ValueError('case_id is required')
    if case.get('domain') not in DOMAINS:
        raise ValueError('domain must be M&A, hiring, or clinical')
    if not isinstance(case.get('events'), list):
        raise ValueError('events must be a list')
    seen = set()
    for i, e in enumerate(case['events']):
        if not isinstance(e, dict) or REQUIRED - e.keys():
            raise ValueError(f'event {i}: missing required fields')
        date.fromisoformat(e['date'])
        if e['kind'] not in KINDS or e['visibility'] not in VISIBILITY:
            raise ValueError(f'event {i}: invalid kind or visibility')
        if not all(isinstance(e[k], str) and e[k].strip() for k in ('actor', 'topic', 'evidence')):
            raise ValueError(f'event {i}: actor/topic/evidence must be nonempty strings')
        if not isinstance(e['value'], (str, int, float, bool)):
            raise ValueError(f'event {i}: value must be scalar')
        eid = e.get('id', f'auto_{i}')
        if eid in seen:
            raise ValueError(f'duplicate event id: {eid}')
        seen.add(eid)
        if e['kind'] == 'holding' and e.get('deadline'):
            date.fromisoformat(e['deadline'])
    return True


def analyze(case, as_of=None):
    validate(case)
    as_of = as_of or date.today().isoformat()
    date.fromisoformat(as_of)
    # Restricted records are never included in outputs; no override flag.
    events = sorted((e for e in case['events'] if e['visibility'] != 'restricted'),
                    key=lambda e: (e['date'], e.get('id', '')))
    grouped = defaultdict(list)
    comparisons = defaultdict(list)
    for e in events:
        item = {k: e[k] for k in ('date', 'actor', 'kind', 'topic', 'value', 'evidence', 'visibility')}
        item['id'] = e.get('id')
        grouped[e['kind']].append(item)
        comparisons[(e['actor'], e['topic'], e['kind'])].append(item)
    revisions = []
    for (actor, topic, kind), rows in sorted(comparisons.items()):
        if kind not in {'imagined_future', 'reference_frame', 'feasible_option', 'commitment'}:
            continue
        for before, after in zip(rows, rows[1:]):
            if before['value'] != after['value']:
                revisions.append({'actor': actor, 'topic': topic, 'kind': kind,
                                  'before': before['value'], 'after': after['value'],
                                  'before_date': before['date'], 'after_date': after['date'],
                                  'note': 'Recorded difference only; not inferred causality.'})
    holdings = []
    for e in events:
        if e['kind'] != 'holding':
            continue
        deadline = next((raw.get('deadline') for raw in case['events']
                         if raw.get('id') == e.get('id')), None)
        # For events without IDs, match on their source fields instead.
        if e.get('id') is None:
            deadline = next((raw.get('deadline') for raw in case['events']
                             if all(raw.get(k) == e.get(k) for k in ('date', 'actor', 'topic', 'value'))), None)
        status = 'missing_deadline' if not deadline else ('review_due' if deadline <= as_of else 'scheduled')
        holdings.append({'topic': e['topic'], 'actor': e['actor'], 'deadline': deadline,
                         'review_status': status, 'note': 'Status is a date check, not a delay recommendation.'})
    return {
        'case_id': case['case_id'], 'domain': case['domain'], 'as_of': as_of,
        'synthetic': bool(case.get('synthetic', False)),
        'timeline': events, 'recorded_revisions': revisions,
        'original_and_revised_commitments': grouped['commitment'],
        'imagined_futures': grouped['imagined_future'],
        'feasible_options': grouped['feasible_option'],
        'observations': grouped['observation'],
        'residuals': grouped['residual'], 'holdings': holdings,
        'decisions': grouped['decision'], 'option_changes': grouped['option_change'],
        'boundary_changes': grouped['boundary_change'],
        'privacy': {'restricted_count': sum(e['visibility'] == 'restricted' for e in case['events']),
                    'rule': 'Restricted records excluded from every report; consented data requires separate lawful-purpose review.'},
        'limitations': ['No causal inference or prediction.',
                        'No inferred trust, intent, psychological state or success probability.',
                        'Option changes are recorded assertions, not measured future updateability.',
                        'No automated decision or ROI substitution.',
                        'Not mathematically integrated with idos_reference_v1_1.py.']
    }


def compare_domains(cases, as_of=None):
    reports = [analyze(c, as_of=as_of) for c in cases]
    # Structural comparability only. Never pool individual outcomes or scores.
    dimensions = ['imagined_futures', 'feasible_options', 'observations', 'residuals',
                  'holdings', 'decisions', 'option_changes', 'boundary_changes',
                  'original_and_revised_commitments', 'recorded_revisions']
    matrix = [{ 'case_id': r['case_id'], 'domain': r['domain'],
                'counts': {k: len(r[k]) for k in dimensions}} for r in reports]
    return {'method': 'cross-domain schema coverage, not outcome equivalence',
            'shared_dimensions': dimensions, 'coverage': matrix,
            'reports': reports,
            'caution': 'Equal field names do not establish equivalent constructs across domains.'}


def ev(id, date_, actor, kind, topic, value, evidence, visibility='public', **kwargs):
    return dict(id=id, date=date_, actor=actor, kind=kind, topic=topic,
                value=value, evidence=evidence, visibility=visibility, **kwargs)

MA_DEMO = {'case_id': 'SYNTHETIC_MA', 'domain': 'M&A', 'synthetic': True, 'events': [
    ev('M1','2026-01-10','buyer','imagined_future','strategy','Double operating profit','Synthetic buyer memo'),
    ev('M2','2026-01-10','seller','imagined_future','employment','Maintain employment','Synthetic seller memo'),
    ev('M3','2026-01-15','board','commitment','profit_target','2x baseline in three years','Synthetic approval'),
    ev('M4','2026-01-20','joint','feasible_option','integration','Full or staged integration','Synthetic options memo'),
    ev('M5','2026-02-01','joint','residual','culture','Management-style difference unresolved','Synthetic workshop','consented'),
    ev('M6','2026-02-02','joint','holding','culture','Proceed while keeping issue open','Synthetic decision','consented',deadline='2026-08-01'),
    ev('M7','2026-02-03','board','decision','transaction','Staged integration','Synthetic board minutes'),
    ev('M8','2026-08-01','finance','observation','profit','Below original plan','Synthetic financial report'),
    ev('M9','2026-08-01','buyer','option_change','adjacent_service','Pilot became available','Synthetic project memo'),
    ev('M10','2026-08-01','buyer','imagined_future','strategy','Improve core and test adjacent service','Synthetic strategy revision'),
    ev('M11','2026-08-02','employee','observation','private_interview','Sensitive private note','Synthetic interview','restricted'),
]}

HIRING_DEMO = {'case_id': 'SYNTHETIC_HIRING', 'domain': 'hiring', 'synthetic': True, 'events': [
    ev('H1','2026-01-10','candidate','imagined_future','career','Lead new product within two years','Synthetic candidate statement','consented'),
    ev('H2','2026-01-10','employer','imagined_future','role','Improve existing product operations','Synthetic hiring brief'),
    ev('H3','2026-01-12','employer','commitment','role_scope','Operations leadership, not product ownership','Synthetic offer letter'),
    ev('H4','2026-01-15','joint','feasible_option','role_design','Start in operations; review later','Synthetic agreement'),
    ev('H5','2026-01-20','joint','residual','expectation_gap','Career and role expectations differ','Synthetic meeting notes','consented'),
    ev('H6','2026-01-21','joint','holding','expectation_gap','Review role expectations after onboarding','Synthetic review plan','consented',deadline='2026-07-21'),
    ev('H7','2026-02-01','employer','decision','hire','Hire for operations role','Synthetic hiring decision'),
    ev('H8','2026-07-21','manager','observation','role','Operations delivery improved','Synthetic performance summary'),
    ev('H9','2026-07-21','joint','option_change','new_product','Cross-functional pilot became possible','Synthetic planning memo'),
    ev('H10','2026-07-22','candidate','imagined_future','career','Lead a cross-functional pilot first','Synthetic candidate statement','consented'),
    ev('H11','2026-07-22','candidate','observation','private_sentiment','Do not disclose','Synthetic interview','restricted'),
]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--as-of', default='2026-10-21')
    args = parser.parse_args()
    if not args.demo and not args.input:
        parser.error('use --demo or --input')
    if args.demo:
        result = compare_domains([MA_DEMO, HIRING_DEMO], as_of=args.as_of)
    else:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        result = compare_domains(data, as_of=args.as_of) if isinstance(data, list) else analyze(data, as_of=args.as_of)
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f'Wrote {args.output}')
    else:
        print(output)

if __name__ == '__main__':
    main()
