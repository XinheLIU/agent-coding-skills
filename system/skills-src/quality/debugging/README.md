# Quality · Debugging

Last updated: 2026-09-12

Cross-cutting debugging skills used reactively when something breaks.

| Skill | Owns |
| --- | --- |
| `triage` | Classify an incoming bug report: severity, scope, reproduction steps, likely owner |
| `resolving-merge-conflicts` | Resolve git merge conflicts with correct intent reconstruction |

`diagnosing-bugs` has moved to `maintain/diagnose-incident` — root-cause analysis belongs in the maintenance loop where it feeds the autonomous fix decision. The typical incident flow is now: `triage` to classify → `maintain/diagnose-incident` to find the cause → fix via `/build` → `review-code-quality` before merge.

`triage` remains here as a cross-cutting entry point; it runs at any phase, not just during maintenance.
