# Pull request body

Last updated: 2026-10-23

Fill from observed output; no placeholder is acceptance evidence. Save locally before an authorized PR write. Use a compact before/after table for a small change; a diagram is optional when it clarifies a dependency or rollout. Never invent a screenshot.

```markdown
## Change
<Concrete trigger and resulting behavior; canonical change/ticket reference>

| Before | After |
| --- | --- |
| <Observed problem> | <Verified result> |

## Verification
Source: <current full tree fingerprint and branch revision>
Target: <target branch and revision>; BASE: <immutable dispatch identity>
Environment/configuration: <identity and revision>

| Criterion | Exact command | Revision | Timestamp | Result / evidence |
| --- | --- | --- | --- | --- |
| <ID> | <executed command> | <tested fingerprint> | <RFC3339> | <observed result and retained reference> |

Review: <current review reference>; converged: <true/false>
Review fix rounds: <used>/3; operational retries: <used>/<policy cap>
CI: <required gates and current results>; omissions: <none or blocking effect>

## Merge danger
<low / elevated / blocked, with reason; migration, compatibility, rollout and rollback implications>
<Unverified behavior and unresolved decisions; do not infer deploy readiness from PR readiness>

## Stop lists
Stop: unset commands/environments, missing next-action authorization, ownership/conflicts,
failed/missing/stale checks, blocking review, exhausted limits, new scope/user decisions.
Never stop within scope: existing PR, completed actions, routine wording, in-scope fixes
below cap, preservable unrelated dirty files. Stop rules always take precedence.
```

Do not include credentials, raw production logs or unrelated local changes. PR success requires an observed open PR URL for the intended branch; a local body alone is `PR not opened`.
