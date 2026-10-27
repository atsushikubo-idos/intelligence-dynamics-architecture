"""Controlled frame adoption with append-only, hash-linked JSONL transition evidence.

Adoption registers a frame in the existing IDOS registry; it does NOT switch a
unit's active frame. Authorization and evidence provenance are external claims.
"""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from idos_reference_v1_2 import FrameGenesisStatus, ProvenanceEvent, ReferenceFrame
from reference_transition import Decision


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


class TransitionLedger:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        records = []
        previous = 'GENESIS'
        if not self.path.exists():
            return records
        for line in self.path.read_text(encoding='utf-8').splitlines():
            item = json.loads(line)
            digest = item['digest']
            body = {k: v for k, v in item.items() if k != 'digest'}
            if body['previous'] != previous or sha256(_canonical(body).encode()).hexdigest() != digest:
                raise ValueError('Transition ledger integrity failure')
            records.append(item)
            previous = digest
        return records

    def append(self, payload):
        records = self.read()
        body = {'previous': records[-1]['digest'] if records else 'GENESIS', 'payload': payload}
        item = {**body, 'digest': sha256(_canonical(body).encode()).hexdigest()}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('a', encoding='utf-8') as f:
            f.write(_canonical(item) + '\n')
            f.flush()
        return item


@dataclass
class ControlledTransition:
    adapter: object
    ledger: TransitionLedger

    def adopt(self, genesis_id: str, frame: ReferenceFrame, *, authorization_id: str,
              adoption_evidence: tuple[str, ...]):
        bridge = self.adapter.discovery_bridge
        genesis = bridge.registry.geneses.get(genesis_id)
        if genesis is None or genesis.status != FrameGenesisStatus.PROPOSED:
            raise ValueError('A pending registered genesis is required')
        if not self.adapter.reviews:
            raise ValueError('A transition review is required')
        review = self.adapter.reviews[-1]
        if review.target != genesis_id or review.source != bridge.baseline_frame_id:
            raise ValueError('Latest review does not match this transition')
        if review.decision != Decision.AUTHORIZED or review.authorization_id != authorization_id or not authorization_id.strip():
            raise ValueError('Matching explicit authorization required')
        if review.lost or review.unresolved:
            raise ValueError('Cannot adopt with unresolved or lost distinctions')
        if not adoption_evidence or any(not e.strip() for e in adoption_evidence):
            raise ValueError('Nonempty adoption evidence required')
        if frame.parent_id != bridge.baseline_frame_id:
            raise ValueError('New frame must retain baseline lineage')
        if frame.id in bridge.registry.frames:
            raise ValueError('Frame must be new')
        # Frame content is caller-supplied: categories do not prove semantic equivalence.
        if not review.retained.union(review.gained).issubset(set(frame.categories)):
            raise ValueError('Candidate frame must explicitly represent reviewed distinctions')
        if any(x['payload'].get('genesis_id') == genesis_id and x['payload'].get('event') == 'adopted'
               for x in self.ledger.read()):
            raise ValueError('Transition already recorded in ledger')
        payload = {
            'event': 'adopted', 'genesis_id': genesis_id,
            'old_frame_id': bridge.baseline_frame_id, 'new_frame_id': frame.id,
            'new_frame': {'name': frame.name, 'assumptions': list(frame.assumptions),
                          'categories': list(frame.categories), 'constraints': list(frame.constraints),
                          'version': frame.version, 'parent_id': frame.parent_id},
            'retained': sorted(review.retained), 'gained': sorted(review.gained),
            'lost': sorted(review.lost), 'unresolved': sorted(review.unresolved),
            'authorization_id': authorization_id, 'adoption_evidence': list(adoption_evidence),
            'note': 'Registry adoption only; active unit frame unchanged; external authorization not authenticated',
        }
        # Validate registry preconditions before recording. An external ledger and in-memory
        # registry cannot be committed atomically; recovery must reconcile on restart.
        self.ledger.append(payload)
        bridge.registry.adopt_frame(genesis_id, frame, adoption_evidence)
        bridge.relation.trajectory.provenance.append(ProvenanceEvent(
            'reference_transition_adopted', 'Registered candidate frame; active frame unchanged',
            [genesis_id, frame.id, authorization_id, *adoption_evidence]))
        return payload

    def history(self):
        return [record['payload'] for record in self.ledger.read()]
