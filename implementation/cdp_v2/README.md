# CDP v2.0-draft — reference implementation

**Status:** `[P]` draft proposal. Executable ≠ validated. Synthetic only.

Specification: [`theory/COMMON_DYNAMICS_PROTOCOL_v2.0_DRAFT.md`](../../theory/COMMON_DYNAMICS_PROTOCOL_v2.0_DRAFT.md)
Architecture: [`architecture/IDOS_v2.0_PROTOCOL_ARCHITECTURE_PROPOSAL.md`](../../architecture/IDOS_v2.0_PROTOCOL_ARCHITECTURE_PROPOSAL.md)

## Run

Python 3.9+, standard library only.

```bash
cd implementation/cdp_v2
python -m unittest -v          # 26 conformance tests
python example.py              # three-unit walk-through, prints the audit
```

## Files

| File | Content |
|---|---|
| `cdp2.py` | `Session` (ledger + rules), `slot()`, `commitment()`, `audit()` |
| `test_cdp2.py` | Conformance tests, named after spec rules R1–R25 |
| `example.py` | Human / AI / organisation scenario that triggers seven findings |
| `cdp2.schema.json` | JSON Schema for the envelope and slot |

## Minimal use

```python
from cdp2 import Session, slot

s = Session()
s.hello("human", 0, unit_type="human", frame="narrative",
        min_review_latency=86400, verifies=["evidence_pointer"])
s.hello("ai", 0, unit_type="ai_system", frame="probabilistic",
        min_review_latency=1, verifies=["evidence_pointer", "prediction"])

s.describe("ai", 10, {
    "difference": slot("forecast error tripled", basis="observed"),
    "frame": slot(disclosure="private"),
})
p = s.propose_action("ai", 20, action="cancel contracts",
                     reversibility="irreversible", affected=["human"],
                     review_window=3600)
print(s.audit()["findings"])   # TEMPORAL_INCOMPATIBLE
```

## Boundaries

1. The module **records and reports**. It enforces nothing outside its own ledger.
2. `t` and `sender` are trusted as given. Authenticated identity and trusted time must come from the carrier layer.
3. `audit()` returns bookkeeping over recorded events. The CFV and MU figures are not validated measures of those constructs.
4. The walk-through is built to trigger findings. It is a demonstration of checkability, not evidence of benefit.
5. Standalone by design: it does not import `src/idos_reference_v1_2.py`. A bridge is future work.
6. No network, no model calls, no external service.
