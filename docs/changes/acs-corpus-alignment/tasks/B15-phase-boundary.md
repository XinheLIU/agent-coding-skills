# B15-phase-boundary: Add the phase-boundary rule for persisting handoffs

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/protocols/context-coordination.md`; handoff section in `skill-declarations.md`
Effort: S

## Scope

The protocol says to persist before handoff but not when a phase boundary is real.

Add the two questions: does the next phase consume this one as a primary source, and is there context room left? If both are yes, continue and persist afterwards. A handoff stays mandatory across sessions, worktrees and agents.

## Inputs

- Analysis: §7.2, §10 B15.
- Source: Pocock `ask-matt/PHASE-BOUNDARIES.md`.

## Verification

- The rule appears once in the protocol and is linked, not restated, by skills.
- A run that crosses a session boundary persists; a continuous run does not.
- A test asserts both branches on a fixture transcript.

## Blockers

none

## Coordination proposal

`context-coordination.md` is shared with B8 and B19; separate sections.

## Evidence

Implementation complete; independent review pending. The canonical rule lives at `system/protocols/context-coordination.md#phase-boundaries`; shared handoff declarations and `acs-implement` link to it. Protocol versions and registry entries advance together. Existing formal-review, authorization, evidence, claim-transfer, and retention gates remain. Continuous same-agent/session/worktree work defers phase-boundary persistence until afterwards; it does not omit the final record.

### Changed files relative to starting baseline

- `system/protocols/context-coordination.md`
- `system/protocols/skill-declarations.md`
- `system/protocols/registry.json`
- `system/skills-src/build/acs-implement/SKILL.md`
- `system/evals/tests/test_phase_boundary.py`
- `system/evals/fixtures/phase-boundary-transcripts.json`
- `docs/changes/acs-corpus-alignment/tasks/B15-phase-boundary.md`

No other pre-existing source file changed. Generated output is separate under `.scratch/B15-phase-boundary/plugins/`; tracked `plugins/` is untouched. No files staged; no commits, installations, pushes, publication, or subagents.

### Verification and consumed revisions

Baseline HEAD: `fbc81fd046ea0c2093e4516cc8dbdd289d473395`, with the existing dirty B1/B2/B3/B4/B5/B14/B19 integration preserved. The baseline includes 1,121 tracked/untracked paths. Captured before edits: `.scratch/B15-phase-boundary/baseline.json` SHA-256 `78e936cb2e1e23e361445185f21134d9d5f01f4a2370ccb0d450d5eb74372258`; tracked baseline diff SHA-256 `8eaa999a54060ea97267de5de7d86477de8edf0de7d3361c27a7b4add2bc3607`. Baseline status and HEAD are retained alongside them. The registry and implementation skill already contained integrated changes and received only the B15 version/link edits.

The local analysis's B15 entry specifies AND, while upstream uses OR; this implementation follows the authorized ticket. Read-only upstream source: `references/matt-pocock/skills/engineering/ask-matt/PHASE-BOUNDARIES.md` from the supplied corpus, pinned `49dd158`, SHA-256 `a8aa20158609ef39e2b308b6ba0660c91066838d07a867202e63a7744a88a3ed`. Provenance is retained in the canonical protocol without a runtime corpus dependency.

Environment: Python `3.14.6`, `Darwin arm64`, stdlib and existing tooling only.

| Exact command | Result |
| --- | --- |
| `python3 -m unittest discover -s system/evals/tests -p test_phase_boundary.py -v` | PASS: 4 tests; 8 authored transcript cases, negative mutations, single-owner/link checks and relocated standalone package closure. |
| `python3 scripts/build-plugins.py --output .scratch/B15-phase-boundary/plugins` | PASS: 10 package outputs in scratch. |
| `python3 scripts/validate-protocols.py --plugins .scratch/B15-phase-boundary/plugins` | PASS: protocol registry, source links and generated package closure. |
| `python3 system/evals/validate_suite.py` | PASS: 43 source skills; inventory, catalog budget, declarations, local links/anchors. |
| `python3 -m unittest discover -s system/evals/tests -p test_*.py -v` | PASS: all 48 tests, including prior integrated contract tests and real packaged subprocess exercises. |
| `git diff --check` | PASS: no whitespace errors. |
| `python3 -m unittest discover -s system/evals/evals -p test_evidence_binding.py -v` | PASS: all 11 evidence-binding tests. |

Source/test SHA-256 fingerprints (ticket excluded from its own fingerprint):

```text
4c5cdb4cac961e096ad1521d3757cbff3f125c0acfcc1216b971d9cf16089f03  system/protocols/context-coordination.md
ac6611d7bb2f7985952e2784a3625cb07235a7a5a308bd0dfa45a5909e118272  system/protocols/skill-declarations.md
4c22f1a3eceb66e1f04c7203dac5bdde8f000f35ae6613e0e6f58f0035592f9a  system/protocols/registry.json
f1ac464793d5e93b71ebe092ef142335c20a9700f9f80d3abc40000808dd42db  system/skills-src/build/acs-implement/SKILL.md
fd27d7a51dc8b181bf6ffdd7c6dc6b78f3184803fa2244a6cabb679f8214e18c  system/evals/tests/test_phase_boundary.py
d0641abf0a64a109bf212a665900efee009ab0221ba81c9d64633dc576adc9e5  system/evals/fixtures/phase-boundary-transcripts.json
```

Generated output manifest: `928` files, SHA-256 `2fed1223dc5d192294bbe960ef5595acc57166aea08729d2f9870e8121440845` of sorted, indented JSON mapping relative paths to SHA-256, with a trailing newline. Scratch holds the full manifest and raw command logs; the commands, results and source fingerprints above remain sufficient when scratch is unavailable.

### Limitations

The transcript fixtures are explicitly authored examples, not observed model or agent sessions. They check both persistence branches and invalid order/envelope mutations; static checks bind them to the prose contract. They do not establish host-runtime or live-model compliance, estimate actual context capacity, or implement a coordinator runtime. The relocated package check validates closure and the new anchor; external URL reachability was not tested. Independent acceptance review is still required before ticket completion.

## Parent acceptance

2026-10-23: reconciled source passed canonical plugin build, derived-surface check, protocol and suite validators, 91 eval tests and 19 contract tests. [Independent review](../evidence/third-batch-review.md) found no blockers. Constraint scanning remains heuristic; fixture checks do not prove general model compliance. Canonical integration resolved shared-file conflicts and retained all provenance sections.
