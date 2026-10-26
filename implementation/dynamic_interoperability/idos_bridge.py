"""Thin adapter to the real IDOS Reference v1.2 CommonDynamicsProtocol.

Run from repository root. No local reimplementation of Reference or CDP.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
from idos_reference_v1_2 import CommonDynamicsProtocol, UpdatingUnit
from interoperability import Ledger, Claim, Assessment


def exchange_via_cdp(ledger: Ledger, source: UpdatingUnit, target: UpdatingUnit,
                     claims: list[Claim], translated_text: str,
                     assessments: list[Assessment], *, round: int,
                     declared_by: str, previous_exchange_id: str | None = None):
    protocol = CommonDynamicsProtocol()
    src = protocol.describe(source)
    dst = protocol.describe(target)
    partial = protocol.translate(src, target.name)
    # CDP translation is structural/partial. It does not translate the claim text.
    return ledger.record(
        round=round, source_id=src.unit_id, target_id=dst.unit_id,
        source_frame=src.frame_name, target_frame=dst.frame_name,
        source_trajectory=src.trajectory_id, target_trajectory=dst.trajectory_id,
        original=claims, translated=translated_text, assessments=assessments,
        cdp_quality=partial['translation_quality'],
        cdp_residual=partial['translation_residual'],
        declared_by=declared_by, previous_exchange_id=previous_exchange_id)
