# IDOS Social Connection Architecture — Integration Note v0.3

**Status:** working, limited integration of earlier implementations (7 November 2026). This note does **not** revise MASTER_MAP v1.1, 12CDP, or the 13-equation research note.

## Research purpose

IDOS aims at a **social connection architecture** that preserves differences and decision rights among heterogeneous intelligences while supporting the emergence of relational distributions and the renewal of what can be explored. It does not select a single answer for all actors.

The question motivating v0.3 is narrower: Can three previously implemented branches of the IDOS repository be **actually coupled in one auditable workflow**, rather than merely mentioned as related concepts?

### Actual connections

**Dynamic Interoperability:** A directional statement is passed to the original `Ledger` with its originating and receiving reference frames, associated trajectories, provenance references and reviewer-declared residual disposition. Unresolved content remains unresolved. This does not establish a shared meaning between two intelligences.

**Discovery Architecture:** A Social Connection frame candidate is linked to the original `DiscoveryCycle` through a reported intervention, an evidence-linked difference, proposal, and later reality recontact. The system keeps observation/proposal/adoption distinct. A reported historical action is not retroactively caused by the system.

**Coexistence Governance:** The original `CoexistenceGovernor` receives proposed actions and evaluates explicit approvals, risk, objections and reversibility. The governance outcome is logged as advice to the separate execution layer; it cannot make another actor adopt an option or cause any external action.

### Invariants being tested

- **Nonidentity and autonomy:** Different reference frames and explicit adopt/hold/reject decisions remain separate.
- **Provenance and temporal integrity:** Shared sources carry attribution and can only be used in the time step they were actually submitted. Private values are excluded from shared snapshots.
- **Relational trace:** Exchange directions, per-actor trajectories and discovery provenance links are recorded without asserting that an autonomous relational subject has been proven to exist.
- **CFV:** Explicit assessment and ability to register an unresolved cross-frame discrepancy—not a declaration of full comprehension or objective truth.
- **MU:** Distinct actors may independently accept or refuse a candidate. There is no evidence yet of meaningful mutual internal updates in real agents.
- **Holding and Reopening:** Alternatives and historical records are retained for later recontact.
- **Reality Contact:** Later observations can be linked to earlier proposals, but causal inference is not guaranteed.
- **Governance:** External execution is not automatic; safety and permission claims remain assertions made by the caller, pending independent verification.

### Non-integration decisions

The existing execution gate, full CDP reference system, relation-analysis aggregate, automatic reference-generation engine and real external connectors are deliberately not folded into the core. Each needs its own interface validation rather than a superficial import. The bridge currently uses the foundational ledger, discovery cycle, and coexistence governor classes **from their original source files**.

### Assessment

The outcome is a **real code-level integration**, not yet an empirically demonstrated social connection. The question for subsequent independent validation is whether this integrated interface changes the way actual heterogeneous actors can maintain verifiability, alternatives, nonidentity and future updateability, as opposed to a normal interoperability, workflow and governance stack with equivalent information.
