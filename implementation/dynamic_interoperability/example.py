"""Run from repository root. AI-provider examples are intentionally not mocked as real AI."""
from idos_reference_v1_2 import make_unit
from idos_bridge import exchange_via_cdp
from interoperability import Ledger, Claim
from semantic_detection import detect
from relation_analysis import analyze

human = make_unit("Human", "human", "Future choices")
ai = make_unit("AI", "ai", "Efficiency")
ledger = Ledger()
claims = [Claim("c1", "Reduce routine decision time", "human", human.frame.name),
          Claim("c2", "Never remove human override", "human", human.frame.name)]
rendition = "Reduce routine decision time"
candidates = detect(claims, rendition)
exchange_via_cdp(ledger, human, ai, claims, rendition,
                 [c.to_assessment() for c in candidates], round=1,
                 declared_by="automated-candidate-only")
for item in candidates:
    print(item.claim_id, item.proposed.value, item.method, item.rationale)
for report in analyze(ledger):
    print("Observed directional report:", report)
print("No semantic conclusion was automatically certified.")
