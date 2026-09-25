# Deploy Workflow

Last updated: 2026-09-25

Release an authorized, verified artifact using the project's existing deployment tooling and the [Operations contract](../protocols/operations-memory.md).

## Inputs

Resolve the canonical change, verification evidence, immutable artifact digest and source/build revision, target environment/configuration, applicable migration constraints, and rollback procedure. Reuse configured record homes. Missing evidence blocks the affected release; a green test percentage or a report alone does not establish readiness.

Existing authorization persists. This workflow does not authorize staging/production deployment, commits, tags, or rollback by itself. Resolve only missing decisions or actions outside the authorized scope.

## Execute and record

1. **Verify readiness.** Match criterion-linked verification to the exact artifact, environment, required CI gates and applicable decisions. Record failures, omissions and their impact. A changed artifact or environment requires scoped reassessment.
2. **Present a release decision when needed.** Save the release proposal and essential evidence in Persistent Memory before review. The [Presenter](../protocols/presenter.md) displays these revisions; the coordinator records feedback against the actual scope and version. Reuse prior applicable authorization.
3. **Deploy within scope.** Execute the project's authorized staging/production steps. Record exact commands, environment/configuration revision, migration and rollout outcomes. Keep verbose logs in Working Memory while retaining enough evidence to understand the result without those logs.
4. **Verify behavior.** Run the required smoke/acceptance and observability checks against the deployed artifact. Record criterion IDs, exact commands, results, omissions and rollback outcome if performed.
5. **Reconcile.** Retain compact release evidence in the configured change/release home: change ID, artifact digest, source/build revision, verification reference, environment, gates, migration, rollout and rollback references. Update operational Current State only from observed deployment/rollback evidence. If no release ran, record `not released`.

## Handoff and completion

Return the [shared envelope](../protocols/skill-declarations.md#handoff-envelope) with persistent release/evidence references and consumed revisions to maintenance, Product and Testing as relevant. A human report is an optional derived view. Preserve one configured Working Memory recovery entry while the release is active.

Completion requires a verified release outcome or a precise blocker, durable evidence, and accessible references. Apply the retention gate before clearing completed run material; preserve history and exact reviewed content. No commit or tag is implied.

Shared context coordination: [context-coordination.md](context-coordination.md)
