# B13-security-evidence: Add a security evidence rubric to the review

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/test/review/acs-review-code-quality/SKILL.md` security lens
Effort: M

## Scope

The security lens lists greps; it does not separate a claim from its evidence.

Add: severity, confidence and evidence as separate fields; a "supported" finding needs an entrypoint, a boundary crossing and demonstrated impact; an independent challenger sees the evidence without the producer's conclusion; "unknown reachability remains unknown, not unreachable".

## Inputs

- Analysis: §10 B13.
- Sources: gstack `cso:121-148` (rubric only); Addy `security-and-hardening`.

## Verification

- The rubric table exists and every finding names the three evidence parts.
- Five fixture findings classify consistently; one with unknown reachability is not marked unreachable.
- A challenger transcript shows the conclusion withheld.

## Blockers

none

## Coordination proposal

Same file as B6 and B2; separate sections, rebase on the earlier one.

## Evidence

Implemented the rubric and finding fields in the review skill, and routed security claims from all domain lenses to that rubric. Preserved B2 questioning, B6 quote-gate precedence, Standards/Spec separation, ARC/CON architecture routing, and the B20 source shared-semantics link plus generated injection.

### Contribution boundary

Baseline: 1,089 tracked/unignored file byte streams captured before editing in `.scratch/B13-security-evidence/baseline-hashes.json`; initial dirty status in `baseline-status.txt`. Comparison is against the integrated dirty baseline, not HEAD. Exactly these five repository files changed:

- `docs/changes/acs-corpus-alignment/tasks/B13-security-evidence.md`
- `system/evals/fixtures/acs-security-evidence.json`
- `system/evals/tests/test_security_evidence.py`
- `system/skills-src/test/review/acs-review-code-quality/SKILL.md`
- `system/skills-src/test/review/acs-review-code-quality/references/domain-lenses.md`

No other baseline files changed. No files staged. Generated packages remain under `.scratch/B13-security-evidence/plugins`; parent owns generated-output integration.

### Acceptance evidence

- Rubric table separates severity, confidence and evidence state. Every security finding requires entrypoint, boundary crossing and demonstrated impact, with explicit unknowns and next checks when absent.
- Five authored findings: supported static tenant disclosure, an illustrative reproduction record, dependency reachability unknown, ownership guard disproving a disclosure claim, and missing impact. Unknown reachability remains unknown and candidates cannot enter supported totals or blocking priorities.
- The authored challenger exchange separates private producer conclusions from the neutral evidence input, includes challenger dissent and reconciliation, and explicitly states no independent model was invoked. The illustrative reproduction was not executed. These are fixture contracts, not observed model compliance or a live security assessment.
- Eight B13 tests check source contracts, inherited gates, five classifications, missing-part/reproduction mutations, unknown-reachability/reporting bypasses, conclusion leakage, pinned provenance, and standalone relocation preserving generated shared semantics.
- Full source/package suite: 99 tests passed. Evidence-binding suite: 19 tests passed. Source validator: 43 skills passed. Scratch builder, generated-surface `--check`, protocol/package closure and whitespace validation passed.

### Commands and results

Raw logs and exact command/output hashes are in `.scratch/B13-security-evidence/validation.json`:

- `python3 -m unittest discover -s system/evals/tests -p test_security_evidence.py -v` → exit 1; `.scratch/B13-security-evidence/validation-1.log` (SHA256 `3991b5da6e610e67a942e7744859cf548a1f3b7f05233ac79992ef7f33fe5271`).
- `python3 -m unittest discover -s system/evals/tests -p test_security_evidence.py -v` → exit 0; `.scratch/B13-security-evidence/validation-2.log` (SHA256 `86d595ede5204f3db9796ec01a636930c29f4149bddfe1b4b0ae6d9b6784fbfd`).
- `python3 -m unittest discover -s system/evals/tests -p test_*.py -v` → exit 0; `.scratch/B13-security-evidence/validation-3.log` (SHA256 `ac1d6ca7269c69d54c8b8379479623092dc641d4efafa14d1a3c4b0337b0b606`).
- `python3 -m unittest discover -s system/evals/evals -p test_*.py -v` → exit 0; `.scratch/B13-security-evidence/validation-4.log` (SHA256 `3a626ff31d88f72d0ba2fa78cc9b5b2d2a9287da3ee6e6b44c8be19b501ab3ff`).
- `python3 system/evals/validate_suite.py` → exit 0; `.scratch/B13-security-evidence/validation-5.log` (SHA256 `24f08422067a2ac854b1ba7702ef14e44ba5be239ceb609c78dabcab80d28e9c`).
- `python3 scripts/build-plugins.py --output .scratch/B13-security-evidence/plugins` → exit 0; `.scratch/B13-security-evidence/validation-6.log` (SHA256 `32d7559f7dc01da08058e82504290fb5223ca21a30585e4abd1e9a1b13059964`).
- `python3 scripts/build-plugins.py --output .scratch/B13-security-evidence/plugins --check` → exit 0; `.scratch/B13-security-evidence/validation-7.log` (SHA256 `21430c246de4388eacb656b5e696b7a039b92c189fc850cbf4910d3bb4ff4b65`).
- `python3 scripts/validate-protocols.py --plugins .scratch/B13-security-evidence/plugins` → exit 0; `.scratch/B13-security-evidence/validation-8.log` (SHA256 `febb7838d6d0c19d767aa81f8f704dc7838c9d2e9a9325ab613f36e5daac7eea`).
- `git diff --check` → exit 0; `.scratch/B13-security-evidence/validation-9.log` (SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

The initial focused run had one test expectation failure: it expected the source shared-semantics marker in the standalone package. The existing builder correctly injects shared protocol text. The assertion was corrected to verify that injection and resolved links; the focused and full suites then passed. The full suite also emits intentional red-phase child failures in its existing TDD tests; the enclosing 99-test suite passed.

### Fingerprints and review limits

- `system/evals/fixtures/acs-security-evidence.json`: baseline `absent (new file)`; final SHA256 `8c3bc4c995250eaa471ba834ab8df8975a33edce9e290b0a66376eabec5d8bc5`.
- `system/evals/tests/test_security_evidence.py`: baseline `absent (new file)`; final SHA256 `5f75e864f0077bc54feccc7f12876dbacc16ba6ceaa9f4312f4e3587bfe1903b`.
- `system/skills-src/test/review/acs-review-code-quality/SKILL.md`: baseline `63a9fb674b59f80733e97c304a6a0b8821964672b872297b2f207f5e4a7cbfea`; final SHA256 `60e0c3d842924f05f998a7eaae0ddaf5d766813e67d38ad92ac4add12c1e3077`.
- `system/skills-src/test/review/acs-review-code-quality/references/domain-lenses.md`: baseline `cc4af0294535ca19ac95342d76e054cd7b4e5ed5b9e4e8263b6524115416fe8e`; final SHA256 `16e979fe07d73946b1588eee4ba7f8e3d192fef9e36df6f715b5214964157008`.
- `.scratch/B13-security-evidence/baseline-hashes.json` SHA256 `a2338131f4aca30478fac2a810529bb53f84b85e86f8ebc349ad97df319dd27e`.
- `.scratch/B13-security-evidence/build-manifest.json` SHA256 `b6bb61f66c5671f55f16ff71bee12ce2f6d565966a3c8d804ee8c92914126ef2`.
- `.scratch/B13-security-evidence/validation.json` SHA256 `801c296b4ff3ae3d5cbd312a1252556b3aed584d9bd8161cdc05604d2655ef74`.

No live model challenge or security reproduction was run. Independent reviewer acceptance remains pending; Status stays `in_progress` and Readiness stays `needs-review`. No infrastructure or user-owned decision is blocked. Upstream corpus was inspected read-only; pinned provenance is recorded beside the rubric.

## Parent acceptance

2026-10-23: integrated validation passed (110 suite tests, 19 evidence checks, build/check and validators). Follow-up compaction corrections passed configured focused tests and validators. [Independent acceptance review](../evidence/fourth-batch-review.md) found no remaining blockers. Named-tokenizer proof is not live-host certification; security challenger fixtures are authored, not an observed independent model security review.
