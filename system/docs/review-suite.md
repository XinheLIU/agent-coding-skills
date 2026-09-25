# Code Review

Last updated: 2026-09-25

[System home](../README.md) · [Workflows](../workflows/README.md)

This folder defines a technical review system with two primary orchestrators and a shared subagent fleet. `acs-review-architecture` and `acs-review-code-quality` own domain review reasoning while the shared coordinator owns runtime orchestration; the gate chain `acs-review-design-doc → acs-review-implementation-gaps → acs-review-code-quality` runs a change from plan to merge verdict, `acs-analyze-test-gaps` audits whole-codebase test adequacy, and `acs-refactor-code` is the corrective follow-up that acts on findings. `acs-tdd` enters this pipeline at gap-review — it routes its spec and quality reviews here rather than embedding its own reviewers.

## TL;DR — Which Skill?

```text
                        Are you judging the system's
                        DESIGN  or  the CODE?
                                |
                ┌───────────────┴───────────────┐
                ▼                               ▼
         design / structure                code as written
       /acs-review-architecture              /acs-review-code-quality
                                                │
                            ready to ship a PR? │ yes
                                                ▼
                                        verdict + next steps
```

- `acs-review-architecture`: intent, boundaries, topology, contracts, and ADR quality.
- `acs-review-code-quality`: concrete defects, maintainability, tests, and merge readiness.
- Cross-skill findings are routed via cross-reference sections, not mixed into the wrong skill.

## MECE Boundary

| Concern | acs-review-architecture | acs-review-code-quality |
|---|---|---|
| Business intent, personas, golden paths | Yes | No |
| Module decomposition, layering, runtime ownership | Yes | No |
| Data layering, ownership, lineage, contracts | Yes | No |
| Technology choice fit and scaling cliffs | Yes | No |
| Deploy topology, trust boundaries, exposure model | Yes | No |
| ADR discipline and decision drift | Yes | No |
| Endpoint validation and error-envelope correctness | No | Yes |
| SQL/query correctness and DB safety defects | No | Yes |
| Code-level auth and authorization bugs | No | Yes |
| Reliability implementation bugs (timeouts/retries/shutdown) | No | Yes |
| Performance implementation smells | No | Yes |
| App security implementation bugs | No | Yes |
| Test quality, code complexity, maintainability smells | No | Yes |

Rule of thumb: `acs-review-architecture` judges the system design; `acs-review-code-quality` judges the code implementing that design.

## Skill 1: acs-review-architecture

`acs-review-architecture` proposes relevant aspect pairs (`explorer` then `reviewer`) and consolidates a design-level report. The coordinator handles authorized delegation or inline execution.

### Architecture Scope

- Reviews design quality across business, application, data, technology, deploy, and ADR aspects.
- Supports whole codebase and narrowed scopes (subtree, commit ranges, branch diff, working tree, custom file list).
- Produces a single consolidated artifact with executive summary, aspect scorecard, cross-aspect findings, and ADR ledger.

### Aspect subagents

| Aspect | Explorer | Reviewer | What it answers |
|---|---|---|---|
| `business` | `business-explorer` (haiku, `Read`/`Grep`/`Glob`) | `business-reviewer` (sonnet, `Read`/`Grep`, plan mode) | Mission-to-implementation alignment, persona coverage, golden path completeness |
| `application` | `application-explorer` | `application-reviewer` | Module decomposition, layer discipline, contract stability, topology coherence |
| `data` | `data-architecture-explorer` | `data-architecture-reviewer` | Schema ownership, ODS/DWD/APP layering, lineage integrity, dataset contract health |
| `technology` | `technology-explorer` | `technology-reviewer` | Stack fit vs workload, scaling cliffs, observability posture, dependency risk |
| `deploy` | `deploy-explorer` | `deploy-reviewer` | Compose topology, network trust boundaries, env-var contracts, prod/dev variant fit |
| `adr` | `adr-explorer` | `adr-reviewer` | Decision inventory and status: Sound, Reconsider, Missing-but-needed, Drifted, Stale |

### Architecture Pipeline

```text
/acs-review-architecture
  -> choose aspects + scope
  -> run selected explorers in parallel
  -> run paired reviewers in parallel
  -> consolidate + dedupe + rank + cross-reference
  -> write architecture artifact
```

### Architecture Output Artifact

`docs/eng-reviews/review-architecture-<YYYYMMDD-HHMM>.md`

## Skill 2: acs-review-code-quality

`acs-review-code-quality` runs domain review subagents plus a standalone `code-reviewer`, then produces a merge verdict and prioritized next steps.

### Code Quality Scope

- Reviews implementation quality and production-readiness defects.
- Tags every finding on two axes — **Standards** (code vs the repo's documented conventions and quality bar, fed by the domain subagents and inline pass) and **Spec** (code vs what the plan/issue asked for, fed by a spec-fidelity pass against a located spec source) — reported separately, never reranked against each other. Finding format: `[P0|P1|P2] [Standards|Spec] (confidence: N/10) file:line — description`.
- Supports three modes:
  - Mode A: recent changes (default).
  - Mode B: whole codebase against specs/rules.
  - Mode C: drill-down from acs-review-architecture output.
- Always includes consolidation, confidence calibration, test-coverage gap analysis, and verdicting.

### Domain subagents

| Domain | Explorer | Reviewer | What it catches |
|---|---|---|---|
| `api` | `api-explorer` (haiku) | `api-reviewer` (sonnet, plan mode) | Endpoint contract issues, boundary validation gaps, error envelope/status misuse |
| `db` | `db-explorer` | `db-reviewer` | Schema integrity risks, SQL safety defects, migration and DB-level performance issues |
| `auth` | `auth-explorer` | `auth-reviewer` | Auth flow flaws, token/session weaknesses, authorization bypass risks |
| `reliability` | `reliability-explorer` | `reliability-reviewer` | Missing timeouts/retries, weak degradation, observability and lifecycle gaps |
| `performance` | `performance-explorer` | `performance-reviewer` | Cache/pool/concurrency/scaling and memory pressure risks |
| `security` | `security-explorer` | `security-reviewer` | Secrets, crypto posture, audit/PII handling, supply-chain and non-API injection sinks |
| code quality | *(no explorer)* | `code-reviewer` (sonnet, plan mode, includes `Bash`) | Cyclomatic complexity, test quality, code smells, FIRST/AAA, test pyramid health |

### Code Quality Pipeline

```text
/acs-review-code-quality
  -> pick mode + scope + domains + spec source
  -> run explorers in parallel
  -> run paired reviewers in parallel
  -> run standalone code-reviewer
  -> inline quality pass + spec-fidelity pass (Spec axis) + coverage diagram + consolidation
  -> verdict: READY | READY-WITH-FIXES | NOT-READY
  -> write next-steps artifact
```

### Code Quality Output Artifact

`docs/eng-reviews/next-steps-<branch>-<YYYYMMDD-HHMM>.md`

### Retired: request-code-review

The former `request-code-review` skill (pre-commit verification pipeline) is folded into `acs-review-code-quality`: its pre-commit triggers ("verify my changes", "review before commit/merge") and its static security greps now live there. Its auto-fix loop, stash-based test baseline, and auto-commit behavior were dropped by design — this system never commits without explicit user authority.

## Standalone Agent: tdd-builder

`tdd-builder` is not part of either review pipeline. It is an orchestration agent for new features using strict test-first delivery.

- Sequence: `acs-brainstorm` (when needed) → `acs-settle-requirements` (reuse canonical requirements) → `acs-plan-delivery` → `acs-implement` / `acs-tdd` (criterion-based execution). The coordinator selects verified host capabilities or executes serially.
- Optional execution loop: red -> green -> refactor.
- Enforces story-by-story progression and blocks code-before-test behavior.

## Shared Subagent Contract

Most domains follow the same two-stage contract:

```text
<domain>-explorer
  - maps scope and emits structured domain context
  - no severity assignment
  - can return Status: NOT DETECTED

<domain>-reviewer
  - requires explorer output as first input
  - emits Critical / Warning / Suggestion findings
  - assigns Confidence (HIGH / MEDIUM / LOW)
  - routes out-of-scope issues via cross-reference recommendations
```

Operational defaults:

- Explorers: haiku, typically `Read` + `Grep` + `Glob`.
- Reviewers: sonnet, `Read` + `Grep`, plan permission mode, read-only posture.
- Reviewer sequencing rule: reviewers consume available explorer evidence; the coordinator selects parallel or inline execution based on authorization and capability.

## Cross-Skill Handoff

Use cross-reference routing when a finding belongs to the other skill:

- Design-level issue found during `acs-review-code-quality` -> reference `acs-review-architecture` with aspect hint (`business`, `application`, `data`, `technology`, `deploy`, `adr`).
- Code-level issue found during `acs-review-architecture` -> reference `acs-review-code-quality` with domain hint (`api`, `db`, `auth`, `reliability`, `performance`, `security`, `code-reviewer`).

This keeps findings MECE and avoids duplicate or contradictory reporting.

## Shared Rules (DO / DON'T)

```text
DO                                          DON'T
--                                          -----
Use coordinator-selected execution          Require unavailable delegation
Pass scoped file lists when restricted      Review outside the requested scope
Preserve file:line anchors and confidence   Paraphrase away evidence
Consolidate before presenting               Dump raw subagent outputs at user
Keep LOW confidence out of Critical         Promote uncertain claims to blockers
Route cross-domain findings via references  File findings on the wrong side
```

## Output Artifacts

| Skill | Artifact path |
|---|---|
| `acs-review-architecture` | `docs/eng-reviews/review-architecture-<YYYYMMDD-HHMM>.md` |
| `acs-review-code-quality` | `docs/eng-reviews/next-steps-<branch>-<YYYYMMDD-HHMM>.md` |

Preserve established artifact homes; new local change evidence defaults to `docs/changes/<change-id>/verification/`. Each report includes canonical change/task, criterion/contract references, consumed revisions, environment assumptions, failures/omissions, and actionable next steps. Standards and Spec verdicts remain separate. Use the [shared handoff envelope](../protocols/skill-declarations.md#handoff-envelope) and [coordinator](../workflows/context-coordination.md).

## Pointers

- Skills: `system/skills/`
- Subagents: `system/agents/`
- Runtime copies (if used): `.claude/skills/...`, `.claude/agents/...`
