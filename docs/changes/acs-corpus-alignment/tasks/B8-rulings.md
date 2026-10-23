# B8-rulings: Record rulings and bound retries instead of stalling

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: B2-questioning-protocol
affects: `system/protocols/context-coordination.md`; `system/protocols/orchestration.md`; handoff envelope in `skill-declarations.md`
Effort: M

## Scope

The loop stops on open questions and retries through the user.

Add:
- the three-class taxonomy from B2 (mechanical, taste, user challenge) as the rule for execution-time decisions;
- a ruling record: `Ruling: <what> — <why> — <cost if wrong>`, kept in the run's recovery entry and promoted to Persistent Changes when consequential;
- a "Rulings made" list in the handoff envelope;
- stop only for destructive, security-sensitive or externally visible actions, or a hopeless plan;
- bounded autonomous retries for a failed ticket before the user is asked.

This reuses the existing authorization rule; it does not widen it.

## Inputs

- Analysis: §7.3, §10 B8.
- Sources: Superpowers `subagent-driven-development:19-31` ("rulings, not stalls"); gstack `autoplan:69-100`.

## Verification

- The envelope schema and its section list carry rulings.
- A fixture run with an open taste decision records a ruling and continues.
- A destructive action still stops; a test asserts the stop class list.
- Retry count is bounded and recorded.

## Blockers

B2 defines the classifier this ticket references.

## Coordination proposal

Shares `orchestration.md` with B7/B19 and `skill-declarations.md` with B15. Sequence B2 → B8 → B7.

## Evidence

Implemented for review; `Status: in_progress` and `Readiness: needs-review` remain until parent acceptance.

- Added execution-time mechanical/taste/user-challenge routing, the exact ruling format, recovery-entry recording, consequential promotion, and the four authorization-aware stop classes in `context-coordination.md`.
- Added required **Rulings made** to the shared envelope schema and its consumers. The existing phase-boundary fixtures now carry an empty rulings list where appropriate.
- Added a default of two autonomous retries after the initial attempt, persisted counters across resume/redispatch, evidence-backed correction, current verification, early stops, and exhausted-budget reporting. The minimal `acs-implement` caller update removes its contradictory user-only retry instruction; the supervisor approved this consistency edit.
- `system/evals/tests/test_rulings.py` adds six checks covering source contracts, eleven authored fixture cases, negative mutations, and relocated standalone packaging. The fixtures are authored contract examples, **not observed model behavior or independent model transcripts**. No runtime enforcement claim is made.
- Validation: 97 source/package tests and 19 evidence eval tests passed; suite validator passed for 43 source skills; scratch package build, builder `--check`, protocol/package closure, and six revision-bound evidence rows passed. Generated packages remain under `.scratch/B8-rulings/plugins`, separate from tracked output.
- Completion source fingerprint: `sha256:d1e8a634a2a7dff7c1e0fcc72c1e6e0d1ed971b48794064b0fe2e534d945e1b6`; dispatch baseline: `sha256:9340cf15e7b2274e710196f5e261fc3554901dc522ba30d24c266a3e0d1ec237`. Fingerprints cover nonignored tracked/untracked `system/`, `scripts/`, `catalog/`, and `.gitignore`, including symlink targets; ticket/evidence documentation and generated scratch are excluded. Per-file baseline, tested hashes, exact commands, timestamps, and raw logs are in `.scratch/B8-rulings/`.
- Initial focused validation had one incorrect test expectation that shared semantics would remain a link in packaged output. Corrected the assertion to verify the existing injection behavior; the complete final suite passed. Shared-semantics source link and generator remain unchanged.
- Remaining review: independent parent acceptance; actual model adherence remains unmeasured. B7 review/fix rounds are not implemented here and must retain B8's authorization and bounded failure-retry stops when integrated.

## Parent acceptance

2026-10-23: integrated validation passed (110 suite tests, 19 evidence checks, build/check and validators). Follow-up compaction corrections passed configured focused tests and validators. [Independent acceptance review](../evidence/fourth-batch-review.md) found no remaining blockers. Named-tokenizer proof is not live-host certification; security challenger fixtures are authored, not an observed independent model security review.
