---
protocol: acs:operations-memory
version: 1.2.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/operations-memory.md
---

# Operations Context Contract

Last updated: 2026-10-23

The active coordinator and Operations skills use the project's existing CI/CD commands or authorized provider capabilities. This contract defines its handoff boundary under the [shared protocol](skill-declarations.md); it does not introduce a deployment framework. Environment/runbook facts are Persistent Current; release decisions and compact evidence are Persistent Changes. Execution logs and transient rollout checks are Working. Human reports use [Presenter](presenter.md); they do not own release status or authorization.

## Persistent Current

`operations.constraints` and `operations.checks` resolve the applicable environment/topology, build and deploy configuration, CI gates, migration constraints, observability, operational limits, and rollback procedures. Read configuration as executable evidence and record the relevant environment/configuration revision. Runbooks explain present operating procedures; change records retain why release decisions were made.

## Consumer release configuration

The consumer declares exact verification/readiness commands, working directories, criterion coverage and required CI gates in `operations.checks`; it declares available environments, target/configuration revisions and authorized action boundaries in `operations.constraints`. Unset commands or environments block execution. Do not guess project commands, infer a production target, or treat a local check as a release. Existing authorization persists for its scope; a readiness verdict grants no new authority.

For production, also require rollout stages/exposure, dwell/check interval, minimum sample size, evidence/telemetry freshness limits, advance/hold/rollback thresholds, migration compatibility and verified rollback procedure. Record an error-budget policy (SLO/window, low-budget band, burn-rate limit) and current observations: exhausted budget freezes feature releases, low budget allows only slow low-risk rollout, excessive burn holds. Unknown budget, missing policy or stale/missing telemetry blocks advancement. Observability design remains in `design.contracts`; Operations consumes its current thresholds.

First use or a configuration change requires a non-mutating dry-run invocation that ends `not released`, retaining the preview and configuration revision before later authorized execution. A dry-run flag alone does not prove a command is non-mutating. Local mocks may test mechanics but establish no live provider behavior.

Readiness requires current criterion-linked commands/results bound to source, immutable artifact/build provenance, environment/configuration and CI. The shared [evidence checker](../../skills/acs-implement/scripts/check-evidence.py) checks BASE and source rows; the consumer must separately inspect actual outputs, coverage, freshness and artifact/environment bindings. A rebuilt artifact cannot inherit verification; establish its new source/build/digest link and rerun affected checks.

After a merge error, read server state; never retry the merge. Confirm the actual merged revision or block release when unmerged/unknown. Canary pattern alerts require two consecutive valid checks for the same artifact/environment; healthy or invalid/missing checks break the streak, with missing data holding advancement. Debouncing alerts never delays configured immediate safety stops or rollback thresholds. Rollback still requires applicable authorization and observed recovery evidence.

## Release input

Require the same canonical change/task identity, verified source revision and immutable artifact identity/digest, verification summary and criterion references, target environment, CI requirements, topology, and applicable contracts. Identify migration/release/rollback decisions before execution. A changed artifact, runtime, configuration, migration, topology, or production condition triggers review of affected readiness; never attach old verification to a newly built artifact without establishing the link.

## Release evidence

`change.release_evidence` retains the change ID, artifact digest and source/build reference, verification reference, target environment/configuration revision, gate results, migration outcome, rollout result, observability checks, and rollback reference/result. Name failures, omissions, and unresolved operational questions with their blocking effect. When no release ran, state `not released`; a local test run is not a release.

Pass evidence to Product for observed behavior reconciliation and to Testing for regressions/environment findings. Update relevant operational Persistent Current after deployment or rollback; preserve release history in Persistent Changes. Store minimal evidence rather than credentials or raw production logs. The coordinator handles scheduling, freshness propagation, and authorized runtime calls; Operations owns the release assessment.
