# B4-tdd-seams: Add the seam rule and move refactoring out of the TDD loop

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/build/acs-tdd/SKILL.md`
Effort: S

## Scope

`acs-tdd` mentions "public seam" once (line 29) and keeps refactoring inside the loop (step 5).

Add:
- a seam rule: write a test only at a seam named in an accepted TST, or one the user confirmed when no TST exists;
- the three named anti-patterns and "expected values come from an independent source of truth";
- move refactoring out of the loop into review, so a red-green loop ends at green.

Keep the criterion → test → revision mapping unchanged.

## Inputs

- Analysis: §6.1, §8.8 G5, §10 B4.
- Source: Pocock `tdd:20-38`, `tdd/tests.md`.

## Verification

- `grep -n "seam" system/skills-src/build/acs-tdd/SKILL.md` shows the rule with both conditions.
- The loop steps no longer contain a refactor step; the review handoff names refactoring.
- A scripted ticket run produces a red-to-green transcript whose test sits on a confirmed seam.

## Blockers

none

## Coordination proposal

`acs-tdd` is also referenced by B12 and B19; those add checks around it and do not rewrite these sections.

## Evidence

Implemented only the TDD preparation, anti-pattern, loop, and review sections plus focused fixtures. The catalog description, evidence-binding step, and criterion → test/evidence → revision handoff are byte-for-byte preserved from the integrated baseline. Refactoring now belongs to review, with its Current State/ADR contract retained.

Provenance: adapted the seam and anti-pattern principles from Matt Pocock `49dd158`, `skills/engineering/tdd/SKILL.md:20-38` and `tests.md`, read-only under `/Users/xhl/GitHub/skills/agent-coding-skills/references/matt-pocock/`; the accepted-TST adaptation follows local analysis §10 B4. No reference files changed.

Baseline: HEAD `fbc81fd046ea0c2093e4516cc8dbdd289d473395` plus the pre-existing B1/B2/B14/B19 working tree captured at `2026-10-23T16:00:12.338533+08:00`. `.scratch/B4-tdd-seams/baseline.diff`, `baseline-status.txt`, and `baseline-hashes.json` record it; the hash-manifest SHA-256 is `7ca64caed87db00878dd5aaca448e49165555c1daba505294e430a9fa1da05d2`. HEAD alone is not the dispatch identity.

Validation source identity for every row below: `sha256:e3c69715192d8e40c818d6475814bde812c4ec47ae192a5a39df76f6f525c1a3`. Fingerprint scope: all files beneath `system/`, `scripts/`, and `catalog/`, dereferencing symlinks and excluding `__pycache__`/`.pyc`; SHA-256 of UTF-8 `json.dumps(path_to_file_sha256, sort_keys=True)`. The exact manifest is `.scratch/B4-tdd-seams/validation-source-hashes.json`; `.scratch/B4-tdd-seams/run_checks.py` records the method and verifies source stability before/after each command. Environment: Python 3.14.6, macOS 26.6.2 arm64, `PYTHONDONTWRITEBYTECODE=1`; commands run from this worktree root.

| Criterion | Exact command | Result | Completed (UTC) | Raw output |
| --- | --- | --- | --- | --- |
| AC-1/AC-2/AC-3 | `python3 -m unittest discover -s system/evals/tests -p test_tdd_seams.py -v` | passed | `2026-10-23T08:02:20.955977+00:00` | `.scratch/B4-tdd-seams/check-1.log` |
| Preserve B19 bindings | `python3 -m unittest discover -s system/evals/evals -p test_evidence_binding.py -v` | passed | `2026-10-23T08:02:23.094233+00:00` | `.scratch/B4-tdd-seams/check-2.log` |
| Package build | `python3 scripts/build-plugins.py --output .scratch/B4-tdd-seams/plugins` | passed | `2026-10-23T08:02:23.964062+00:00` | `.scratch/B4-tdd-seams/check-3.log` |
| Source validation | `python3 system/evals/validate_suite.py` | passed | `2026-10-23T08:02:24.209176+00:00` | `.scratch/B4-tdd-seams/check-4.log` |
| Source/package closure | `python3 scripts/validate-protocols.py --plugins .scratch/B4-tdd-seams/plugins` | passed | `2026-10-23T08:02:24.921077+00:00` | `.scratch/B4-tdd-seams/check-5.log` |

AC-1 is the accepted-TST/user-confirmed seam rule and independent oracle/three anti-patterns. AC-2 is green-ending execution with refactoring in review and preserved mapping. AC-3 is the scripted ticket fixture: three focused tests passed overall; its real subprocess test fails with `AssertionError: 0 != 15`, then passes after changing only the implementation. Both phases retain separate file hashes, command, timestamp, and output in `check-1.log`. The accepted TST and worked example are authored fixture inputs, not a real user's approval or a model transcript. The fixture demonstrates the prescribed sequence mechanically; agent compliance was not measured. The no-TST user-confirmation branch is checked structurally only.

The existing B19 suite passed 11 tests. The suite validator passed all 43 source skills; builder produced all 10 packages; protocol/package closure passed. A direct comparison confirmed the preserved description, evidence-binding step and handoff, and the generated `acs-build/skills/acs-tdd/SKILL.md` contains the new seam and review rules.

B4 changed files only:
- `system/skills-src/build/acs-tdd/SKILL.md`
- `system/evals/tests/test_tdd_seams.py` (new; two source contract checks, one authored executable fixture)
- `docs/changes/acs-corpus-alignment/tasks/B4-tdd-seams.md` (this record)

Generated packages are separate in `.scratch/B4-tdd-seams/plugins`; repository `plugins/` and marketplace were not edited. Baseline hashes confirm all unrelated baseline files are preserved. No files staged; no commits, installs, pushes, publication, or subagents. Independent reviewer gate remains pending; parent should review this contribution and regenerate generated surfaces after integration.


## Parent acceptance

2026-10-23: canonical build and affected suite passed; independent review found no remaining issues. See [bounded model exercises and source review](../evidence/bounded-model-exercises.md). B2/B3 evidence is one actual bounded model turn each, not a reliability benchmark. B4 has real scripted red/green evidence; B5 requires an explicitly simulated transcript.
