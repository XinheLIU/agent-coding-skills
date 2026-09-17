# Quality

Last updated: 2026-09-17

Correctness, clarity, and resilience across delivery. Skills in two lanes that run
throughout the lifecycle, not after it: a review
pipeline (design doc → gap analysis → code quality → corrective refactor), and a debugging
lane (triage → verified fix). `acs-review-code-quality` is the convergence point —
every lane passes through it before code ships.

Note: `acs-tdd` has moved to `build/` — test-driven development is part of the implementation loop, not a separate quality phase. `acs-analyze-test-gaps` has moved to `test/` — coverage audit runs after build, not during. `diagnosing-bugs` has moved to `maintain/acs-diagnose-incident` — incident diagnosis belongs in the maintenance loop. `acs-triage` remains here as a cross-cutting entry point for incoming bug reports.

## The review pipeline

```mermaid
flowchart LR
    subgraph REVIEW["Review pipeline — review/"]
        RDD[acs-review-design-doc] --> RIG[acs-review-implementation-gaps] --> RCQ{acs-review-code-quality}
        RA[acs-review-architecture] <-.->|cross-references| RCQ
        RCQ -->|"READY"| PR([open PR])
        RCQ -->|"fix-ups"| RC[acs-refactor-code] --> RCQ
    end
    subgraph DEBUG["Debugging — debugging/"]
        TRI[acs-triage] --> DX[maintain/acs-diagnose-incident] --> FIX([fix via build]) --> RCQ
    end
    RMC[acs-resolving-merge-conflicts]
```

`acs-review-code-quality` is the gate. It judges a change on two axes — **Standards** (does the code follow this repo's conventions and quality bar?) and **Spec** (does it do what the plan/issue asked?) — reported separately so one axis cannot mask the other, and issues a merge verdict. `acs-review-architecture` is its design-level peer: the two share a MECE boundary table and route findings to each other through an explicit cross-reference channel rather than duplicating them. `acs-resolving-merge-conflicts` is standalone — invoked whenever an in-progress merge or rebase leaves conflict markers.

## Where to start

| You have | Start with |
| --- | --- |
| A design doc, about to start coding | `acs-review-design-doc` |
| A partially implemented plan — "what's left?" | `acs-review-implementation-gaps` |
| Changes to verify before commit / PR — "review my code" | `acs-review-code-quality` |
| A system-level design question (boundaries, topology, ADRs) | `acs-review-architecture` |
| Working code that reads poorly | `acs-refactor-code` — Depth 1, quick polish |
| Structural debt — duplication across files, oversized units | `acs-refactor-code` — Depth 2, gated |
| An incoming bug report to classify | `acs-triage` |
| Conflict markers in an in-progress merge / rebase | `acs-resolving-merge-conflicts` |

`acs-review-code-quality` runs standalone on any diff. `acs-triage` runs standalone on any bug report.

## The skills

### Review (`review/`) — is it built right?

**`acs-review-design-doc`** — plan-stage review before any code exists: scope challenge, architecture and assumption checks, test strategy, completeness. Artifact: `docs/eng-reviews/plan-review-*.md`.

**`acs-review-implementation-gaps`** — compares a design doc to the code and classifies every planned item COMPLETE / PARTIAL / MISSING / DIVERGENT / UNEXPECTED with confidence scores. Its artifact (`docs/eng-reviews/gap-analysis-*.md`) carries a hand-off hint that `acs-review-code-quality` auto-consumes.

**`acs-review-code-quality`** — the production-readiness gate. Orchestrates domain subagent pairs (api, db, auth, reliability, performance, security, code-reviewer) in parallel with an inline fallback, tags every finding Standards or Spec, builds a test-coverage diagram, runs static security greps, and issues a READY / READY-WITH-FIXES / NOT-READY verdict with a prioritized next-steps plan. Three modes: recent changes (default), whole codebase vs spec/rules, drill-down after an architecture review.

**`acs-review-architecture`** — design-level review across business, application, data, technology, deploy, and ADR aspects with its own explorer/reviewer subagent fleet. MECE with `acs-review-code-quality`; findings on the wrong side of the line travel via cross-references.

**`acs-refactor-code`** — the corrective action, behavior-preserving at two depths. Depth 1: quick polish of recently modified code (naming, nesting, redundancy, project style), applied directly and verified by tests. Depth 2: structural refactor (cross-file duplication, pattern application, complexity reduction) with baseline metrics, a ranked proposal the user approves, grouped edits with tests between groups, and a before/after report.

### Debugging (`debugging/`) — initial signal and conflict resolution

**`acs-triage`** — classifies an incoming bug report: severity, scope, reproduction steps, likely owner, and a durable brief for whoever picks it up. Cross-cutting: runs at any lifecycle phase, not just during maintenance.

**`acs-resolving-merge-conflicts`** — resolves in-progress merge/rebase conflicts by reconstructing both sides' intent. Never auto-commits.

Root-cause analysis and the fix loop live in `maintain/acs-diagnose-incident` → `build`. `acs-triage` hands off there after classification.

## Boundaries with other phases

- **TDD and test-first implementation** belong to `build/acs-tdd` — testing during implementation is part of the build loop, not a quality step after it.
- **Coverage audit and integration tests** belong to `test/acs-analyze-test-gaps` — run after build is complete.
- **Root-cause diagnosis** belongs to `maintain/acs-diagnose-incident` — incident analysis feeds the autonomous maintenance loop.
- **Architecture restructuring** belongs to `design/technical/acs-audit-architecture`; `acs-review-architecture` judges the design, it does not redesign it.
- **Requirements** have one canonical source; `build/acs-plan-delivery` references it when planning child tickets; `build/acs-implement` dispatches `build/acs-tdd` to execute ready slices; `acs-review-implementation-gaps` audits against them.

## Typical workflows

**Pre-PR check** — `acs-review-code-quality` alone (Mode A, both axes). The fastest useful entry point.

**Design-through-code review** — `acs-review-design-doc` before coding → `acs-review-implementation-gaps` mid-implementation → `acs-review-code-quality` before merge → `acs-refactor-code` on fix-ups → re-verdict.

**Architecture drill-down** — `acs-review-architecture` flags design issues at specific files → `acs-review-code-quality` Mode C follows up at code level.

**Bug** — `acs-triage` classifies → `maintain/acs-diagnose-incident` finds the cause → fix via `build` → `acs-review-code-quality` before merge.
