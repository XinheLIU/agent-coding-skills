# Feature Delivery Workflow

Last updated: 2026-09-25

Use approved intent and the [shared coordinator](../protocols/context-coordination.md). Keep one canonical change/ticket ID throughout Product, Design, Implementation, Verification, and Release.

```text
accepted product scope or accepted designs
  → acs-plan-delivery: reuse inputs → slice outcomes → expose design blockers → open HTML plan + DAG
      ↔ Product/Design: settle only missing scope, criteria, or decisions
  → acs-implement: execute ready slices → acs-tdd → scoped end-to-end verification
      ↔ acs-plan-delivery: reconcile scope/dependency changes
  → testing + acs-review-code-quality
  → release evidence when authorized → retained change + run cleanup
```

## Planning and handoff contract

[acs-plan-delivery](../resources/skills-src/build/acs-plan-delivery/SKILL.md) (reference procedure; capability not installed) owns decomposition and graph reconciliation. Product supplies the canonical change ID, accepted scope/outcomes/priorities, and existing specs/decisions. Design supplies criteria, relevant UX behavior, accepted contracts, migration constraints, and unresolved blockers. Link source artifacts and consumed revisions rather than copying requirements.

Planning can start before all design is settled. Execution readiness is per implementation ticket: criteria/checks are testable, necessary decisions are current and accepted, external preconditions hold, and prerequisite evidence is applicable. The planner routes specific blockers to their specialist and reuses `acs-explore-unknowns` decision tickets where present. Independent ready slices can proceed.

Reuse IDs and tracker homes; the default is `docs/changes/<change-id>/tasks/<task-id>.md`. Tickets retain scope, dependencies, input revisions, readiness, checks, and evidence. Fine-grained execution plans/checklists and claims remain Run Context. After accepted-scope confirmation, the default user handoff is one openable `docs/changes/<change-id>/delivery-plan.html`, following the [delivery report contract](../resources/skills-src/build/acs-plan-delivery/references/delivery-report.md). Its plan and embedded DAG derive from canonical sources.

## Scheduling and reconciliation

`acs-implement` consumes the existing graph or invokes `acs-plan-delivery` when tickets are missing or materially stale. The coordinator validates readiness, prerequisite evidence, exclusive claims, and concurrent-write risks. Write conflicts constrain scheduling separately from logical dependency edges. Design tickets go to their specialist rather than a TDD executor.

Execution status/evidence updates refresh the same HTML report, its next action, and its DAG; reload an open tab. Scope/dependency changes return to `acs-plan-delivery`, which preserves IDs and completed evidence, reassesses affected consumers, and records changed edges and rationale. Superseded or disputed prerequisites do not unlock dependents. Do not infer parent completion from child checkboxes.

## Execution contract

Before editing, recheck the active task's requirements/design revisions, dependencies, affected code, and exclusive claim. Implement the scoped slice using existing project conventions. Use criterion-based red → green loops when testing behavior; run appropriate checks for other changes. Report failed verification and scope/design deviations rather than silently revising accepted requirements.

Return code revision/diff identity, affected surfaces, decision and criterion references, checks run, failures/omissions, and next verification needs. The coordinator reconciles evidence and proposed transitions. Uncommitted work needs a reproducible diff identity; HEAD alone cannot identify it. A worktree is optional isolation selected by the coordinator, not a requirement imposed upstream; all handed-off references must resolve in the receiver's environment.

## Verification contract

Use [Testing](testing.md) and the [engineering evidence contract](../protocols/engineering-memory.md). Review both Standards and Spec axes. Retain criterion → test/evidence → revision mappings, environment assumptions, failures, omissions, and scoped readiness. Static implementation presence is not passing acceptance evidence. Changes to relevant requirements, contracts, code, tests, or environment trigger scoped reassessment.

## Release and close

Use the [Operations contract](../protocols/operations-memory.md) with existing project tooling and task authorization. Release evidence links the same change to the verified revision/artifact digest, target environment/configuration, gates, migration results, observability, and rollback references. If no release was requested or performed, record that without implying one occurred.

Reconcile applicable Product/System/Design/Operations Current State with observed evidence. Apply the protocol's retention gate: retain compact Change Context; verify it remains understandable without the run directory; then remove only reconciled scratch. When another session must continue, transfer through the [shared handoff envelope](../protocols/skill-declarations.md#handoff-envelope), with explicit claim transfer when applicable.
