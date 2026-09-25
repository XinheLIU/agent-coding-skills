# Working / Persistent / Presenter Verification

Last updated: 2026-09-25

Change: implement the user-accepted [Context design](../../docs/context-memory-presenter-proposal.md). This records verification of the working tree, not a release or a claim of host runtime parity. Existing user changes were retained; no commit or deployment was performed.

## Implemented scope

- One canonical protocol home, two memory classes, Persistent Intent/Current/Changes, and a shared Presenter contract.
- All 44 source skills link the shared contracts; contextual report references are consolidated without changing canonical product HTML or prototype formats.
- Proposed records saved before formal review/dependent handoff, version-scoped feedback reconciliation, retrievable exact reviewed content/assets, and a single configured recovery entry.
- Source discovery/resource links repaired; generated packages embed transitive resources and reference procedures without requiring companion plugins.
- Legacy DAG scanning now hashes source bytes and exposes provenance; missing external-manifest revisions are explicitly labelled.

## Structural and executable evidence

Environment: local macOS and Python 3 standard library; no new dependency, service or frontend. Commands below ran against this implementation.

| Check | Result |
| --- | --- |
| `python3 -B system/evals/validate_suite.py` | PASS: 44 source skills, declarations, discovery/catalog inventory, local links and anchors |
| `python3 -B scripts/validate-protocols.py` | PASS: protocol registry plus all 10 generated package closures |
| `python3 -B -m unittest discover -s system/evals/tests -p 'test_*.py' -v` | PASS: 14 inventory/package tests; includes source removal, relocation, repeat-build byte equality, stale generated-directory cleanup, and preservation of unrelated user files |
| `python3 -B -m unittest discover -s system/evals/evals -p 'test_*.py' -v` | PASS: 6 declaration, stable-identity and cleanup-reference tests |
| `python3 -B -m unittest discover -s system/skills-src/authoring/acs-draw-portfolio-dag/tests -p 'test_*.py' -v` | PASS: 6 scan/render tests; these also run from relocated `acs-craft` within the package tests |
| `python3 -B scripts/validate-visual-report.py` | PASS |
| `python3 -B system/skills-src/authoring/scripts/check-visual-report-contract.py` | PASS: 6 consumers |
| `git diff --check` | PASS |

Generation: `python3 -B scripts/build-plugins.py`; isolated generation uses `--output <temporary-directory>`. Existing plugin names and marketplace grouping were preserved. Four existing phase packages were also rebuilt so they do not retain the old Context contract. A default rebuild initially exposed old `acs-context/protocols/` files; cleanup and a regression test now cover that case.

## Independent agent forward exercise

A separate agent followed the actual protocols and context skills in a synthetic EXP-42 fixture. It performed the transitions and produced artifacts; a read-only audit checked the results. The root agent independently followed only the fixture's `AGENTS.md` routing to inspect cold recovery. No production runtime was added to simulate enforcement.

| Scenario | Observed outcome |
| --- | --- |
| Proposal before review | D7 r1, unique rationale, exact prototype HTML and CSS were saved in Persistent Changes before review |
| Scoped acceptance | One D12 contribution retained synthetic feedback F1: accept export interaction r1 only; implementation explicitly denied |
| Replay feedback | Re-reading F1/D12 caused no write or duplicate decision; canonical digest manifest unchanged |
| Cosmetic report edit | Source and decision hashes unchanged |
| Material r2 | Current D7 became proposed / needs review with RF-1; historical r1 acceptance and exact artifacts remained unchanged |
| Delete and rebuild view | Generated HTML removed and rebuilt from canonical records only; no canonical source changed |
| Cold receiver | AGENTS → routing → sole recovery entry resolved D7 r2, historical r1-only acceptance, implementation denial, and next action without reading the report |
| Completed-run cleanup | Scratch moved outside the fixture and original path became unavailable; routing repaired; all five audit groups passed and 46 persistent links/assets resolved |

The receiver's next action was to assess the r2 modal against AC-9 and RF-1. It did not implement: the r2 decision was missing and F1 denied implementation. The exercise completed as a review/handoff run; it did not claim the underlying feature was delivered.

Retained r1 SHA-256 values observed by the audit:

| Artifact | Digest |
| --- | --- |
| Design text | `ab44ccefa7cad2f55d667c14992920d69d019734b858d270d07bed7eb14f3564` |
| Exact reviewed HTML | `b36637ed7ba30d169cfa388dc7eb87a1022e0df2da6b9f8e7ea94e7271b6dd3f` |
| Required CSS | `1705cca2381908e6637de905672f4161fe144199136cf7e2d490033c2536a9db` |
| Rationale | `7264aac0716c5f2655f8120d36c47501cd8be5d8a9e95ce0957041bb4b4b06ea` |

The temporary exercise directory was `/tmp/acs-memory-forward-UZb0Xx`; its raw logs are disposable. This summary retains the outcome and limitations independently of those files. Repeatable prompts are in [context-lifecycle.json](context-lifecycle.json).

## Limits

The forward exercise used synthetic feedback and source/asset checks, not a browser rendering assessment or a real product implementation. It verifies one agent execution of the written protocol, not automatic acceptance enforcement, atomic concurrent writes, all future agents, external trackers, or Codex/Claude/Pi runtime parity. Scenario JSON is a prompt corpus; structural checks do not execute those scenarios. Package checks verify resource availability and exercised scripts, not arbitrary installer behavior.
