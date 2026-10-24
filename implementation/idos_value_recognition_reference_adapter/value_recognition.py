"""Experimental IDOS-inspired value-recognition trajectories.

Standalone prototype: no claim of compatibility with IDOS Reference v1.1.
Only explicitly observed features are evaluated. Unknown is not zero.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class Observation:
    id: str
    domain: str
    timestamp: str
    features: Mapping[str, float]
    description: str
    questions: tuple[str, ...] = ()

@dataclass(frozen=True)
class ReferenceFrame:
    id: str
    timestamp: str
    weights: Mapping[str, float]
    required_features: tuple[str, ...] = ()
    context: str = ""

@dataclass(frozen=True)
class Evaluation:
    observation_id: str
    frame_id: str
    status: str
    score: float | None
    missing: tuple[str, ...]
    rationale: str

@dataclass
class Trajectory:
    observations: dict[str, Observation] = field(default_factory=dict)
    frames: dict[str, ReferenceFrame] = field(default_factory=dict)
    evaluations: list[Evaluation] = field(default_factory=list)
    held: dict[str, str] = field(default_factory=dict)

    def observe(self, observation: Observation) -> None:
        if observation.id in self.observations:
            raise ValueError(f"Duplicate observation: {observation.id}")
        self.observations[observation.id] = observation

    def add_frame(self, frame: ReferenceFrame) -> None:
        if frame.id in self.frames:
            raise ValueError(f"Duplicate frame: {frame.id}")
        if not frame.weights or any(w < 0 for w in frame.weights.values()):
            raise ValueError("Weights must be nonnegative and nonempty")
        self.frames[frame.id] = frame

    def evaluate(self, observation_id: str, frame_id: str) -> Evaluation:
        obs = self.observations[observation_id]
        frame = self.frames[frame_id]
        needed = set(frame.weights) | set(frame.required_features)
        missing = tuple(sorted(needed - obs.features.keys()))
        if missing:
            result = Evaluation(obs.id, frame.id, "unassessable", None, missing,
                                "Insufficient observed features; do not equate unknown with zero")
        else:
            total = sum(frame.weights.values())
            score = sum(obs.features[k] * w for k, w in frame.weights.items()) / total if total else 0.0
            result = Evaluation(obs.id, frame.id, "assessed", round(score, 4), (),
                                "Illustrative weighted score under this reference frame")
        self.evaluations.append(result)
        return result

    def hold(self, observation_id: str, reason: str) -> None:
        if observation_id not in self.observations:
            raise KeyError(observation_id)
        if not reason.strip():
            raise ValueError("Holding requires an explicit reason")
        self.held[observation_id] = reason

    def reevaluate(self, observation_id: str, new_frame_id: str) -> dict[str, Any]:
        prior = [e for e in self.evaluations if e.observation_id == observation_id]
        if not prior:
            raise ValueError("Evaluate under an earlier frame first")
        previous = prior[-1]
        current = self.evaluate(observation_id, new_frame_id)
        return {
            "observation_id": observation_id,
            "previous": previous.__dict__,
            "current": current.__dict__,
            "recognition_transition": f"{previous.status} -> {current.status}",
            "score_delta": (round(current.score - previous.score, 4)
                            if previous.score is not None and current.score is not None else None),
            "held_reason": self.held.get(observation_id),
            "new_questions": list(self.observations[observation_id].questions),
            "caution": "Change in evaluation is not proof that intrinsic value was discovered.",
        }
