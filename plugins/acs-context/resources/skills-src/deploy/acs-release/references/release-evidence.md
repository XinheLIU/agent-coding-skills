# Release evidence fields

Last updated: 2026-10-23

Use the configured Persistent Changes home, with raw logs in Working Memory. These fields extend the [Operations contract](../../../../protocols/operations-memory.md); they do not introduce a deployment service or a second source of release status.

| Record | Required evidence |
| --- | --- |
| Identity | Change ID, immutable dispatch BASE, merged source revision, full source fingerprint, build reference, immutable artifact digest |
| Environment | Target, topology, configuration revision, consumed contract revisions |
| Authorization | Existing authorization references and exact allowed actions; missing actions block execution |
| Configuration | Exact verification/readiness/deploy/rollback commands and working directories, required CI gates, criteria, observation freshness limits |
| Readiness | Command, criterion, tested revision, RFC3339 timestamp and observed result per row; artifact/build binding and CI references |
| Budget | SLO/window, observed remaining budget and burn rate, policy thresholds, decision and observation time |
| Stages | Exposure, dwell/check interval, minimum sample size, advance/hold/rollback thresholds; applicability reason for any omitted stage |
| Observations | Artifact/environment, pattern, valid sample time, consecutive count, pending/confirmed/reset state; missing checks and holds |
| Recovery | Migration result, rollback trigger, authorization, command and actual observed state; counters and unresolved blocker |
| Outcome | `not released`, `released`, `deployed; verification incomplete`, or observed rollback outcome; omissions and blocking effects |

Dry run records the preview and `not released`, including which mutating actions were not executed. It cannot update production Current State or certify that the deploy/rollback commands work. A successful rollback command alone cannot establish recovery; retain the post-rollback observation.
