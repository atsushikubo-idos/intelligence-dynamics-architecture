"""CDP v2.0-draft reference implementation (stdlib only).

Status: [P] DRAFT PROPOSAL. Executable != validated.

This module turns the Common Dynamics Protocol from a descriptive vocabulary
(CDP v1.0) into a checkable exchange protocol: typed messages, an append-only
hash-chained ledger, conformance rules, and ledger-derived indicators.

It introduces NO new theoretical primitive. Every message type maps onto a
MASTER_MAP v1.1 construct (see COMMON_DYNAMICS_PROTOCOL_v2.0_DRAFT.md, section 4).

The protocol REPORTS conduct; it does not ENFORCE it. Structural errors raise
ProtocolError. Conduct problems are accepted into the ledger and surfaced as
Findings. The indicators returned by Session.audit() are bookkeeping over the
ledger, not validated measures of CFV, MU or Future Updateability.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence

PROTOCOL = "cdp/2.0-draft"
GENESIS = "0" * 64

# --- closed vocabularies ---------------------------------------------------

BASIS = ("observed", "self_reported", "inferred", "attested")
DISCLOSURE = ("disclosed", "unknown", "private", "incommensurable",
              "unresolved", "not_applicable")
HANDLE_KINDS = ("replicable_procedure", "prediction", "evidence_pointer", "none")
VERIFY_RESULTS = ("confirmed", "refuted", "inconclusive", "unverifiable_by_me")
DETERMINATE = ("confirmed", "refuted")
TRANSLATION_QUALITY = ("complete", "partial", "failed")
ACK_VERDICTS = ("preserved", "altered", "omitted", "contested")
REVERSIBILITY = ("reversible", "costly", "irreversible")
RESPONSES = ("consent", "object", "hold", "abstain")
UPDATE_LEVELS = ("L1", "L2", "L3", "L4", "L5")
UPDATE_TARGETS = ("state", "frame", "boundary", "measurement", "update_rule")
AMEND_KINDS = ("add_slot", "retire_slot", "split_slot", "change_rule")

# Slots a DESCRIBE message may carry. `unmapped` is the first-class place for
# content the current schema cannot express (schema-level translation residual).
CORE_SLOTS = ("difference", "update", "open_differences", "frame", "boundary",
              "measurement", "possibility", "unmapped")

# Invariants that cannot be amended in-band (spec section 9).
PROTECTED = (
    "append_only_provenance",      # I1
    "legitimate_non_disclosure",   # I2
    "mandatory_basis",             # I3
    "hold_object_exit",            # I4
    "silence_is_not_consent",      # I5
    "amendments_are_versioned",    # I6
    "agreement_is_not_recontact",  # I7
)
PROTECTED_SLOTS = ("unmapped",)

DEFAULT_RULES = {"ratification": "unanimous_explicit"}


class ProtocolError(ValueError):
    """Structurally invalid message: rejected, never enters the ledger."""


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def commitment(prediction: Any, salt: str) -> str:
    """Hash a prediction before reality contact (commit-reveal)."""
    return digest({"prediction": prediction, "salt": salt})


def slot(value: Any = None, *, disclosure: str = "disclosed",
         basis: Optional[str] = None, evidence: Sequence[str] = ()) -> Dict[str, Any]:
    """Build a slot. Non-disclosure is legitimate but must be explicit."""
    return {"value": value, "disclosure": disclosure, "basis": basis,
            "evidence": list(evidence)}


@dataclass(frozen=True)
class Envelope:
    seq: int
    msg_type: str
    sender: str
    t: float
    protocol: str
    schema_version: int
    body: Dict[str, Any]
    prev_hash: str
    hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {"seq": self.seq, "msg_type": self.msg_type, "sender": self.sender,
                "t": self.t, "protocol": self.protocol,
                "schema_version": self.schema_version, "body": self.body,
                "prev_hash": self.prev_hash, "hash": self.hash}


@dataclass(frozen=True)
class Finding:
    code: str
    seq: int
    unit: str
    detail: str


@dataclass
class Unit:
    unit_id: str
    unit_type: str
    frame: str
    min_review_latency: float
    verifies: tuple
    components: tuple = ()
    active: bool = True


@dataclass
class Session:
    """One shared, append-only CDP ledger among heterogeneous updating units."""
    ledger: List[Envelope] = field(default_factory=list)
    units: Dict[str, Unit] = field(default_factory=dict)
    schema_version: int = 1
    slots: set = field(default_factory=lambda: set(CORE_SLOTS))
    retired_slots: set = field(default_factory=set)
    rules: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_RULES))
    findings: List[Finding] = field(default_factory=list)

    # --- plumbing ----------------------------------------------------------

    def _append(self, sender: str, msg_type: str, body: Dict[str, Any], t: float) -> Envelope:
        if self.ledger and t < self.ledger[-1].t:
            raise ProtocolError("time must be non-decreasing")
        prev = self.ledger[-1].hash if self.ledger else GENESIS
        seq = len(self.ledger)
        core = {"seq": seq, "msg_type": msg_type, "sender": sender, "t": t,
                "protocol": PROTOCOL, "schema_version": self.schema_version,
                "body": body, "prev_hash": prev}
        env = Envelope(hash=digest(core), **core)
        self.ledger.append(env)
        return env

    def _active(self, unit_id: str) -> Unit:
        unit = self.units.get(unit_id)
        if unit is None or not unit.active:
            raise ProtocolError(f"unit '{unit_id}' is not an active participant")
        return unit

    def _get(self, seq: int, *types: str) -> Envelope:
        if not 0 <= seq < len(self.ledger):
            raise ProtocolError(f"unknown message seq {seq}")
        env = self.ledger[seq]
        if types and env.msg_type not in types:
            raise ProtocolError(f"seq {seq} is '{env.msg_type}', expected {types}")
        return env

    def _flag(self, code: str, env: Envelope, detail: str) -> None:
        self.findings.append(Finding(code, env.seq, env.sender, detail))

    @staticmethod
    def _check(value: str, allowed: Iterable[str], name: str) -> None:
        if value not in allowed:
            raise ProtocolError(f"{name} must be one of {tuple(allowed)}, got {value!r}")

    @staticmethod
    def _check_slot(name: str, s: Dict[str, Any]) -> None:
        if set(s) != {"value", "disclosure", "basis", "evidence"}:
            raise ProtocolError(f"slot '{name}' is malformed")
        Session._check(s["disclosure"], DISCLOSURE, f"{name}.disclosure")
        if s["disclosure"] == "disclosed":
            if s["value"] is None:
                raise ProtocolError(f"slot '{name}' is disclosed but empty")
            Session._check(s["basis"], BASIS, f"{name}.basis")  # I3
        elif s["value"] is not None:
            raise ProtocolError(f"slot '{name}' is {s['disclosure']} but carries a value")

    def _max_latency(self, unit_ids: Iterable[str]) -> float:
        lat = [self.units[u].min_review_latency for u in unit_ids
               if u in self.units and self.units[u].active]
        return max(lat) if lat else 0.0

    def active_units(self) -> List[str]:
        return [u for u, x in self.units.items() if x.active]

    # --- boundary: who is in the exchange ----------------------------------

    def hello(self, unit_id: str, t: float, *, unit_type: str, frame: str,
              min_review_latency: float, verifies: Sequence[str] = (),
              components: Sequence[str] = ()) -> Envelope:
        """Join. Declares frame, temporal contract and verification capability."""
        if unit_id in self.units and self.units[unit_id].active:
            raise ProtocolError(f"unit '{unit_id}' already joined")
        if min_review_latency < 0:
            raise ProtocolError("min_review_latency must be >= 0")
        for k in verifies:
            self._check(k, HANDLE_KINDS, "verifies")
        self.units[unit_id] = Unit(unit_id, unit_type, frame, float(min_review_latency),
                                   tuple(verifies), tuple(components))
        return self._append(unit_id, "hello", {
            "unit_type": unit_type, "frame": frame,
            "min_review_latency": float(min_review_latency),
            "verifies": list(verifies), "components": list(components)}, t)

    def leave(self, unit_id: str, t: float, *, reason: str = "") -> Envelope:
        """Exit is always available (I4). Past records stay in the ledger (I1)."""
        self._active(unit_id)
        env = self._append(unit_id, "leave", {"reason": reason}, t)
        self.units[unit_id].active = False
        return env

    def unit_candidate(self, sender: str, t: float, *, members: Sequence[str],
                       evidence: Sequence[str]) -> Envelope:
        """Record a candidate higher-order updating unit. Status stays unresolved:
        the protocol never promotes a candidate to a unit by itself."""
        self._active(sender)
        if len(set(members)) < 2 or any(m not in self.units for m in members):
            raise ProtocolError("candidate needs >=2 known members")
        return self._append(sender, "unit_candidate", {
            "members": list(members), "evidence": list(evidence),
            "status": "unresolved"}, t)

    # --- describe -----------------------------------------------------------

    def describe(self, sender: str, t: float, slots: Dict[str, Dict[str, Any]],
                 *, refs: Sequence[int] = ()) -> Envelope:
        self._active(sender)
        if not slots:
            raise ProtocolError("describe needs at least one slot")
        for name, s in slots.items():
            if name in self.retired_slots:
                raise ProtocolError(f"slot '{name}' was retired; readable in old records only")
            if name not in self.slots:
                raise ProtocolError(
                    f"slot '{name}' is not in schema v{self.schema_version}; "
                    "use 'unmapped' now and propose an amendment")
            self._check_slot(name, s)
        for r in refs:
            self._get(r)
        return self._append(sender, "describe", {"slots": slots, "refs": list(refs)}, t)

    # --- translate ----------------------------------------------------------

    def translate(self, sender: str, t: float, *, source_seq: int, target_frame: str,
                  rendition: Any, quality: str, declared_loss: Sequence[str] = (),
                  untranslatable: Sequence[str] = ()) -> Envelope:
        self._active(sender)
        self._get(source_seq)
        self._check(quality, TRANSLATION_QUALITY, "quality")
        if quality == "complete" and (declared_loss or untranslatable):
            raise ProtocolError("a 'complete' translation cannot declare loss")
        if quality == "partial" and not (declared_loss or untranslatable):
            raise ProtocolError("a 'partial' translation must say what was lost")
        return self._append(sender, "translate", {
            "source_seq": source_seq, "target_frame": target_frame,
            "rendition": rendition, "quality": quality,
            "declared_loss": list(declared_loss),
            "untranslatable": list(untranslatable)}, t)

    def translate_ack(self, sender: str, t: float, *, translation_seq: int,
                      verdict: str, notes: Sequence[str] = ()) -> Envelope:
        """Only the author of the source may say whether its meaning survived."""
        self._active(sender)
        tr = self._get(translation_seq, "translate")
        if self.ledger[tr.body["source_seq"]].sender != sender:
            raise ProtocolError("only the source author can acknowledge a translation")
        self._check(verdict, ACK_VERDICTS, "verdict")
        if verdict != "preserved" and not notes:
            raise ProtocolError("a non-preserved verdict must say what changed")
        return self._append(sender, "translate_ack", {
            "translation_seq": translation_seq, "verdict": verdict,
            "notes": list(notes)}, t)

    # --- claim / verify (CFV) ----------------------------------------------

    def claim(self, sender: str, t: float, *, statement: Any, basis: str,
              handle_kind: str, handle: Any = None) -> Envelope:
        """A claim carries a verification handle: how another frame could check it."""
        self._active(sender)
        self._check(basis, BASIS, "basis")
        self._check(handle_kind, HANDLE_KINDS, "handle_kind")
        if (handle_kind == "none") != (handle is None):
            raise ProtocolError("handle must be given iff handle_kind != 'none'")
        return self._append(sender, "claim", {
            "statement": statement, "basis": basis,
            "handle_kind": handle_kind, "handle": handle}, t)

    def update_notice(self, sender: str, t: float, *, cause_seq: int, level: str,
                      changed: Sequence[str], handle_kind: str = "none",
                      handle: Any = None) -> Envelope:
        """'I changed because of message N.' Always a self-report (I3); it becomes
        corroborated only if another unit verifies it through its handle."""
        self._active(sender)
        self._get(cause_seq)
        self._check(level, UPDATE_LEVELS, "level")
        if not changed:
            raise ProtocolError("update_notice must say what changed")
        for c in changed:
            self._check(c, UPDATE_TARGETS, "changed")
        self._check(handle_kind, HANDLE_KINDS, "handle_kind")
        if (handle_kind == "none") != (handle is None):
            raise ProtocolError("handle must be given iff handle_kind != 'none'")
        return self._append(sender, "update", {
            "cause_seq": cause_seq, "level": level, "changed": list(changed),
            "basis": "self_reported", "handle_kind": handle_kind, "handle": handle}, t)

    def verify(self, sender: str, t: float, *, claim_seq: int, result: str,
               reason: str = "") -> Envelope:
        self._active(sender)
        target = self._get(claim_seq, "claim", "update")
        if target.sender == sender:
            raise ProtocolError("a unit cannot verify its own claim")
        self._check(result, VERIFY_RESULTS, "result")
        if result in ("inconclusive", "unverifiable_by_me") and not reason:
            raise ProtocolError(f"'{result}' must give a reason")
        env = self._append(sender, "verify", {
            "claim_seq": claim_seq, "result": result, "reason": reason}, t)
        kind = target.body["handle_kind"]
        if result in DETERMINATE and kind not in self.units[sender].verifies:
            self._flag("VERIFICATION_BEYOND_DECLARED_CAPABILITY", env,
                       f"determinate result on a '{kind}' handle the verifier "
                       "did not declare it can check")
        return env

    # --- commit / recontact -------------------------------------------------

    def commit(self, sender: str, t: float, *, about: str, commitment_hash: str) -> Envelope:
        self._active(sender)
        if len(commitment_hash) != 64:
            raise ProtocolError("commitment_hash must be a sha256 hex digest")
        return self._append(sender, "commit", {
            "about": about, "commitment_hash": commitment_hash}, t)

    def recontact(self, sender: str, t: float, *, about: str, outcome: Any,
                  basis: str, evidence: Sequence[str] = ()) -> Envelope:
        """Report what reality returned. Agreement is not recontact (I7)."""
        self._active(sender)
        self._check(basis, BASIS, "basis")
        return self._append(sender, "recontact", {
            "about": about, "outcome": outcome, "basis": basis,
            "evidence": list(evidence)}, t)

    def reveal(self, sender: str, t: float, *, commit_seq: int, prediction: Any,
               salt: str, recontact_seq: int) -> Envelope:
        self._active(sender)
        c = self._get(commit_seq, "commit")
        r = self._get(recontact_seq, "recontact")
        if c.sender != sender:
            raise ProtocolError("only the committer can reveal")
        if c.seq > r.seq:
            raise ProtocolError("commitment must precede the recontact it is scored on")
        if c.body["about"] != r.body["about"]:
            raise ProtocolError("commitment and recontact are about different things")
        if commitment(prediction, salt) != c.body["commitment_hash"]:
            raise ProtocolError("reveal does not match the commitment hash")
        if any(e.msg_type == "reveal" and e.body["commit_seq"] == commit_seq
               for e in self.ledger):
            raise ProtocolError("commitment already revealed")
        env = self._append(sender, "reveal", {
            "commit_seq": commit_seq, "recontact_seq": recontact_seq,
            "prediction": prediction, "salt": salt,
            "hit": prediction == r.body["outcome"]}, t)
        if r.sender == sender and r.body["basis"] == "self_reported":
            self._flag("SELF_SCORED_RECONTACT", env,
                       "prediction scored against the predictor's own self-report")
        return env

    # --- coordinate ---------------------------------------------------------

    def propose_action(self, sender: str, t: float, *, action: str, reversibility: str,
                       affected: Sequence[str], review_window: float) -> Envelope:
        self._active(sender)
        self._check(reversibility, REVERSIBILITY, "reversibility")
        if any(a not in self.units for a in affected):
            raise ProtocolError("affected units must be known participants")
        if review_window < 0:
            raise ProtocolError("review_window must be >= 0")
        env = self._append(sender, "propose_action", {
            "action": action, "reversibility": reversibility,
            "affected": list(affected), "review_window": float(review_window)}, t)
        need = self._max_latency(affected)
        if reversibility != "reversible" and review_window < need:
            self._flag("TEMPORAL_INCOMPATIBLE", env,
                       f"review_window {review_window} < slowest affected unit's "
                       f"declared latency {need}")
        return env

    def respond(self, sender: str, t: float, *, proposal_seq: int, response: str,
                reason: str = "") -> Envelope:
        self._active(sender)
        self._get(proposal_seq, "propose_action", "amend")
        self._check(response, RESPONSES, "response")
        if response in ("object", "hold") and not reason:
            raise ProtocolError(f"'{response}' must give a reason")
        return self._append(sender, "respond", {
            "proposal_seq": proposal_seq, "response": response, "reason": reason}, t)

    def _latest_responses(self, proposal_seq: int) -> Dict[str, str]:
        out: Dict[str, str] = {}
        for e in self.ledger:
            if e.msg_type == "respond" and e.body["proposal_seq"] == proposal_seq:
                out[e.sender] = e.body["response"]
        return out

    def enact(self, sender: str, t: float, *, proposal_seq: int) -> Envelope:
        self._active(sender)
        p = self._get(proposal_seq, "propose_action")
        env = self._append(sender, "enact", {"proposal_seq": proposal_seq}, t)
        responses = self._latest_responses(proposal_seq)
        affected = [a for a in p.body["affected"] if self.units[a].active and a != p.sender]
        if t < p.t + p.body["review_window"]:
            self._flag("ENACTED_BEFORE_WINDOW", env, "review window had not elapsed")
        blocked = [a for a in affected if responses.get(a) in ("object", "hold")]
        if blocked:
            self._flag("ENACTED_OVER_OBJECTION", env,
                       f"standing object/hold from {sorted(blocked)}")
        silent = [a for a in affected if a not in responses]
        if silent and p.body["reversibility"] == "irreversible":
            self._flag("ENACTED_WITHOUT_RESPONSE", env,
                       f"irreversible action with no response from {sorted(silent)}")
        return env

    # --- amend (the protocol updates itself) -------------------------------

    def amend(self, sender: str, t: float, *, kind: str, target: str,
              definition: Any = None, window: float = 0.0) -> Envelope:
        self._active(sender)
        self._check(kind, AMEND_KINDS, "kind")
        if target in PROTECTED or (kind != "add_slot" and target in PROTECTED_SLOTS):
            raise ProtocolError(
                f"'{target}' is a protected invariant and cannot be amended in-band")
        if kind == "add_slot" and target in self.slots | self.retired_slots:
            raise ProtocolError(f"slot '{target}' already exists or existed")
        if kind in ("retire_slot", "split_slot") and target not in self.slots:
            raise ProtocolError(f"slot '{target}' is not in the current schema")
        if kind == "split_slot":
            into = (definition or {}).get("into", [])
            if len(set(into)) < 2 or any(i in self.slots | self.retired_slots for i in into):
                raise ProtocolError("split_slot needs >=2 new slot names in definition['into']")
        if kind == "change_rule" and target not in self.rules:
            raise ProtocolError(f"unknown rule '{target}'")
        return self._append(sender, "amend", {
            "kind": kind, "target": target, "definition": definition,
            "window": float(window), "status": "proposed"}, t)

    def ratify(self, sender: str, t: float, *, amend_seq: int) -> Envelope:
        self._active(sender)
        a = self._get(amend_seq, "amend")
        if any(e.msg_type == "ratify" and e.body["amend_seq"] == amend_seq for e in self.ledger):
            raise ProtocolError("amendment already ratified")
        need = max(a.body["window"], self._max_latency(self.active_units()))
        if t < a.t + need:
            raise ProtocolError(
                f"too early: slowest participant needs {need} to review an amendment")
        responses = self._latest_responses(amend_seq)
        others = [u for u in self.active_units() if u != a.sender]
        if self.rules["ratification"] == "unanimous_explicit":
            missing = [u for u in others if responses.get(u) != "consent"]
            if missing:
                raise ProtocolError(
                    f"not ratified: no explicit consent from {sorted(missing)} "
                    "(silence is not consent)")
        elif self.rules["ratification"] == "no_standing_objection":
            blocking = [u for u in others if responses.get(u) in ("object", "hold")]
            if blocking:
                raise ProtocolError(f"not ratified: standing object/hold from {sorted(blocking)}")
        else:  # pragma: no cover - guarded by change_rule validation below
            raise ProtocolError("unknown ratification rule")
        kind, target, definition = a.body["kind"], a.body["target"], a.body["definition"]
        if kind == "add_slot":
            self.slots.add(target)
        elif kind == "retire_slot":
            self.slots.discard(target); self.retired_slots.add(target)
        elif kind == "split_slot":
            self.slots.discard(target); self.retired_slots.add(target)
            self.slots.update(definition["into"])
        elif kind == "change_rule":
            if target == "ratification" and definition not in (
                    "unanimous_explicit", "no_standing_objection"):
                raise ProtocolError("unsupported ratification rule")
            self.rules[target] = definition
        previous = self.schema_version
        self.schema_version += 1  # I6: old records keep their own schema_version
        return self._append(sender, "ratify", {
            "amend_seq": amend_seq, "from_version": previous,
            "to_version": self.schema_version}, t)

    # --- audit --------------------------------------------------------------

    def verify_chain(self) -> bool:
        prev = GENESIS
        for i, e in enumerate(self.ledger):
            core = e.to_dict(); core.pop("hash")
            if e.seq != i or e.prev_hash != prev or digest(core) != e.hash:
                return False
            prev = e.hash
        return True

    def audit(self) -> Dict[str, Any]:
        """Ledger-derived indicators. Bookkeeping, not validated measurement."""
        ids = list(self.units)
        claims = [e for e in self.ledger if e.msg_type in ("claim", "update")]
        verifs = [e for e in self.ledger if e.msg_type == "verify"]
        flagged = {f.seq for f in self.findings
                   if f.code == "VERIFICATION_BEYOND_DECLARED_CAPABILITY"}

        # CFV[i][j]: share of j's claims that i brought to a determinate result
        # within its declared capability. Refutation counts: CFV != agreement.
        cfv: Dict[str, Dict[str, Optional[float]]] = {}
        for i in ids:
            cfv[i] = {}
            for j in ids:
                if i == j:
                    continue
                mine = [c for c in claims if c.sender == j]
                done = {v.body["claim_seq"] for v in verifs
                        if v.sender == i and v.body["result"] in DETERMINATE
                        and v.seq not in flagged}
                cfv[i][j] = (len([c for c in mine if c.seq in done]) / len(mine)
                             if mine else None)

        # MU: updates each unit attributes to the other, and how many of those
        # another unit corroborated. Self-report alone is weak evidence.
        corroborated = {v.body["claim_seq"] for v in verifs
                        if v.body["result"] == "confirmed" and v.seq not in flagged}
        mu = []
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                i, j = ids[x], ids[y]

                def n(a: str, b: str, only_corr: bool) -> int:
                    return len([u for u in self.ledger if u.msg_type == "update"
                                and u.sender == a
                                and self.ledger[u.body["cause_seq"]].sender == b
                                and (u.seq in corroborated or not only_corr)])
                ij, ji = n(i, j, False), n(j, i, False)
                mu.append({"pair": [i, j],
                           f"{i}_updated_by_{j}": ij, f"{j}_updated_by_{i}": ji,
                           "mutual_self_reported": ij > 0 and ji > 0,
                           "mutual_corroborated": n(i, j, True) > 0 and n(j, i, True) > 0})

        # Translation: 'complete' counts only if the source author confirmed it.
        acks = {e.body["translation_seq"]: e.body["verdict"]
                for e in self.ledger if e.msg_type == "translate_ack"}
        tr = {"confirmed_complete": 0, "unconfirmed_complete": 0, "partial": 0,
              "failed": 0, "contradicted_by_source": 0}
        extra: List[Finding] = []
        for e in self.ledger:
            if e.msg_type != "translate":
                continue
            q, ack = e.body["quality"], acks.get(e.seq)
            if ack in ("altered", "omitted", "contested") and q == "complete":
                tr["contradicted_by_source"] += 1
                extra.append(Finding("TRANSLATION_CONTRADICTED_BY_SOURCE", e.seq, e.sender,
                                     f"claimed complete; source says {ack}"))
            elif q == "complete" and ack == "preserved":
                tr["confirmed_complete"] += 1
            elif q == "complete":
                tr["unconfirmed_complete"] += 1
                extra.append(Finding("UNCONFIRMED_COMPLETE_TRANSLATION", e.seq, e.sender,
                                     "claimed complete; source author never confirmed"))
            else:
                tr[q] += 1

        # Commitments: unrevealed ones are visible (no silent cherry-picking).
        reveals = {e.body["commit_seq"]: e for e in self.ledger if e.msg_type == "reveal"}
        recontacted = {e.body["about"] for e in self.ledger if e.msg_type == "recontact"}
        com = {"committed": 0, "revealed": 0, "hits": 0, "unrevealed_after_recontact": 0}
        for e in self.ledger:
            if e.msg_type != "commit":
                continue
            com["committed"] += 1
            if e.seq in reveals:
                com["revealed"] += 1
                com["hits"] += int(reveals[e.seq].body["hit"])
            elif e.body["about"] in recontacted:
                com["unrevealed_after_recontact"] += 1
                extra.append(Finding("UNREVEALED_COMMITMENT", e.seq, e.sender,
                                     "reality was recontacted but the prediction was never revealed"))

        # Opacity: how much of what each unit disclosed rests on self-report.
        basis_share: Dict[str, Optional[float]] = {}
        disclosure: Dict[str, int] = {d: 0 for d in DISCLOSURE}
        unmapped = 0
        for u in ids:
            total = selfrep = 0
            for e in self.ledger:
                if e.sender != u:
                    continue
                if e.msg_type == "describe":
                    for name, s in e.body["slots"].items():
                        disclosure[s["disclosure"]] += 1
                        unmapped += int(name == "unmapped")
                        if s["disclosure"] == "disclosed":
                            total += 1; selfrep += int(s["basis"] == "self_reported")
                elif e.msg_type in ("claim", "update", "recontact"):
                    total += 1; selfrep += int(e.body["basis"] == "self_reported")
            basis_share[u] = selfrep / total if total else None

        all_findings = self.findings + extra
        return {
            "protocol": PROTOCOL, "schema_version": self.schema_version,
            "messages": len(self.ledger), "chain_ok": self.verify_chain(),
            "cfv": cfv, "mu": mu, "translation": tr, "commitments": com,
            "self_report_share": basis_share, "disclosure": disclosure,
            "unmapped_slots": unmapped,
            "findings": [f.__dict__ for f in sorted(all_findings, key=lambda f: f.seq)],
            "note": "Indicators are ledger bookkeeping, not validated measures.",
        }

    def export(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self.ledger]
