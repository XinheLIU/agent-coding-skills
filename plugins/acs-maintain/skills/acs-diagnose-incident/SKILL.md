---
name: acs-diagnose-incident
description: Use when behavior is broken, intermittent, slow, or resistant to an obvious fix.
---

# Diagnose Incident

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [change.symptom]
  retrieves: [change.requirements, system.affected_source, verification.failure_history, operations.environment]
  produces: [change.diagnosis, change.regression_evidence]
  updates: [run.investigation]
  invalidates: [verification.for_changed_code, system.disproved_assumptions]
  handoff_to: [implementation, testing]
```

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.


Read shared memory, relevant domain context, and ADRs. Create or update the active effort’s `diagnosis.md`.

## 1. Build the loop

Produce one agent-runnable command that has already gone red on the user’s exact symptom. Prefer a failing test, then a request/CLI/browser replay, captured trace, throwaway harness, property loop, bisection, or differential check. Tighten it until deterministic and fast. If no red-capable loop is possible, record attempts and request the missing artifact or access.

## 2. Reproduce and minimize

Confirm the right symptom, then remove inputs and steps one at a time until every remaining element is load-bearing.

## 3. Test hypotheses

Write up to three ranked, falsifiable hypotheses and the prediction for each. Change one variable per probe. Record evidence, not narrative guesses. For performance, measure and profile before changing code.

Apply these numbered rules throughout diagnosis and the fix:

1. **Three-strike stop.** After three falsified hypotheses in this investigation, stop probing and present the evidence with options: continue with a proposed new hypothesis, escalate for human review, or instrument and wait for recurrence. Wait for the user's choice before a fourth probe or new instrumentation; do not reset the count by reranking hypotheses.
2. **Directory boundary.** Once a hypothesis forms, record the narrowest directory containing the affected code in `diagnosis.md` and restrict edits to it. Reading outside it is allowed. If evidence requires an edit elsewhere (including a regression test), record the reason and revised narrowest boundary before editing; exclude unrelated cleanup.
3. **Five-file ask.** Before a fix would touch more than five distinct files in total, list the files and rationale and ask whether to proceed, split the fix, or rethink it. Count source, tests, configuration, and instrumentation together, not per probe. Existing explicit approval for that scope persists; otherwise wait before editing a sixth file.
4. **Tagged logs.** Prefix every temporary debug log with a unique investigation tag in the form `[DEBUG-xxxx]` (for example, `[DEBUG-a4f2]`). Record the tag in `diagnosis.md` so cleanup can find every occurrence.

Use the [runtime-debugger recipes](references/runtime-debuggers.md) when a breakpoint can distinguish predictions more directly than logs.

## 4. Fix

Turn the minimized reproduction into a failing regression test at the correct public seam. Apply the smallest fix, rerun the regression, original loop, and project checks.

## 5. Close

Remove temporary instrumentation and search the recorded edit boundary with `rg -n -F '[DEBUG-a4f2]' <directory>` (substitute the recorded tag and directory); verify no temporary tagged logs remain. Record the confirmed cause and verification, return routing updates to the coordinator, and route architectural seam failures to `acs-design-architecture` (missing invariants or failure handling to `acs-design-contracts`). Do not commit unless asked.

## Credit

The stop, scope, and file-count rules adapt gstack `investigate` at `35dd014`; tagged instrumentation adapts Matt Pocock's `diagnosing-bugs` at `49dd158`. These are workflow principles, with no dependency on upstream hooks or tools.
