---
protocol: acs:orchestration
version: 1.1.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/orchestration.md
---

# Orchestration protocol

Last updated: 2026-10-23

How `acs-implement` coordinates ticket execution. The skill logic uses five abstract operations when delegation is available; a verified host binding supplies their implementation. The [harness architecture](../resources/docs/harness-architecture.md) owns the host boundary. With no authorized delegation, the active agent executes serially and retains the same canonical evidence and state semantics.

## The five operations

| Operation | Contract |
| --- | --- |
| `dispatch(ticket) → agent_ref` | Start an isolated sub-agent executing the `acs-tdd` skill against one ticket. Record immutable `BASE` (the dispatch source revision or tree fingerprint) in the recovery entry before execution. The prompt carries BASE and its fingerprint method/scope, the ticket file path, criterion references, prerequisite evidence paths, and the evidence file it must write. |
| `await(agent_refs) → completions` | Block until at least one dispatched agent reaches a terminal state (done, blocked, failed). |
| `collect(agent_ref) → evidence` | Read the agent's evidence file and terminal output; validate each criterion → exact command/result → tested revision → timestamp row against the independently resolved current completion source identity. Reject stale rows with `STALE-REVISION`. |
| `review(ticket, package) → verdicts` | After green collection, obtain a read-only per-ticket review from a reviewer who did not implement the ticket. Validate the package before entering `in_review`; return spec compliance first, then quality, and explicit cannot-verify items. Follow the [ticket review gate](#ticket-review-gate). |
| `reclaim(agent_ref)` | Reconcile contributions and release verified disposable resources. Preserve unmerged work; merging or committing follows the user's Git authorization. |

## Evidence contract

Every executor, delegated or serial, writes evidence to the coordinator-resolved Working path, normally `<work-root>/<run-id>/evidence/<ticket-id>.md`, before finishing. Use the [evidence template](../resources/skills-src/build/acs-implement/references/evidence-template.md) and its adjacent JSON sidecar. Each acceptance row records criterion, exact command (working directory and relevant environment included), result, tested source revision or tree fingerprint, and actual command completion timestamp in RFC 3339 with timezone. Record deviations, omissions, environment assumptions, and raw-output references. Terminal output supplements the file; it never replaces it.

`BASE` is immutable dispatch provenance, not the revision that final tests must match: implementation changes the source. Before running a check, resolve its tested source identity; ensure the source does not change during the command. At collection, independently resolve the ticket's current completion source identity using the same method and scope. Use a full commit ID only for a clean tested source tree. For uncommitted work, fingerprint the tested source including relevant tracked changes, deletions, and untracked source/test inputs; record the reproducible method and path scope. HEAD alone cannot identify dirty work. Exclude evidence, run logs, and generated outputs from the source fingerprint to avoid self-reference; include generator source/configuration and validate generated output separately. Do not exclude implementation or test inputs merely to keep evidence current.

`collect` runs the [stdlib row checker](../resources/skills-src/build/acs-implement/scripts/check-evidence.py) with the recorded BASE and independently measured current completion identity, never a revision copied from the submitted rows. Missing/malformed rows, missing commands/revisions/timestamps, a BASE mismatch, and failed/not-run results block green collection. A row whose revision differs from the current completion identity is rejected with `STALE-REVISION`; rerun on the current source, never relabel an old result. Earlier red runs remain history with their original identities, outside the current acceptance rows. Source changes during verification or later reconciliation require fresh checks before downstream handoff. A timestamp records when a check ran; it does not make stale source current.

The checker validates recorded bindings, not command execution or criterion coverage. The coordinator also checks actual output, criterion coverage, environment and fingerprint scope. Before downstream handoff or cleanup, reconcile the minimum necessary evidence into the ticket's Persistent change/verification home and hand off that accessible reference. Keep raw output in Working.

Adapted principles: exact-command evidence from gstack `ship` at `35dd014` (`references/gstack/source/ship/SKILL.md`) and revision-keyed verification from pstack at `0b8e952` (`references/pstack/skills/poteto-mode/scripts/orch/store.ts`). These are source-checkout provenance, not runtime dependencies.

## Select a host binding

Use capabilities verified in the current session, not a preferred product or model name. An in-process sub-agent API or external orchestrator can implement the five operations. Check delegation authorization, resource access, claims, and isolation before selecting parallel execution. The [herdr example](../resources/docs/runtime-bindings/herdr.md) records one optional binding separately from this protocol.

Without authorized delegation or safe claims, execute the ready tickets serially as the active agent; collect criterion-linked evidence and reconcile canonical status after each ticket. Missing optional parallelism is not a blocker. A missing required execution tool is a concrete blocker for the affected ticket.

Without worktree isolation, shared-write risks serialize work. Parallel dispatch requires the semantic safety rules even when files are disjoint. Worktree creation, merge, and cleanup remain host operations governed by existing task and Git authorization.

## State lifecycle

Resolve the run directory and its single recovery entry from memory configuration under the [shared protocol](skill-declarations.md#repository-configuration-and-resolution). The default entry is `<work-root>/<run-id>/state.md`; it owns one next action, blockers, canonical references and consumed revisions.

An optional `<work-root>/<run-id>/execution.json` ([schema](../resources/skills-src/build/acs-implement/references/state-schema.json)) stores subordinate scheduler details: agent references, timestamps, evidence pointers and a derived frontier. The recovery entry links it. Its per-ticket statuses are scheduler observations derived from canonical tickets, never independent project status. Update affected scheduler observations and the recovery entry together on each transition, then refresh the derived DAG when useful.

An existing JSON recovery entry can remain canonical when explicitly configured and carrying the recovery information above; do not add a competing `state.md` or fixed `docs/changes/.../run/` entry. Scheduler transitions are `ready` → `in_progress` → `in_review` → `done`; findings take `in_review` → `fix_round` → `in_review` after fresh collection. Execution failures enter `failed`; missing dependencies, review inputs, authorization, or a required reviewer enter `blocked`. `in_review` and `fix_round` are scheduler observations only: the canonical ticket stays `in_progress` with `Readiness: needs-review` until acceptance. Remove reconciled Working state only after run completion or abandonment; retain tickets and required evidence in Persistent Memory.

## Ticket review gate

Before dispatch, retain immutable BASE **and a retrievable source snapshot** sufficient to produce the ticket's complete diff, including dirty/untracked inputs. HEAD alone is insufficient for dirty work. Construct the review package from this BASE to the independently resolved completion identity after green collection. Do not use `HEAD~1` or the implementer's claimed revision. Record the fingerprint method/scope, canonical ticket/input revisions, and package reference in the sole recovery entry (or its subordinate scheduler JSON).

The package must contain readable **brief**, **acceptance criteria**, and **diff** references plus BASE, completion revision, and consumed input revision identity. The brief is the accepted ticket scope and binding design constraints; do not infer it from the patch. Reject missing, empty, inaccessible, or stale inputs with `INVALID-REVIEW-PACKAGE` before requesting a verdict. Never pass the implementer's report, terminal narrative, self-review, or copied rationale to the reviewer, including during re-review. The coordinator keeps execution evidence and performs the B19 checks separately. The [scheduler schema](../resources/skills-src/build/acs-implement/references/state-schema.json) describes the package fields; host bindings enforce readability and freshness, which JSON shape alone cannot establish.

The reviewer reads the brief and criteria before the diff, remains read-only, and returns, in order:

1. **Spec compliance**: `pass`, `fail`, or `cannot_verify`, with criterion-linked missing/extra/misunderstood behavior and source locations.
2. **Quality**: `pass` or `changes_requested`, with Critical/Important/Minor findings and source locations.
3. **Cannot verify from the diff**: an explicit list (empty when none) of criterion IDs, missing evidence, and the focused check needed. Report the reviewed source and consumed input identities with the verdicts.

The coordinator resolves every cannot-verify item against current criterion-linked evidence before completion; unresolved items block `done`, and a discovered defect enters a fix round. A missing/failed spec verdict cannot be overridden by quality approval. Critical/Important findings block completion; record nonblocking Minor observations for whole-branch review. Accept only when spec compliance is established, quality has no blocking findings, all cannot-verify items are resolved, and B19 evidence still covers the independently measured current source. Source or consumed-input changes invalidate the verdict: reconcile the accepted inputs, collect fresh evidence as needed, and review the changed diff before `done` or downstream handoff.

A fix round is one correction dispatch plus one scoped re-review. Persist `fix_rounds_used: 0` before the initial review. Before each correction increment and record the counter, prior reviewed revision (`FIX_BASE`), findings, executor reference, and evidence paths. Rounds **1–3 resume the implementer**; rounds **4–5 use a fresh implementer**, carrying the same accepted brief, criteria, unresolved findings, BASE and prior fix history. If the host cannot resume or provide the required fresh executor, record that capability blocker; do not silently reset or substitute the seat. After each correction, collect fresh B19 evidence and re-review the findings and `FIX_BASE` → current diff, retaining the original BASE and brief. Re-review checks addressed findings and new breakage in the fix; observations on untouched code go to whole-branch review without extending this loop.

After round 5, do not dispatch round 6 automatically. Record a [B8 ruling](context-coordination.md#execution-time-rulings) on unresolved findings and the blocking next action. A ruling may reject a demonstrably inapplicable finding with criterion/source evidence; it cannot waive unmet criteria, unresolved verification, authorization, or explicit user gates. An actual defect or exhausted plan remains blocked for the specific decision or revised plan. Preserve counters/history across resume, redispatch, or context reset; missing history blocks automatic continuation.

Review fix rounds and [operational retries](#failure-policy) are separate counters. A review finding after successful execution consumes a fix round, not an operational retry. A failed execution/tool attempt during a fix uses B8's `retries_used` budget, without buying another fix round; resume that round only after successful collection. Neither counter resets the other. B8 authorization stops and stricter existing budgets apply before every correction or retry, even when review rounds remain. Recheck claims, dependencies, accepted inputs and source freshness each time.

The coordinator never fixes code; it routes findings to the implementer. During serial implementation the active agent acts explicitly as the executor; switching back to coordination cannot substitute for an independent review. Workers, including reviewers, never spawn sub-agents. With no authorized delegation, serial implementation remains available, but its self-review cannot fill the independent review seat: use an available authorized independent reviewer (including a human) or retain `blocked` pending that capability. No model choice or additional budget is implied. Keep `acs-review-code-quality` as the separate whole-branch review after ticket gates; this narrow review does not replace it.

Adapted from Superpowers `subagent-driven-development` and `task-reviewer-prompt.md` at `5bf4e78`, Addy Osmani `orchestration-patterns.md` at `aeac41d`, and pstack `shipping.md` at `0b8e952`. ACS deliberately excludes the implementer's report even though the upstream reviewer prompt includes it, and keeps Git/external actions under existing authorization.

## Failure policy

A failed or blocked-and-stuck executor records the failed attempt and its evidence; keep its dependents blocked and continue every independent authorized ticket. Never discard another ticket's work to restart a loop. Apply [execution-time rulings and stop classes](context-coordination.md#execution-time-rulings) before deciding whether to retry; this policy covers delegated and serial execution alike.

Allow at most **two autonomous retries per ticket** after the initial attempt (three attempts total). A stricter existing budget wins. Before the first attempt, record the limit and `retries_used: 0` in the single configured recovery entry. Before each retry, increment and persist `retries_used`, the failed attempt's revision/evidence, the evidence-backed corrective hypothesis, and the next check. Record the result and tested revision after each attempt. Resume, redispatch, a new executor, or a context reset does not reset this ticket's counter. If prior counts cannot be recovered, stop automatic retries and report the missing history rather than assume a fresh budget.

Retry only a recoverable failure with a concrete correction inside existing scope and authorization. Recheck dependencies, claims, and consumed revisions before re-entering `ready`; retain immutable BASE provenance and collect fresh evidence for the current completion identity under the evidence contract. Never relabel an earlier failure or reuse stale green evidence. A failed attempt alone does not ask the user to retry while this safe budget remains.

Stop automatic retries immediately for a pending authorization or user challenge, an explicit gate, any unapproved action in the four stop classes, a hopeless plan, a missing required capability, or no evidence-backed correction. Stop at budget exhaustion even if another correction seems possible. Do not retry an external side effect with an unknown outcome: inspect available state first and retain the unknown if it cannot be resolved. A retry grants no new authorization and never weakens criteria, tests, or verification gates to obtain green.

On execution success, enter the ticket review gate; mark the ticket done only after current criterion-linked verification and review acceptance. Otherwise retain failed/blocked status as applicable, the attempt count, stop reason, evidence trail, and dependent blocking effects in the final envelope and compact Persistent Changes. Ask for the specific missing decision or intervention; only an explicit user-directed retry or approved revised plan can authorize a new bounded budget. Preserve earlier attempt history when recording that budget.

## Handoff envelope

The run's return value is the [shared handoff envelope](skill-declarations.md#handoff-envelope) — the retired standalone `handoff` skill's format, now produced by every `acs-implement` run: canonical change identity, criterion → ticket → evidence → revision mapping, end-to-end verification result, Rulings made, review verdicts and unresolved cannot-verify items, fix-round counts, retry counts and stop reasons, unresolved questions with blocking effects, and one executable next action.
