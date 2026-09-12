# Test Workflow

Last updated: 2026-09-12

Audit test coverage after implementation, add missing integration and end-to-end tests, and verify the full suite is green before deploy.

```
entry_artifact: Code changes with passing unit tests (from build phase)
exit_artifact:  Full test suite passing, coverage report
approval_gate:  Tests must meet coverage threshold before handoff to /deploy
```

## Overview

```
code + unit tests → analyze-test-gaps → add integration/e2e tests → full suite green → /deploy
```

**Note:** Unit tests and TDD happen in the build phase. This phase is for coverage audit and integration tests — do not redo unit-level work here.

## Skill Sequence

### 1. Audit coverage
- `/analyze-test-gaps` — read the implementation, map it against the acceptance criteria in `specs/<spec>.md`, identify gaps: missing integration tests, untested edge cases, missing error path coverage

### 2. Fill gaps
Write integration tests and e2e tests for the gaps identified. These tests exercise multiple components together or verify behavior from the outside.

### 3. Run the full suite
Run all tests (unit + integration + e2e). Every test must be green. A flaky test is a failing test.

### 4. Verify coverage threshold
Check that overall coverage meets the project threshold (default: 80% line coverage for modified files). If the project has no threshold configured, establish one and record it in `docs/agents/memory.md`.

## Entry Criteria

- Code changes on branch with unit tests passing.
- `specs/<spec>.md` available to cross-check acceptance criteria against test coverage.

## Exit Criteria

- Full suite green (unit + integration + e2e).
- Coverage meets threshold for modified files.
- Acceptance criteria from spec have corresponding passing tests.
- No tests skipped without explicit justification.

## Handoff

Passes green test suite and coverage report to `/deploy`.

Shared context coordination: [context-coordination.md](context-coordination.md)
