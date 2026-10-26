"""Automatic *candidate* detection; never silently certifies semantic preservation.

Built-in heuristics are deterministic, not a trained AI model. An optional external
AI assessor can propose a disposition/evidence; all proposals remain provisional.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable
import re
from interoperability import Claim, Assessment, Disposition

_STOP = {"the", "a", "an", "to", "of", "and", "or", "in", "on", "for", "with",
         "is", "are", "be", "that", "it", "this", "by", "from", "at"}
_NEG = {"not", "never", "no", "without", "cannot", "mustn't", "don't"}
_TOKEN = re.compile(r"[a-z]+(?:'[a-z]+)?|\d+(?:\.\d+)?", re.I)


def tokens(text: str) -> set[str]:
    return set(_TOKEN.findall(text.lower())) - _STOP


@dataclass(frozen=True)
class Candidate:
    claim_id: str
    proposed: Disposition
    rationale: str
    confidence: float  # heuristic/model self-report, NOT calibrated probability
    method: str
    reviewed: bool = False

    def to_assessment(self) -> Assessment:
        # Only attach *tentative* states. No algorithmic PRESERVED/ALTERED/OMITTED
        # gets promoted to an attested finding without external review.
        return Assessment(self.claim_id, Disposition.UNRESOLVED,
                          f"Candidate {self.proposed.value}: {self.rationale}",
                          f"automated:{self.method}")


def heuristic_candidate(claim: Claim, rendition: str) -> Candidate:
    original, rendered = tokens(claim.text), tokens(rendition)
    if not original:
        return Candidate(claim.id, Disposition.UNRESOLVED, "No inspectable source tokens", 0.0, "heuristic")
    missing = sorted(original - rendered)
    negation_conflict = bool((original & _NEG) != (rendered & _NEG))
    numbers = {t for t in original if t[0].isdigit()}
    missing_numbers = sorted(numbers - rendered)
    if negation_conflict or missing_numbers:
        return Candidate(claim.id, Disposition.ALTERED,
                         f"Negation mismatch={negation_conflict}; missing numbers={missing_numbers}",
                         0.7, "heuristic")
    coverage = len(original & rendered) / len(original)
    if coverage >= 0.85:
        return Candidate(claim.id, Disposition.PRESERVED,
                         f"Lexical overlap={coverage:.2f}; entailment not established", 0.5, "heuristic")
    if coverage <= 0.2:
        return Candidate(claim.id, Disposition.OMITTED,
                         f"Lexical overlap={coverage:.2f}; paraphrase remains possible", 0.35, "heuristic")
    return Candidate(claim.id, Disposition.UNRESOLVED,
                     f"Lexical overlap={coverage:.2f}; requires interpretation", 0.2, "heuristic")


# Pluggable provider: caller owns authentication, prompt safety and evidence quality.
# Provider returns proposed disposition and explanatory evidence, never an approval.
AIProvider = Callable[[str, str], tuple[Disposition, str]]


def detect(claims: list[Claim], rendition: str,
           provider: AIProvider | None = None) -> list[Candidate]:
    if not rendition.strip():
        raise ValueError("Rendition required")
    result = []
    for claim in claims:
        if provider is None:
            result.append(heuristic_candidate(claim, rendition))
        else:
            state, rationale = provider(claim.text, rendition)
            if not isinstance(state, Disposition) or not rationale.strip():
                raise ValueError("AI provider must return a disposition and rationale")
            result.append(Candidate(claim.id, state, rationale, 0.0, "external-ai"))
    return result
