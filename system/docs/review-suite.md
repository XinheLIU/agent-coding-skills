# Code Review

Last updated: 2026-08-02

[System home](../README.md) · [Workflows](../workflows/README.md) · [Organization report](organization-report.md)

This folder defines a technical review system with five complementary skills and a shared subagent fleet. `review-architecture` and `review-code-quality` are the primary review orchestrators; `review-design-doc`, `review-implementation-gaps`, and `analyze-test-gaps` provide focused gates around them.

## TL;DR — Which Skill?

```text
                        Are you judging the system's
                        DESIGN  or  the CODE?
                                |
                ┌───────────────┴───────────────┐
                ▼                               ▼
         design / structure                code as written
       /review-architecture              /review-code-quality
                                                │
                            ready to ship a PR? │ yes
                                                ▼
                                        verdict + next steps
```

- `review-architecture`: intent, boundaries, topology, contracts, and ADR quality.
- `review-code-quality`: concrete defects, maintainability, tests, and merge readiness.
- Cross-skill findings are routed via cross-reference sections, not mixed into the wrong skill.

## MECE Boundary

| Concern | review-architecture | review-code-quality |
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

Rule of thumb: `review-architecture` judges the system design; `review-code-quality` judges the code implementing that design.

## Skill 1: review-architecture

`review-architecture` orchestrates six aspect pairs (`explorer` then `reviewer`) in parallel, then consolidates a design-level report.

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
/review-architecture
  -> choose aspects + scope
  -> run selected explorers in parallel
  -> run paired reviewers in parallel
  -> consolidate + dedupe + rank + cross-reference
  -> write architecture artifact
```

### Architecture Output Artifact

`docs/eng-reviews/review-architecture-<YYYYMMDD-HHMM>.md`

## Skill 2: review-code-quality

`review-code-quality` runs domain review subagents plus a standalone `code-reviewer`, then produces a merge verdict and prioritized next steps.

### Code Quality Scope

- Reviews implementation quality and production-readiness defects.
- Supports three modes:
  - Mode A: recent changes (default).
  - Mode B: whole codebase against specs/rules.
  - Mode C: drill-down from review-architecture output.
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
/review-code-quality
  -> pick mode + scope + domains
  -> run explorers in parallel
  -> run paired reviewers in parallel
  -> run standalone code-reviewer
  -> inline quality pass + coverage diagram + consolidation
  -> verdict: READY | READY-WITH-FIXES | NOT-READY
  -> write next-steps artifact
```

### Code Quality Output Artifact

`docs/eng-reviews/next-steps-<branch>-<YYYYMMDD-HHMM>.md`

## Standalone Agent: tdd-builder

`tdd-builder` is not part of either review pipeline. It is an orchestration agent for new features using strict test-first delivery.

- Sequence: `brainstorm-feature` (when needed) -> `spec` -> `plan` -> `tasks` (tests required).
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
- Reviewer sequencing rule: reviewers must run after explorer outputs exist; sibling reviewers should run in parallel.

## Cross-Skill Handoff

Use cross-reference routing when a finding belongs to the other skill:

- Design-level issue found during `review-code-quality` -> reference `review-architecture` with aspect hint (`business`, `application`, `data`, `technology`, `deploy`, `adr`).
- Code-level issue found during `review-architecture` -> reference `review-code-quality` with domain hint (`api`, `db`, `auth`, `reliability`, `performance`, `security`, `code-reviewer`).

This keeps findings MECE and avoids duplicate or contradictory reporting.

## Shared Rules (DO / DON'T)

```text
DO                                          DON'T
--                                          -----
Dispatch explorers/reviewers in parallel    Run everything sequentially
Pass scoped file lists when restricted      Review outside the requested scope
Preserve file:line anchors and confidence   Paraphrase away evidence
Consolidate before presenting               Dump raw subagent outputs at user
Keep LOW confidence out of Critical         Promote uncertain claims to blockers
Route cross-domain findings via references  File findings on the wrong side
```

## Output Artifacts

| Skill | Artifact path |
|---|---|
| `review-architecture` | `docs/eng-reviews/review-architecture-<YYYYMMDD-HHMM>.md` |
| `review-code-quality` | `docs/eng-reviews/next-steps-<branch>-<YYYYMMDD-HHMM>.md` |

Both artifacts are expected to be self-contained: scope, invoked aspects/domains, evidence-anchored findings, and actionable next steps.

## Pointers

- Skills: `system/skills/`
- Subagents: `system/agents/`
- Runtime copies (if used): `.claude/skills/...`, `.claude/agents/...`
