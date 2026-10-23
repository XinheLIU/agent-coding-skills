# B6-review-quote-gate: Make unquotable review findings unverified and prefer UNVERIFIABLE over DONE

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/test/review/acs-review-code-quality/SKILL.md`; `system/skills-src/design/technical/acs-trace-requirements/SKILL.md`
Effort: S

## Scope

The review carries confidence scores (`:209`, `:260`) and an evidence-identity section (`:165`), but a finding needs no quoted line.

Add two rules:
- "If you cannot quote the motivating line, the finding is unverified": cap its confidence at 5 and mark it unverified.
- "Code that handles a deliverable is not the deliverable": when the artifact itself cannot be reached, report UNVERIFIABLE, not DONE.

Wire the same two rules into `acs-trace-requirements` so the compliance axis cannot claim DONE on a handler.

## Inputs

- Analysis: §6.6, §10 B6.
- Sources: gstack `review:720-735`, `ship/sections/plan-completion.md:90`.

## Verification

- A fixture finding with no quoted line is capped at confidence 5 and labelled unverified.
- A fixture where only a handler exists returns UNVERIFIABLE.
- Both skills cite the same rule text; no duplicate wording drift.

## Blockers

none

## Coordination proposal

`acs-review-code-quality` is also edited by B2 (line 340) and B13 (security lens). Keep edits in separate sections.

## Evidence

Implemented 2026-10-23; independent review pending. Both skills cite identical rule text and the canonical `engineering-memory.md#review-evidence-gate` (protocol version 1.2.0; registry synchronized). Unquoted findings remain unverified at ≤ 5/10, appendix-only, without raising lower confidence or driving priorities/verdicts. Trace ledger findings map to LOW. Artifact access failures use UNVERIFIABLE, while confirmed missing/incomplete artifacts retain MISSING/PARTIAL; REACHABLE remains static wiring evidence. Existing questioning, evidence identity, and Use when descriptions are preserved.

### Baseline and exact delta

Baseline HEAD: `fbc81fd046ea0c2093e4516cc8dbdd289d473395`. The starting worktree was dirty with integrated B1/B2/B3/B4/B5/B14/B19 changes. Baseline captured before edits in `.scratch/B6-review-quote-gate/{baseline.json,baseline-status.txt,baseline.diff,baseline-staged.diff,baseline/}`. Baseline manifest SHA256: `8411c493d1d945b4dbaa560a8f5bf6648806430c62589c7642dee6c6e260df2a`. All non-B6 baseline files and symlink targets remain unchanged.

Exactly these eight files changed relative to that starting baseline (not relative to HEAD):

- `system/THIRD_PARTY_NOTICES.md`
- `system/evals/fixtures/acs-review-quote-gate.json`
- `system/evals/tests/test_review_quote_gate.py`
- `system/protocols/engineering-memory.md`
- `system/protocols/registry.json`
- `system/skills-src/design/technical/acs-trace-requirements/SKILL.md`
- `system/skills-src/test/review/acs-review-code-quality/SKILL.md`
- `docs/changes/acs-corpus-alignment/tasks/B6-review-quote-gate.md`

The existing `system/skills-src/context/acs-init-context/references/engineering-memory.md` symlink was not edited; its resolved bytes follow the canonical protocol update. No generated output was written into tracked `plugins/`. No files are staged; no commits, installs, pushes, publication, or subagents were used.

### Acceptance evidence

- Unquoted fixture: initial confidence 9 → authored result 5, unverified, appendix-only; initial 3 remains 3. Paraphrase rejected; quoted low-confidence evidence does not inflate confidence.
- Handler-only fixture: handler and passing handler tests exist but the required publishing artifact is unreachable → UNVERIFIABLE with a specific next check. Missing/incomplete/present cases remain distinct.
- Seven focused tests check shared wording and links, precedence before questioning, appendix and ledger integration, authored cases and invalid mutations, provenance, and both standalone skills after relocation. Package validation confirms copied canonical gate content and link closure without symlinks.
- Fixtures are authored contract examples, not fabricated transcripts. Tests execute Python validation and package materialization; they do not establish live model compliance.

### Commands and results

Environment: Python 3.14.6; stdlib and existing repository tools only. Exact argv and output SHA256 values are retained in `.scratch/B6-review-quote-gate/validation.json`; raw logs are adjacent.

- `python3 -m unittest discover -s system/evals/tests -p test_*.py -v` → exit 0; `.scratch/B6-review-quote-gate/validation-1.log` SHA256 `509975af19bf754c19a7fcbfeb805d30fc4b69d6f2a7122351d00e394b23f0a0`.
- `python3 -m unittest discover -s system/evals/evals -p test_*.py -v` → exit 0; `.scratch/B6-review-quote-gate/validation-2.log` SHA256 `78efe8e28db03bdb6c1d31b6bdae4faaeaf4bb912d7ba1bc141814888595d088`.
- `python3 system/evals/validate_suite.py` → exit 0; `.scratch/B6-review-quote-gate/validation-3.log` SHA256 `24f08422067a2ac854b1ba7702ef14e44ba5be239ceb609c78dabcab80d28e9c`.
- `python3 scripts/build-plugins.py --output .scratch/B6-review-quote-gate/plugins` → exit 0; `.scratch/B6-review-quote-gate/validation-4.log` SHA256 `32d7559f7dc01da08058e82504290fb5223ca21a30585e4abd1e9a1b13059964`.
- `python3 scripts/validate-protocols.py --plugins .scratch/B6-review-quote-gate/plugins` → exit 0; `.scratch/B6-review-quote-gate/validation-5.log` SHA256 `febb7838d6d0c19d767aa81f8f704dc7838c9d2e9a9325ab613f36e5daac7eea`.
- `git diff --check` → exit 0; `.scratch/B6-review-quote-gate/validation-6.log` SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `python3 -m unittest discover -s system/evals/tests -p test_review_quote_gate.py -v` → exit 0; `.scratch/B6-review-quote-gate/validation-7.log` SHA256 `dd51a0646d7cc4810c7098d553314cbcdcb89a6b1454428a8c9248b2f5a60d8d`.
- `python3 system/evals/validate_suite.py` → exit 0; `.scratch/B6-review-quote-gate/validation-8.log` SHA256 `24f08422067a2ac854b1ba7702ef14e44ba5be239ceb609c78dabcab80d28e9c`.
- `python3 scripts/build-plugins.py --output .scratch/B6-review-quote-gate/plugins` → exit 0; `.scratch/B6-review-quote-gate/validation-9.log` SHA256 `32d7559f7dc01da08058e82504290fb5223ca21a30585e4abd1e9a1b13059964`.
- `python3 scripts/validate-protocols.py --plugins .scratch/B6-review-quote-gate/plugins` → exit 0; `.scratch/B6-review-quote-gate/validation-10.log` SHA256 `febb7838d6d0c19d767aa81f8f704dc7838c9d2e9a9325ab613f36e5daac7eea`.
- `git diff --check` → exit 0; `.scratch/B6-review-quote-gate/validation-11.log` SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The full source/package suite passed 51 tests; evidence-binding suite passed 19 tests; focused B6 suite passed 7 tests. Source validation passed all 43 skills, catalog budget, declarations, links and anchors. Scratch builder and registry/package-closure validation passed. The existing TDD suite intentionally logs a failing red-phase child test; its enclosing test and suite passed. After a final wording clarification, the focused suite, source validator, builder, package validator, and whitespace check were rerun successfully.

A one-off baseline audit initially asserted seven changed byte streams and failed because it followed the unchanged engineering-memory symlink, observing eight streams. The corrected audit compares symlink targets separately and passed: seven edited source/test files plus this ticket; one unchanged alias observes the target update. This was an audit-script counting error, not a product/test failure.

### Fingerprints and limitations

Final source hashes (ticket excluded to avoid self-reference):

- `system/THIRD_PARTY_NOTICES.md`: SHA256 `1ad492764951d6dd545dd697e028c67375859c30995c4ffb33fc4a173c357774`.
- `system/evals/fixtures/acs-review-quote-gate.json`: SHA256 `c43adac15d9a6f06b63285d2c9fada1c33bb3757a5b88db57a465b42b9aa16f7`.
- `system/evals/tests/test_review_quote_gate.py`: SHA256 `414c44d327a988def047a96d7f06b54feaace37ebcbd7d96d82c838069364fa8`.
- `system/protocols/engineering-memory.md`: SHA256 `6d5b73e85e417fd36de3b80b0d3d196ff09e8901d8541b038c30b9b191282638`.
- `system/protocols/registry.json`: SHA256 `6ee691df10555a5ff3fbbd7a3c713a0a66a4c7917b3dc69415e4fc265f21b90e`.
- `system/skills-src/design/technical/acs-trace-requirements/SKILL.md`: SHA256 `1843f62d146f28b28279ff8d144a5fe79a0509a69ff4979efd113bddb1126266`.
- `system/skills-src/test/review/acs-review-code-quality/SKILL.md`: SHA256 `e1064cae72517f34daa1cd35511fa0bd4d09d7069d8613334d3dc3635cf21821`.

Scratch build manifest SHA256: `b92af82efea6ce502eba2412b122fb28f2b47c5db2634a5d139a3008faf4e2a3` (`.scratch/B6-review-quote-gate/build-manifest.json`). Validation manifest SHA256: `8d742948417f78f16abe3e7e4666d87306a1c02ab22b5d18b01a2f6b8cc344dc`.

No live model/host review was run; fixture output is specified, not observed agent judgment. Independent reviewer gate remains pending. Generated package output stays under `.scratch/B6-review-quote-gate/plugins` for validation; parent owns the final build/integration. No scope or infrastructure decision is blocked.

## Parent acceptance

2026-10-23: reconciled source passed canonical plugin build, derived-surface check, protocol and suite validators, 91 eval tests and 19 contract tests. [Independent review](../evidence/third-batch-review.md) found no blockers. Constraint scanning remains heuristic; fixture checks do not prove general model compliance. Canonical integration resolved shared-file conflicts and retained all provenance sections.
