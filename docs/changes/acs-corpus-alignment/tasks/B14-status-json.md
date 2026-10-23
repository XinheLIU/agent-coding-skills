# B14-status-json: Give scan_tasks.py a machine-readable status and next action

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py`
Effort: S-M

## Scope

`scan_tasks.py` only writes a manifest with `-o/--out`.

Add `--json`: per ticket, readiness, missing dependencies, the frontier, and exactly one `next` action. Keep the existing manifest output and overlay. Carry OpenSpec's warning in the output: status shows a record's state, not whether its prerequisites were satisfied.

## Inputs

- Analysis: §10 B14.
- Source: OpenSpec `openspec-propose:107-137`.

## Verification

- `--json` output validates against a schema and names one `next`.
- A missing dependency appears in `missing_dependencies` and removes the ticket from the frontier.
- The existing `-o` path still produces the same manifest.

## Blockers

none

## Coordination proposal

B23 calls this; land B14 first. Only this script changes.

## Evidence

Implemented on 2026-10-23; verification is incomplete because the required plugin build is blocked. Independent acceptance review remains pending. These are deterministic CLI fixtures and repository checks, not model behavioral runs.

Contract approved by the supervising agent: `--json` writes `{root,tickets,frontier,next,warnings}` to stdout; per-ticket status keeps canonical readiness and source revisions, reports absent IDs in `missing_dependencies`, and present prerequisites not accepted as done (including stale readiness) in `blocked_dependencies`. `execution_ready` includes direct dependency gates. `next` is one object `{action,ticket_id}`: first sorted implementation frontier ID, otherwise wait for active work, otherwise resolve blockers, otherwise complete only when no unresolved non-superseded work remains. Design tickets never enter the implementation frontier. The output always warns that recorded status does not prove prerequisites or execution evidence. Missing IDs are reportable in JSON; cycles still fail. `-o` and renderer overlays retain their existing contract.

| Criterion | Exact command / result |
| --- | --- |
| JSON schema and exactly one next action | `python3 -m unittest discover -s system/skills-src/authoring/acs-draw-portfolio-dag/tests -p test_scan_tasks.py` before implementation: expected RED, 9 tests, 8 failures because JSON mode was absent. `python3 -m unittest discover -s system/skills-src/authoring/acs-draw-portfolio-dag/tests -v` after implementation: PASS, 16 tests (9 new, 7 existing). Schema fixture uses an explicit stdlib validator for its type/required/enum/items/properties subset; a two-action mutation is rejected. |
| Missing dependency reported and excluded from frontier | Same 16-test command: PASS; absent local/cross-change IDs, stale completed prerequisites, design/unready/failed records, unresolved dependency prose, and cross-change completion are covered. Cycles with missing IDs still fail. |
| Existing manifest unchanged and overlay preserved | Existing roadmap tests in the same command: PASS, including overlay cycle validation and rendering. `python3 .scratch/B14-status-json/baseline_scan_tasks.py docs/changes/acs-corpus-alignment -o .scratch/B14-status-json/baseline-manifest.json` and `python3 system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py docs/changes/acs-corpus-alignment -o .scratch/B14-status-json/manifest.json`, then `cmp .scratch/B14-status-json/baseline-manifest.json .scratch/B14-status-json/manifest.json`: PASS, byte-identical 25-ticket manifests before this evidence update. Baseline scanner was extracted with `git show HEAD:system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py`. |
| Repository status smoke check | `python3 system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py docs/changes/acs-corpus-alignment --json > .scratch/B14-status-json/status.json`: PASS; test schema validation PASS, 25 tickets, 14 frontier IDs, one next action `implement` for `acs-corpus-alignment/B1-catalog-budget`, before this ticket changed to in_progress. |
| Repository validators | `python3 system/evals/validate_suite.py`: PASS, 43 source skills. `python3 scripts/validate-protocols.py`: failed on partial builder output, then PASS after restoring generated files to the known pre-build baseline. This checks package closure, not freshness of B14 packaged output. `git diff --check`: PASS. |
| Required generated plugin build | `python3 scripts/build-plugins.py`: FAIL, `ValueError: Linked resource escapes repository: /Users/xhl/GitHub/skills/agent-coding-skills/references/OpenSpec/docs/concepts.md`, reached through the preexisting notice change and reference symlink. Stopped and escalated; supervisor authorized read-only remaining checks and restoring only partial generated output. No generated edits retained; parent must verify packaging in the canonical checkout. |

Evidence revision: base HEAD `fbc81fd046ea0c2093e4516cc8dbdd289d473395`. Source/test fingerprint is SHA-256 of the following ordered UTF-8 lines, each terminated by a newline (`<sha256><two spaces><relative path>`):

```text
50ddbf4c18d6c33c96a1e701338dae38b766e5254722f2403c265f316eaa1598  system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py
1effd4860e58700d280196d866103d60775f223f3317580fa30ba7ce9f254fae  system/skills-src/authoring/acs-draw-portfolio-dag/tests/status.schema.json
4df09e9988586fb45e07038a3426aaae1d4b30a543b6c8e0c81e5c4dccd14a7d  system/skills-src/authoring/acs-draw-portfolio-dag/tests/test_scan_tasks.py
```

Combined source/test tree fingerprint: `sha256:6cfbcc7cd425bad0fda4a34db7eabb13965cf90d44f3a8bab5fe142907e47cd2`. Evidence text itself is excluded to avoid a self-referential hash. Logs and pre-build preservation hashes are in `.scratch/B14-status-json/`. Preexisting CHANGELOG and source notices, and every copied plan file other than this ticket, remain unchanged. No files staged. Remaining gates: successful plugin generation/freshness in the canonical checkout and independent review.

## Integrated acceptance

2026-10-23: source reconciled into canonical checkout; `python3 scripts/build-plugins.py`, `python3 scripts/validate-protocols.py`, `python3 system/evals/validate_suite.py`, and affected unittest suites passed. Independent first-batch review found no blocking source defects for this ticket. Prior isolated packaging blocker is resolved by canonical generation. Exact commands and logs: `.scratch/acs-corpus-alignment/verification.json`; review run `66a6103a-dd18-410b-b984-c84346a08432`. Scope remains deterministic contract verification, not proof of model reliability.
