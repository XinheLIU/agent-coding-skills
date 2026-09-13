# Build Workflow

Last updated: 2026-09-13

Implement a locked, verifiable change end-to-end. Starts after the spec phase; produces working code verified on the running system, with evidence.

```
entry_artifact: a verifiable change — spec section, user story, or bug report with acceptance criteria
exit_artifact:  tickets + evidence under docs/changes/<change-id>/ + handoff envelope
approval_gate:  criteria locked before dispatch; user approves ticket graph before parallel execution
```

## Overview

```
locked change → implement: gate → decompose into tickets → render DAG
                → [user sees graph, goes AFK]
                → parallel tdd dispatch via orchestrator → merge in dependency order
                → end-to-end verification → handoff envelope
```

## Skill Sequence

### 1. Enter with a verifiable change
- `/implement` — the single entry point. Gates on acceptance criteria testable at code and experience level. Small gaps get one or two inline questions; real design work routes to `design/`.

### 2. Decompose and visualize
`implement` writes dependency-ordered tickets to `docs/changes/<change-id>/tasks/` and renders the interactive HTML DAG (`draw-portfolio-dag`). The user sees frontier/blocked/done before anything runs.

### 3. Execute in parallel
`implement` dispatches each safe frontier ticket to a `tdd` sub-agent through the orchestration protocol (herdr primary, in-process fallback), merges completed worktrees in dependency order, and re-renders the graph on every transition. Failed tickets keep their dependents blocked; independent work continues.

### 4. Verify end to end
Code-level green is not done: `implement` starts the system the way a user would and exercises the delivered behavior — browser, local run, or integration suite — recording commands and results as evidence.

### 5. Return the envelope
Every run ends with the shared handoff envelope: criterion → ticket → evidence → revision mapping, verification result, failures with blocking effects, next action.

## Entry Criteria

- A canonical change with testable acceptance criteria (existing spec, ticket, or explicit user intent locked through the gate).
- Accepted design/contract references when the change depends on them.

## Exit Criteria

- Every criterion maps to a done ticket with evidence, or an explicit failure/omission with impact.
- End-to-end verification recorded (pass, or failure with evidence).
- Handoff envelope returned; tickets and evidence retained under `docs/changes/<change-id>/`.

## Handoff

Verified code changes go to `quality/review` (Standards and Spec axes) and `/test` for coverage audits and integration/e2e tests. Refactoring beyond the loop's own green-preserving cleanups belongs to `refactor-code`.

Shared context coordination: [context-coordination.md](context-coordination.md)
