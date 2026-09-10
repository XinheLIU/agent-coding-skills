---
name: tasks
description: Decompose an active change into independently deliverable child tickets with dependencies and acceptance references. Keep fine-grained execution steps in a temporary checklist. Use when implementation boundaries or ordering need to be made explicit.
---

# Tasks — Decompose deliverable slices

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [change.requirements, implementation.approach]
  retrieves: [design.contracts, system.dependencies, operations.checks, change.existing_tickets]
  produces: [change.child_ticket_proposals, implementation.parallel_boundaries]
  updates: [run.execution_checklist]
  invalidates: [run.dependent_plans]
  handoff_to: [coordinator, implementation]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Use the canonical change/spec, accepted design, and implementation approach supplied through [delivery](../../../../workflows/feature-delivery.md). Substantive planning is required; a particular plan filename or planning skill is not.

## Propose the decomposition

1. Read relevant requirement/criterion IDs and priorities, accepted contracts, affected dependencies, operational checks, and existing tickets.
2. Identify vertical slices with an independently verifiable outcome. A small change stays one ticket; do not manufacture children for file edits or test/code steps.
3. Match existing child tickets by parent, scope, and outcome before proposing new ones. Keep existing IDs. For new local records use tracked `docs/changes/<change-id>/tasks/<task-id>.md`; preserve existing tracker homes.
4. Each child references its parent, canonical spec/criteria, accepted decisions/contracts and revisions, affected surfaces, `depends_on`, verification expectations, and blocking questions. Use [the ticket template](references/tasks-template.md) only when the tracker lacks a format.
5. Check dependencies for cycles and missing IDs. Propose parallel boundaries only when shared contracts, config, generated files, migrations, tests, and source edits will not conflict; different filenames alone are insufficient.
6. Keep fine-grained execution steps in the run plan/checklist, grouped under canonical ticket references. They are not new tickets or another status source.

## Verification expectations

Choose checks from acceptance criteria, regression risk, preservation constraints, and project conventions. Behavioral slices need meaningful tests; TDD requests order the expected failing test before its implementation. Simple reversible documentation edits may use reference/schema checks. Do not default all tests off or introduce a new dependency without authorization.

## Return to the coordinator

Return proposed child records, coverage mapping, dependencies, shared-write risks, omissions, and next action. The coordinator serializes ticket writes and claim acquisition and schedules execution. This skill proposes safe boundaries; it does not dispatch agents or create shadow claim tickets.

Verify every accepted criterion maps to a slice/check or an explicit omission with impact; every child belongs to the same parent; references resolve; rerunning with unchanged inputs proposes no duplicate tickets. Do not edit normative requirements, start implementation, commit, or push.
