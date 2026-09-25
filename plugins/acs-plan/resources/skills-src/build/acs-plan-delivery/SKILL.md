---
name: acs-plan-delivery
description: Turn accepted product scope or designs into delivery tickets and an openable HTML plan with an embedded DAG. Use after scope confirmation, to break a substantial change into smaller tickets, or to reconcile dependencies and readiness as decisions and execution change.
---

# Plan Delivery

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [change.accepted_scope]
  retrieves: [product.accepted_intent, change.requirements, verification.acceptance_criteria, design.relevant_decisions, design.contracts, change.tickets, change.implementation_evidence, system.affected_modules]
  produces: [change.tickets, change.ticket_graph]
  updates: [change.delivery_readiness, run.derived_views]
  invalidates: [run.dependent_plans]
  handoff_to: [design, implementation]
```

Shared semantics: [shared protocol](../../context/acs-init-context/references/PROTOCOL.md#skill-declarations); shared writes and claims: [Coordination](../../../protocols/context-coordination.md). Existing authorization persists. A planning request authorizes the plan, not implementation. Working Memory holds run recovery; Persistent Memory holds reusable domain records, including proposed review inputs. Save referenced conclusions before formal review or dependent handoff. For human-facing reports and review feedback, use [Presenter](../../../protocols/presenter.md); views carry source revisions and never own domain facts.

## Enter from Product or Design

Plan one accepted change, preserving its canonical ID and tracker. Product supplies scope, outcomes, priorities, and roadmap/spec references; Design supplies testable requirements, relevant UX behavior, contracts, migration constraints, and remaining questions. Record consumed revisions and reuse substantive answers regardless of which skill produced them.

After Product's grilling confirms scope for a concrete change, generate the delivery plan as the default handoff. Reuse the confirmation already given; no second grilling round is required. A confirmed problem or demand verdict alone is insufficient: if product scope remains unsettled, retain the Product report and open questions. A specific missing design decision becomes a blocker in the delivery plan.

**Planning-ready** means enough accepted scope exists to identify useful outcomes and concrete blockers. **Execution-ready** is per implementation ticket: testable criteria and checks exist, necessary decisions/contracts are settled and current, external preconditions are satisfied, and prerequisite tickets have completed with applicable evidence. Missing design blocks only affected slices. Existing conventions can settle a simple change without new design artifacts.

If scope itself is unsettled, return that question to Product. Use [acs-explore-unknowns](../../../../skills/acs-explore-unknowns/SKILL.md) when broad uncertainty needs investigation; reuse its existing decision tickets rather than creating a second decision backlog.

## Create or reconcile the graph

1. **Inspect inputs and current implementation.** Resolve accepted scope, criterion/decision references, existing tickets, relevant source, and evidence. Identify changed premises on a resumed run. Finish when each proposed outcome or blocker has a source; keep insufficiently understood work coarse and explicitly unready.
2. **Slice outcomes.** Apply [decomposition rules](references/decomposition-rules.md). Keep one ticket for a small change; put execution checklists inside Run Context. Reuse IDs by parent, scope, and outcome. Each implementation ticket links its criteria, input revisions, affected surfaces, checks, and concurrency risks. Work whose criteria are still being designed links accepted product intent and stays unready.
3. **Expose design blockers.** Create a design ticket only for a concrete question preventing a slice from becoming executable. Record the question, affected tickets, responsible skill, and decision/check that resolves it. Route missing behavior/criteria to `acs-settle-requirements`, experience questions to the relevant UX skill, and contracts/migrations to technical design. Link existing questions instead of duplicating them. Specialists own answers and acceptance; the planner owns sequencing.
4. **Persist and validate.** Use the [ticket template](templates/ticket.md) for new local records at `docs/changes/<change-id>/tasks/<task-id>.md`; preserve established trackers and schemas. Record true prerequisites in `depends_on`; keep write/resource conflicts in coordination notes. Check cycles, missing IDs, and scope coverage: every accepted outcome maps to a slice or an explicit unresolved blocker, and every available criterion maps to a ticket/check or a stated omission. Accepted scope changes return to Product; missing design returns to Design.
5. **Present the plan.** Follow the [HTML delivery report contract](references/delivery-report.md) to generate `docs/changes/<change-id>/delivery-plan.html` using [acs-draw-portfolio-dag](../../authoring/acs-draw-portfolio-dag/SKILL.md) (reference procedure; capability not installed). Reconcile scanner warnings, then open the report in the available browser and return its clickable path. The report contains accepted scope/outcomes, design blockers, the ready frontier, the next action, ticket details/evidence, and the embedded DAG. Return canonical ticket references, consumed revisions, and changed edges/reasons alongside the report. Planning ends here; invoke `acs-implement` only when execution is in scope.

## Reconcile across sessions

After a decision, execution result, or scope/input revision changes, reconcile affected tickets and downstream consumers. Preserve stable IDs, completed evidence, and unrelated work. Mark stale inputs `needs-review`; a completed prerequisite with disputed evidence must not unlock its dependents. Record why edges changed. Split or supersede pending tickets with replacement links; a superseded ticket is not a satisfied prerequisite. Rewire its dependents to the accepted replacements before scheduling. Coordinate with the claim holder before changing active work.

Design resolves its question with accepted artifact/evidence links; `acs-plan-delivery` then checks whether affected implementation tickets are ready. `acs-implement` owns execution status and evidence through the coordinator, refreshes the same delivery-plan report for ordinary progress, and returns scope/dependency changes here. Completion checkboxes alone never complete the parent change.

Canonical tickets retain boundaries, dependencies, readiness, and durable status. Specs retain normative requirements. Claims and scheduling state remain Run Context. The DAG manifest, HTML, and Mermaid are reproducible views, not additional stores of truth.
