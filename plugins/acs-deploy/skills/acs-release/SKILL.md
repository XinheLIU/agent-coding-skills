---
name: acs-release
description: Use when a merged artifact is ready for a production rollout.
---

# Release a verified artifact

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [change.task, change.implementation_evidence, operations.checks, operations.constraints]
  retrieves: [change.ship_evidence, design.contracts, verification.acceptance_criteria]
  produces: [change.release_evidence]
  updates: [operations.current_state, run.orchestration_state]
  invalidates: [verification.for_changed_environment]
  handoff_to: [operations, product, testing]
```

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.

## Completion criteria and hard rules

Use declared tooling under [Operations](../../resources/protocols/operations-memory.md). Existing authorization persists; release readiness never grants merge, deploy, rollback or communication permission. Unset commands or environments block execution.

1. **Resolve identity and state.** Require canonical change, confirmed merged source revision, immutable artifact digest and build provenance, target environment/configuration revision, topology, required CI/criterion evidence, migration decisions and rollback procedure. Independently read server state if a preceding merge reported an error; never retry the merge. If merged, bind the actual merge revision; if unmerged or unknown, stop. Do not initiate a merge.
2. **First-use dry run.** On first use or configuration change, record the exact commands, targets, stage order, gates, rollback thresholds and authorization references without running mutating commands. Check preview semantics; use local mocks or a documented non-mutating preview. A `--dry-run` name alone is not proof. End this invocation with `not released`; retain preview/configuration revision for later authorized execution. No production, PR, merge, tag, flag, migration or deploy writes in dry run.
3. **Gate current readiness.** Apply [consumer configuration and readiness](../../resources/protocols/operations-memory.md#consumer-release-configuration). Run declared readiness checks and inspect actual outputs. Validate source-bound rows through the [B19 checker](../../resources/skills-src/build/acs-implement/scripts/check-evidence.py) with independently resolved `--base`/`--revision`; separately match artifact digest/build provenance, environment/configuration, CI and freshness. A rebuilt artifact cannot inherit verification: establish and verify its new source/build/digest link and rerun affected checks. Unknown, missing, failed or stale evidence blocks rollout.
4. **Stage within scope.** Follow configured staging → canary → progressive expansion → full rollout, with explicit applicability reasons for omitted stages. Record exposure, dwell/check interval, minimum sample size and advance/hold/rollback thresholds before execution. Read the current error budget and burn rate: exhausted freezes feature releases; the declared low-budget band permits only slow, low-risk rollout; excessive burn holds. Missing budget/policy blocks. Check migration compatibility and rollback authority each stage. Hold on missing telemetry or unmet gates; advance only on current passing observations for this artifact/environment.
5. **Observe and recover.** Canary pattern alerts require the same pattern in two consecutive valid checks for the same artifact/environment; the first is pending, a healthy check resets it, and a missing/invalid check breaks the streak and holds advancement. This alert debounce never delays a configured immediate safety stop or rollback threshold. On a breach, halt expansion, execute rollback only within authorization, otherwise retain the hold and request the missing decision. Verify actual rollback state before claiming recovery. Retries use the persisted [failure policy](../../resources/protocols/orchestration.md#failure-policy); never retry a merge, and never reset counters by resuming.
6. **Persist the outcome.** Persist `change.release_evidence` using all [release evidence fields](references/release-evidence.md): identity, commands/timestamps/results, criteria, budget, stages, observations, migrations and rollback. `released` requires observed deployment and required post-deploy checks; a deployed but unverified artifact is `deployed; verification incomplete`, with advancement held. Dry run or no deployment is `not released`; never infer production success from a local check. Update operational Current only from observed state and return the shared envelope to Operations, Product and Testing.

<!-- compaction-core:end -->
