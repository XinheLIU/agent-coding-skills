# B10-release-tail: Build the missing release tail: acs-ship and acs-release

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: B19-evidence-binding
affects: new `system/skills-src/deploy/acs-ship`, `acs-release`; `system/protocols/operations-memory.md`; registry, catalog, package mapping and release-tail tests
Effort: L

## Scope

`system/skills-src/deploy/` is empty and `workflows/deploy.md` is 27 lines with no skill behind it.

`acs-ship`: take a verified branch to an open PR. Rerun verification every time; only actions are idempotent. Explicit stop and never-stop lists. A bounded fix loop that ends in `converged: false`. A PR body with the smallest visual summary, evidence and a merge-danger call.

`acs-release`: take a merged artifact to production. Rollout stages, rollback thresholds and an error-budget gate; a dry run on first use; a readiness gate on current evidence; canary alerts only after two consecutive checks; "read server state after a merge error, never retry the merge".

Keep the existing rule that a rebuilt artifact cannot inherit verification.

## Inputs

- Analysis: §8.8 G7, §10 B10.
- Sources: gstack `ship`, `land-and-deploy`, `canary`; Addy `shipping-and-launch`; `operations-memory.md`.

## Verification

- `validate_suite.py` passes with two new skills registered.
- A scratch branch runs `acs-ship` and produces a PR body with evidence and the stop lists.
- A simulated failed merge reads state instead of retrying.
- `acs-release` dry run leaves production untouched and records `not released`.

## Settled rulings

Recorded before implementation: the consumer declares its exact verification commands and environments in `operations.checks` and `operations.constraints`; unset values block execution. This contribution uses local mock, scratch and dry-run checks only, with no external PR, merge or deployment. Existing authorization persists and source/artifact freshness remains mandatory. Review fix rounds are separate from operational retry counters; neither resets the other.

Adjacent parent rulings remain outside B10: B23 owns a stdlib Python CLI reusing B14/B19; B11 puts observability design in `acs-design-contracts`; B17 owns trigger fixtures/configurable runner. B16/B17 model and budget selection remains pending; no live model metric is claimed here.

## Blockers

Project-specific command/environment selection is a consumer prerequisite, not a guessed repository default. Independent agent execution and live release behavior remain unverified by local fixtures.

## Coordination proposal

`deploy.md` and `operations-memory.md` are shared with B11. Land B10 first; B11 extends the contract.

## Evidence

Implemented two discovery-linked skills, PR/release evidence templates, the `acs-deploy` package mapping/catalog entry, Operations v1.2.0 and deploy workflow routing. Generated output is scratch-only. No external PR, merge, deployment, commit, install or publication occurred; no files are staged.

### Tested source and baseline

Captured the complete integrated dirty baseline (1,144 file/symlink paths) before edits under `.scratch/B10-release-tail/baseline/`, with manifest and initial status alongside it. HEAD is `fbc81fd046ea0c2093e4516cc8dbdd289d473395`; HEAD alone does not identify the dirty tree. Baseline source fingerprint: `sha256:c4f361580c7b0f0963f204b97cad9fc474c31386f74a4af716828fd560b577bf`.

Final tested source: `sha256:e85351a19f3cc5d2bc58d2b50b674c2933094bc39b39ad7fd5d33acad1f16bb3`. Fingerprint method matches B19: sorted files beneath `system`, `scripts`, `catalog`, plus `.gitignore` and `LICENSE`; exclude `__pycache__`/`.pyc`, dereference source symlinks, join `relative path + NUL + SHA256(bytes) + newline`, then SHA256 the manifest. Ticket, logs and generated output are excluded. Per-file manifest, command completion timestamps and logs are under `.scratch/B10-release-tail/`.

### Acceptance checks (2026-10-23)

| Exact command | Result |
| --- | --- |
| `python3 -m unittest discover -s system/evals/tests -p 'test_release_tail.py' -v` | PASS, 5 tests: discovery, core rules, relocated checker/templates/shared semantics, authored positive/negative traces, local scratch-branch PR-body/evidence rehearsal |
| `python3 -m unittest discover -s system/evals/tests -p 'test_*.py' -v` | 114/115 pass; the only failure is preexisting `test_scope_postures.test_phase_c_defines_postures_and_record_contract` literal wording drift |
| `PYTHONPATH=.scratch/B10-release-tail/baseline/system/evals/tests python3 -m unittest test_scope_postures -v` | Same scope-posture failure against captured baseline; B10 leaves those files untouched |
| `python3 -m unittest discover -s system/evals/evals -p 'test_*.py' -v` | PASS, 19 tests including B19 positive/negative evidence checks |
| `python3 scripts/build-plugins.py --output .scratch/B10-release-tail/plugins` | PASS, including `acs-deploy` with two skills |
| `python3 scripts/build-plugins.py --output .scratch/B10-release-tail/plugins --check` | PASS, deterministic generated surfaces |
| `python3 scripts/validate-protocols.py --plugins .scratch/B10-release-tail/plugins` | PASS, registry/source/package closure |
| `python3 system/evals/validate_suite.py` | PASS, 45 skills; catalog descriptions total 3,720/5,000 bytes |
| `git diff --check` | PASS |
| `git diff --cached --name-only` | Empty |

Compaction regression used the configured cached Python/tokenizer environment, with tokenizer SHA256 `c241737df24b4e7f7c9af4fdcee29a0ca903dcb288a8b753bc346a3092911767`. Both new skill bodies also pass a tokenizer-independent 5,000-byte bound including shared injection and relocated links (plugin: ship 4,878 bytes; release 4,958 bytes). Initial focused tests caught a 5,153-byte standalone overflow and missing explicit release checker flags; both were corrected before final validation. The generated-boilerplate inventory assertion now expects 45 skills instead of 43.

### Behavioral limits and provenance

The scratch-branch rehearsal executes a real local check twice, fills the actual PR-body template, invokes the B19 checker, changes source and observes `STALE-REVISION`. It does not invoke an independent agent. Merge-error/readback, no-merge-retry, two-check canary and production-write-free dry run scenarios are authored fixtures with rejecting negative mutations, not live provider or model transcripts. Independent `acs-ship`/`acs-release` compliance, real PR opening, production deployment, rollback effectiveness and live metric success remain **unverified**. No deployment occurred: `not released`. Review acceptance remains pending.

Read-only source SHA256 fingerprints (collection-relative paths; full manifest in scratch):

- `gstack/source/ship/SKILL.md`: `0c76ef3ed1b4c700c740110ab52cf633f4322e017f30211afa1c1bf43782d0ff`
- `gstack/source/land-and-deploy/SKILL.md`: `7cb768c8dc78fbed2a591328a4c67cefbb8ca2602dcdd9225b1679ce2dbbdd1e`
- `gstack/source/land-and-deploy/sections/merge-and-deploy.md`: `fcf05e7cd9da94fdfcd1094d76adc95054d1e1059eddc9dfb88d2f2539cb7973`
- `gstack/source/canary/SKILL.md`: `f80821433175b1e2692074003b42cca6869d681e53faab1dc0bbae46e4627a9a`
- `addy-osmani/skills/shipping-and-launch/SKILL.md`: `726f3e546369db289160b8d42195590f00b6432887e17bf19070dcc9a347fe39`

ACS deliberately applies the approved stricter no-merge-retry rule even where upstream permits a narrow retry. Source provenance is retained in `system/THIRD_PARTY_NOTICES.md`; no upstream runtime was copied.

## Parent acceptance

2026-10-23: integrated source accepted after 152 suite tests, build/check, both validators and [independent review](../evidence/fifth-batch-review.md). Acceptance is the source contract and explicitly described local scripted exercises. It does not certify live agent/host enforcement, real PR/release actions, or production telemetry. No external operation was performed.
