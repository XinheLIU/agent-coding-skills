# B25-positioning: State who ACS is for and make Bounded the default path

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: B9-rigor-tiers
affects: `README.md`; `system/README.md`
Effort: S

## Scope

State the audience and the non-audience:
- For: work that spans sessions, agents or people, where the why must survive — client repositories, brownfield changes with audit needs, parallel delivery.
- Not for: a solo developer making a bounded change, better served by Pocock-style skills or by ACS's Bounded tier.

Default to Bounded in the README quick start. State the smallest useful path in five lines.

## Inputs

- Analysis: §5, §8.5, §10 B25.
- Requires B9's tier names.

## Verification

- `README.md` and `system/README.md` state both audiences and the default tier.
- The quick start's first path is Bounded and names the skills it invokes.
- No claim contradicts B9.

## Blockers

B9 must land first so the tier has a canonical name.

## Coordination proposal

README is an interface file; repair only the routing and positioning text.

## Evidence

Implemented 2026-10-23; parent acceptance and independent review remain pending. The two README entry points state the intended audience and the lighter path for solo bounded work, link B9's canonical tier contract, and lead with Bounded. The root quick start gives the smallest useful route in five numbered lines, naming optional `acs-init-context`, `acs-implement`, and its `acs-tdd` execution. System navigation also identifies the Bounded build route and makes setup conditional on routing needs. Tier semantics, authorization, shared-semantics links/injection, and implementation contracts remain unchanged.

Exact contribution-relative changed files (compared with the integrated dirty dispatch baseline, not HEAD):

- `README.md`
- `system/README.md`
- `docs/changes/acs-corpus-alignment/tasks/B25-positioning.md`

Baseline HEAD: `fbc81fd046ea0c2093e4516cc8dbdd289d473395`. Captured 1,133 file/symlink hashes in `.scratch/B25-positioning/baseline-manifest.json` (SHA-256 `14ba0d6a9aed9212092be9aec5e4eb03e0c8d8437cd52ddd786444fdbca79f70`), raw status in `baseline-status.txt`, and pre-edit copies of the three assigned files in `baseline/`. No tests were added to product source for this documentation-only change; the existing tier and integrated regression tests were run.

| Command | Result |
| --- | --- |
| `python3 -m unittest discover -s system/evals/tests -v` | PASS — 91 tests |
| `python3 -m unittest discover -s system/evals/evals -p test_evidence_binding.py -v` | PASS — 11 tests |
| `python3 system/evals/validate_suite.py` | PASS — 43 source skills, inventory, catalog budget, declarations, links/anchors |
| `python3 scripts/build-plugins.py --output .scratch/B25-positioning/plugins` | PASS — generated output isolated in scratch |
| `python3 scripts/build-plugins.py --output .scratch/B25-positioning/plugins --check` | PASS — generated surfaces current |
| `python3 scripts/validate-protocols.py --plugins .scratch/B25-positioning/plugins` | PASS — registry, links, package closure |
| `python3 .scratch/B25-positioning/check-positioning.py` | PASS — both audiences, default, five numbered lines, named skills, tier safeguards, added links/anchors |
| `git diff --check` | PASS |
| `git diff --cached --name-only` | Empty — no staged files |

Command exit codes and logs: `.scratch/B25-positioning/checks.json` and `logs/01.log` through `logs/09-positioning-acceptance.log`. Tested source fingerprint: `sha256:8405af6abe3cfe1fca500da15aa5fbd5cf77d1eb5f4058dff73559a4a4d2c269`. Method: map regular non-symlink files in `README.md`, `scripts/`, `system/`, `catalog/`, and `LICENSE` to byte SHA-256, excluding `__pycache__` and `.pyc`; hash UTF-8 `json.dumps(manifest, sort_keys=True, separators=(',', ':'))`. Manifest: `.scratch/B25-positioning/tested-source-manifest.json`. Ticket bookkeeping and generated output are outside this source fingerprint.

Manual review confirms the positioning follows the read-only corpus analysis's B25 recommendation and B9's canonical tier policy. Static authored assertions and existing scripted fixtures are not independent model transcripts or evidence of live host/model behavior. An initial broad README link assertion found the pre-existing planned `system/skills-src/deploy` link without a directory; the scoped check confirms it is unchanged and all added local links/anchors resolve. That baseline gap remains outside B25. No commits, staging, installs, publication, pushes, reference edits, or tracked generated-output changes.

## Parent acceptance

2026-10-23: integrated validation passed (110 suite tests, 19 evidence checks, build/check and validators). Follow-up compaction corrections passed configured focused tests and validators. [Independent acceptance review](../evidence/fourth-batch-review.md) found no remaining blockers. Named-tokenizer proof is not live-host certification; security challenger fixtures are authored, not an observed independent model security review.
