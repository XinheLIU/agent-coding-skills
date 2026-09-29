# Code Review

Last updated: 2026-09-29

[System home](../README.md) · [Workflows](../workflows/README.md)

This folder defines a technical review system with two levels. Each level is a skill that carries its own lenses; there are no separate agent prompts.

- **Design level.** The technical design aspect cards (`acs-technical-design` router plus ARC, MOD, CON, TST and TRC) each review one aspect and write findings into one record, `docs/design/technical-design.md`, with a single ledger.
- **Code level.** `acs-review-code-quality` judges the code as written and produces a merge verdict.

The shared coordinator owns runtime orchestration. The gate chain from plan to merge verdict is `acs-technical-design` (review mode) → `acs-trace-requirements` (post-build) → `acs-review-code-quality`. `acs-analyze-test-gaps` audits whole-codebase test adequacy, and `acs-refactor-code` is the corrective follow-up. `acs-tdd` enters at the trace step; it routes its spec and quality reviews here rather than embedding its own reviewers.

## TL;DR — Which Skill?

```text
                        Are you judging the system's
                        DESIGN  or  the CODE?
                                |
                ┌───────────────┴───────────────┐
                ▼                               ▼
         design / structure                code as written
       /acs-technical-design                /acs-review-code-quality
        (ARC MOD CON TST TRC cards)             │
                            ready to ship a PR? │ yes
                                                ▼
                                        verdict + next steps
```

- Design cards: system shape and decisions (ARC), module boundaries (MOD), contracts and failure semantics (CON), test strategy (TST), and requirement reachability (TRC).
- `acs-review-code-quality`: concrete defects, maintainability, tests, and merge readiness.
- Cross-level findings are routed, not mixed into the wrong skill.

## MECE Boundary

| Concern | Design card | acs-review-code-quality |
|---|---|---|
| Business intent, personas, golden paths | ARC | No |
| Module decomposition, layering, runtime ownership | ARC / MOD | No |
| Data layering, ownership, lineage | ARC | No |
| Technology choice fit and scaling cliffs | ARC | No |
| Deploy topology, trust boundaries, exposure model | ARC | No |
| ADR discipline and decision drift | ARC | No |
| Invariants, API evolution, error and failure semantics | CON | No |
| Test layers, seams, gates (before code) | TST | No |
| Requirement → code reachability | TRC | Spec axis reuses TRC rows |
| Endpoint validation and error-envelope correctness | No | Yes |
| SQL/query correctness and DB safety defects | No | Yes |
| Code-level auth and authorization bugs | No | Yes |
| Reliability implementation bugs (timeouts/retries/shutdown) | No | Yes |
| Performance implementation smells | No | Yes |
| App security implementation bugs | No | Yes |
| Test quality, code complexity, maintainability smells | No | Yes |

Rule of thumb: the design cards judge the system design; `acs-review-code-quality` judges the code implementing it.

## Level 1: Technical design cards

`acs-technical-design` challenges scope, picks cards, and consolidates the ledger into a verdict (READY TO BUILD / NEEDS REVISION / AT RISK). Each card also runs alone. See [design/technical](../skills-src/design/technical/README.md).

### Architecture deep mode

`acs-design-architecture` applies six lenses for a whole-system review: `business`, `application`, `data`, `technology`, `deploy` and `adr`. Each lens maps the system first, then judges it. The checklists live in the skill's [architecture-lenses.md](../skills-src/design/technical/acs-design-architecture/references/architecture-lenses.md). A lens runs inline, or as a delegated task when the coordinator allows it; either way, its findings become `FND-ARC` ledger rows with anchors and confidence kept verbatim.

### Design output

`docs/design/technical-design.md` (sections plus the findings ledger) and its derived view, `docs/design/technical-design.html`.

## Level 2: acs-review-code-quality

`acs-review-code-quality` applies seven domain lenses plus an inline quality pass, then produces a merge verdict and prioritized next steps.

### Code Quality Scope

- Reviews implementation quality and production-readiness defects.
- Tags every finding on two axes — **Standards** (code vs the repo's documented conventions and quality bar, fed by the domain lenses and inline pass) and **Spec** (code vs what the plan/issue asked for, fed by a spec-fidelity pass against a located spec source) — reported separately, never reranked against each other. Finding format: `[P0|P1|P2] [Standards|Spec] (confidence: N/10) file:line — description`.
- Supports three modes:
  - Mode A: recent changes (default).
  - Mode B: whole codebase against specs/rules.
  - Mode C: drill-down from open `FND-ARC` ledger rows.
- Always includes consolidation, confidence calibration, test-coverage gap analysis, and verdicting.

### Domain lenses

| Lens | What it catches |
|---|---|
| `api` | Endpoint contract issues, boundary validation gaps, error envelope/status misuse |
| `db` | Schema integrity risks, SQL safety defects, migration and DB-level performance issues |
| `auth` | Auth flow flaws, token/session weaknesses, authorization bypass risks |
| `reliability` | Missing timeouts/retries, weak degradation, observability and lifecycle gaps |
| `performance` | Cache/pool/concurrency/scaling and memory pressure risks |
| `security` | Secrets, crypto posture, audit/PII handling, supply-chain and non-API injection sinks |
| `code` | Cyclomatic complexity, test quality, code smells, FIRST/AAA, test pyramid health |

The checklists live in the skill's [domain-lenses.md](../skills-src/test/review/acs-review-code-quality/references/domain-lenses.md).

### Code Quality Pipeline

```text
/acs-review-code-quality
  -> pick mode + scope + domains + spec source
  -> apply domain lenses (inline, or delegated when allowed)
  -> inline quality pass + spec-fidelity pass (Spec axis) + coverage diagram + consolidation
  -> verdict: READY | READY-WITH-FIXES | NOT-READY
  -> write next-steps artifact
```

### Code Quality Output Artifact

`docs/eng-reviews/next-steps-<branch>-<YYYYMMDD-HHMM>.md`

### Retired: request-code-review

The former `request-code-review` skill (pre-commit verification pipeline) is folded into `acs-review-code-quality`: its pre-commit triggers ("verify my changes", "review before commit/merge") and its static security greps now live there. Its auto-fix loop, stash-based test baseline, and auto-commit behavior were dropped by design — this system never commits without explicit user authority.

## Lens Contract

Every lens in both skills follows the same two steps:

```text
map    — record what exists in scope with file:line anchors; no severity; may be NOT DETECTED
judge  — apply the lens checks; assign severity and confidence (HIGH / MEDIUM / LOW);
         route out-of-scope issues as cross-references
```

A lens runs inline by default. When the coordinator allows delegation, a lens may run as a delegated task whose whole instruction is that lens's section of the reference file. Test-first feature delivery is `acs-implement` with `acs-tdd`, not a review lens.

## Cross-Skill Handoff

Use cross-reference routing when a finding belongs to the other level:

- Design-level issue found during `acs-review-code-quality` -> reference the owning card (`ARC` with lens hint `business`, `application`, `data`, `technology`, `deploy`, `adr`; or `MOD`, `CON`, `TST`).
- Code-level issue found by a design card -> ledger row with status `routed` to `acs-review-code-quality` with domain hint (`api`, `db`, `auth`, `reliability`, `performance`, `security`, `code`).

This keeps findings MECE and avoids duplicate or contradictory reporting.

## Shared Rules (DO / DON'T)

```text
DO                                          DON'T
--                                          -----
Use coordinator-selected execution          Require unavailable delegation
Pass scoped file lists when restricted      Review outside the requested scope
Preserve file:line anchors and confidence   Paraphrase away evidence
Consolidate before presenting               Dump raw lens outputs at user   
Keep LOW confidence out of Critical         Promote uncertain claims to blockers
Route cross-domain findings via references  File findings on the wrong side
```

## Output Artifacts

| Skill | Artifact path |
|---|---|
| Technical design cards | `docs/design/technical-design.md` + `.html` view |
| `acs-review-code-quality` | `docs/eng-reviews/next-steps-<branch>-<YYYYMMDD-HHMM>.md` |

Preserve established artifact homes; new local change evidence defaults to `docs/changes/<change-id>/verification/`. Each report includes canonical change/task, criterion/contract references, consumed revisions, environment assumptions, failures/omissions, and actionable next steps. Standards and Spec verdicts remain separate. Use the [shared handoff envelope](../protocols/skill-declarations.md#handoff-envelope) and [coordinator](../workflows/context-coordination.md).

## Pointers

- Skills: `system/skills/`
- Lens checklists: each skill's `references/` folder
- Runtime copies (if used): `.claude/skills/...`
