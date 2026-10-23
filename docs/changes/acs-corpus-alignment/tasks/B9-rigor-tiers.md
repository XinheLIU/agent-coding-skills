# B9-rigor-tiers: Declare three rigor tiers with a one-way ratchet

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: design
Status: done
Readiness: ready
depends_on: none
affects: `system/workflows/README.md`; `system/skills-src/build/acs-implement/SKILL.md`; README quick start
Effort: M

## Scope

23 of 43 skills sit in plan and design, and no tier is declared, so a user cannot tell what a bugfix will pass through.

Declare three tiers:

| Tier | Route |
| --- | --- |
| Spike | `acs-validate-prototype` or a spike: a question in, an answer out, nothing kept |
| Bounded (default) | One ticket, an in-chat design, an approval, then `acs-implement` |
| Architectural | The full plan → design → build route |

Three rules: say the tier out loud so the user can override; the ratchet only goes up; approval is staged ("a reply approves the stage actually presented"). Add the model-tier note: run sensors continuously on a cost-optimized model, as a final gate on a frontier model.

## Inputs

- Analysis: §7.4, §8.5 U6/U7, §10 B9.
- Sources: Superpowers `brainstorming`; OpenSpec `concepts.md:169`; Addy `ship.toml:71`.

## Verification

- `workflows/README.md` states the three tiers, the default and the ratchet.
- A new run records its tier before the first skill.
- The Bounded route is reachable end to end on one scratch ticket.

## Blockers

none

## Coordination proposal

B25 quotes the default tier; land B9 first. `acs-implement` is shared with B7.

## Evidence

Implemented 2026-10-23; independent review remains required before integration. The approved three-tier contract lives in `system/workflows/README.md`; coordinator entry records the tier before any skill, and `acs-implement` provides the one-ticket Bounded route without a spec or HTML delivery plan. Existing questioning and revision-bound evidence remain authoritative. Coordination protocol and registry advance together to 1.2.0. Quick-start ordering declares the tier before optional context setup. Provenance records the inspected pinned sources; the upstream corpus was not edited.

Exact files changed relative to the starting dirty baseline (not relative to HEAD):

- `README.md`
- `docs/changes/acs-corpus-alignment/tasks/B9-rigor-tiers.md`
- `system/THIRD_PARTY_NOTICES.md`
- `system/evals/tests/test_rigor_tiers.py`
- `system/protocols/context-coordination.md`
- `system/protocols/registry.json`
- `system/skills-src/build/acs-implement/SKILL.md`
- `system/workflows/README.md`
- `system/workflows/build.md`

Baseline: HEAD `fbc81fd046ea0c2093e4516cc8dbdd289d473395`, plus all integrated dirty B1/B2/B3/B4/B5/B14/B19 work. Captured 1,121 file/symlink identities in `.scratch/B9-rigor-tiers/baseline.json`, raw status in `baseline-status.txt`, and existing tracked diff in `baseline.diff`. Baseline-manifest file SHA-256: `9b70c5803b321b916330a8ef376ca44e82364d8dafcb58083691be7853423722`. Baseline comparison found no modifications outside the nine files above. No files staged; no commits, installs, pushes, or publication.

Final tested source identity: `sha256:972c161fd7fb824c221fec5561711e9cba84b35dccd60b98c6bd633d7383e5e2`. Method: collect regular non-symlink files in `README.md`, `scripts/`, `system/`, `catalog/`, and `LICENSE`, excluding `__pycache__` and `.pyc`; map repository-relative paths to byte SHA-256; serialize with Python `json.dumps(manifest, sort_keys=True, separators=(',', ':'))`; SHA-256 those UTF-8 bytes. Reproducible path/hash manifest: `.scratch/B9-rigor-tiers/tested-source-manifest.json`. This scope excludes ticket/report bookkeeping and generated output. Source link/package validators separately cover symlinks. Exact commands, completion timestamps, tested revision, exit codes, and output paths are retained in `.scratch/B9-rigor-tiers/checks.json`; initial passing checks before final wording changes remain in `checks-initial.json` and initial logs.

All commands below ran from this worktree root on the final tested source:

| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -m unittest discover -s system/evals/tests -v` | PASS — 48 tests, including four new B9 checks and integrated regressions | `.scratch/B9-rigor-tiers/logs/final-01.log` |
| `python3 -m unittest discover -s system/evals/evals -p test_evidence_binding.py -v` | PASS — 11 B19 evidence-binding tests | `.scratch/B9-rigor-tiers/logs/final-02.log` |
| `python3 system/evals/validate_suite.py` | PASS — 43 skills; description budgets, declarations, links/anchors | `.scratch/B9-rigor-tiers/logs/final-03.log` |
| `python3 scripts/build-plugins.py --output .scratch/B9-rigor-tiers/plugins` | PASS — all plugin families built into scratch | `.scratch/B9-rigor-tiers/logs/final-04.log` |
| `python3 scripts/validate-protocols.py --plugins .scratch/B9-rigor-tiers/plugins` | PASS — registry, links, and generated package closure | `.scratch/B9-rigor-tiers/logs/final-05.log` |
| `git diff --check` | PASS — no whitespace errors | `.scratch/B9-rigor-tiers/logs/final-06.log` |
| `git diff --cached --name-only` | PASS — empty output; nothing staged | `.scratch/B9-rigor-tiers/logs/final-07.log` |

Acceptance evidence:

- Tier/default/ratchet/staged approval/model cadence are source-checked; coordinator and README entry paths connect to the same canonical contract. Questions still use `protocols/questioning.md`; descriptions are unchanged from baseline.
- A real scripted subprocess exercise starts with one scratch ticket and an authored Bounded design/approval precondition, observes a failing CLI test, repairs the existing flow, runs green tests and the CLI, then successfully collects two revision-bound evidence rows. A later source edit causes `STALE-REVISION` rejection. The exercise retains one ticket and creates neither a spec nor an HTML plan.
- A relocated standalone `acs-implement` package retains the workflow tier contract, questioning, and executable evidence checker; package validation succeeds without symlinks. Full plugin output stays at `.scratch/B9-rigor-tiers/plugins/`; tracked generated packages are untouched.

Limitations: source assertions and scripted subprocess reachability are not model behavioral transcripts. The approval is explicitly authored fixture input, not an invented user reply. No live host/model tier-selection, user override, ratchet behavior, or two-model cost comparison was run. Continuous/final sensor policy is documented, not enforced by a new runtime. Scratch logs/manifests are local diagnostic artifacts; this ticket retains the commands, fingerprint method, results, and limitations. Independent reviewer gate is still pending.


## Parent acceptance

2026-10-23: reconciled source passed canonical plugin build, derived-surface check, protocol and suite validators, 91 eval tests and 19 contract tests. [Independent review](../evidence/third-batch-review.md) found no blockers. Constraint scanning remains heuristic; fixture checks do not prove general model compliance. Canonical integration resolved shared-file conflicts and retained all provenance sections.
