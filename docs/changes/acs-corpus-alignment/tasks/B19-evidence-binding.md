# B19-evidence-binding: Bind evidence to a command and a revision

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/protocols/orchestration.md` evidence contract; collect step; evidence template
Effort: M

## Scope

`collect` rejects evidence that "claims green without commands" (`orchestration.md:25`), but nothing checks the command ran against the current revision.

Require each evidence row to carry the exact command, the revision or tree fingerprint, and a timestamp. `collect` rejects a row whose revision is not the ticket's current one. Record BASE at dispatch so the comparison has a target.

## Inputs

- Analysis: §7.5, §8.5 U3, §10 B19.
- Sources: gstack `ship` (`--expect-cmd`, `--max-age`); pstack's SHA-keyed ledger.

## Verification

- A stale-revision fixture is rejected with a named reason.
- A valid row passes with command, revision and timestamp.
- No evidence example omits a revision.

## Blockers

none

## Coordination proposal

Feeds B7 (BASE) and B23 (verify command). Land before B7.

## Evidence

Implemented source contract; verification is **incomplete** because isolated package generation is blocked. No actual model-behavior or host-dispatch run was performed. The following are deterministic executable fixtures and structural checks, not fabricated agent transcripts.

### Source identity and scope

Checkout HEAD: `fbc81fd046ea0c2093e4516cc8dbdd289d473395` (the checkout is dirty, so HEAD alone is not the tested revision).

Tested source fingerprint: `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb`, measured 2026-10-23; final focused checks completed by `2026-10-23T07:48:18Z`. Fingerprint covers 253 source/input paths, including untracked implementation and tests. Evidence/ticket records and generated plugins are excluded. Reproduce from the repository root:

```sh
python3 - <<'PY'
import hashlib
from pathlib import Path
roots = [Path('system'), Path('scripts'), Path('catalog')]
paths = sorted(p for root in roots for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
paths += [Path('.gitignore'), Path('LICENSE')]
manifest = ''.join(f'{p.as_posix()}\0{hashlib.sha256(p.read_bytes()).hexdigest()}\n' for p in sorted(paths))
print('sha256:' + hashlib.sha256(manifest.encode()).hexdigest())
PY
```

Paths and per-file SHA-256 values are sorted and joined with NUL/newline separators; symlinks inside the source scope are read as target bytes. The read-only external corpus is outside the scope. Preexisting `system/THIRD_PARTY_NOTICES.md` bytes are included unchanged. No Git index changes were made.

### Criterion-to-check mapping

All commands below ran from this worktree root against the source fingerprint above unless explicitly identified as an earlier red run or temporary mutation. Results were recorded on 2026-10-23.

| Criterion | Exact command / fixture | Result | Tested revision |
| --- | --- | --- | --- |
| Stale revision rejected with named reason | `python3 -m unittest discover -s system/evals/evals -p 'test_evidence_binding.py' -v`; `test_stale_revision_has_named_rejection`, `test_each_row_is_checked` | PASS; stale rows return nonzero with `STALE-REVISION` | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| Valid command/revision/timestamp row passes | Same command; `test_current_completion_passes_even_when_base_differs`, `test_offset_timestamp_is_valid` | PASS; dispatch BASE may differ from tested completion tree | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| No evidence example omits revision | Same command; `test_template_example_has_complete_revision_binding` | PASS; every JSON example in the new shared template validates. Protocol/dispatch/collect/TDD instructions route to this single template | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| Required fields, timestamps, provenance and failed checks | Same command; remaining negative fixtures | PASS; 11 focused tests total | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| Shared regression checks | `python3 -m unittest discover -s system/evals/evals -p 'test_*.py' -v` | PASS; 19 tests | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| Protocol registry, links and existing package closure | `python3 scripts/validate-protocols.py` | PASS; existing generated packages only, not regenerated B19 packages | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| Suite inventory and source declarations | `python3 system/evals/validate_suite.py` | PASS; 43 source skills | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| Generated plugin refresh | `python3 scripts/build-plugins.py` | BLOCKED / exit 1: builder resolves external references symlink outside worktree | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |
| Inventory and package fixtures | `python3 -m unittest discover -s system/evals/tests -p 'test_*.py' -v` | FAIL; 16 tests, 13 pass, 1 failure and 2 errors from the same builder/reference-path blocker | `sha256:0e1e889da61e9b2dfd515cfef9573a2a1cb898c9b4e8df3cea7bda518e1a2fcb` |

The initial focused run failed before checker/template creation (34 assertions and one missing-template error); this is only missing-artifact evidence. A stronger mutation check copied the completed checker to a temporary directory, replaced `if row["revision"] != revision:` with `if False:`, and ran `test_stale_revision_has_named_rejection`: the fixture failed because the stale row incorrectly exited 0. The mutation was confined to the temporary copy; source bytes stayed unchanged. This establishes red capability for the actual stale-evidence rule.

`git diff --check` passed. `git diff --cached --name-only` was empty. Preexisting changelog/notices and other copied plan files were preserved.

### Blocker and decisions

The builder raises `ValueError: Linked resource escapes repository: /Users/xhl/GitHub/skills/agent-coding-skills/references/OpenSpec/docs/concepts.md`. With supervisor authorization, only its partial generated-plugin changes were restored to the initially clean baseline; no generated files were hand-edited. The supervisor directed continuing read-only checks and leaving package generation for parent reconciliation in the canonical checkout. No execution-mode switch, reference edit, builder change, dependency install, commit, or publication was performed.

The supervisor approved a minimal reusable stdlib row checker within B19 scope. BASE is immutable dispatch provenance; collection compares rows to the independently resolved completion tree, not BASE. The checker validates recorded rows, not execution truth or criterion completeness; the coordinator retains those responsibilities. No B7 review lifecycle or B23 command-discovery mechanism was added.

Next action: parent regenerates plugins in a supported checkout, reruns package fixtures and validators, and obtains independent review before marking this ticket done.

## Integrated acceptance

2026-10-23: source reconciled into canonical checkout; `python3 scripts/build-plugins.py`, `python3 scripts/validate-protocols.py`, `python3 system/evals/validate_suite.py`, and affected unittest suites passed. Independent first-batch review found no blocking source defects for this ticket. Prior isolated packaging blocker is resolved by canonical generation. Exact commands and logs: `.scratch/acs-corpus-alignment/verification.json`; review run `66a6103a-dd18-410b-b984-c84346a08432`. Scope remains deterministic contract verification, not proof of model reliability.
