# Maintain Workflow

Last updated: 2026-09-12

Ingest monitoring alerts, diagnose root causes, write verifiable implementation change records, and re-enter `/build` for allowed patterns — without human initiation for low-risk fixes.

```
entry_artifact: Monitoring alerts, scheduled scans, or on-call incidents
exit_artifact:  Implementation change records in docs/product/<product>/product.html OR immediate fix + regression test
approval_gate:  Autonomous for within-control-band fixes; escalate to user for breaking changes or data loss risk
```

## Overview

```
alert/incident → diagnose-incident → triage → decision point:
                                                ├── within control band → record-change → /build → /test → /deploy
                                                └── outside control band → record-change (open questions) → escalate to user
```

## Skill Sequence

### 1. Ingest and diagnose
- `/diagnose-incident` — ingest the alert or incident report, extract symptoms (service degradation, error rate spike, data inconsistency), build a diagnosis hypothesis, test it against logs and code, identify root cause

### 2. Triage
- `/triage` — classify severity (P0/P1/P2/P3), estimate blast radius, determine whether the fix is within the control band

**Control band (autonomous fix allowed):**
- Config change or environment variable rollback
- Known hotfix pattern (previously diagnosed and documented)
- Scaling adjustment (replicas, resource limits)
- Non-breaking bug fix (corrects wrong behavior, does not change API contract or data shape)
- Rollback to prior release via `/deploy`

**Outside control band (requires user approval):**
- Schema change or data migration
- Behavior change that requires design input
- Data loss risk
- Breaking API change
- Any change affecting authentication or authorization

### 3. Write implementation change record
Write a verifiable record to `docs/product/<product>/product.html` with:
- **Current behavior**: what broke, observed symptoms, evidence
- **Intended behavior**: what should happen, acceptance criteria
- **Implementation scope**: config change, hotfix, rollback, or "needs design"
- **Severity**: P0/P1/P2/P3
- **Decision**: within-band auto-fix OR escalation with open questions

### 4a. Within control band — auto-fix loop
Pass change record to `/build` → `/test` → `/deploy`.

The change record is the spec; no separate requirements phase needed for in-band fixes. The fix must include a regression test that would have caught the original issue.

After deploy: update `docs/operations/incidents.md` with resolution timestamp and fix reference.

### 4b. Outside control band — escalate
Surface the change record with open questions to the user. Wait for their decision before re-entering `/design` or `/build`.

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

If no `autonomy_rules` are configured, all fixes require user approval. The first 5 autonomous fixes in a new project are logged in `docs/operations/incidents.md` and flagged for retroactive user review.

## Entry Criteria

- Alert payload, incident description, or scheduled scan result.
- Access to logs, monitoring data, or reproduction steps.

## Exit Criteria

- Verifiable change record written to `product.html`.
- `docs/operations/incidents.md` updated with diagnosis and resolution.
- Fix deployed and verified (for in-band), OR escalation surfaced with open questions (for out-of-band).

## Closes the Loop

For allowed patterns: alert → diagnosis → implementation change record → `/build` → `/test` → `/deploy` completes without human initiation. This is the autonomous maintenance loop.

Shared context coordination: [context-coordination.md](context-coordination.md)
