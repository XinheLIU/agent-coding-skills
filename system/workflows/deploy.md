# Deploy Workflow

Last updated: 2026-09-17

Release passing changes to staging and production with recorded evidence and a rollback plan.

```
entry_artifact: Passing changes on branch, target environment config
exit_artifact:  Release evidence (deploy log, version tag, rollback plan), docs/operations/releases.md updated
approval_gate:  User must approve production deploy; staging deploys may be auto-approved
```

## Overview

```
green tests → verify environment → check release gate → deploy staging → [USER APPROVES] → deploy production → record evidence
                                                                                            ↓ if issues
                                                                                          rollback
```

## Skill Sequence

### 1. Verify environment constraints
Check `docs/operations/environments.md` for the target environment's constraints, config requirements, and known issues. If the file does not exist, note this as a gap and proceed with what is known.

### 2. Check the release gate
All of the following must be true before deploying:
- Full test suite green (from `test` phase)
- Required approvals obtained (PR review, if applicable)
- No blocking issues open against this change
- Branch is up to date with the target base branch

### 3. Deploy to staging
Execute the project's staging deployment steps. Record the exact command, timestamp, environment, and outcome in `docs/operations/releases.md`.

For staging: proceed if release gate is met. No additional approval needed.

### 4. Smoke test staging
Verify the deployment against acceptance criteria from `specs/<spec>.md`. This is a quick behavioral check, not a full regression. Note any discrepancies.

### 5. User approves production deploy
Present staging evidence (deploy log, smoke test results) and request explicit user approval before proceeding to production.

### 6. Deploy to production
Execute production deployment steps. Record evidence identically to staging.

### 7. Record release
Update `docs/operations/releases.md` with:
- Version tag or commit SHA
- Deploy timestamp and environment
- What was shipped (spec reference)
- Smoke test outcome
- Rollback procedure (specific command or steps to undo)

### 8. Rollback (if needed)
If post-deploy issues are detected, execute the rollback procedure recorded in step 7. After rollback, record the rollback event in `docs/operations/releases.md` and pass the incident to `maintain` for diagnosis.

## Entry Criteria

- Full test suite passing (unit + integration + coverage threshold met).
- Branch approved and ready to merge.
- Target environment config accessible.

## Exit Criteria

- Release evidence committed to `docs/operations/releases.md`.
- Version tag applied.
- Rollback procedure documented.
- Production deploy confirmed healthy (or rollback completed).

## Handoff

Passes release record to `maintain`. The maintain workflow monitors the deployed version and closes the loop on any post-deploy incidents.

Shared context coordination: [context-coordination.md](context-coordination.md)
