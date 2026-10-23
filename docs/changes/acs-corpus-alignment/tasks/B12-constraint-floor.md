# B12-constraint-floor: Add a constraint floor that catches silenced checks

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/test/acs-analyze-test-gaps/SKILL.md` or a new test-phase skill; new `CONSTRAINTS.md` guidance
Effort: M

## Scope

"Never skip or weaken a valid test to claim green" (`acs-tdd:38`) has no detector.

Add two pieces:
- a `CONSTRAINTS.md` whose checks are placed by cost, so a cheap check guards an expensive claim;
- a diff-scoped guard for five silencing moves: lowered thresholds, skipped or weakened tests, suppression comments, stubbed catches, new exception rows.

The guard reports; it does not auto-fix.

## Inputs

- Analysis: §7.6, §8.8 G8, §10 B12.
- Sources: Addy `constraint-driven-development` and `floor-guard.md`; pstack `correct`.

## Verification

- Each of the five moves is caught by a fixture diff.
- A clean diff passes.
- The guard names the file, line and move, and refuses to claim green.

## Blockers

none

## Coordination proposal

`acs-analyze-test-gaps` is untouched by other tickets. No shared write.

## Evidence

Implemented 2026-10-23. Canonical source stays in `acs-analyze-test-gaps`:
its packaged `references/CONSTRAINTS.md` provides edit-loop/task/CI placement,
record shape, exception disposition and canonical questioning/evidence links.
The stdlib `scripts/floor_guard.py` reports all five moves without auto-fixing.
The description and six context fields are unchanged. No boilerplate moved.

Baseline: HEAD `fbc81fd046ea0c2093e4516cc8dbdd289d473395`, 1,121 file/link
fingerprints captured before writing. The full dirty baseline is in
`.scratch/B12-constraint-floor/baseline.json`, `baseline-status.txt`,
`baseline.diff` and `baseline/`. Integrated B1/B2/B3/B4/B5/B14/B19 edits
remain intact; the only baseline-modified source files additionally edited here
are the skill and third-party notices. No source repository commits, staging,
installs, pushes or publication. Git commits inside disposable fixture repositories
are test setup only. Generated plugins remain in scratch for parent build ownership.

### Exact delta relative to starting baseline

- `docs/changes/acs-corpus-alignment/tasks/B12-constraint-floor.md` — this ticket evidence/status.
- `system/THIRD_PARTY_NOTICES.md` — replace the now-stale no-Addy-adaptation claim with B12 provenance.
- `system/evals/tests/test_constraint_floor.py` — 23 subprocess fixture tests.
- `system/skills-src/test/acs-analyze-test-gaps/SKILL.md` — constraint-floor invocation, evidence and readiness rules.
- `system/skills-src/test/acs-analyze-test-gaps/references/CONSTRAINTS.md` — cost placement and target-record guidance.
- `system/skills-src/test/acs-analyze-test-gaps/scripts/floor_guard.py` — read-only diff guard.

Source SHA256 values at validation (the ticket's own digest is kept in the external
implementation report to avoid a self-referential hash):

| File | SHA256 |
| --- | --- |
| `system/THIRD_PARTY_NOTICES.md` | `b58a5592874327fcdafda663128812334db335f07433333027f20b22e26d252c` |
| `system/evals/tests/test_constraint_floor.py` | `d1c2670f262deec67a195218c52fc1256666362f22e74efe85451fc59afabeb1` |
| `system/skills-src/test/acs-analyze-test-gaps/SKILL.md` | `0c1fe769997fb1b53ddc053ada09d62bd443c5a352d4131f85a14e41cd001ce9` |
| `system/skills-src/test/acs-analyze-test-gaps/references/CONSTRAINTS.md` | `a2f3b152afe35c755184682b31850c5df9ad9f58e8de972ba5329c285c415ce1` |
| `system/skills-src/test/acs-analyze-test-gaps/scripts/floor_guard.py` | `454fb764ddc0567e3a97c27866d06e2991627bcdccbcb41008aeb81200ad61aa` |

### Commands and outcomes

Environment: Python 3.14.6, Git 2.50.1 (Apple Git-155), macOS 26.6.2 arm64.
Exact commands, exit codes, UTC timestamps and output hashes are retained in
`.scratch/B12-constraint-floor/commands.json`. All commands below exited 0;
the packaged suppression exercise internally asserted the guard's expected exit 1.

| Command | Result | Output SHA256 |
| --- | --- | --- |
| `python3 -B -m unittest discover -s system/evals/tests -p test_constraint_floor.py -v` | PASS (exit 0) | `81b550c1aa063953551b106f6d5b9eb80fd3edd89fd3dc86e20804e313fbda45` |
| `python3 -B system/evals/validate_suite.py` | PASS (exit 0) | `24f08422067a2ac854b1ba7702ef14e44ba5be239ceb609c78dabcab80d28e9c` |
| `python3 -B scripts/validate-protocols.py --source-only` | PASS (exit 0) | `febb7838d6d0c19d767aa81f8f704dc7838c9d2e9a9325ab613f36e5daac7eea` |
| `python3 -B scripts/build-plugins.py --output .scratch/B12-constraint-floor/plugins` | PASS (exit 0) | `32d7559f7dc01da08058e82504290fb5223ca21a30585e4abd1e9a1b13059964` |
| `python3 -B scripts/validate-protocols.py --plugins .scratch/B12-constraint-floor/plugins` | PASS (exit 0) | `febb7838d6d0c19d767aa81f8f704dc7838c9d2e9a9325ab613f36e5daac7eea` |
| `git diff --check` | PASS (exit 0) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git diff --cached --exit-code` | PASS (exit 0) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `python3 -B -m unittest discover -s system/evals/tests -v` | PASS (exit 0) | `e68ca8db626b58f458358eb6f1a49058948766be7e39d0d4e551de897ef7554c` |
| `python3 -B .scratch/B12-constraint-floor/verify_package.py` | PASS (exit 0) | `01b69148760a8e04e9cea3296ac4ee31ddebca6929d3fdc3d5a047c2288e4770` |

The focused suite passed 23 tests; the complete existing eval tests directory
passed 67 tests. The latter includes an intentionally failing red-phase fixture
inside a passing TDD test; it is not a regression failure. All five silencing moves
have executable fixture changes with exact file/line/move assertions. Additional
cases cover threshold tightening, clean diff/tree, changed and removed exceptions,
staged/unstaged/untracked/committed changes, subdirectory invocation, unusual
filenames, deletion-only empty catches, historical unchanged suppressions,
input failures, nonmutation, and content fingerprints. These are actual scripted
subprocess exercises on authored fixtures, not behavioral model transcripts or
claims of historical production incidents.

Suite validation: 43 skills; inventory, description budgets, declarations and local
links/anchors PASS. Builder produced scratch plugins; protocol validation passed
for source and built package closure. The packaged guard is byte-identical to the
source and actually ran on clean and suppressed-check changes. Its clean diff hash
was `cfe71bb1ab24589632fe8686fbff0b118522d69309652625291b557ba79559eb`;
the suppression diff hash was
`53fb96c1c4b17f60a550b1febe1743ef454aeb1f0e8f360516722a8266e50b78`.
Both explicitly returned `green_claim: false`. Package exercise output is in
`.scratch/B12-constraint-floor/package-exercise.log`.

### Limitations and review handoff

- Detection is deliberately textual. Conventional test paths and common language
  patterns are supported; arbitrary assertion semantics, languages and external
  checker configurations require review. Numeric ratchets apply to stable
  rows/bullets in files named `CONSTRAINTS.md`, not arbitrary config formats.
- Conservative assertion replacements, rule/stage edits and renames can require
  review even when legitimate. New/changed approved exceptions remain findings;
  canonical evidence supplies disposition rather than an automatic bypass.
- Ordinary Markdown examples and ignored files are outside code-pattern scanning.
  Changed binary files, symlinks/submodules, unreadable inputs and ambiguous
  duplicate constraint table IDs return exit 2 (unavailable), never clean.
- The guide does not install tools, wire CI, invent numeric budgets or change
  lifecycle rigor tiers. Existing one-shot test-run and questioning rules remain.
- No overall green claim is derived from a clean scan. Required checks and criteria
  still govern readiness; incomplete scans and unresolved findings block green.
- Parent owns independent reviewer gate and canonical generated build. Generated
  output here is scratch only; no staged files. Baseline-relative source diff and
  complete fingerprints are retained under `.scratch/B12-constraint-floor/`.


## Parent acceptance

2026-10-23: reconciled source passed canonical plugin build, derived-surface check, protocol and suite validators, 91 eval tests and 19 contract tests. [Independent review](../evidence/third-batch-review.md) found no blockers. Constraint scanning remains heuristic; fixture checks do not prove general model compliance. Canonical integration resolved shared-file conflicts and retained all provenance sections.
