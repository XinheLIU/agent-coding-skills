---
name: acs-ship
description: Use when a verified branch is ready for a pull request.
---

# Ship a verified branch

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [change.task, change.implementation_evidence, verification.acceptance_criteria]
  retrieves: [operations.checks, operations.constraints, change.review, source.implementation]
  produces: [change.ship_evidence]
  updates: [change.pull_request, run.orchestration_state]
  invalidates: [verification.for_changed_code]
  handoff_to: [code_review, release]
```

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.

## Completion criteria and hard rules

Take a verified feature branch to one open PR within existing authorization. Resolve the consumer's exact verification commands, working directories, criterion coverage, environments/configuration revisions and required CI gates from [Operations](../../resources/protocols/operations-memory.md#consumer-release-configuration). Unset commands or environments block execution; never invent `npm test`, a production target, or a successful check. Without external authorization, prepare a local body; report `PR not opened`.

1. **Read current state.** Resolve change ID, immutable dispatch BASE, current branch and target branch revisions, full working-tree fingerprint (including relevant untracked files), prior review and PR state. Preserve unrelated local work. Stop on the target branch or ambiguous ownership/conflicts. Existing authorization persists, but invocation alone does not authorize commits, pushes, PR writes, merges or deployment.
2. **Rerun verification every invocation.** Run all declared checks against the current source/environment even when an existing PR or green record is present. Record exact command, criterion, revision, timestamp and result using the [evidence template](../../resources/skills-src/build/acs-implement/references/evidence-template.md). Invoke the [B19 row checker](../../resources/skills-src/build/acs-implement/scripts/check-evidence.py) with independently resolved `--base` and `--revision`; also inspect actual output, required coverage and current CI. A checker pass validates bindings, not execution truth. Source changes invalidate affected evidence; rerun checks on the final tree before publication.
3. **Bound review fixes.** Read the current diff and review findings. Allow at most three review fix rounds per change/branch attempt, persisted across resume; each round makes authorized in-scope fixes, reruns verification, and rereviews the final diff. Record start/end fingerprints and unresolved findings. These review fix rounds are separate from [operational retries](../../resources/protocols/orchestration.md#failure-policy); neither resets the other. Unresolved blocking findings at the cap end with `converged: false`, no publish, and a precise blocker. `converged: true` requires current clean review and passing checks.
4. **Prepare and publish within scope.** Fill the [PR body](references/pr-body.md): concrete behavior change, smallest useful visual summary, criterion evidence and merge-danger call. Recheck source/target revisions and authorization immediately before any write. Only actions are idempotent: inspect remote state, reuse/update the matching PR and skip already-completed authorized writes; never skip verification. On an ambiguous PR-write error, read server state before considering another write. No force push, automatic merge or deployment. Persist PR URL/state or local body and source identity before handoff.

**Stop list:** unset commands/environments; missing authorization for the next external action; target branch/ownership conflicts; failed, missing or stale required checks; unresolved blocking review; exhausted fix/retry limit; new scope or user-owned release/version decisions. Stop the affected action and retain evidence.

**Never-stop list (within authorized scope):** an existing PR; already-completed actions; routine PR wording; actionable in-scope review fixes below the cap; unrelated dirty files that can be preserved. Continue safe local preparation without reasking settled decisions. This list never overrides the stop list or permits publishing uncommitted unrelated work.

Return the shared envelope with body/PR reference, consumed revisions, current evidence, `converged`, both counters, blockers and next action. A local rehearsal is not an open PR. Reviewed content stays in Persistent Changes; logs/recovery stay Working.

<!-- compaction-core:end -->
