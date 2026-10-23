# B18-lesson-ladder: Turn lessons into checks before instructions

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/authoring/acs-review-agent-instructions/SKILL.md` Intake
Effort: M

## Scope

Lesson intake routes each lesson to an instruction file — the weakest rung.

Add the ladder: architecture, types, lint, test, then documentation last. Prove that each new check fails on the recorded mistake. Change the completion criterion to "the new check would have failed on the recorded failure, or no check is possible and the instruction is the fallback".

## Inputs

- Analysis: §7.6, §10 B18.
- Sources: pstack `correct`; Pocock `retro:19`.

## Verification

- The intake section states the ladder order and the proof requirement.
- A recorded lesson produces a check that fails on the old code.
- A lesson with no possible check is explicitly marked an instruction fallback.

## Blockers

none

## Coordination proposal

Only the authoring skill. No shared write.

## Evidence

Implemented the lesson ladder only in Intake: architecture → types → lint → test → documentation. Each new check must reproduce the recorded failure for the expected reason, then pass unchanged against the correction. An instruction fallback must explain why all four enforcement rungs cannot work; unavailable tools, permission or reproduction evidence leave work incomplete. The existing narrow-scope routing table and all content outside Intake are byte-for-byte preserved from the starting dirty baseline, including the B1 description and date. No shared protocol or generated source was edited.

Provenance: adapted pstack `correct` at `0b8e952` and Matt Pocock `retro` at `49dd158`, inspected read-only under `/Users/xhl/GitHub/skills/agent-coding-skills/references/`. Local `ANALYSIS.md` now places the B18 details in §16 (the ticket's older §7.6/§10 references have shifted). No upstream files changed.

Baseline: HEAD `fbc81fd046ea0c2093e4516cc8dbdd289d473395` plus the integrated dirty B1/B2/B3/B4/B5/B14/B19 files. The full 1,121-file manifest is `.scratch/B18-lesson-ladder/baseline.json`, SHA-256 `c7beb7f92cf424ad733c46881c97050940847f7517818058f51a95347e45fe10`; `baseline.diff`, `baseline.status`, and `baseline.skill.md` preserve the initial content. The baseline manifest hashes tracked and nonignored untracked files (symlinks hash their link target text); HEAD alone is not the source identity.

Changed files relative to that baseline (exactly three):

- `system/skills-src/authoring/acs-review-agent-instructions/SKILL.md`
- `system/evals/tests/test_lesson_ladder.py` (new: four tests)
- `docs/changes/acs-corpus-alignment/tasks/B18-lesson-ladder.md` (this evidence record)

Validation source identity: `sha256:151aa7e20865c90ef5fa669a61ebf7b7002b7875a31d95711836402be1750504`. Method: SHA-256 of UTF-8 `json.dumps(path_to_file_sha256, sort_keys=True)` for all files beneath `system/`, `scripts/`, and `catalog/`, dereferencing symlinks and excluding `__pycache__`/`.pyc`. Includes relevant existing integrated changes and the new test, excludes ticket/evidence/generated outputs to avoid self-reference. Exact manifest: `.scratch/B18-lesson-ladder/validation-source-hashes.json`; runner: `.scratch/B18-lesson-ladder/run_checks.py`. The runner verifies unchanged source identity before/after every command. Python 3.14.6, macOS 26.6.2 arm64; all commands below ran from this worktree root with `PYTHONDONTWRITEBYTECODE=1`.

| Criterion | Exact command | Result | Completed (UTC) | Raw output |
| --- | --- | --- | --- | --- |
| AC-1/AC-2/AC-3 and source/package regressions | `python3 -m unittest discover -s system/evals/tests -v` | passed | `2026-10-23T08:14:22.119106+00:00` | `.scratch/B18-lesson-ladder/check-1.log` |
| Preserve B19 evidence binding | `python3 -m unittest discover -s system/evals/evals -p test_evidence_binding.py -v` | passed | `2026-10-23T08:14:24.245393+00:00` | `.scratch/B18-lesson-ladder/check-2.log` |
| Build scratch packages | `python3 scripts/build-plugins.py --output .scratch/B18-lesson-ladder/plugins` | passed | `2026-10-23T08:14:25.135770+00:00` | `.scratch/B18-lesson-ladder/check-3.log` |
| Source inventory, budget, declarations, links | `python3 system/evals/validate_suite.py` | passed | `2026-10-23T08:14:25.371505+00:00` | `.scratch/B18-lesson-ladder/check-4.log` |
| Protocol registry and package closure | `python3 scripts/validate-protocols.py --plugins .scratch/B18-lesson-ladder/plugins` | passed | `2026-10-23T08:14:26.176835+00:00` | `.scratch/B18-lesson-ladder/check-5.log` |
| Whitespace | `git diff --check` | passed | `2026-10-23T08:14:26.261387+00:00` | `.scratch/B18-lesson-ladder/check-6.log` |

AC-1: ordered ladder, preference for existing enforcers, higher-rung rationale, proof and evidence binding are source-tested. AC-2: an authored empty-recipient incident fixture runs an actual subprocess check against buggy code (`all([])` incorrectly accepts the list), fails with `AssertionError: True is not false : empty recipient list accepted`, then runs the unchanged check against the correction and passes all three assertions. Old/corrected source hashes, unchanged check hash, exact commands, timestamps and outputs are retained in `check-1.log`. AC-3: a documented tone/judgment lesson is explicitly marked **instruction fallback** with its enforcement limitation and desired behavior; a source assertion protects that example and the narrow-scope routing. The fourth test builds a standalone skill and validates the new evidence-contract link and transitive package closure.

Results: 48 source/package tests passed (including four new B18 tests and integrated B1/B2/B3/B4/B5 checks); 11 B19 evidence tests passed; all 10 packages built separately in `.scratch/B18-lesson-ladder/plugins`; all 43 source skills and protocol registry/package closure passed. The initial pre-edit focused run failed with one missing-ladder error and one missing-fallback assertion; it is source-contract red evidence only (`red.log`). The scripted old-code regression is separate behavioral evidence for the authored example, not a real incident or a model transcript. Model compliance and automated choice among rungs were not measured; the instruction fallback's judgment is checked structurally, not by pretending a deterministic test can enforce respectful tone.

The existing evidence checker passed at `2026-10-23T08:16:32.529659+00:00` using `.scratch/B18-lesson-ladder/evidence.json`, `--base sha256:c7beb7f92cf424ad733c46881c97050940847f7517818058f51a95347e45fe10` and `--revision sha256:151aa7e20865c90ef5fa669a61ebf7b7002b7875a31d95711836402be1750504`; raw output is `binding-check.log`. Unrelated baseline files are byte-for-byte preserved, and no files are staged. Generated repository `plugins/` and marketplace remain unchanged. No commits, installations, pushes, publication, or subagents. Status is implemented, independent review pending. Next step: review this three-file contribution and regenerate integrated outputs in the parent build.

## Parent acceptance

2026-10-23: reconciled source passed canonical plugin build, derived-surface check, protocol and suite validators, 91 eval tests and 19 contract tests. [Independent review](../evidence/third-batch-review.md) found no blockers. Constraint scanning remains heuristic; fixture checks do not prove general model compliance. Canonical integration resolved shared-file conflicts and retained all provenance sections.
