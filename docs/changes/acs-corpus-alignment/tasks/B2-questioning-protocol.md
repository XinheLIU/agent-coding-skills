# B2-questioning-protocol: Replace four conflicting questioning rules with one protocol

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: new `system/protocols/questioning.md`; `system/protocols/registry.json`; four skill files
Effort: S-M

## Scope

Promote `system/skills-src/plan/acs-validate-demand/references/shared-understanding.md` to `system/protocols/questioning.md` and register it in `protocols/registry.json`.

Keep what works: numbered blocks, a recommended answer per question, and "skipped questions are findings". Add three things:

1. Frontier ordering: never ask a question whose premise is still open in the same round; cap a round at five.
2. A classifier before every question: a fact you can look up → sub-agent; a fact observable by running something → `acs-validate-prototype`; a mechanical decision → decide and record; a taste decision → decide and show at the next gate; a user challenge → always ask.
3. Wording so that "yes" accepts the recommendation.

Then delete the local rules and point at the protocol from `acs-challenge-approach:26` ("ask one question at a time"), `acs-review-code-quality:340` ("Never batch"), `acs-design-interaction-flow:215,415` ("NOT batched"), and `shared-understanding:10` ("4–5 questions per message").

## Inputs

- Analysis: §7.3, §8.5 U11, §8.8 G2, §10 B2.
- Sources: Pocock `grilling`; pstack `poteto-mode:20`; gstack `autoplan:69-100`.
- Conflict evidence: the four sites named in Scope.

## Verification

- `python3 scripts/validate-protocols.py` passes; the registry lists the new protocol with id, version and canonical link.
- `grep -rn "one question at a time\|Never batch\|NOT batched\|never one at a time" system/` returns no normative rule outside the protocol.
- A fixture run of `acs-validate-demand` shows one round with at most five questions and a classifier decision per question.

## Blockers

Standalone packaging is blocked in this isolated worktree: a preexisting notice link resolves through the read-only `references` symlink outside the repository, and the builder raises `ValueError: Linked resource escapes repository: /Users/xhl/GitHub/skills/agent-coding-skills/references/OpenSpec/docs/concepts.md`. The supervisor identified this as a coordinator-owned isolation limitation and directed that builder, references, and notices remain unchanged. Canonical-checkout regeneration and package verification remain pending. Actual model behavioral execution was not run; deterministic fixtures do not establish it.

## Coordination proposal

`acs-review-code-quality` is also edited by B6 and B13; keep this edit to line 340 and rebase. The registry is shared with any other protocol addition.

## Evidence

Implemented 2026-10-23; intentionally not marked done. Source contract and deterministic checks are complete; regenerated package verification, actual model behavioral validation, and independent review remain open.

### Source changes and decisions

- Added `system/protocols/questioning.md` version `1.0.0`, its registry entry, and protocol index routing. The contract defines five classifier routes, authorized delegation with direct-lookup fallback, prerequisite frontier rounds capped at five, affirmative recommendation wording, skipped-question findings, and the established/assumption/disputed close.
- Converted the old `shared-understanding.md` to a relative compatibility symlink. All seven existing product-skill aliases resolve to the canonical protocol; source link validation passes. Portable package materialization remains unverified because of the isolation blocker.
- Replaced the challenge, review, and interaction-flow local rules. With supervisor approval, also routed demand's skill/framework and brainstorm's opening/JTBD interview rule to the protocol; those adjacent rules otherwise preserved the contradiction. Review-code-quality changes are limited to its questioning bullet and top date.
- Preserved preexisting `CHANGELOG.md`, `system/THIRD_PARTY_NOTICES.md`, copied plan files other than this ticket, and the read-only references symlink. Provenance is recorded in the new protocol. No generated plugin files changed; builder attempts used temporary output directories. No staged files, commits, installations, publication, or subagents.

### Criterion-to-command results

Commands run from the isolated B2 worktree:

| Criterion | Command | Result and limit |
| --- | --- | --- |
| Registered protocol, canonical links, declarations | `python3 scripts/validate-protocols.py` | PASS: registry, links, and existing package closure. Existing generated artifacts were not regenerated, so this does not prove new package content. |
| Repository structure | `python3 system/evals/validate_suite.py` | PASS: 43 source skills; inventory, declarations, local links/anchors. |
| Remove conflicting rules | `rg -ni 'one question at a time\|Never batch\|NOT batched\|never one at a time' system/protocols system/skills-src system/workflows` | Exit 1, no matches: PASS. Broader than the requested case-sensitive normative-source scan. The literal ticket `grep -rn` also finds negative-test strings and Python bytecode under `system/evals`, which are not normative rules. |
| Canonical callers, seven aliases, deterministic demand round, negative fixtures | `PYTHONPATH=system/evals/tests python3 -m unittest -v test_questioning.QuestioningTests.test_registered_protocol_and_compatibility_aliases test_questioning.QuestioningTests.test_callers_use_canonical_protocol_without_conflicting_rules test_questioning.QuestioningTests.test_authored_validate_demand_round test_questioning.QuestioningTests.test_fixture_rejects_contract_violations` | PASS: 4 tests. Authored fixture has 5 numbered questions, classifier decisions, one deferred dependent question, and a skipped-answer finding. Seven mutations reject excess count, bad classifier route, auto-decided user challenge, unsettled premise, reversed yes polarity, missing reason, and missing skipped finding. This is not a model run. |
| Red-capable source and standalone checks | `python3 -m unittest discover -s system/evals/tests -p 'test_questioning.py' -v` | Before implementation: FAIL, 7 failing subtests and 2 errors from absent protocol/routing. After implementation: 4 tests passed, standalone test errored on the preexisting external references path. No claim of green full suite. |
| Existing regression contracts | `python3 -m unittest discover -s system/evals/evals -p 'test_*.py' -v` | PASS: 8 tests. |
| Existing inventory suite | `python3 -m unittest discover -s system/evals/tests -p 'test_inventory.py' -v` | 10 passed; context-builder test failed on the same external references path. Stopped packaging attempts per supervisor direction. |
| Whitespace and index | `git diff --check`; `git diff --cached --name-only`; `git diff --name-only -- plugins` | PASS; empty staged-file list; empty generated-plugin diff. |
| Actual `acs-validate-demand` behavioral fixture run | Not run | UNVERIFIED. The JSON fixture is explicitly authored deterministic evidence, not an agent transcript. |
| Regenerate plugins | `python3 scripts/build-plugins.py` | Not run after the standalone builder exposed the infrastructure blocker. Parent must run in canonical checkout. |

### Verified tree identity and reproduction

Base HEAD: `fbc81fd046ea0c2093e4516cc8dbdd289d473395` (uncommitted source changes). Final system-tree fingerprint: `sha256:bcaab3abff76e67f90f26cc539efa8b0d3e78142734b498c02a708466c305544`, 244 files. Includes preserved notices and fixture/test sources; excludes Python cache files and the ticket itself. Symlink file contents are dereferenced, matching validators. Reproduce with:

```sh
python3 - <<'PY'
import hashlib
from pathlib import Path
paths = sorted(p for p in Path('system').rglob('*')
               if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
h = hashlib.sha256()
for p in paths:
    h.update(str(p).encode() + b'\0' + p.read_bytes() + b'\0')
print(len(paths), h.hexdigest())
PY
```

Preservation was checked against a startup SHA-256 manifest in `.scratch/B2-questioning-protocol/preserved.json`: 29 preexisting files matched before this ticket update; final verification excludes only this ticket. Initial failing check output is in `.scratch/B2-questioning-protocol/red.log`. These scratch files are supporting local records; the commands, results, and fingerprint above are the durable evidence.

Parent follow-up: reconcile the uncommitted source diff, rebuild using the existing builder in the canonical checkout, rerun both validators and `test_questioning.py`, conduct the actual model behavioral fixture run, and obtain independent review before marking this ticket done.

## Parent acceptance

2026-10-23: canonical build and affected suite passed; independent review found no remaining issues. See [bounded model exercises and source review](../evidence/bounded-model-exercises.md). B2/B3 evidence is one actual bounded model turn each, not a reliability benchmark. B4 has real scripted red/green evidence; B5 requires an explicitly simulated transcript.
