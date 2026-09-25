# Build Workflow

Last updated: 2026-09-25

Turn accepted scope into a delivery graph, and execute the ready implementation slices when authorized.

```text
entry_artifact: accepted product scope or accepted requirements/designs, with canonical references
planning_exit: canonical tickets + dependencies + readiness + open delivery-plan.html with embedded DAG
execution_exit: delivered-scope evidence + remaining blockers + handoff envelope
execution_gate: testable criteria, current necessary decisions, satisfied prerequisites, and execution authorization
```

## Plan or resume delivery

Use [acs-plan-delivery](../resources/skills-src/build/acs-plan-delivery/SKILL.md) (reference procedure; capability not installed) to break a change into tickets or reconcile an existing graph. Product can hand off accepted scope before every design question is settled. Design can hand off a complete design or one resolved blocker. Inputs are reused by canonical ID and revision.

The planner records independently verifiable slices and concrete design blockers, validates dependencies and coverage, and uses `acs-draw-portfolio-dag` to generate the [combined HTML delivery plan](../resources/skills-src/build/acs-plan-delivery/references/delivery-report.md). It opens that report as the planning handoff. Design tickets route to their specialist; ready implementation slices can advance independently. A planning-only request ends with the report and next action.

## Execute ready slices

Use [acs-implement](../resources/skills-src/build/acs-implement/SKILL.md) (reference procedure; capability not installed) for authorized delivery. It invokes `acs-plan-delivery` only when tickets are absent or materially stale, then checks per-ticket readiness and prerequisite evidence. Show the graph before dispatch; reuse authorization already given for implementation.

The coordinator acquires claims and checks shared-write/contract risks before dispatching `acs-tdd` executors. Logical independence alone does not establish safe parallelism. `acs-implement` merges completed work in dependency order, records canonical status/evidence, and refreshes the same HTML plan and DAG, reloading the open report. Design blockers, failures, and stale decisions keep only dependent work blocked.

## Verify and hand off

Use the configured Working Memory recovery entry for the run; orchestration JSON is referenced execution detail, not another source of ticket status or next action. Keep review proposals, accepted contracts and criterion-linked final evidence in Persistent Memory. The [Presenter](../protocols/presenter.md) refreshes the derived delivery view from those records; the next skill consumes source references and revisions.

Exercise delivered behavior on the running system, retaining criterion → ticket → check/evidence → revision mappings. Report undelivered scope and blockers explicitly; child completion never implies parent completion. Return scope/dependency changes to `acs-plan-delivery`, and code ready for assessment to `quality/review` and `test`.

Planning is complete when accepted scope is accounted for, all graph references resolve, readiness/blockers are explicit, and the rendered view matches canonical tickets. Execution is complete only for the verified scope; code-level green alone is insufficient.

Shared context coordination: [context-coordination.md](../protocols/context-coordination.md)
