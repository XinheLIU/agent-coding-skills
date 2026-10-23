# B17-trigger-fixtures: Add trigger fixtures with near-misses and collision pairs

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: pending
Readiness: needs-design
depends_on: B1-catalog-budget
affects: per-skill `evals/trigger-fixtures.json`; a runner in `system/evals/`
Effort: M

## Scope

Nothing checks whether a description triggers the right skill.

For every model-invocable skill, add at least 8 should-trigger and 8 should-not queries, including near-misses that name the neighboring skill. Pin the router to a weak model. Add reciprocal "When NOT to use" pointers for collision pairs, starting with `acs-trace-requirements` ↔ `acs-review-code-quality` and the four questioning skills.

## Inputs

- Analysis: §10 B17.
- Source: PM-Skills `deliver-prd/evals/trigger-fixtures.json`.

## Verification

- Every model-invocable skill has a fixture file with both classes and at least one near-miss.
- The runner reports precision and recall per skill and fails under a set threshold.
- Collision pairs route correctly on the weak model.

## Blockers

Description text must be final first; B1 owns it.

## Coordination proposal

B1 owns descriptions; B16 owns the harness runner. Land B1, then B17, then wire into B16.

## Accepted execution rulings

Recorded before implementation on 2026-10-23. B17 owns trigger fixtures and a configurable, host-independent router runner; B16 owns the broader behavioral harness. Weak-model selection and budget remain user-owned and pending: implement independent artifacts, do not fabricate predictions or claim live metric success. B1 descriptions and invocation flags remain unchanged.

The four questioning collision participants are `acs-challenge-approach`, `acs-review-code-quality`, `acs-design-interaction-flow`, and explicit-only `acs-validate-demand` (the B2 caller set). Supervisor confirmed reciprocal pointers across all four, automatic fixtures for all model-invocable skills, and separate explicit-invocation fixtures for demand. Automatic routing excludes explicit-only skills; a casual mention never grants invocation. Separate automatic and explicit metrics.

Parent rulings retained without expanding this ticket: B23 uses a stdlib Python CLI under `scripts/`, read-only by default, reusing B14/B19; B11 observability belongs in `acs-design-contracts`; B10 consumers declare verification commands/environments and unset values block execution, with local mock/scratch/dry-run checks only and no external PR/merge/deploy. B7 review fix rounds remain distinct from B8 operational retries; preserve authorization and source freshness. No subagents, installs, commits, pushes, publication, or corpus edits. Generated outputs stay in scratch. Shared protocol changes are not needed.

## Evidence

Implemented 2026-10-23; status remains `in_progress`, readiness `needs-review` pending independent acceptance and the user-owned measured gate. Integrated dirty baseline captured before edits: 1,144 file copies plus SHA-256 manifest retained outside the repository for contribution-only integration. Baseline manifest fingerprint: `dc603f74f10df1892081b730dccd3df08e93ba1ea0196dbf16cb8642359d631a` (SHA-256 of sorted-key JSON records). Exact 46-file contribution list and baseline copies accompany the implementation artifact; inherited changes are not included.

### Implementation

- Added 34 per-skill fixture files: 33 automatically invocable skills each have eight automatic positives and eight automatic negatives; demand has eight explicit positives, eight neighbor negatives, and two automatic abstention cases. Extra explicit demand near-misses on the three automatic questioning callers bring the total to 552 queries.
- Added reciprocal body links across all six questioning pairs plus trace/review. The compact interaction-flow body uses shortened link labels; validation resolves targets rather than requiring duplicate name text. All descriptions and invocation flags remain unchanged (3,720-byte automatic catalog).
- Added the stdlib `system/evals/trigger_evals.py` runner, unconfigured JSON config, usage documentation, and regression coverage. Default is a read-only dry plan (1,656 calls at three repetitions, zero completed). Execution requires explicit pinned model, adapter argv, and call budget. Labels/neighbor/target are withheld from adapter requests; metrics split automatic and explicit cases. Threshold and reciprocal neighbor gates fail incorrect routes. Partial/invalid/mismatched-model/unauthorized/source-stale runs are `void`, with raw partial observations and no metrics. No retries or external skill actions.
- Added compaction assertions for collision pointers. Kept all pointers inside the existing core marker and shortened only wording in interaction-flow to preserve the conservative bound after package link expansion. Final generated `acs-design` interaction-flow is 4,994 bytes; review source/plugin/standalone pass the configured local tokenizer check. No protocol changes or generated tracked output.

### Commands and results

All generated artifacts and command logs are under `.scratch/B17-trigger-fixtures/` and copied alongside the implementation report. Commands run from the worktree root:

| Command | Result |
| --- | --- |
| `python3 system/evals/trigger_evals.py --check` | PASS: complete coverage and reciprocal links. |
| `python3 system/evals/trigger_evals.py --output .scratch/B17-trigger-fixtures/dry-run.json` | PASS: `dry-run`, 552 queries, 1,656 planned/0 completed calls, no metrics. |
| `python3 -m unittest discover -s system/evals/tests -p 'test_trigger_evals.py' -v` | Initial 14 tests passed; final 15 tests pass within full and affected suites, including real local JSON subprocess transport and CLI failure/void exits. Mock responses only. |
| `PYTHONPATH=system/evals/tests python3 -m unittest -v test_trigger_evals test_compaction_safe_bodies test_catalog_budget test_packages test_questioning test_review_quote_gate test_security_evidence` with configured local compaction environment | PASS: 56 tests, no skips. Final shorter interaction wording also covered by subsequent full run. |
| `python3 -m unittest discover -s system/evals/tests -p 'test_*.py' -v` with the same local compaction environment | 125 tests, 124 pass; one inherited scope-posture string mismatch fails. B17 and compaction/package tests all pass. |
| `python3 -m unittest discover -s system/evals/evals -p 'test_*.py' -v` | PASS: 19 contract/evidence tests. |
| `python3 scripts/build-plugins.py --output .scratch/B17-trigger-fixtures/plugins` | PASS: scratch-only package generation. |
| `python3 scripts/build-plugins.py --output .scratch/B17-trigger-fixtures/plugins --check` | PASS: generated surfaces current. |
| `python3 scripts/validate-protocols.py --plugins .scratch/B17-trigger-fixtures/plugins` | PASS: registry, links, and regenerated package closure. |
| `python3 system/evals/validate_suite.py` | PASS: 43 skills, inventory/catalog budget/declarations/links. |
| `git diff --check`; `git diff --cached --name-only` | PASS; no staged files. |

The local compaction environment used `ACS_COMPACTION_PYTHON`, `ACS_COMPACTION_PYTHONPATH`, and `ACS_COMPACTION_TOKENIZER` supplied by the parent; exact machine paths remain only in the external implementation report. Tokenizer SHA-256: `c241737df24b4e7f7c9af4fdcee29a0ca903dcb288a8b753bc346a3092911767`. Review source: 2,083 tokens; relocated standalone/plugin: 2,205/2,196. The 7,083-token output belongs to the intentional overflow negative test.

Initial regression runs exposed B17 pointer placement and expanded-link overflow; both were repaired without changing thresholds. The remaining failure is `test_scope_postures.ScopePostureTests.test_phase_c_defines_postures_and_record_contract`: it expects `Raise concerns about it once` while baseline shape-solution says `Raise concerns once`. Both source and test are byte-identical to the pre-edit snapshot; running the five scope-posture tests against that snapshot reproduces exactly this single failure. Neither unrelated file was changed.

### Source identity

Contribution source fingerprint, excluding this evidence ticket: `ef625f97fc951278d3af1a5638c7d2240bc99f1357637a5378f81da0d9f7c2af`. Algorithm: sorted contribution-relative paths, each hashed as path + NUL + SHA-256(file bytes). Runner fingerprint covering all 43 skill bodies, all fixture files, and runner: `b73ab578ecbbdf24a73a8e7c15cc31ec1c80d43e7ba281ccec9ec9e54f24f18d`; reproduced by the final dry-plan command. Configuration and runner-only hashes are in that report.

Read-only upstream SHA-256 identities:

- `references/README.md`: `0ab530acc0ff6c3722be1beeee41103639fad3c8e0dfe0d8afbb8ef7dcaeadbb`.
- `references/ANALYSIS.md`: `6c4fa9615d90f74fc4a05a53f0c12ac7382af0578ae80adc367a01c339c30fb9`.
- `references/pm-skills/skills/deliver-prd/evals/trigger-fixtures.json`: `f457b8eb86b5d12a48115f83d5e18fd3ec96c0a1dcea6cb09a53ce3439847255`.
- `references/pm-skills/scripts/run-trigger-evals.mjs`: `fe396b1895c5a343d01a92793394a21dfb123c17faac376edcc8471b5c5c4945`.

### Explicitly unverified criteria

Actual weak-model precision/recall and collision correctness remain unverified pending user model and budget selection. Deterministic success establishes fixture coverage and runner mechanics only. The generic adapter validates the reported model identity but cannot attest the provider behind that response; retain adapter and provider evidence for the measured gate. Fixture judgments and broad routing reliability still need independent review and measurement. The call ceiling is not a monetary spending cap. No live predictions, API requests, host installation, commits, publication, or skill execution occurred.

## Integrated implementation and remaining gate

Source implementation reviewed; 35 automatically discoverable skills plus explicit-only demand have 584 cases. Release-tail fixture coverage added at integration. Both review findings fixed and all 16 trigger tests pass. Actual weak-model precision/recall/collision evaluation remains unmeasured pending model and call-budget selection; do not treat mock outputs as measured success.
