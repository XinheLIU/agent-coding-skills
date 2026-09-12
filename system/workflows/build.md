# Build Workflow

Last updated: 2026-09-12

Implement features from settled requirements and engineering design. Produces working code with passing tests and a committed `plan.md` that records the approach before implementation begins.

```
entry_artifact: specs/<spec>.md + DESIGN.md (technical decisions)
exit_artifact:  plan.md (approved approach) + code changes + passing tests + state.md
approval_gate:  User must approve plan.md before implementation; user approves risky changes during implementation
```

## Overview

```
spec + DESIGN.md → analyze → plan-implementation → [USER APPROVES plan.md]
                                                    → break-into-tasks → tdd loop → handoff
```

## Skill Sequence

### 1. Understand the codebase
- `/analyze` — read codebase context, identify affected surfaces, understand existing patterns before touching anything

### 2. Optionally explore approaches
- `/brainstorm-approaches` — when multiple valid implementation paths exist; skip for straightforward changes

### 3. Write the plan
- `/plan-implementation` — read-only pass over codebase + spec + DESIGN.md; write `docs/changes/<change-id>/plan.md`

The plan captures: problem statement, proposed approach (which modules, seams, patterns), ordered implementation steps, verification plan (unit + integration + manual), and risks/alternatives considered.

**User reviews and approves `plan.md` before any code is written.** This is the single approval gate for the whole feature.

### 4. Break into tasks
- `/break-into-tasks` — decompose the approved plan into incremental steps; each step should be independently testable

### 5. Implement with TDD
- `/tdd` — for each task: write failing test → implement minimum code to pass → refactor → repeat

The TDD loop is part of build, not a separate test phase. Unit tests live here. Integration and coverage audits are the test phase's job.

### 6. Hand off
- `/handoff` — write `state.md` recording the current resume point, what was done, deviations from plan, and open items

## Entry Criteria

- `specs/<spec>.md` with complete functional requirements and testable acceptance criteria.
- `DESIGN.md` with module boundaries, interface specs, and ADRs (or explicit note that technical design was skipped and why).
- `docs/agents/memory.md` exists.

## Exit Criteria

- `docs/changes/<change-id>/plan.md` committed to branch, status updated to `implemented`.
- All unit tests pass.
- Deviations from plan are noted in plan.md's "Actual Implementation Notes" section.
- `state.md` written for handoff.

## Handoff

Passes code changes with passing unit tests to `/test`. The test phase audits coverage and adds integration/e2e tests; it does not redo unit tests already written here.

Shared context coordination: [context-coordination.md](context-coordination.md)
