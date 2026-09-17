# Quality · Debugging

Last updated: 2026-09-17

Cross-cutting debugging skills used reactively when something breaks.

| Skill | Owns |
| --- | --- |
| `acs-triage` | Classify an incoming bug report: severity, scope, reproduction steps, likely owner |
| `acs-resolving-merge-conflicts` | Resolve git merge conflicts with correct intent reconstruction |

`diagnosing-bugs` has moved to `maintain/acs-diagnose-incident` — root-cause analysis belongs in the maintenance loop where it feeds the autonomous fix decision. The typical incident flow is now: `acs-triage` to classify → `maintain/acs-diagnose-incident` to find the cause → fix via `build` → `acs-review-code-quality` before merge.

`acs-triage` remains here as a cross-cutting entry point; it runs at any phase, not just during maintenance.
