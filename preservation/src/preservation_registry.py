"""IDOS primary-source fidelity registry — no ontology reduction, no transition simulator.

The sources, not this index, are authoritative. This software does not infer that
an unrecorded phenomenon is absent; no hypothesis is treated as a verified fact.
"""
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class SourceEvidence:
    source_path: str
    digest_sha256: str
    source_type: str
    epistemic_status: str  # direct_original | secondary_audit | interpretation | unresolved


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_areas() -> dict:
    return json.loads((ROOT / "metadata/five_areas_index.json").read_text(encoding="utf-8"))


def read_primary_ledger_exact(filename: str) -> bytes:
    """Returns verbatim UTF-8 bytes. Never normalizes or summarizes them."""
    base = ROOT / "primary_ledgers"
    path = base / filename
    if not path.is_file() or path.parent.resolve() != base.resolve():
        raise FileNotFoundError(filename)
    return path.read_bytes()


def validate_primary_image_zip(archive: str | Path) -> list[str]:
    """Hashes all 183 original PNGs, detects mismatch; no modification."""
    expected = json.loads((ROOT / "metadata/original_183_images_sha256.json").read_text(encoding="utf-8"))
    errors=[]
    with zipfile.ZipFile(archive) as z:
        present=set(z.namelist())
        for e in expected:
            if e['file'] not in present:
                errors.append('MISSING ' + e['file'])
            elif sha256_bytes(z.read(e['file'])) != e['sha256']:
                errors.append('MISMATCH ' + e['file'])
    return errors


def search_ledger_exact(phrase: str) -> list[tuple[str,int,str]]:
    """Find source context; never asserts conceptual equivalence."""
    results=[]
    for p in sorted((ROOT / 'primary_ledgers').glob('*.md')):
        for line_number,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
            if phrase in line:
                results.append((p.name,line_number,line))
    return results


def describe_distinctions(area_key: str) -> list[str]:
    """Index aid only; not replacements for the diagrams/ledgers."""
    return get_areas()[area_key]['distinctions']
