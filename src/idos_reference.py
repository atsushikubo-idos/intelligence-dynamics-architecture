from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
from typing import Any, Dict, Iterable, List, Optional, Protocol, Sequence
from uuid import uuid4

"""
Intelligence Dynamics Architecture (IDOS)
Executable Reference Architecture v1.0

This implementation is intended to make the architecture inspectable,
executable, and criticizable—not to claim that intelligence has been reduced to code.

Successful execution is not scientific validation.

Epistemic labels used in comments/docstrings:
[D] Defined software structure
[P] Provisional architectural mapping
[O] Open research question

Design constraints represented here:
- Reality contact is mediated, not direct access to Reality.
- Difference is not automatically Residual.
- Holding can preserve unresolved Residual without immediate collapse.
- Trajectory is central, but Trajectory itself is not fixed.
- Physical Entity is not assumed to equal Updating Unit.
- Coupling does not imply Enactment or Agency.
- Boundaries, Reference Frames, and Possibility Spaces can change.
- Provenance supports traceability but does not prove identity or causality.
- CDP supports partial interoperability without representational unification.
- All open criteria are replaceable; no universal thresholds are asserted.
"""


def uid(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def unique(values: Iterable[str]) -> List[str]:
    return list(dict.fromkeys(values))


class EpistemicStatus(str, Enum):
    DEFINED = "D"
    PROVISIONAL = "P"
    OPEN = "O"


class Phase(str, Enum):
    BIRTH = "birth"
    PERSISTENCE = "persistence"
    ENACTMENT = "enactment"
    TRANSITION = "transition"
    DORMANCY = "dormancy"
    DISSOLUTION = "dissolution"
    REEMERGENCE = "re-emergence"


class UpdateLevel(str, Enum):
    L1 = "L1_local_absorption"
    L2 = "L2_parameter_update"
    L3 = "L3_frame_transformation"
    L4 = "L4_frame_traversal"
    L5 = "L5_possibility_space_transformation"


# -----------------------------------------------------------------------------
# Reality contact, Difference, Residual, Holding
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class RealityContact:
    """[P] A mediated observation/contact event, not Reality itself."""

    source: str
    observation: Any
    mode: str = "observation"
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("contact"))


@dataclass(frozen=True)
class Difference:
    """[D/P] A represented mismatch. It is not automatically a Residual."""

    description: str
    magnitude: Optional[float] = None
    confidence: Optional[float] = None
    id: str = field(default_factory=lambda: uid("diff"))


@dataclass
class Residual:
    """[P] A Difference treated as not adequately absorbed by the current frame."""

    description: str
    difference: Difference
    precision: Optional[float] = None
    salience: Optional[float] = None
    resolved: bool = False
    id: str = field(default_factory=lambda: uid("res"))


class ResidualCriterion(Protocol):
    """[O] No universal criterion for Difference -> Residual is claimed."""

    def evaluate(
        self,
        unit: "UpdatingUnit",
        contact: RealityContact,
        expected: Any,
        difference: Difference,
    ) -> bool: ...


class ExplicitMismatchCriterion:
    """[P] Demo-only criterion: caller chooses whether mismatch counts as Residual."""

    def __init__(self, accept_as_residual: bool = True):
        self.accept_as_residual = accept_as_residual

    def evaluate(
        self,
        unit: "UpdatingUnit",
        contact: RealityContact,
        expected: Any,
        difference: Difference,
    ) -> bool:
        return self.accept_as_residual


@dataclass
class HoldingState:
    """[P] Temporary preservation of unresolved Residual(s)."""

    residual_ids: List[str] = field(default_factory=list)
    competing_interpretations: List[str] = field(default_factory=list)
    reason: str = "unresolved"
    active: bool = True
    id: str = field(default_factory=lambda: uid("holding"))


# -----------------------------------------------------------------------------
# Mutable architectural contexts
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class ReferenceFrame:
    name: str
    assumptions: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    version: int = 1
    parent_id: Optional[str] = None
    id: str = field(default_factory=lambda: uid("frame"))

    def revise(
        self,
        *,
        name: Optional[str] = None,
        add_assumptions: Sequence[str] = (),
        remove_assumptions: Sequence[str] = (),
        add_categories: Sequence[str] = (),
        remove_categories: Sequence[str] = (),
        add_constraints: Sequence[str] = (),
        remove_constraints: Sequence[str] = (),
    ) -> "ReferenceFrame":
        def changed(old: Sequence[str], add: Sequence[str], remove: Sequence[str]) -> List[str]:
            removed = set(remove)
            return unique([x for x in old if x not in removed] + list(add))

        return ReferenceFrame(
            name=name or self.name,
            assumptions=changed(self.assumptions, add_assumptions, remove_assumptions),
            categories=changed(self.categories, add_categories, remove_categories),
            constraints=changed(self.constraints, add_constraints, remove_constraints),
            version=self.version + 1,
            parent_id=self.id,
        )


@dataclass(frozen=True)
class Boundary:
    included: List[str]
    excluded: List[str] = field(default_factory=list)
    permeability: Optional[float] = None
    version: int = 1
    parent_id: Optional[str] = None
    id: str = field(default_factory=lambda: uid("boundary"))

    def revise(
        self,
        *,
        include: Sequence[str] = (),
        remove_included: Sequence[str] = (),
        exclude: Sequence[str] = (),
        remove_excluded: Sequence[str] = (),
        permeability: Optional[float] = None,
    ) -> "Boundary":
        included = unique([x for x in self.included if x not in set(remove_included)] + list(include))
        excluded = unique([x for x in self.excluded if x not in set(remove_excluded)] + list(exclude))
        return Boundary(
            included=included,
            excluded=excluded,
            permeability=self.permeability if permeability is None else permeability,
            version=self.version + 1,
            parent_id=self.id,
        )


@dataclass(frozen=True)
class PossibilitySpace:
    actions: List[str] = field(default_factory=list)
    frames: List[str] = field(default_factory=list)
    relations: List[str] = field(default_factory=list)
    version: int = 1
    parent_id: Optional[str] = None
    id: str = field(default_factory=lambda: uid("space"))

    def revise(
        self,
        *,
        actions: Sequence[str] = (),
        remove_actions: Sequence[str] = (),
        frames: Sequence[str] = (),
        remove_frames: Sequence[str] = (),
        relations: Sequence[str] = (),
        remove_relations: Sequence[str] = (),
    ) -> "PossibilitySpace":
        def changed(old: Sequence[str], add: Sequence[str], remove: Sequence[str]) -> List[str]:
            removed = set(remove)
            return unique([x for x in old if x not in removed] + list(add))

        return PossibilitySpace(
            actions=changed(self.actions, actions, remove_actions),
            frames=changed(self.frames, frames, remove_frames),
            relations=changed(self.relations, relations, remove_relations),
            version=self.version + 1,
            parent_id=self.id,
        )


# -----------------------------------------------------------------------------
# Provenance, Update, Trajectory
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class ProvenanceEvent:
    event_type: str
    description: str
    source_ids: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("prov"))


@dataclass(frozen=True)
class UpdateEvent:
    level: UpdateLevel
    description: str
    residual_ids: List[str] = field(default_factory=list)
    reversible: Optional[bool] = None
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("upd"))


@dataclass(frozen=True)
class TrajectoryPoint:
    event: UpdateEvent
    frame_id: str
    boundary_id: str
    possibility_space_id: str
    timestamp: str = field(default_factory=now)


@dataclass
class Trajectory:
    """
    [P] Traceable update history.

    A Trajectory can change phase, branch, become dormant, dissolve, and be used as
    provenance for a re-emergent trajectory. These operations demonstrate
    'trajectory-centered, but not trajectory-fixed'; they do not define a universal
    ontology of trajectory identity.
    """

    label: str
    id: str = field(default_factory=lambda: uid("traj"))
    phase: Phase = Phase.BIRTH
    points: List[TrajectoryPoint] = field(default_factory=list)
    provenance: List[ProvenanceEvent] = field(default_factory=list)
    parent_trajectory_ids: List[str] = field(default_factory=list)

    def record(self, point: TrajectoryPoint) -> None:
        if self.phase == Phase.DISSOLUTION:
            raise RuntimeError("Cannot append to a dissolved trajectory; create a re-emergent trajectory instead.")
        self.points.append(point)
        if self.phase in (Phase.BIRTH, Phase.DORMANCY, Phase.REEMERGENCE):
            self.phase = Phase.PERSISTENCE
        self.provenance.append(
            ProvenanceEvent(
                event_type="trajectory_record",
                description=point.event.description,
                source_ids=[point.event.id],
            )
        )

    def transition(self, phase: Phase, reason: str) -> None:
        old = self.phase
        self.phase = phase
        self.provenance.append(
            ProvenanceEvent(
                event_type="phase_transition",
                description=f"{old.value} -> {phase.value}: {reason}",
                source_ids=[self.id],
            )
        )

    def branch(self, label: str, reason: str) -> "Trajectory":
        child = Trajectory(
            label=label,
            phase=Phase.BIRTH,
            parent_trajectory_ids=[self.id],
        )
        child.provenance.append(
            ProvenanceEvent(
                event_type="trajectory_branch",
                description=reason,
                source_ids=[self.id],
            )
        )
        self.provenance.append(
            ProvenanceEvent(
                event_type="branch_source",
                description=f"Branched to {child.id}: {reason}",
                source_ids=[child.id],
            )
        )
        return child

    def reemerge(self, label: str, reason: str) -> "Trajectory":
        """[O/P] Creates a new trace linked to an earlier one; identity is not asserted."""
        child = Trajectory(
            label=label,
            phase=Phase.REEMERGENCE,
            parent_trajectory_ids=[self.id],
        )
        child.provenance.append(
            ProvenanceEvent(
                event_type="trajectory_reemergence",
                description=reason,
                source_ids=[self.id],
            )
        )
        return child


# -----------------------------------------------------------------------------
# Updating Unit
# -----------------------------------------------------------------------------

@dataclass
class UpdatingUnit:
    """[P/O] Temporarily identifiable organization of updating processes."""

    name: str
    unit_type: str
    frame: ReferenceFrame
    boundary: Boundary
    possibility_space: PossibilitySpace
    trajectory: Trajectory
    id: str = field(default_factory=lambda: uid("unit"))
    component_ids: List[str] = field(default_factory=list)
    residuals: Dict[str, Residual] = field(default_factory=dict)
    holdings: List[HoldingState] = field(default_factory=list)

    def contact_reality(
        self,
        contact: RealityContact,
        *,
        expected: Optional[Any] = None,
        residual_criterion: Optional[ResidualCriterion] = None,
    ) -> Optional[Residual]:
        """
        [P] Minimal mediated Reality-contact path.

        Mismatch creates Difference. Difference becomes Residual only through an
        explicit replaceable criterion. This avoids hard-coding Difference = Residual.
        """
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="reality_contact",
                description=f"Contact via {contact.source} ({contact.mode})",
                source_ids=[contact.id],
            )
        )
        if expected is None or expected == contact.observation:
            return None

        difference = Difference(
            description=f"Expected {expected!r}, observed {contact.observation!r}"
        )
        # [O] A mismatch is not promoted to Residual by default.
        # Promotion requires an explicit, replaceable criterion.
        if residual_criterion is None:
            self.trajectory.provenance.append(
                ProvenanceEvent(
                    event_type="difference_unclassified",
                    description=difference.description,
                    source_ids=[difference.id, contact.id],
                )
            )
            return None
        criterion = residual_criterion
        if not criterion.evaluate(self, contact, expected, difference):
            self.trajectory.provenance.append(
                ProvenanceEvent(
                    event_type="difference_not_promoted",
                    description=difference.description,
                    source_ids=[difference.id, contact.id],
                )
            )
            return None

        residual = Residual(
            description=f"Difference treated as unresolved relative to frame '{self.frame.name}'",
            difference=difference,
        )
        self.residuals[residual.id] = residual
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="residual_registered",
                description=residual.description,
                source_ids=[contact.id, difference.id, residual.id],
            )
        )
        return residual

    def hold(
        self,
        residuals: Sequence[Residual],
        *,
        interpretations: Sequence[str] = (),
        reason: str = "unresolved",
    ) -> HoldingState:
        state = HoldingState(
            residual_ids=[r.id for r in residuals],
            competing_interpretations=list(interpretations),
            reason=reason,
        )
        self.holdings.append(state)
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="holding",
                description=f"Holding {len(state.residual_ids)} residual(s): {reason}",
                source_ids=state.residual_ids,
            )
        )
        return state

    def update(
        self,
        level: UpdateLevel,
        description: str,
        *,
        residuals: Sequence[Residual] = (),
        new_frame: Optional[ReferenceFrame] = None,
        new_boundary: Optional[Boundary] = None,
        new_possibility_space: Optional[PossibilitySpace] = None,
        reversible: Optional[bool] = None,
    ) -> UpdateEvent:
        old_frame = self.frame
        old_boundary = self.boundary
        old_space = self.possibility_space

        event = UpdateEvent(
            level=level,
            description=description,
            residual_ids=[r.id for r in residuals],
            reversible=reversible,
        )

        if new_frame is not None:
            self.frame = new_frame
        if new_boundary is not None:
            self.boundary = new_boundary
        if new_possibility_space is not None:
            self.possibility_space = new_possibility_space

        # [O] Update does not automatically mean that its motivating Residuals
        # have been resolved. Resolution requires a separate explicit judgment.

        self.trajectory.record(
            TrajectoryPoint(
                event=event,
                frame_id=self.frame.id,
                boundary_id=self.boundary.id,
                possibility_space_id=self.possibility_space.id,
            )
        )

        if self.frame.id != old_frame.id:
            self.trajectory.provenance.append(
                ProvenanceEvent("frame_revision", description, [old_frame.id, self.frame.id])
            )
        if self.boundary.id != old_boundary.id:
            self.trajectory.provenance.append(
                ProvenanceEvent("boundary_revision", description, [old_boundary.id, self.boundary.id])
            )
        if self.possibility_space.id != old_space.id:
            self.trajectory.provenance.append(
                ProvenanceEvent("possibility_space_revision", description, [old_space.id, self.possibility_space.id])
            )
        return event

    def resolve_residuals(
        self, residuals: Sequence[Residual], *, reason: str
    ) -> None:
        """[P/O] Explicitly records a provisional judgment that Residuals are resolved."""
        ids = []
        for residual in residuals:
            if residual.id in self.residuals:
                residual.resolved = True
                ids.append(residual.id)
        touched = set(ids)
        for holding in self.holdings:
            if holding.active and touched.intersection(holding.residual_ids):
                holding.active = False
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="residual_resolution_judgment",
                description=reason,
                source_ids=ids,
            )
        )

    def recontact(
        self,
        contact: RealityContact,
        *,
        expected: Optional[Any] = None,
        residual_criterion: Optional[ResidualCriterion] = None,
    ) -> Optional[Residual]:
        """[P] Explicit semantic alias emphasizing recursive return to Reality contact."""
        return self.contact_reality(
            contact,
            expected=expected,
            residual_criterion=residual_criterion,
        )


# -----------------------------------------------------------------------------
# Coupling and Enactment
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Coupling:
    trajectory_ids: List[str]
    description: str
    directionality: str = "mutual"
    strength: Optional[float] = None
    id: str = field(default_factory=lambda: uid("coupling"))


class EnactmentCriterion(Protocol):
    """[O] No universal enactment criterion is claimed."""

    def evaluate(self, units: Sequence[UpdatingUnit], coupling: Coupling) -> bool: ...


class ExplicitAuthorizationCriterion:
    """[P] Demo criterion only. Authorization is not a theory of emergence or agency."""

    def __init__(self, authorized: bool):
        self.authorized = authorized

    def evaluate(self, units: Sequence[UpdatingUnit], coupling: Coupling) -> bool:
        return self.authorized and len(units) >= 2


def enact_higher_order_unit(
    name: str,
    units: Sequence[UpdatingUnit],
    coupling: Coupling,
    criterion: EnactmentCriterion,
) -> Optional[UpdatingUnit]:
    """
    [P/O] Demonstrates Physical Entity != Updating Unit.

    Coupling alone does not enact a unit. No Agency is inferred here.
    """
    if not criterion.evaluate(units, coupling):
        return None

    frame = ReferenceFrame(
        name=f"{name} shared provisional frame",
        assumptions=["component frames remain distinct"],
    )
    boundary = Boundary(
        included=[u.id for u in units],
        permeability=None,  # [O] No universal permeability value is asserted.
    )
    possibilities = PossibilitySpace(
        actions=["joint inquiry", "independent action"],
        relations=["coordinate without unification"],
    )
    trajectory = Trajectory(
        label=f"{name} higher-order trajectory",
        phase=Phase.ENACTMENT,
        parent_trajectory_ids=[u.trajectory.id for u in units],
    )
    trajectory.provenance.append(
        ProvenanceEvent(
            event_type="enactment",
            description=f"Provisional enactment from coupling {coupling.id}",
            source_ids=[coupling.id] + [u.trajectory.id for u in units],
        )
    )
    return UpdatingUnit(
        name=name,
        unit_type="higher_order",
        frame=frame,
        boundary=boundary,
        possibility_space=possibilities,
        trajectory=trajectory,
        component_ids=[u.id for u in units],
    )


# -----------------------------------------------------------------------------
# Common Dynamics Protocol (CDP)
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class CDPDescription:
    unit_id: str
    trajectory_id: str
    phase: str
    frame_name: str
    boundary_version: int
    possibility_space_version: int
    unresolved_residuals: int
    active_holdings: int
    component_ids: List[str]
    epistemic_status: EpistemicStatus = EpistemicStatus.PROVISIONAL


class CommonDynamicsProtocol:
    """[P] Candidate interoperability layer; not a universal semantic protocol."""

    def describe(self, unit: UpdatingUnit) -> CDPDescription:
        return CDPDescription(
            unit_id=unit.id,
            trajectory_id=unit.trajectory.id,
            phase=unit.trajectory.phase.value,
            frame_name=unit.frame.name,
            boundary_version=unit.boundary.version,
            possibility_space_version=unit.possibility_space.version,
            unresolved_residuals=sum(not r.resolved for r in unit.residuals.values()),
            active_holdings=sum(h.active for h in unit.holdings),
            component_ids=list(unit.component_ids),
        )

    def translate(self, description: CDPDescription, target_label: str) -> Dict[str, Any]:
        """[P/O] Partial translation; internal semantics are deliberately not unified."""
        return {
            "target": target_label,
            "source_unit": description.unit_id,
            "dynamic_state": {
                "phase": description.phase,
                "frame": description.frame_name,
                "unresolved_residuals": description.unresolved_residuals,
                "active_holdings": description.active_holdings,
            },
            "translation_quality": "partial",
            "translation_residual": "Internal semantics and values are not assumed equivalent.",
        }

    def compare(self, a: CDPDescription, b: CDPDescription) -> Dict[str, Any]:
        return {
            "same_phase": a.phase == b.phase,
            "same_frame_name": a.frame_name == b.frame_name,
            "residual_difference": a.unresolved_residuals - b.unresolved_residuals,
            "both_holding": a.active_holdings > 0 and b.active_holdings > 0,
            "note": "Comparison does not imply identical internal representation.",
        }

    def coordinate(self, a: UpdatingUnit, b: UpdatingUnit, purpose: str) -> Coupling:
        return Coupling(
            trajectory_ids=[a.trajectory.id, b.trajectory.id],
            description=purpose,
        )

    def trace(self, unit: UpdatingUnit) -> List[Dict[str, Any]]:
        """Traceability only. Provenance does not prove trajectory identity or causality."""
        return [asdict(event) for event in unit.trajectory.provenance]

    def recontact(
        self,
        unit: UpdatingUnit,
        contact: RealityContact,
        *,
        expected: Optional[Any] = None,
        residual_criterion: Optional[ResidualCriterion] = None,
    ) -> Optional[Residual]:
        return unit.recontact(
            contact,
            expected=expected,
            residual_criterion=residual_criterion,
        )


# -----------------------------------------------------------------------------
# Construction and executable demonstration
# -----------------------------------------------------------------------------


def make_unit(name: str, unit_type: str, frame_name: str) -> UpdatingUnit:
    unit = UpdatingUnit(
        name=name,
        unit_type=unit_type,
        frame=ReferenceFrame(frame_name),
        boundary=Boundary(included=[name]),
        possibility_space=PossibilitySpace(actions=["observe", "act", "hold"]),
        trajectory=Trajectory(label=f"{name} trajectory"),
    )
    unit.trajectory.provenance.append(
        ProvenanceEvent(
            event_type="unit_initialized",
            description=f"Initialized {unit_type} updating unit '{name}'",
            source_ids=[unit.id],
        )
    )
    return unit


def demo() -> Dict[str, Any]:
    print("IDOS Executable Reference Architecture v1.0")
    print("Executable != validated\n")

    human = make_unit("Human", "human", "Efficiency-first frame")
    ai = make_unit("AI", "ai", "Optimization frame")

    # 1. Mediated Reality contact -> Difference -> explicitly accepted Residual.
    contact = RealityContact(
        source="joint task outcome",
        observation="higher efficiency but reduced option diversity",
    )
    residual = human.contact_reality(
        contact,
        expected="higher efficiency with preserved option diversity",
        residual_criterion=ExplicitMismatchCriterion(True),
    )
    assert residual is not None

    # 2. Holding keeps multiple interpretations open temporarily.
    human.hold(
        [residual],
        interpretations=[
            "the optimization objective is incomplete",
            "the reference frame may be too narrow",
        ],
    )

    # 3. A deeper update changes frame, boundary, and possibility space.
    revised_frame = human.frame.revise(
        name="Efficiency-and-optionality frame",
        add_assumptions=["future option diversity matters"],
    )
    revised_boundary = human.boundary.revise(
        include=["AI advisory process"],
        permeability=0.65,
    )
    revised_space = human.possibility_space.revise(
        actions=["test alternative objective", "preserve minority option"],
        frames=["optionality-sensitive frame"],
    )
    human.update(
        UpdateLevel.L3,
        "Revised frame after holding unresolved residual",
        residuals=[residual],
        new_frame=revised_frame,
        new_boundary=revised_boundary,
        new_possibility_space=revised_space,
    )

    # 4. Reality re-contact: the revised frame is exposed again to a new outcome.
    recontact = RealityContact(
        source="follow-up task outcome",
        observation="efficiency retained and option diversity partially restored",
    )
    second_residual = human.recontact(
        recontact,
        expected="efficiency retained and option diversity partially restored",
    )
    assert second_residual is None
    human.resolve_residuals(
        [residual],
        reason="Follow-up Reality contact provisionally supports treating the earlier Residual as resolved.",
    )

    # 5. CDP coordinates trajectories; Coupling alone does not enact a new unit.
    cdp = CommonDynamicsProtocol()
    coupling = cdp.coordinate(
        human,
        ai,
        "Joint inquiry into efficiency versus future optionality",
    )
    rejected_joint = enact_higher_order_unit(
        "Rejected Human-AI Inquiry",
        [human, ai],
        coupling,
        ExplicitAuthorizationCriterion(authorized=False),
    )
    assert rejected_joint is None

    # 6. A replaceable demo criterion permits provisional higher-order enactment.
    joint = enact_higher_order_unit(
        "Human-AI Inquiry",
        [human, ai],
        coupling,
        ExplicitAuthorizationCriterion(authorized=True),
    )
    assert joint is not None
    assert set(joint.component_ids) == {human.id, ai.id}

    # 7. Trajectory is not fixed: branch, dormancy, dissolution, and linked re-emergence.
    branch = human.trajectory.branch(
        "Human alternative inquiry trajectory",
        "Preserve an alternative line of inquiry without asserting identity equivalence.",
    )
    branch.transition(Phase.DORMANCY, "Alternative inquiry paused")
    branch.transition(Phase.DISSOLUTION, "This trace is no longer actively updated")
    reemergent = branch.reemerge(
        "Human re-emergent inquiry trajectory",
        "A later inquiry reuses historical provenance; sameness is not asserted.",
    )
    assert branch.id in reemergent.parent_trajectory_ids
    assert reemergent.id != branch.id

    human_desc = cdp.describe(human)
    ai_desc = cdp.describe(ai)
    joint_desc = cdp.describe(joint)

    result = {
        "human": asdict(human_desc),
        "ai": asdict(ai_desc),
        "comparison": cdp.compare(human_desc, ai_desc),
        "translation_to_ai": cdp.translate(human_desc, "AI"),
        "coupling": asdict(coupling),
        "coupling_without_enactment": rejected_joint is None,
        "higher_order_unit": asdict(joint_desc),
        "trajectory_nonfixity_demo": {
            "branch_id": branch.id,
            "branch_phase": branch.phase.value,
            "reemergent_id": reemergent.id,
            "reemergent_phase": reemergent.phase.value,
            "identity_claimed": False,
        },
        "human_provenance": cdp.trace(human),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return result


if __name__ == "__main__":
    demo()
