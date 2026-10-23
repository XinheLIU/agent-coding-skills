# B11-observability: Make observability answer on-call questions

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/design/technical/acs-design-contracts/SKILL.md`
Effort: M

## Scope

Instrumentation appears as a contract concern, but nothing ties a signal to a question an on-call engineer asks.

Add a section: write two to four on-call questions before instrumenting; map each signal to a question; give each alert a three-line runbook and test-fire it once; prove that an induced failure can be found from telemetry alone.

## Inputs

- Analysis: §10 B11.
- Source: Addy `observability-and-instrumentation`.

## Verification

- The contract requires the question list before signal names.
- A fixture design produces 2–4 questions, a signal map and runbooks.
- One induced-failure exercise is diagnosable from telemetry alone.

## Settled direction

Parent ruling recorded before implementation: B11 belongs in `acs-design-contracts`; it is independent of B10. Keep observability requirements in CON and hand verification design to TST. Existing authorization and source freshness remain binding. Exercise failures and alerts only in a local mock/scratch environment here; external notification, PR, merge, and deploy actions are outside this contribution.

Other parent rulings stay with their owners: B23 uses a stdlib Python CLI under `scripts/`, read-only by default, reusing B14/B19; B10 requires declared verification commands and environments and blocks execution when unset; B7 review fix rounds differ from B8 operational retries; B16/B17 model and budget selection remain pending, so authored fixtures cannot establish live model metrics. No implementation of those tickets is included here.

## Integration baseline

Captured the integrated dirty tree before any edits in `.scratch/B11-observability/baseline/`, with `baseline-manifest.json`, `baseline-status.z`, `baseline.diff`, and `baseline-head.txt` alongside it. Contribution changes must be measured against that snapshot, not against HEAD. Generated packages and validation logs stay in scratch. No staged files at entry.

## Evidence

Implemented the Observability subsection in `acs-design-contracts`, with CON ownership and TST/implementation handoff. Added an authored two-question checkout design, one mapped structured signal, a linked three-line runbook, and an executed stdlib local mock. The healthy request does not fire; the injected provider timeout fires the alert into a temporary inbox; the diagnostic function receives only telemetry and a runbook query and returns the affected request, path, dependency, and timeout cause. Negative cases cover question count/order, invalid or uncovered mappings, missing runbook content, unset execution settings, and missing/ambiguous telemetry. Package relocation retains the requirements.

Commands and results (2026-10-23):

- `python3 -m unittest discover -s system/evals/tests -p test_design_contracts_observability.py -v`: PASS, 4 tests. Telemetry, receipt, diagnosis and source/fixture/runner SHA256s retained in `.scratch/B11-observability/focused-tests.log`.
- `python3 scripts/build-plugins.py --output .scratch/B11-observability/plugins`: PASS.
- `python3 scripts/build-plugins.py --output .scratch/B11-observability/plugins --check`: PASS.
- `python3 scripts/validate-protocols.py --plugins .scratch/B11-observability/plugins`: PASS.
- `python3 system/evals/validate_suite.py`: PASS, 43 source skills including catalog budget.
- `python3 -m unittest discover -s system/evals/tests -v`, with supplied local `ACS_COMPACTION_*` configuration: 114 tests, 113 pass, 1 baseline failure. Compaction checks pass; tokenizer SHA256 `c241737df24b4e7f7c9af4fdcee29a0ca903dcb288a8b753bc346a3092911767`.
- `python3 -m unittest discover -s .scratch/B11-observability/baseline/system/evals/tests -p test_scope_postures.py -v`: reproduces the same unrelated failure, 5 tests/1 failure. `test_phase_c_defines_postures_and_record_contract` expects `Raise concerns about it once`; the captured baseline says `Raise concerns once`. No B22 changes made.
- `git diff --check`: PASS; `git diff --cached --name-only`: empty.

Upstream provenance: Addy `observability-and-instrumentation`, pinned `aeac41d`, read-only source SHA256 `e7fcb0820306d46268de9594d676ad98e35040858926c412b7000faa52a61f87`. Attribution is recorded in `system/THIRD_PARTY_NOTICES.md`. Baseline HEAD: `fbc81fd046ea0c2093e4516cc8dbdd289d473395`; the baseline also includes previously integrated uncommitted changes. Source fingerprint manifests and contribution-relative patch are retained in `.scratch/B11-observability/`.

## Acceptance limits

Ready for independent review, not accepted. Static contracts and an authored local mock pass; no live model was asked to generate the design or diagnose the failure, no production or staging telemetry backend was exercised, and no external alert delivery was tested. Those behavioral and operational criteria remain unverified. The local fixture proves only the named mock exercise; it does not establish model performance or operational readiness. The unrelated baseline regression remains open with its owning ticket.

## Parent acceptance

2026-10-23: integrated source accepted after 152 suite tests, build/check, both validators and [independent review](../evidence/fifth-batch-review.md). Acceptance is the source contract and explicitly described local scripted exercises. It does not certify live agent/host enforcement, real PR/release actions, or production telemetry. No external operation was performed.
