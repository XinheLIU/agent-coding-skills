---
name: acs-analyze-test-gaps
description: Use when business-critical flows may lack adequate tests, test health is uncertain, or a refactor needs a test safety assessment.
---

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [verification.expected_behavior]
  retrieves: [change.requirements, design.contracts, verification.test_strategy, source.changed_code, verification.failure_history, operations.environment]
  produces: [verification.criteria_coverage, verification.gap_findings]
  updates: [change.verification_evidence]
  invalidates: [verification.unsupported_readiness]
  handoff_to: [testing, refactoring, implementation]
```

[Shared semantics](../../../docs/shared-semantics.md#execution)

# Test Gap Analyzer

## Procedure

1. **Identify critical business paths.** Read criteria/contracts/TST paths+layers, source/diff revision, failure history, environment/instructions. Summaries are optional; source/schemas/tests/config establish facts. Rank blast radius × change/refactor exposure; ≤8, never pad. Each crosses service boundary or DB write: entry/nodes/success/business risk/exposure/criterion IDs+revisions. Unclear success → drop/ask, never invent.
2. **Map existing tests statically.** Count unit/integration/E2E by behavior, not folder. Inspect assertions. Covered = meaningful full flow; Partial = fragments/weak assertions; Not covered = none. Flag coverage theater/trivial getter/framework tests, E2E-only logic (push down), unit-only cross-service flows (push up). Percent coverage never proves flow protection.
3. **Run standard tests once.** Resolve command from config; ask once if ambiguous. Capture command/timestamp/timezone/environment/runtime/pass/fail/skips/failures. Classify with evidence: code bug → test broken → environment suspicion order. No fix/retry. Green requires all required checks pass, no blocking omissions/floor findings; Yellow incomplete/uncertain (unavailable floor too); Red required failure. Pass rate/clean floor alone never prove readiness.
4. **Compute focused gaps.** Compare flow success/coverage; ≤20 gaps, ≤10 P0s (target ~5–10 if warranted), selected paths only. Each: path/criterion IDs, trigger→assertion, risk, integration/unit/characterization, P0 before refactor/release or P1, effort. Sort P0 then path; cut excess with reasons. Preserve prior failures.

## Constraint floor before a readiness claim

Read repository CONSTRAINTS.md and [constraint guide](references/CONSTRAINTS.md). Run read-only [floor guard](scripts/floor_guard.py) against accepted base before costly checks and final diff before readiness; separate from one test invocation. Retain command/exit/merge base/diff fingerprint/completion timestamp+timezone/environment/findings, dispatch base/prior failures. Lowered thresholds, weakened/skipped tests, suppressions, stub catches, new exceptions block green pending evidenced resolution. Unavailable = incomplete; exit 0 = no supported pattern found only. [Questioning](../../../protocols/questioning.md) routes unresolved choices; never alter checks/thresholds/exceptions/CI to clear report.

## Completion criteria and hard rules

- ALL four steps; ≤8 flows/20 gaps/10 P0s, no padding. Source/tests/config/CI read-only; write analysis only. One standard test invocation, no auto-fix.
- Missing criteria block readiness, not static analysis. Label unknown/unassessed criteria, omissions/blockers; evidence for failure causes, never default environment blame. PR/diff review → `acs-review-code-quality`.
- Use [engineering evidence](../../../protocols/engineering-memory.md): change/task identity, criteria/contract/code revisions, regression scope, environment, failures, skipped checks, omissions and scoped readiness. Static inventory is not executed acceptance evidence.
- Write critical-path, static/dynamic test-status and test-gap artifacts in resolved evidence home. Preserve canonical docs/unrelated results; new change output → `docs/changes/<change-id>/verification/`, standalone drafts → run root. Reconcile scope/revision; retain Change Context summary before raw cleanup. Update every Markdown `Last updated:`; coordinator owns transitions.
- Finish with <15 lines: flow coverage, run health/counts, gap/P0/P1 counts, top three risks and artifact paths. The files are the deliverable. Load [report templates](references/report-templates.md) only when formatting artifacts; their legacy `docs/` paths are illustrative, never overwrite authority blindly.

<!-- compaction-core:end -->
