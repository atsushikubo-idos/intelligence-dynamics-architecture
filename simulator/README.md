# IDOS Living Common Map — Research Preview v0.49

**Status:** Experimental software artifact · synthetic only · noncanonical · no empirical validation.

> **IDOS is an architecture for observing a world in which even the questions and purposes underlying AI-generated answers may change.**

**Implementation metaphor:** A living common map that connects changes in heterogeneous intelligences without erasing their differences.

## Scope and motivation

The IDOS research program investigates a dynamic common protocol for heterogeneous updating units (human, AI, organization and hypothetical future intelligences) and the question **“After a system changes, can it still change again?”** This prototype makes selected interactions, relations and changes inspectable as a time-indexed synthetic trace. It does not claim discovery of universal laws or actual prediction of future purposes.

## Six retained characteristics

1. Dynamic common protocol among heterogeneous intelligences.
2. Connection without erasure of differences or sovereignty.
3. Reference frames and update rules may themselves change.
4. Retention of unresolved residuals.
5. Future Updateability as an explicit research question.
6. Contact with Reality as a required conceptual boundary.

## Run

Open **[index.html](index.html)** in a modern browser. The HTML uses local JavaScript assets; no account, server, network or API key is required.

1. Choose **Adaptive interaction**, **Boundary / blocked contact**, or **Withheld observation**.
2. Click **Run experiment**. Navigate the time slider and select any of the five units on the map.
3. Inspect the changing six illustrative axes, update-rule values, relations, event audit and residual statements.
4. Use **Compare assumptions** to compare two *externally specified* feedback configurations with the same events.
5. Use **Run scoped checks**. The current release targets **42 bounded software assertions**; compare the report against the included fixture.
6. Click **Export audit JSON** to obtain the synthetic trace and optional test/comparison data.

**Important distinction:** The six radar axes are *presentation choices*, not the six canonical IDOS characteristics. Question/purpose/criterion text is a labeled illustrative annotation; it is not an inference of an agent's internal state. The feedback toggle does not represent measured changes in purpose.

## What is implemented

- Five distinct synthetic units, including a fallible observer and hypothetical ASI.
- Consent-aware proposals, observations, boundary constraints, contacts and synthetic recontact using the v0.37/v0.38 transition kernel.
- Playback of the same deterministic event history on a living common map.
- Read-only display of illustrative questions/purposes/criteria, reference axes and update rules.
- Historical event/audit entries, synthetic provenance, and preserved residual descriptions.
- An **exploratory six-field canonical mapping**, without claims of conformance certification.
- Comparison of explicit feedback assumptions; unchanged-input deterministic control.
- Manual Path Closure questions and explicit `unknown`/`unmeasured` status for Future Updateability.
- Browser-side export and bounded regression checks.

## Scope of the English release

This **focused English interface** reuses the original experimental v0.37/v0.38 kernels and preserves their transition behavior. It does **not** implement all of the historical Japanese v0.1–v0.49 UI panels. It is not a comprehensive translation of the original 467 KB HTML file. The previous v0.49 Japanese prototype remains a separate development artifact. Historical 42/42 checks and the present English 42/42 checks have different test scopes and should not be presented as identical validation.

## Research boundaries

Read [Scope and limitations](docs/SCOPE_AND_LIMITATIONS.md), [canonical mapping](docs/CANONICAL_MAPPING.md), and [validation method](validation/TEST_INSTRUCTIONS.md) before reusing or citing the software.

The frozen source documents **MASTER MAP v1.1**, **IDOS Purpose and Use Canonical v0.2**, and **CDP v1.0** are *not amended by this software*. CDP v2.0 is a separate research draft. No numerical model parameters are claimed to have been derived from canonical definitions.

## File overview

```text
simulator/
  index.html                    English interactive interface
  assets/core.js               Extracted/translated experimental v0.37/v0.38 kernel
  assets/app.js                English release UI and 42 scoped checks
  fixtures/scenario_index.json Synthetic scenario catalog
  docs/CANONICAL_MAPPING.md    Definition-to-view mapping and caveats
  docs/SCOPE_AND_LIMITATIONS.md Research and implementation boundaries
  validation/TEST_INSTRUCTIONS.md
  validation/browser_test_report.json
  manifest.json                Exact file hashes and release status
```

## Citation / publication status

Research preview v0.49, dated 2026-11-19. Publication on GitHub and registration on Zenodo are **not** implied by these files. Add the Git commit identifier and a Zenodo DOI only after those actions actually occur.

Author: Atsushi Kubo (IDOS / Intelligence Dynamics Architecture).

Repository: https://github.com/atsushikubo-idos/intelligence-dynamics-architecture

Existing architectural reference: https://doi.org/10.5281/zenodo.23311009
