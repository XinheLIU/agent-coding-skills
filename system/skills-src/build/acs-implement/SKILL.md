---
name: acs-implement
description: Use when accepted bootstrap, feature, or bugfix scope is authorized for implementation or a delivery run needs resuming.
---

# Implement — the delivery loop

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [change.task, verification.acceptance_criteria]
  retrieves: [design.contracts, system.dependencies, operations.environment, change.tickets, change.ticket_graph]
  produces: [change.implementation_evidence]
  updates: [source.implementation, source.tests, run.orchestration_state]
  invalidates: [verification.for_changed_code]
  handoff_to: [delivery_planning, code_review, release]
```

[Shared semantics](../../../docs/shared-semantics.md#execution)

Apply [phase-boundary persistence](../../../protocols/context-coordination.md#phase-boundaries) when continuing across phases.

Accept an authorized change, use its declared tier to prepare one ticket or a delivery graph, then execute ready implementation tickets; other slices may still await design. Its input is a locked, verifiable change — a user story with test scenarios, a spec section with criteria, a bug report with reproduction steps, or a bootstrap request backed by accepted technical decisions. Its output is working code, verified end-to-end on the running system, with evidence.

## Bounded entry

Read the coordinator's declared [rigor tier](../../../workflows/README.md#rigor-tiers) before dispatch; if absent, declare and record it before continuing. Spike returns an answer through the probe route, not retained implementation. Architectural uses the graph route below.

For **Bounded**, reuse or create one canonical ticket in the established tracker (the [ticket template](../acs-plan-delivery/templates/ticket.md) applies to new local records). Record scope, testable criteria/checks, affected surfaces, settled input revisions, and the short in-chat design with its approval reference. Apply [Questioning](../../../protocols/questioning.md) to missing decisions. Present the design and obtain implementation approval only if that stage/scope is not already authorized; a reply approves the stage actually presented.

With one current execution-ready ticket, proceed directly through the readiness gate, serial `acs-tdd` execution, and verification below. No `acs-plan-delivery` invocation, separate spec, or HTML delivery plan is required. The ticket is the one-node frontier; its status and compact evidence remain canonical, and the recovery entry holds the next action. Keep the same claim, immutable BASE, current source fingerprint, evidence sidecar/checker, and handoff requirements as the graph route. Where the loop says render or re-render, update the ticket and recovery entry for Bounded instead.

If new scope, dependencies, or structural decisions exceed this one-ticket route, stop dependent work, announce and record an upward tier change, and complete the missing stages before execution. Do not silently expand Bounded into a graph or downgrade an Architectural run to skip its gates.

## Reuse or prepare the delivery graph

For Architectural work, read canonical tickets and their consumed input revisions. If tickets are missing or scope, dependencies, or relevant inputs have changed, invoke [acs-plan-delivery](../acs-plan-delivery/SKILL.md). It owns decomposition and graph reconciliation; reuse an existing valid graph. A small change may remain one ticket. Planning-only requests return that handoff without dispatch.

On execution results, update canonical status/evidence through the coordinator and refresh derived run state. Return newly discovered scope or dependency changes to `acs-plan-delivery`; keep independent ready work moving.

## Gate: a verifiable change or nothing

Check that each selected implementation ticket has current criteria, settled necessary designs/contracts, satisfied prerequisites, and acceptance checks an agent can test — at code level and at experience level (browser or local run). If criteria are missing:

- **Small gap** — ask one or two focused questions inline, offering ranked technical options when the user only has a vague preference. Lock the answers into criteria and proceed.
- **Real design work** — intent exploration, spec authoring, or architecture decisions belong to the design phase. Name the missing artifact and route there; do not simulate it here.

Proceed only with execution-ready implementation tickets. Design tickets route to their specialist; unready slices stay blocked while independent ready work proceeds. If none are ready, return the blockers and next design/planning action.

## Render the graph

For Architectural work, refresh the existing `delivery-plan.html` with [`acs-draw-portfolio-dag`](../../authoring/acs-draw-portfolio-dag/SKILL.md), following the [delivery report contract](../acs-plan-delivery/references/delivery-report.md). Show the ready work before dispatching. On ticket transitions, re-scan canonical tickets, update the derived next action, re-render with `--plan` at the same path and storage key, and reload the open report. This preserves scope, blockers, and evidence alongside live progress. Each node's colour is its [task graph](../../../protocols/task-graph.md) view status, so read progress from that contract rather than from a per-skill colour list.

## Orchestrate the frontier

Resume through the coordinator-configured recovery entry, default `<work-root>/<run-id>/state.md`. It may reference `<work-root>/<run-id>/execution.json` ([schema](references/state-schema.json)) for scheduler details of selected implementation tickets. If an existing project explicitly configures JSON as its recovery entry, use that entry alone. Canonical tickets own durable status; the canonical graph retains design blockers. Loop until the authorized execution scope is verified or no safe implementation ticket can advance; report remaining design, readiness, and failure blockers:

1. Compute the implementation frontier: pending implementation tickets whose criteria/design are current and ready, external preconditions hold, and prerequisites are done with applicable evidence. Never dispatch design tickets or treat superseded/stale prerequisites as satisfied.
2. Filter for parallel safety — worktrees isolate files, not semantics; shared contracts, migrations, and generated artifacts still serialize (rules in [decomposition rules](../acs-plan-delivery/references/decomposition-rules.md#parallel-safety)).
3. Recheck ticket/input revisions and acquire its exclusive claim through the coordinator. Record immutable dispatch `BASE` and the source fingerprint method/path scope in the recovery entry; supply them with the criteria, prerequisite evidence and resolved evidence path to [`acs-tdd`](../acs-tdd/SKILL.md), serially or through authorized delegation.
4. Collect completed execution evidence using the [evidence template](references/evidence-template.md). Independently resolve the current completion source identity and run the [row checker](scripts/check-evidence.py) with that identity and dispatch BASE. Reject `STALE-REVISION` rows and missing command/revision/timestamp bindings; inspect actual output and criterion coverage before accepting. Reconcile contributions in dependency order, merging worktrees only within Git authorization; rerun checks if reconciliation changes tested source, then enter `in_review` through the [ticket review gate](references/orchestration-protocol.md#ticket-review-gate). Supply the accepted brief, criteria, and BASE-to-current diff, never the implementer report. Resolve ordered spec/quality verdicts and cannot-verify items before `done`; findings enter `fix_round` (1–3 resume, 4–5 fresh implementer, then a B8 ruling). Keep review rounds separate from operational retries. The coordinator never fixes code and workers never spawn sub-agents. If an independent reviewer is unavailable, retain the review blocker. Update state and re-render the graph.
5. Record failed attempts and follow the [bounded autonomous retry policy](references/orchestration-protocol.md#failure-policy), including its persisted counter, authorization stops, and fresh evidence requirements. Dependents stay blocked while independent authorized work continues. Report terminal failures, retry counts, and stop reasons in the envelope.

Dispatch, await, collect, review, and reclaim are the five operations of [the orchestration protocol](references/orchestration-protocol.md). Bind them to verified host capabilities when delegating; otherwise execute serially with the same evidence contract. Scheduler details are Working Memory and derive ticket status from canonical tickets. Update the sole recovery entry with the next action; do not maintain another independent continuation state. Retain criterion-linked verification and consequential failures in Persistent Memory before handoff or run cleanup.

## Verify end to end

Verify the delivered scope against its criteria; report still-blocked or unimplemented parent scope separately. Child completion does not establish parent completion.

Code-level green is not done. Start the system the way a user would (documented run command, dev server, CLI) and exercise the delivered behavior — browser session, local run, or integration suite. Record commands, environment, and results. If the system cannot start, that is a failed verification with evidence, not a skipped step.

## Return the envelope

Return the [shared handoff envelope](../../../protocols/skill-declarations.md#handoff-envelope): criterion → ticket → evidence → revision mapping, end-to-end verification result, Rulings made (including pending taste review), failed tickets with blocking effects, and the single next action. Whole-branch code review and refactoring belong to the quality suite (`acs-review-code-quality`, `acs-refactor-code`); no commit or release is implied.
