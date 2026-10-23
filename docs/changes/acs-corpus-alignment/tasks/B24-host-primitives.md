# B24-host-primitives: Bind coordination duties to host primitives

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: B15-phase-boundary
affects: `system/docs/harness-architecture.md` adapter table; `system/protocols/context-coordination.md`
Effort: M

## Scope

Control flow is specified as prose for the agent to emulate: claims, dispatch, progress, approval.

Record, per duty, which host primitive implements it:

| Duty | Host primitive |
| --- | --- |
| Claims | Worktrees plus a single writer |
| Dispatch | Subagents |
| Progress | The host todo list |
| Approval | A hook |

The prose keeps only what must be serialized and why. Apply the rule that an approval belongs at a gate, not mid-build.

## Inputs

- Analysis: §9.1, §10 B24.
- Sources: the SDLC playbook ("Hooks are the approval gates"); Superpowers' deference to native worktrees and skills.

## Verification

- The adapter table covers all four duties with a named primitive or an explicit "unavailable" row.
- Each prose paragraph that restates a primitive is either removed or marked as the semantic rule.
- `validate-protocols.py` passes.

## Blockers

none

## Coordination proposal

Overlaps B23 (kernel) and B8 (approval class). Separate files except `context-coordination.md`.

## Evidence

Implemented the four-duty adapter table in `system/docs/harness-architecture.md` and routed `context-coordination.md` to it. Every binding remains explicitly unavailable until host/session verification records concrete evidence; no host hook, subagent API, or todo runtime is claimed as implemented. Coordination prose labels dispatch, claims, reconciliation, progress, and approval as semantic rules. Existing B15 phase-boundary text, canonical ownership, and authorization boundaries remain intact.

Acceptance checks and contribution-relative hashes are recorded in the implementation report for this run. Checks cover the four table rows, explicit availability, preserved phase-boundary and shared-semantics sources, scratch plugin build and read-only `--check`, protocol/package validation, suite validation, and existing regression tests. These are structural/package checks, including previously authored fixture checks; they are not model behavior runs or proof of runtime host enforcement. Generated output remains under `.scratch/B24-host-primitives/` for parent integration. Parent review and acceptance remain pending.

## Parent acceptance

2026-10-23: integrated validation passed (110 suite tests, 19 evidence checks, build/check and validators). Follow-up compaction corrections passed configured focused tests and validators. [Independent acceptance review](../evidence/fourth-batch-review.md) found no remaining blockers. Named-tokenizer proof is not live-host certification; security challenger fixtures are authored, not an observed independent model security review.
