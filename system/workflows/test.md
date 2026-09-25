# Test Workflow

Last updated: 2026-09-25

Audit test coverage after implementation, add missing integration and end-to-end tests, and verify the full suite is green before deploy.

```
entry_artifact: Code changes with passing unit tests (from build phase)
exit_artifact:  Full test suite passing, coverage report
approval_gate:  Tests must meet coverage threshold before handoff to deploy
```

## Overview

```
code + unit tests → acs-analyze-test-gaps → add integration/e2e tests → full suite green → deploy
```

**Note:** Unit tests and TDD happen in the build phase. This phase is for coverage audit and integration tests — do not redo unit-level work here.

## Skill Sequence

### 1. Audit coverage
- `/acs-analyze-test-gaps` — read the implementation, map it against the acceptance criteria in `specs/<spec>.md`, identify gaps: missing integration tests, untested edge cases, missing error path coverage

### 2. Fill gaps
Write integration tests and e2e tests for the gaps identified. These tests exercise multiple components together or verify behavior from the outside.

### 3. Run the full suite
Run all tests (unit + integration + e2e). Every test must be green. A flaky test is a failing test.

### 4. Verify coverage threshold
Check any established project threshold and retain its source reference. Criterion coverage and executed evidence determine readiness; a percentage cannot replace missing acceptance checks. Record unknown expectations without inventing a threshold in the routing configuration.

## Entry Criteria

- Code changes on branch with unit tests passing.
- `specs/<spec>.md` available to cross-check acceptance criteria against test coverage.

## Exit Criteria

- Full suite green (unit + integration + e2e).
- Coverage meets threshold for modified files.
- Acceptance criteria from spec have corresponding passing tests.
- No tests skipped without explicit justification.

## Handoff

Retain criterion → check → result mappings, consumed requirement/design revisions, code/diff identity, environment/configuration, failures, skips and omissions in Persistent Memory under the [engineering evidence contract](../protocols/engineering-memory.md). Raw logs remain Working Memory after unique evidence is retained.

Return canonical references and scoped readiness to the coordinator; deployment also requires artifact identity and authorization. The [Presenter](../protocols/presenter.md) may organize a human report from the retained evidence. The report is not a second verification record.

Shared context coordination: [context-coordination.md](context-coordination.md)
