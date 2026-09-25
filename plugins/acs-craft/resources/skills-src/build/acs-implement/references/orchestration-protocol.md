---
protocol: acs:orchestration
version: 1.1.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/orchestration.md
---

# Orchestration protocol

Last updated: 2026-09-25

How `acs-implement` coordinates ticket execution. The skill logic uses four abstract operations when delegation is available; a verified host binding supplies their implementation. The [harness architecture](../../../../docs/harness-architecture.md) owns the host boundary. With no authorized delegation, the active agent executes serially and retains the same canonical evidence and state semantics.

## The four operations

| Operation | Contract |
| --- | --- |
| `dispatch(ticket) → agent_ref` | Start an isolated sub-agent executing the `acs-tdd` skill against one ticket. The prompt carries the ticket file path, criterion references, prerequisite evidence paths, and the evidence file it must write. |
| `await(agent_refs) → completions` | Block until at least one dispatched agent reaches a terminal state (done, blocked, failed). |
| `collect(agent_ref) → evidence` | Read the agent's evidence file and terminal output; validate the criterion → test/evidence → revision mapping is present. |
| `reclaim(agent_ref)` | Reconcile contributions and release verified disposable resources. Preserve unmerged work; merging or committing follows the user's Git authorization. |

## Evidence contract

Every dispatched agent writes evidence to the coordinator-resolved Working path, normally `<work-root>/<run-id>/evidence/<ticket-id>.md`, before finishing: criteria addressed, tests with exact commands and results, revision/diff identity, deviations and environment assumptions. Terminal output supplements the file; it never replaces it. `collect` fails a ticket whose evidence is missing or claims green without commands. Before downstream handoff or cleanup, reconcile the minimum necessary evidence into the ticket's Persistent change/verification home and hand off that accessible reference. Keep raw output in Working.

## Select a host binding

Use capabilities verified in the current session, not a preferred product or model name. An in-process sub-agent API or external orchestrator can implement the four operations. Check delegation authorization, resource access, claims, and isolation before selecting parallel execution. The [herdr example](../../../../docs/runtime-bindings/herdr.md) records one optional binding separately from this protocol.

Without authorized delegation or safe claims, execute the ready tickets serially as the active agent; collect criterion-linked evidence and reconcile canonical status after each ticket. Missing optional parallelism is not a blocker. A missing required execution tool is a concrete blocker for the affected ticket.

Without worktree isolation, shared-write risks serialize work. Parallel dispatch requires the semantic safety rules even when files are disjoint. Worktree creation, merge, and cleanup remain host operations governed by existing task and Git authorization.

## State lifecycle

Resolve the run directory and its single recovery entry from memory configuration under the [shared protocol](../../../../protocols/skill-declarations.md#repository-configuration-and-resolution). The default entry is `<work-root>/<run-id>/state.md`; it owns one next action, blockers, canonical references and consumed revisions.

An optional `<work-root>/<run-id>/execution.json` ([schema](state-schema.json)) stores subordinate scheduler details: agent references, timestamps, evidence pointers and a derived frontier. The recovery entry links it. Its per-ticket statuses are scheduler observations derived from canonical tickets, never independent project status. Update affected scheduler observations and the recovery entry together on each transition, then refresh the derived DAG when useful.

An existing JSON recovery entry can remain canonical when explicitly configured and carrying the recovery information above; do not add a competing `state.md` or fixed `docs/changes/.../run/` entry. Scheduler transitions are `ready` → `in_progress` → `done` | `failed`, with `blocked` for unmet dependencies. Remove reconciled Working state only after run completion or abandonment; retain tickets and required evidence in Persistent Memory.

## Failure policy

A failed or blocked-and-stuck agent fails its ticket: record the evidence trail, keep its dependents blocked, continue every independent ticket. Never discard another ticket's work to restart a loop. The final envelope lists failed tickets with blocking effects; the user retries specific tickets, which re-enter the loop as `ready`.

## Handoff envelope

The run's return value is the [shared handoff envelope](../../../../protocols/skill-declarations.md#handoff-envelope) — the retired standalone `handoff` skill's format, now produced by every `acs-implement` run: canonical change identity, criterion → ticket → evidence → revision mapping, end-to-end verification result, unresolved questions with blocking effects, and one executable next action.
