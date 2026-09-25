# Maintain Workflow

Last updated: 2026-09-25

Ingest monitoring alerts, diagnose root causes, write verifiable implementation change records, and re-enter `build` for allowed patterns — without human initiation for low-risk fixes.

```
entry_artifact: Monitoring alerts, scheduled scans, or on-call incidents
exit_artifact:  Implementation change records in docs/product/<product>/product.html OR immediate fix + regression test
approval_gate:  Autonomous for within-control-band fixes; escalate to user for breaking changes or data loss risk
```

## Overview

```
alert/incident → acs-diagnose-incident → acs-triage → decision point:
                                                ├── within control band → record-change → build → test → deploy
                                                └── outside control band → record-change (open questions) → escalate to user
```

## Skill Sequence

### 1. Ingest and diagnose
- `/acs-diagnose-incident` — ingest the alert or incident report, extract symptoms (service degradation, error rate spike, data inconsistency), build a diagnosis hypothesis, test it against logs and code, identify root cause

### 2. Triage
- `/acs-triage` — classify severity (P0/P1/P2/P3), estimate blast radius, determine whether the fix is within the control band

**Control band (autonomous fix allowed):**
- Config change or environment variable rollback
- Known hotfix pattern (previously diagnosed and documented)
- Scaling adjustment (replicas, resource limits)
- Non-breaking bug fix (corrects wrong behavior, does not change API contract or data shape)
- Rollback to prior release via `deploy`

**Outside control band (requires user approval):**
- Schema change or data migration
- Behavior change that requires design input
- Data loss risk
- Breaking API change
- Any change affecting authentication or authorization

### 3. Write implementation change record
Reuse the canonical change/spec and incident home. When absent, create a local change under `docs/changes/<change-id>/`; product records link that same change. Retain diagnosis and regression evidence in Persistent Memory, with raw logs in Working Memory. The record contains:
- **Current behavior**: what broke, observed symptoms, evidence
- **Intended behavior**: what should happen, acceptance criteria
- **Implementation scope**: config change, hotfix, rollback, or "needs design"
- **Severity**: P0/P1/P2/P3
- **Decision**: within-band auto-fix OR escalation with open questions

### 4a. Within control band — auto-fix loop
Pass change record to `build` → `test` → `deploy`.

The change record is the spec; no separate requirements phase needed for in-band fixes. The fix must include a regression test that would have caught the original issue.

After deploy: update the configured incident record with the observed resolution, source/artifact and environment revisions, release evidence and fix reference.

### 4b. Outside control band — escalate
Save the proposed change and open questions before review. Use the [Presenter](../protocols/presenter.md) when a comparison helps; record feedback against the proposal revision through the coordinator. Continue dependent work only when the necessary decision and authorization exist.

## Autonomy Policy

Autonomous fixes require the project to configure allowed patterns:

```json
// .claude/settings.json
{
  "maintenance": {
    "autonomy_rules": {
      "allow": ["config-rollback", "hotfix", "scaling-adjustment"],
      "require_approval_for": ["schema-change", "data-migration", "breaking-change"]
    }
  }
}
```

These settings illustrate project policy, not a verified host integration or a new authorization source. Explicit task authorization also applies. Without applicable authorization, return the proposed action and blocker; do not infer deployment permission from a low-risk label. Retain consequential decisions in the configured change/incident record.

## Entry Criteria

- Alert payload, incident description, or scheduled scan result.
- Access to logs, monitoring data, or reproduction steps.

## Exit Criteria

- Canonical change/spec and incident records contain the retained diagnosis and criterion-linked evidence.
- Configured incident record updated with observed diagnosis/resolution and consumed revisions.
- Fix deployed and verified (for in-band), OR escalation surfaced with open questions (for out-of-band).

## Closes the Loop

For allowed patterns: alert → diagnosis → implementation change record → `build` → `test` → `deploy` completes without human initiation. This is the autonomous maintenance loop.

Shared context coordination: [context-coordination.md](context-coordination.md)
