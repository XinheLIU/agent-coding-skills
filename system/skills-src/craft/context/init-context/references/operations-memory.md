# Operations Context Contract

Last updated: 2026-09-09

Operations has no integrated deployment skill in this suite. The active coordinator uses the project's existing CI/CD commands or authorized provider capabilities. This contract defines its handoff boundary under the [shared protocol](PROTOCOL.md); it does not introduce a deployment framework.

## Current State

`operations.constraints` and `operations.checks` resolve the applicable environment/topology, build and deploy configuration, CI gates, migration constraints, observability, operational limits, and rollback procedures. Read configuration as executable evidence and record the relevant environment/configuration revision. Runbooks explain present operating procedures; change records retain why release decisions were made.

## Release input

Require the same canonical change/task identity, verified source revision and immutable artifact identity/digest, verification summary and criterion references, target environment, CI requirements, topology, and applicable contracts. Identify migration/release/rollback decisions before execution. A changed artifact, runtime, configuration, migration, topology, or production condition triggers review of affected readiness; never attach old verification to a newly built artifact without establishing the link.

## Release evidence

`change.release_evidence` retains the change ID, artifact digest and source/build reference, verification reference, target environment/configuration revision, gate results, migration outcome, rollout result, observability checks, and rollback reference/result. Name failures, omissions, and unresolved operational questions with their blocking effect. When no release ran, state `not released`; a local test run is not a release.

Pass evidence to Product for observed behavior reconciliation and to Testing for regressions/environment findings. Update relevant operational Current State after deployment or rollback; preserve release history in Change Context. Store minimal evidence rather than credentials or raw production logs. The coordinator handles scheduling, freshness propagation, and authorized runtime calls; Operations owns the release assessment.
