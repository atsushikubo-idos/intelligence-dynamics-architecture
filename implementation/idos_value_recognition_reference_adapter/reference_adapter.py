"""Experimental value-recognition adapter for IDOS Reference v1.1.

Keeps observational value hypotheses distinct from Residual/HoldingState.
Does not assert value discovery, causality, or scientific validation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from value_recognition import Observation, ReferenceFrame as ValueFrame, Trajectory as ValueTrajectory
from idos_reference_v1_1 import (UpdatingUnit, ReferenceFrame as IDOSFrame,
                                  UpdateLevel, ProvenanceEvent)

@dataclass
class ValueRecognitionAdapter:
    unit: UpdatingUnit
    model: ValueTrajectory = field(default_factory=ValueTrajectory)
    frame_links: dict[str, str] = field(default_factory=dict)

    def register_frame(self, value_frame: ValueFrame, idos_frame: IDOSFrame) -> None:
        if self.unit.frame.id != idos_frame.id:
            raise ValueError('IDOS frame must be the current frame of the updating unit')
        self.model.add_frame(value_frame)
        self.frame_links[value_frame.id] = idos_frame.id
        self.unit.trajectory.provenance.append(ProvenanceEvent(
            event_type='value_frame_linked',
            description='Provisional mapping of an application-level valuation frame to an IDOS reference frame',
            source_ids=[value_frame.id, idos_frame.id],
        ))

    def observe(self, observation: Observation) -> None:
        self.model.observe(observation)
        self.unit.trajectory.provenance.append(ProvenanceEvent(
            event_type='value_observation_preserved',
            description=f'Application-level observation retained: {observation.description}',
            source_ids=[observation.id],
        ))

    def evaluate(self, observation_id: str, value_frame_id: str):
        self._check_frame(value_frame_id)
        result = self.model.evaluate(observation_id, value_frame_id)
        self._trace_evaluation(result)
        return result

    def hold_unassessed(self, observation_id: str, reason: str) -> None:
        """Application-level preservation; NOT IDOS Residual/HoldingState."""
        self.model.hold(observation_id, reason)
        self.unit.trajectory.provenance.append(ProvenanceEvent(
            event_type='value_candidate_preserved', description=reason,
            source_ids=[observation_id],
        ))

    def revise_frame(self, *, new_idos_frame: IDOSFrame,
                     new_value_frame: ValueFrame, description: str) -> None:
        if new_idos_frame.parent_id != self.unit.frame.id:
            raise ValueError('New IDOS frame must revise the current frame')
        self.unit.update(UpdateLevel.L3, description, new_frame=new_idos_frame)
        self.register_frame(new_value_frame, new_idos_frame)

    def reevaluate(self, observation_id: str, new_value_frame_id: str) -> dict[str, Any]:
        self._check_frame(new_value_frame_id)
        result = self.model.reevaluate(observation_id, new_value_frame_id)
        current = self.model.evaluations[-1]
        self._trace_evaluation(current)
        self.unit.trajectory.provenance.append(ProvenanceEvent(
            event_type='value_recognition_reassessment',
            description=result['recognition_transition'],
            source_ids=[observation_id, result['previous']['frame_id'], new_value_frame_id],
        ))
        return result

    def _check_frame(self, value_frame_id: str) -> None:
        if self.frame_links.get(value_frame_id) != self.unit.frame.id:
            raise ValueError('Value frame is not linked to the current IDOS frame')

    def _trace_evaluation(self, evaluation) -> None:
        self.unit.trajectory.provenance.append(ProvenanceEvent(
            event_type='value_evaluation',
            description=f'{evaluation.status}: {evaluation.rationale}',
            source_ids=[evaluation.observation_id, evaluation.frame_id],
        ))
