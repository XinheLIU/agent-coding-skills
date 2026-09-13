---
name: implement
description: Deliver a verifiable change end-to-end — decompose it into dependency-ordered tickets, render the ticket DAG, dispatch parallel TDD sub-agents through the orchestrator, and verify the result on the running system. Use when a task with acceptance criteria is ready to implement — bootstrap, feature, or bugfix alike.
---

# Implement — the delivery loop

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [change.task, verification.acceptance_criteria]
  retrieves: [design.contracts, system.dependencies, operations.environment]
  produces: [change.implementation_evidence, change.ticket_graph]
  updates: [source.implementation, source.tests, run.orchestration_state]
  invalidates: [verification.for_changed_code]
  handoff_to: [code_review, release]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.

This skill starts **after** the spec phase. Its input is a locked, verifiable change — a user story with test scenarios, a spec section with criteria, a bug report with reproduction steps, or a bootstrap request backed by accepted technical decisions. Its output is working code, verified end-to-end on the running system, with evidence.

## Gate: a verifiable change or nothing

Check that the change has acceptance criteria an agent can test — at code level and at experience level (browser or local run). If criteria are missing:

- **Small gap** — ask one or two focused questions inline, offering ranked technical options when the user only has a vague preference. Lock the answers into criteria and proceed.
- **Real design work** — intent exploration, spec authoring, or architecture decisions belong to the design phase. Name the missing artifact and route there; do not simulate it here.

Proceed only with criteria in hand. Everything downstream keys off them.

## Understand, then decompose

Read the current state (the codebase, or its absence) and the desired end state (criteria, accepted contracts, design decisions). Decomposition follows from that understanding — a bootstrap, a feature, and a bugfix all take the same path: what must change, in what order, with what proof. There are no modes.

Apply [the decomposition rules](references/decomposition-rules.md). Write each ticket from [the template](templates/ticket.md) to tracked `docs/changes/<change-id>/tasks/<task-id>.md` (preserve an existing tracker's home and IDs). Each ticket carries its criterion references, `depends_on`, affected surfaces, verification expectations, and shared-write risks. A small change stays one ticket.

## Render the graph

Generate a manifest from the tickets and render the interactive HTML DAG with [`draw-portfolio-dag`](../../craft/meta/draw-portfolio-dag/SKILL.md). Show the user the frontier before dispatching. Re-render on every ticket transition so a returning user sees live progress: done (green), in progress (yellow), frontier (orange), blocked (blue).

## Orchestrate the frontier

Track run state in `docs/changes/<change-id>/run/state.json` ([schema](references/state-schema.json)). Loop until every ticket is done or failed:

1. Compute the frontier: tickets whose dependencies are all done.
2. Filter for parallel safety — worktrees isolate files, not semantics; shared contracts, migrations, and generated artifacts still serialize (rules in [decomposition rules](references/decomposition-rules.md#parallel-safety)).
3. Dispatch each safe ticket to a sub-agent running [`tdd`](../tdd/SKILL.md) with its criteria and prerequisite evidence.
4. Await completions; collect evidence; merge worktrees in dependency order; update state and re-render the graph.
5. A failed ticket is marked failed with its evidence — its dependents stay blocked, everything else continues. Report failures in the envelope; the user retries specific tickets.

Dispatch, await, collect, and reclaim are the four operations of [the orchestration protocol](references/orchestration-protocol.md); the herdr binding is primary, the in-process Agent tool is the fallback. `state.json` is Run Context — disposable after reconciliation; the tickets are the retained record.

## Verify end to end

Code-level green is not done. Start the system the way a user would (documented run command, dev server, CLI) and exercise the delivered behavior — browser session, local run, or integration suite. Record commands, environment, and results. If the system cannot start, that is a failed verification with evidence, not a skipped step.

## Return the envelope

Return the [shared handoff envelope](../../craft/context/init-context/references/PROTOCOL.md#handoff-envelope): criterion → ticket → evidence → revision mapping, end-to-end verification result, failed tickets with blocking effects, and the single next action. Code review and refactoring belong to the quality suite (`review-code-quality`, `refactor-code`); no commit or release is implied.
