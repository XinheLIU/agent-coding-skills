---
name: acs-implement
description: Deliver a verifiable change end-to-end using dependency-ordered tickets from acs-plan-delivery, criterion-based execution, and running-system verification. Use for accepted bootstrap, feature, or bugfix scope; execute serially or through authorized host delegation.
---

# Implement — the delivery loop

Last updated: 2026-09-25

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

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.

Accept an authorized change, prepare or reuse its graph, then execute ready implementation tickets; other slices may still await design. Its input is a locked, verifiable change — a user story with test scenarios, a spec section with criteria, a bug report with reproduction steps, or a bootstrap request backed by accepted technical decisions. Its output is working code, verified end-to-end on the running system, with evidence.

## Reuse or prepare the delivery graph

Read canonical tickets and their consumed input revisions. If tickets are missing or scope, dependencies, or relevant inputs have changed, invoke [acs-plan-delivery](../acs-plan-delivery/SKILL.md). It owns decomposition and graph reconciliation; reuse an existing valid graph. A small change may remain one ticket. Planning-only requests return that handoff without dispatch.

On execution results, update canonical status/evidence through the coordinator and refresh derived run state. Return newly discovered scope or dependency changes to `acs-plan-delivery`; keep independent ready work moving.

## Gate: a verifiable change or nothing

Check that each selected implementation ticket has current criteria, settled necessary designs/contracts, satisfied prerequisites, and acceptance checks an agent can test — at code level and at experience level (browser or local run). If criteria are missing:

- **Small gap** — ask one or two focused questions inline, offering ranked technical options when the user only has a vague preference. Lock the answers into criteria and proceed.
- **Real design work** — intent exploration, spec authoring, or architecture decisions belong to the design phase. Name the missing artifact and route there; do not simulate it here.

Proceed only with execution-ready implementation tickets. Design tickets route to their specialist; unready slices stay blocked while independent ready work proceeds. If none are ready, return the blockers and next design/planning action.

## Render the graph

Refresh the existing `delivery-plan.html` with [`acs-draw-portfolio-dag`](../../resources/skills-src/authoring/acs-draw-portfolio-dag/SKILL.md) (reference procedure; capability not installed), following the [delivery report contract](../acs-plan-delivery/references/delivery-report.md). Show the frontier before dispatching. On ticket transitions, re-scan canonical tickets, update the derived next action, re-render with `--plan` at the same path and storage key, and reload the open report. This preserves scope, blockers, and evidence alongside live progress: done (green), in progress (yellow), frontier (orange), blocked (blue).

## Orchestrate the frontier

Resume through the coordinator-configured recovery entry, default `<work-root>/<run-id>/state.md`. It may reference `<work-root>/<run-id>/execution.json` ([schema](references/state-schema.json)) for scheduler details of selected implementation tickets. If an existing project explicitly configures JSON as its recovery entry, use that entry alone. Canonical tickets own durable status; the canonical graph retains design blockers. Loop until the authorized execution scope is verified or no safe implementation ticket can advance; report remaining design, readiness, and failure blockers:

1. Compute the implementation frontier: pending implementation tickets whose criteria/design are current and ready, external preconditions hold, and prerequisites are done with applicable evidence. Never dispatch design tickets or treat superseded/stale prerequisites as satisfied.
2. Filter for parallel safety — worktrees isolate files, not semantics; shared contracts, migrations, and generated artifacts still serialize (rules in [decomposition rules](../acs-plan-delivery/references/decomposition-rules.md#parallel-safety)).
3. Recheck ticket/input revisions and acquire its exclusive claim through the coordinator. Execute with [`acs-tdd`](../acs-tdd/SKILL.md), serially as the active agent or through authorized delegation with its criteria and prerequisite evidence.
4. Collect completed execution evidence; reconcile contributions in dependency order, merging worktrees only within Git authorization; update state and re-render the graph.
5. A failed ticket is marked failed with its evidence — its dependents stay blocked, everything else continues. Report failures in the envelope; the user retries specific tickets.

Dispatch, await, collect, and reclaim are the four operations of [the orchestration protocol](../../resources/protocols/orchestration.md). Bind them to verified host capabilities when delegating; otherwise execute serially with the same evidence contract. Scheduler details are Working Memory and derive ticket status from canonical tickets. Update the sole recovery entry with the next action; do not maintain another independent continuation state. Retain criterion-linked verification and consequential failures in Persistent Memory before handoff or run cleanup.

## Verify end to end

Verify the delivered scope against its criteria; report still-blocked or unimplemented parent scope separately. Child completion does not establish parent completion.

Code-level green is not done. Start the system the way a user would (documented run command, dev server, CLI) and exercise the delivered behavior — browser session, local run, or integration suite. Record commands, environment, and results. If the system cannot start, that is a failed verification with evidence, not a skipped step.

## Return the envelope

Return the [shared handoff envelope](../../resources/protocols/skill-declarations.md#handoff-envelope): criterion → ticket → evidence → revision mapping, end-to-end verification result, failed tickets with blocking effects, and the single next action. Code review and refactoring belong to the quality suite (`acs-review-code-quality`, `acs-refactor-code`); no commit or release is implied.
