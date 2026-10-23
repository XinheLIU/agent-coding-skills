# B20-generated-boilerplate: Stop generating a fixed date and duplicated boilerplate

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `scripts/build-plugins.py`; all generated plugin READMEs; the shared "Shared semantics" paragraph
Effort: S-M

## Scope

`scripts/build-plugins.py:193` writes the literal `Last updated: 2026-10-04` into every generated README, which contradicts the repository's own dated-documents rule. The shared "Shared semantics …" paragraph is also repeated in all 43 sources.

Derive the generated date from the source. Inject the shared paragraph at build time. Add a `--check` mode that fails when a derived surface differs from what the source would produce.

## Inputs

- Analysis: §7.6, §10 B20.
- Sources: gstack preamble tiers; PM-Skills `--check`.

## Verification

- Two consecutive builds produce byte-identical output.
- `--check` fails when a generated README date or paragraph is stale.
- No generated file contains a hard-coded date literal.

## Blockers

none

## Coordination proposal

`build-plugins.py` is also touched by B1 only if the budget is emitted; keep the edits in separate functions.

## Evidence

Implemented 2026-10-23. Independent review remains required; generated repository surfaces are intentionally left for parent integration.

### Implementation and boundaries

- Replaced the repeated paragraph in all 43 source skills with a readable link to `system/docs/shared-semantics.md`. Its five canonical variants preserve all original wording and contract targets (30 execution, 1 planning, 5 context, 1 README ownership, 6 technical design). The builder expands the selected section in installed skills and companion reference procedures, then closes its links within each package. Source-checkout discovery still has a normal Markdown route to the same rules.
- README dates now use the latest valid declared `Last updated` date among that package's materialized Markdown inputs, including transitive resources and the injected paragraph source. No wall clock, mtime, or fixed date fallback is used. Undated-only packages and invalid ISO calendar dates fail. Copied source documents retain their own declared dates; the verification requirement means no date literal is authored in the generator, not that dated Markdown loses its dates.
- `--check` builds in a temporary directory and compares generated file bytes without repairing the selected output. It supports plugin and standalone output, includes manifests/catalogs and default-output marketplace entries, and detects missing or extra files in owned resource trees. It preserves the established boundary for unrelated user files outside those trees and unrelated retained package IDs. The legacy `acs-protocols` build now resolves output paths before link rewriting, avoiding macOS `/var` versus `/private/var` false drift.
- `Use when` descriptions, canonical questioning and evidence rules, and all non-paragraph skill content are byte-preserved relative to the starting baseline (apart from required date updates). No tiers, runtime policy, registry changes, dependencies, installs, commits, staging, pushes, publication, or corpus edits were added.
- Provenance is recorded in the new shared source: gstack `35dd014` `scripts/gen-skill-docs.ts` single-preamble generation and PM-Skills `scripts/gen-derived-surfaces.mjs` drift checking, inspected read-only from the specified upstream corpus. No upstream implementation was copied.

### Baseline and fingerprints

Starting dirty baseline: `.scratch/B20-generated-boilerplate/baseline.json` (1,121 tracked/untracked paths; SHA-256 `dc937c1cb2b448fc9dfed24d5e4acf350aef42bfb74528c6fa2f46430449ebce`), with `baseline.patch`, `baseline-status.txt`, and `paragraph-baseline.json` beside it. Integrated B1/B2/B3/B4/B5/B14/B19 changes were present before this task.

Tested source fingerprint: `sha256:03feb6353c08e1e2c8bd7d38731047acf4022cfb37d8d8ae8cd392b00581b549` over 311 inputs. The reproducible algorithm in `.scratch/B20-generated-boilerplate/verify.py` hashes sorted relative paths + NUL + raw SHA-256 digests of bytes (literal target text for symlinks), covering `system/`, `scripts/`, `catalog/`, `LICENSE`, and `.claude-plugin/marketplace.json`; Python caches, ticket/evidence records, scratch and generated outputs are excluded. Each acceptance command recorded the same fingerprint before and after execution. Environment: Python 3.14.6, macOS 26.6.2 arm64; stdlib only.

Scratch generated tree: 928 files; SHA-256 `054821e2fe07525d33b674ebae345f2f8e5566686335f89deb2240f7fb632590`, using sorted relative file paths + NUL + raw content SHA-256 digest. All 10 generated root READMEs derive `2026-10-23` from source. `output-fingerprint.json` records the measurement at `2026-10-23T08:21:37.503775+00:00`.

### Acceptance evidence

These are actual unittest/subprocess executions, not model behavioral transcripts. Full logs and command/fingerprint/timestamp records are in `.scratch/B20-generated-boilerplate/acceptance-*.log` and `validation.json`.

| Command | Result | Completion (UTC) |
| --- | --- | --- |
| `python3 -m unittest discover -s system/evals/tests -p test_generated_boilerplate.py -v` | PASS: 5 focused tests | `2026-10-23T08:19:18.112739+00:00` |
| `python3 -m unittest discover -s system/evals/tests -p test_*.py -v` | PASS: 49 tests | `2026-10-23T08:19:49.282078+00:00` |
| `python3 system/evals/validate_suite.py` | PASS: 43 source skills and catalog budget | `2026-10-23T08:19:49.522055+00:00` |
| `python3 scripts/build-plugins.py --output .scratch/B20-generated-boilerplate/plugins` | PASS: 10 packages | `2026-10-23T08:19:50.624667+00:00` |
| `python3 scripts/build-plugins.py --output .scratch/B20-generated-boilerplate/plugins --check` | PASS: no derived drift | `2026-10-23T08:19:51.802474+00:00` |
| `python3 scripts/validate-protocols.py --plugins .scratch/B20-generated-boilerplate/plugins` | PASS: registry, source links, isolated package closure | `2026-10-23T08:19:52.604271+00:00` |
| `git diff --check` | PASS: no whitespace errors | `2026-10-23T08:19:52.693867+00:00` |
| `git diff --cached --name-only` | PASS: empty index | `2026-10-23T08:19:52.763067+00:00` |

Additional checks:

- `python3 -m unittest discover -s system/evals/evals -p test_evidence_binding.py -v`: PASS, all 11 B19 tests; log `evidence-binding.log`, completed before the output fingerprint measurement above, same unchanged source fingerprint.
- `python3 .scratch/B20-generated-boilerplate/preserve.py`: PASS, exact contribution boundary; reversing the shared-paragraph replacement and date update in each of 43 skills reproduces its starting hash. Every unrelated baseline path is unchanged, including generated plugins and marketplace. No staged files.
- Focused subprocess tests run two consecutive plugin builds and compare every output byte; fresh checks pass. Separate mutations of README date, shared paragraph, catalog identity and manifest description each fail check with exit 1 without repair. Missing output/file and unexpected generated resource cases also fail; user notes survive. Standalone build/check and relocated link closure pass. The default-output marketplace branch is tested against an isolated fixture to avoid repository writes.
- The existing package tests additionally relocate packages, remove their original source fixture, validate closure and execute the packaged renderer tests.

Intermediate failures remain in `focused.log` and `focused-second.log`: the first comparison exposed unresolved macOS temporary-path aliases in the legacy package; the second fixture exposed the same unresolved-output issue at the check API. Output normalization fixed both. These exploratory failures are not claimed as deliberate red-phase behavior evidence; final focused and regression runs above pass.

### Exact contribution relative to starting baseline

48 repository paths (including this ticket); this list is not a HEAD-based diff:

- `docs/changes/acs-corpus-alignment/tasks/B20-generated-boilerplate.md`
- `scripts/build-plugins.py`
- `system/docs/shared-semantics.md`
- `system/evals/tests/test_generated_boilerplate.py`
- `system/evals/tests/test_packages.py`
- `system/skills-src/authoring/acs-challenge-approach/SKILL.md`
- `system/skills-src/authoring/acs-draw-portfolio-dag/SKILL.md`
- `system/skills-src/authoring/acs-research/SKILL.md`
- `system/skills-src/authoring/acs-review-agent-instructions/SKILL.md`
- `system/skills-src/authoring/acs-writing-great-skills/SKILL.md`
- `system/skills-src/build/acs-implement/SKILL.md`
- `system/skills-src/build/acs-plan-delivery/SKILL.md`
- `system/skills-src/build/acs-tdd/SKILL.md`
- `system/skills-src/context/acs-create-readme/SKILL.md`
- `system/skills-src/context/acs-engineer-domain-model/SKILL.md`
- `system/skills-src/context/acs-init-context/SKILL.md`
- `system/skills-src/context/acs-manage-context/SKILL.md`
- `system/skills-src/context/acs-sync-context/SKILL.md`
- `system/skills-src/context/acs-translate-agent-context/SKILL.md`
- `system/skills-src/design/requirements/acs-settle-requirements/SKILL.md`
- `system/skills-src/design/technical/acs-design-architecture/SKILL.md`
- `system/skills-src/design/technical/acs-design-contracts/SKILL.md`
- `system/skills-src/design/technical/acs-design-modules/SKILL.md`
- `system/skills-src/design/technical/acs-design-test-strategy/SKILL.md`
- `system/skills-src/design/technical/acs-technical-design/SKILL.md`
- `system/skills-src/design/technical/acs-trace-requirements/SKILL.md`
- `system/skills-src/design/ux/acs-design-context/SKILL.md`
- `system/skills-src/design/ux/acs-design-implement/SKILL.md`
- `system/skills-src/design/ux/acs-design-interaction-flow/SKILL.md`
- `system/skills-src/design/ux/acs-design-system-create/SKILL.md`
- `system/skills-src/design/ux/acs-validate-prototype/SKILL.md`
- `system/skills-src/design/ux/acs-visual-design-variants/SKILL.md`
- `system/skills-src/maintain/acs-diagnose-incident/SKILL.md`
- `system/skills-src/plan/acs-brainstorm/SKILL.md`
- `system/skills-src/plan/acs-define-outcomes/SKILL.md`
- `system/skills-src/plan/acs-design-experiment/SKILL.md`
- `system/skills-src/plan/acs-explore-unknowns/SKILL.md`
- `system/skills-src/plan/acs-ideate-product/SKILL.md`
- `system/skills-src/plan/acs-map-current-product/SKILL.md`
- `system/skills-src/plan/acs-run-premortem/SKILL.md`
- `system/skills-src/plan/acs-shape-solution/SKILL.md`
- `system/skills-src/plan/acs-validate-demand/SKILL.md`
- `system/skills-src/plan/acs-write-prd/SKILL.md`
- `system/skills-src/test/acs-analyze-test-gaps/SKILL.md`
- `system/skills-src/test/debugging/acs-resolving-merge-conflicts/SKILL.md`
- `system/skills-src/test/debugging/acs-triage/SKILL.md`
- `system/skills-src/test/review/acs-refactor-code/SKILL.md`
- `system/skills-src/test/review/acs-review-code-quality/SKILL.md`

### Limitations and next action

Independent reviewer acceptance remains pending. Parent should review the durable source diff and then regenerate the repository's derived surfaces after integration. This task built only `.scratch/B20-generated-boilerplate/plugins`; tracked `plugins/` and marketplace remain at their starting state, so a default `--check` is expected to flag them until parent rebuilds. The check intentionally audits builder-owned surfaces rather than arbitrary user files. Tests verify generator behavior and source/package semantics mechanically; they do not establish how a live model follows a source-reader link. No service, host installation, publication, or live-model behavior was tested.


## Parent acceptance

2026-10-23: reconciled source passed canonical plugin build, derived-surface check, protocol and suite validators, 91 eval tests and 19 contract tests. [Independent review](../evidence/third-batch-review.md) found no blockers. Constraint scanning remains heuristic; fixture checks do not prove general model compliance. Canonical integration resolved shared-file conflicts and retained all provenance sections.
