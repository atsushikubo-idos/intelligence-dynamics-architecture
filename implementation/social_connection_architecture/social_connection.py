"""IDOS Social Connection Architecture v0.1.

A small, auditable protocol integration demonstrator; not a universal intelligence model.
Standard library only. Actors decide for themselves, via explicitly supplied decisions.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import Any
import json

CDP_FIELDS = ("Reality", "Difference", "Representation", "Residual", "Holding",
              "Update", "Possibility Space", "Trajectory", "Limit", "Enactment",
              "Reality′", "Reopening")

@dataclass
class Actor:
    id: str
    kind: str
    native_frame: str
    priorities: tuple[str, ...]
    can_share: bool = True
    adopted_frames: list[str] = field(default_factory=list)
    decision_history: list[dict] = field(default_factory=list)

@dataclass(frozen=True)
class Evidence:
    actor_id: str
    tick: int
    key: str
    value: float
    source: str
    shared: bool

@dataclass
class Candidate:
    id: str
    description: str
    derived_from: list[str]
    formula: str
    created_at: int
    validation: dict[str, Any] = field(default_factory=dict)

class SocialConnection:
    def __init__(self):
        self.actors: dict[str, Actor] = {}
        self.evidence: list[Evidence] = []
        self.events: list[dict] = []
        self.candidates: dict[str, Candidate] = {}
        self.hypothesis_weights: dict[str, float] = {"growth_only": .5, "liquidity_sensitive": .5}
        self.reopenings: list[dict] = []
        self.tick = 0

    def _log(self, event: str, **details):
        self.events.append({"event": event, "tick": self.tick, **details})

    def register(self, actor: Actor):
        if actor.id in self.actors:
            raise ValueError("Duplicate actor")
        self.actors[actor.id] = actor
        self._log("register", actor=actor.id, kind=actor.kind, native_frame=actor.native_frame)

    def observe(self, evidence: Evidence):
        if evidence.actor_id not in self.actors:
            raise ValueError("Unknown actor")
        if evidence.tick != self.tick:
            raise ValueError("Observation belongs to a different round")
        if evidence.shared and not self.actors[evidence.actor_id].can_share:
            raise PermissionError("Actor has not granted sharing permission")
        self.evidence.append(evidence)
        self._log("observation", actor=evidence.actor_id, key=evidence.key,
                  value=evidence.value if evidence.shared else None,
                  provenance=evidence.source, shared=evidence.shared)

    def shared_values(self, tick: int | None = None) -> dict[str, float]:
        at = self.tick if tick is None else tick
        # The same semantic key may be supplied by several actors; disagreement is not silently overwritten.
        values: dict[str, float] = {}
        conflicts: set[str] = set()
        for item in self.evidence:
            if item.tick == at and item.shared:
                if item.key in conflicts:
                    continue
                if item.key in values and abs(values[item.key] - item.value) > 1e-9:
                    self._log("measurement_conflict", key=item.key, tick_of_evidence=at)
                    values.pop(item.key, None)
                    conflicts.add(item.key)
                    continue
                values[item.key] = item.value
        return values

    def cfv_review(self, reviewer: str, claim: dict) -> dict:
        """Verify checkable shared claims. A result cannot certify an actor's internal reasoning."""
        if reviewer not in self.actors:
            raise ValueError("Unknown reviewer")
        source = claim["actor_id"]
        matching = [e for e in self.evidence if e.actor_id == source and e.key == claim["key"]
                    and e.tick == self.tick and e.shared]
        status = "unverifiable" if not matching else (
            "supported" if any(e.value == claim["value"] for e in matching) else "contradicted")
        result = {"reviewer": reviewer, "source": source, "claim_key": claim["key"],
                  "status": status, "evidence": [e.source for e in matching]}
        self._log("cfv_review", **result)
        return result

    def decide(self, actor_id: str, option: str, disposition: str, *, reason: str):
        if disposition not in {"adopt", "hold", "reject"}:
            raise ValueError("Disposition must be adopt, hold, or reject")
        actor = self.actors[actor_id]
        decision = {"tick": self.tick, "option": option, "disposition": disposition,
                    "reason": reason, "native_frame": actor.native_frame}
        actor.decision_history.append(decision)
        self._log("choice", actor=actor_id, **decision)
        return decision

    def update_actor(self, actor_id: str, frame_id: str, *, actor_approved: bool):
        if not actor_approved:
            self._log("update_declined", actor=actor_id, frame=frame_id)
            return False
        if frame_id not in self.candidates:
            raise KeyError("Unvalidated frame ID")
        if not self.candidates[frame_id].validation:
            raise ValueError("Candidate lacks recorded evaluation")
        actor = self.actors[actor_id]
        if frame_id not in actor.adopted_frames:
            actor.adopted_frames.append(frame_id)
        self._log("mutual_update_opportunity", actor=actor_id, frame=frame_id,
                  independent_approval=True)
        return True

    def relationship_distribution(self) -> dict[str, float]:
        """Empirical distribution of heterogeneous choices, NOT model/hypothesis probabilities."""
        counts = Counter(e["disposition"] for e in self.events if e["event"] == "choice")
        total = sum(counts.values())
        return {k: counts[k] / total for k in ("adopt", "hold", "reject")} if total else {}

    def explore(self) -> list[Candidate]:
        """A typed and deliberately LIMITED composition rule, triggered by a real difference."""
        latest = [a.decision_history[-1] for a in self.actors.values()
                  if a.decision_history and a.decision_history[-1]["tick"] == self.tick]
        disagreement = len({(d["option"], d["disposition"]) for d in latest}) >= 2
        shared = self.shared_values()
        if disagreement and shared.get("burn", 0) > 0 and "cash" in shared:
            key = "cash_runway"
            if key not in self.candidates:
                candidate = Candidate(key, "Cash runway as a cross-frame question",
                                      ["cash", "burn", "decision_disagreement"],
                                      "cash / burn", self.tick)
                self.candidates[key] = candidate
                self._log("candidate_generated", candidate=key, method="typed_composition")
            candidate = self.candidates[key]
            runway = shared["cash"] / shared["burn"]
            candidate.validation = {"tick": self.tick, "runway_months": round(runway, 4),
                                    "input_provenance": [e.source for e in self.evidence
                                                          if e.tick == self.tick and e.shared
                                                          and e.key in {"cash", "burn"}],
                                    "limitations": "Derived metric, not a validated causal model"}
            self._log("frame_evaluated", candidate=key, value=round(runway, 4))
            return [candidate]
        self._log("no_candidate", reason="No supported disagreement or missing authorized input")
        return []

    def update_hypotheses(self):
        """Illustrative likelihood weights for competing explanations; no forced decision."""
        values = self.shared_values()
        if not all(k in values for k in ("cash", "burn", "growth")):
            self._log("inference_deferred", reason="insufficient shared evidence")
            return dict(self.hypothesis_weights)
        runway = values["cash"] / values["burn"] if values["burn"] > 0 else float('inf')
        # A low runway supports a liquidity-sensitive explanation. Likelihoods are illustrative.
        likelihood = {"growth_only": .3 if runway < 6 else .65,
                      "liquidity_sensitive": .8 if runway < 6 else .35}
        unnorm = {k: p * likelihood[k] for k, p in self.hypothesis_weights.items()}
        total = sum(unnorm.values())
        self.hypothesis_weights = {k: v / total for k, v in unnorm.items()}
        self._log("inverse_distribution_updated", weights=dict(self.hypothesis_weights),
                  caveat="illustrative likelihoods; not probabilities of normative correctness")
        return dict(self.hypothesis_weights)

    def contact_reality(self, outcome: str, *, note: str):
        self._log("reality_contact", outcome=outcome, note=note)
        if outcome == "unexpected":
            self.reopenings.append({"tick": self.tick, "reason": note,
                                    "preserve_old_frames": list(self.candidates)})
            self._log("reopening", reason=note)

    def snapshot(self) -> dict:
        """A 12CDP-compatible *illustrative mapping*, not the full formal CDP standard."""
        latest_decisions = [{"actor": a.id, **a.decision_history[-1]}
                            for a in self.actors.values() if a.decision_history
                            and a.decision_history[-1]["tick"] == self.tick]
        mapping = {
            "Reality": {"tick": self.tick, "shared_evidence": [asdict(e) for e in self.evidence if e.tick == self.tick and e.shared]},
            "Difference": latest_decisions,
            "Representation": {"relationship_empirical_distribution": self.relationship_distribution(),
                               "inverse_hypothesis_distribution": dict(self.hypothesis_weights)},
            "Residual": [e for e in self.events if e["event"] in {"measurement_conflict", "no_candidate"}],
            "Holding": {"private_observation_count": sum(not e.shared for e in self.evidence),
                        "append_only_event_count": len(self.events)},
            "Update": {a.id: list(a.adopted_frames) for a in self.actors.values()},
            "Possibility Space": {c.id: asdict(c) for c in self.candidates.values()},
            "Trajectory": {a.id: list(a.decision_history) for a in self.actors.values()},
            "Limit": ["Only typed cash/burn composition is implemented",
                      "CFV checks consistency of shared evidence, not truth or comprehension",
                      "No autonomous ontology expansion, no social validation"],
            "Enactment": latest_decisions,
            "Reality′": [e for e in self.events if e["event"] == "reality_contact"],
            "Reopening": list(self.reopenings),
        }
        assert tuple(mapping) == CDP_FIELDS
        return mapping

    def next_round(self):
        self.tick += 1
        self._log("next_round")


def demo() -> dict:
    s = SocialConnection()
    s.register(Actor("h", "human", "growth_and_employment", ("growth", "people")))
    s.register(Actor("a", "ai", "uncertainty_and_options", ("uncertainty", "experimentation")))
    s.register(Actor("o", "organization", "liquidity_and_compliance", ("cash", "continuity")))
    s.observe(Evidence("h", 0, "growth", 0.8, "human:market_assessment", True))
    s.observe(Evidence("o", 0, "cash", 10.0, "org:finance_statement", True))
    s.observe(Evidence("o", 0, "burn", 2.5, "org:cash_forecast", True))
    # No private information is used in the discovery engine.
    s.observe(Evidence("h", 0, "private_criterion", 99.0, "human:private", False))
    s.decide("h", "expand", "adopt", reason="long-term growth priority")
    s.decide("a", "experiment", "hold", reason="need a reversible trial")
    s.decide("o", "expand", "reject", reason="cash continuity constraint")
    review = s.cfv_review("a", {"actor_id": "o", "key": "cash", "value": 10.0})
    rejected_review = s.cfv_review("a", {"actor_id": "o", "key": "cash", "value": 100.0})
    candidates = s.explore()
    s.update_hypotheses()
    s.update_actor("h", "cash_runway", actor_approved=False)
    s.update_actor("a", "cash_runway", actor_approved=True)
    s.update_actor("o", "cash_runway", actor_approved=True)
    s.contact_reality("unexpected", note="A subsequent market shock changes the runway assumptions")
    first = s.snapshot()
    s.next_round()
    s.observe(Evidence("h", 1, "growth", .7, "human:reassessment", True))
    s.observe(Evidence("o", 1, "cash", 7., "org:updated_statement", True))
    s.observe(Evidence("o", 1, "burn", 3.5, "org:updated_forecast", True))
    s.decide("h", "expand", "hold", reason="retain authority to wait")
    s.decide("a", "experiment", "adopt", reason="propose a reversible test")
    s.decide("o", "expand", "reject", reason="runway fell")
    s.explore()
    s.update_hypotheses()
    s.contact_reality("observed", note="Runway fell from 4 to 2 months")
    second = s.snapshot()
    return {"project": "IDOS Social Connection Architecture v0.1", "protocol_mapping": "12CDP illustrative",
            "cfv_verified": review, "cfv_contradiction": rejected_review,
            "candidate_ids": [c.id for c in candidates], "round_0": first, "round_1": second,
            "events": s.events, "limitations": second["Limit"]}

if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
