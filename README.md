# Intelligence Dynamics Architecture (IDOS)

**An open, evolving architecture for describing the dynamics of intelligence across humans, AI and organizations.**

> **Intelligence as a Trajectory.** IDOS investigates what changes, how those changes can be observed, and whether the mechanisms of change can themselves change.

**Status (12 October 2026):** architectural research baseline frozen at **[MASTER_MAP v1.1](architecture/MASTER_MAP_v1.1.md)**. The measurement specification is **provisional (v0.3)**. Independent replication, construct validity and superiority over established methods **have not been demonstrated**. This repository is a research and design archive, **not a production-ready or scientifically validated measurement system**.

## Archived Reference (Zenodo)

Master Map v1.1 was frozen on October 2, 2026, and is permanently archived on Zenodo.

**DOI:** https://doi.org/10.5281/zenodo.23311009

## What is IDOS?

Rather than treating intelligence only as a static score or capability, IDOS explores **how intelligent systems change over time**. Its architecture distinguishes:

| Layer | Question | Elements |
|---|---|---|
| **Dynamics** | What changes, in which unit and boundary? | Updating Unit, Dynamic Boundary, Trajectory |
| **Observability** | How can we know what changed? | Reference Frame, Measurement, Provenance |
| **Second-order updateability** | Can the conditions for future change themselves change? | Future Updateability (latent / not directly validated) |
| **Relational capacities** | How can different systems verify and revise one another? | CFV, MU |

Difference is a transition driver; Power and Temporal Compatibility are cross-cutting conditions; Reality Contact provides external grounding. Detailed definitions and the distinction between foundational and derived concepts are in [MASTER_MAP v1.1](architecture/MASTER_MAP_v1.1.md). The 12-process dynamics vocabulary serves as a descriptive/observation framework, **not** a required sequence or a set of universally validated stages.

## Start here — recommended reading order

1. **[MASTER_MAP v1.1](architecture/MASTER_MAP_v1.1.md)** — current frozen architectural baseline and conceptual scope.
2. **[IDOS Purpose and Use v0.2](architecture/IDOS_PURPOSE_AND_USE_CANONICAL_v0.2.md)** — proposed purpose, use and scope.
3. **[Known Limitations](theory/KNOWN_LIMITATIONS.md)** and **[Related Work and Novelty Boundary](theory/RELATED_WORK_AND_NOVELTY_BOUNDARY.md)** — limits, alternatives and novelty boundaries.
4. **[Cross-Case Synthesis v0.1](validation/comparative_cases/CROSS_CASE_SYNTHESIS_v0.1.md)** — illustrative multi-case comparisons; not proof of empirical superiority.
5. **[Measurement & Observability v0.3](measurement/MEASUREMENT_OBSERVABILITY_PROTOCOL_v0.3.md)** — operational measurement *draft* and evidence requirements; not validated as a general instrument.
6. **[Python Reference Implementation v1.1](src/idos_reference_v1_1.py)** — reference code, not a deployed measurement product.

## Repository navigation

| Directory | Contents and evidence status |
|---|---|
| [`architecture/`](architecture/) | Current master architecture and purpose |
| [`theory/`](theory/) | Definitions, theory comparison, documented limitations |
| [`validation/architecture_tests/`](validation/architecture_tests/) | Conceptual/adversarial reduction and architecture testing |
| [`validation/empirical_cases/`](validation/empirical_cases/) | Analysis of present-day cases and sampling; varies by evidence strength |
| [`validation/comparative_cases/`](validation/comparative_cases/) | V-series comparisons and synthesis; additional value not assumed |
| [`validation/future_regimes/`](validation/future_regimes/) | F-series hypothetical/future-regime stress tests, **not observations of the future** |
| [`measurement/`](measurement/) | Measurement protocols, observations and provisional validation records |
| [`implementation/`](implementation/) | Operational design proposals, **not evidence of production deployment** |
| [`src/`](src/) | Python reference code |
| [`figures/`](figures/) | Historical visual materials, version-specific |
| [`archive/`](archive/) | Superseded frozen versions and chronological history (preserved, not deleted) |

Full file-by-file description: [DOCUMENT_INDEX.md](DOCUMENT_INDEX.md).

## What has and has not been established

**Documented design work:** initial architecture, reductions and internal adversarial analyses; qualitative/prospective case analyses; initial evidence-first measurement procedures; reference code.

**Not yet established:** independently reliable identification of Residual, Holding or an emergent Updating Unit; direct estimation of Future Updateability; cross-domain scientific validity; demonstrated incremental decision value against strong standard approaches; a deployed and independently audited system. An `O` or `P` measurement label indicates availability of evidence for a narrowly specified claim, **not the existence or truth of a theoretical construct**.

### Methodology note

Separate (a) observations supported by primary evidence, (b) interpretations of public case studies, (c) synthetic/adversarial tests, and (d) future-regime scenarios. Do not combine them into a single empirical-validation claim. Versioned research documents retain their original judgments and limitations.

## Historical and legal notes

The original [Canonical v1.0](archive/superseded/CANONICAL_v1.0.md) and [MASTER_MAP v1.0](archive/superseded/MASTER_MAP_v1.0.md) remain available as historical versions; they do not override v1.1. The historical [canonical v1.0 diagram](figures/canonical_v1.0.png) is likewise *not* the current architecture.

See [LICENSE](LICENSE) and [LICENSE-DOCS](LICENSE-DOCS) for the repository's respective licensing terms. No license is altered by this directory reorganization.
