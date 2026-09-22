# acs-test

ACS test phase plugin — test coverage, code and architecture review, and debugging.

## Purpose

This plugin bundles the skills and specialist agents needed to verify, review, and debug a codebase. It operates after implementation (`acs-build`) and requires only `acs-context` as a runtime dependency.

The core workflow is: identify gaps → review quality → debug and resolve issues.

## Installation

```bash
npm install acs-context
npm install acs-test
```

## Workflow

```
acs-init-context
    └─► acs-analyze-test-gaps       # Are the right things tested?
            └─► acs-review-code-quality    # Is the code production-ready?
                    └─► acs-review-architecture    # Is the design sound?
                            └─► acs-triage / acs-resolving-merge-conflicts
```

For a design that is partway implemented, run `acs-review-implementation-gaps` first to get a gap map, then pipe into `acs-review-code-quality`.

## Skill Inventory

### Coverage (1 skill)

| Skill | Trigger phrases |
|-------|----------------|
| `acs-analyze-test-gaps` | "audit our tests", "test gap analysis", "what tests are missing", "test health check", "review test coverage by business flow" |

### Review (5 skills)

| Skill | Trigger phrases |
|-------|----------------|
| `acs-review-code-quality` | "review my code", "code review", "review this PR", "ready for PR?", "review before commit" |
| `acs-review-architecture` | "architecture review", "arch review", "audit architecture", "review the design" |
| `acs-review-design-doc` | "review the plan", "review my DESIGN.md", "check my design doc", "is the plan ready" |
| `acs-review-implementation-gaps` | "what's left to do", "gap analysis", "am I done with the plan", "compare code to the plan" |
| `acs-refactor-code` | "refactor", "simplify", "polish", "clean up what I just wrote", "reduce duplication" |

### Debugging (2 skills)

| Skill | Trigger phrases |
|-------|----------------|
| `acs-triage` | unlabeled issues, needs-info follow-up, selecting agent-ready work |
| `acs-resolving-merge-conflicts` | active Git merge/rebase conflict markers |

## Bundled Specialist Agents (17)

These agents live in `shared/agents/` and are orchestrated by `acs-review-code-quality` and `acs-review-architecture`.

| Agent | Domain |
|-------|--------|
| `code-reviewer.md` | General code quality, diff-level test scoring |
| `auth-explorer.md` / `auth-reviewer.md` | Authentication and authorization |
| `performance-explorer.md` / `performance-reviewer.md` | Performance hotspots and profiling |
| `reliability-explorer.md` / `reliability-reviewer.md` | Error handling, retries, SLO compliance |
| `db-explorer.md` / `db-reviewer.md` | Query quality, schema, migrations |
| `api-explorer.md` / `api-reviewer.md` | API contracts, versioning, error responses |
| `deploy-explorer.md` / `deploy-reviewer.md` | Deployment config, infra, health checks |
| `security-explorer.md` / `security-reviewer.md` | Security vulnerabilities, secrets, input validation |
| `business-explorer.md` / `business-reviewer.md` | Business logic correctness, domain rules |

## Bundled Workflows

- `shared/workflows/testing.md` — test strategy and coverage guidance
- `shared/workflows/debugging.md` — structured debugging approach

## Dependencies

- **Required**: `acs-context ^0.4.0` — provides `acs-init-context` and the shared context protocol
- **Peer**: `acs-build ^0.4.0` — implementation context consumed by review skills when present
