---
name: ideate-product
description: Route a product effort to the right next step. Use when the user has an idea, feature request, existing codebase, request for user stories from code, existing-product improvement, or stalled discovery effort and it is not obvious which question is still open.
disable-model-invocation: true
---

# Ideate Product

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [product.request]
  retrieves: [product.relevant_context, product.open_questions]
  produces: [product.route_proposal]
  updates: []
  invalidates: []
  handoff_to: [coordinator]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Product ideation has two lanes: greenfield creation and existing-product improvement. Most
efforts fail by skipping the earliest unanswered question, not by answering one badly.

```text
Greenfield:
1. Is the demand real?      →  brainstorm → validate-demand
2. What is the solution?    →  shape-solution          (key artifact: target experience)
3. What are the commitments?→  define-outcomes         (verifiable promises + deferred intent)

Existing product:
1. What exists today?       →  map-current-product      (key artifact: current behavior)
2. Is the improvement real? →  validate-demand          (active-product evidence)
3. What changes and proves done? →  define-outcomes     (ADDED / MODIFIED / REMOVED + verification)

Optional: design-experiment — resolve a named uncertainty cheaply before committing
```

This skill diagnoses which question is actually open and routes there. It owns no artifact of
its own and writes no analysis — every substantive output belongs to the skill it routes to.


## Boundary

Routing only. Do not perform the analysis yourself: no demand classification, no user stories,
no feature triage. If you find yourself writing content for a downstream artifact, invoke that
skill instead. Route away from product when there is no user-visible outcome, such as a pure
architecture refactor or code-quality cleanup.

---

## Step 1: Read shared product knowledge

Read [the product memory contract](references/product-memory.md), `docs/agents/memory.md`, and active `state.md`. Resolve the durable `product.html` and working `discovery.html` through their pointers; read legacy documents when those remain canonical. Follow relevant record anchors and inspect their evidence, authority, coverage, and review state. This skill reads records and routes; it does not update product findings.

| Knowledge needed | Ready when |
| --- | --- |
| Problem and persona | Specific job, struggle, context, and desired outcome established |
| Current capabilities | Relevant behavior and assessed coverage have source evidence; unassessed surfaces remain explicit |
| Demand assessment | The scoped claim has sufficient evidence and a Green verdict, with no unresolved contradiction that undermines it |
| Solution and journeys | Proposed stories, first-use moment, and necessary scenarios are established |
| Scope space | Primary scenario, product form, and data grade are resolved and coherent |
| Commitments | Every capability carries a commitment level, `reduced` ones name their depth and lost capability, and `excluded` ones cite a constraint |
| Increment scope | Evidence-backed behavior delta, acceptance, edges, and measurement are established |
| Risks | Relevant failure scenarios and mitigation decisions have been assessed |
| Durable intent / PRD | Accepted conclusions are promoted; unresolved questions and their blocking effects remain explicit |

Readiness is about the relevant records, not whether a skill ran or a file/section exists. A partial standalone analysis can answer the needed question; a polished report with disputed evidence cannot. Route on shared open questions and materially stale conclusions, regardless of which skill raised them.

If a Green demand assessment or accepted scope exists only in working memory, route to `write-prd` for promotion before continuing. If routing and an unambiguous destination are absent, recommend `init-context` before persistence; existing evidence can still support an in-conversation diagnosis.

## Step 2: Diagnose the open question

Route on the **earliest** stage that is not yet closed. Skipping forward is the failure mode
this skill exists to prevent.

Existing-product routing overrides the greenfield table:

| Situation | Route to |
| --- | --- |
| "What does this codebase/app do?" or "write user stories from this codebase" | `map-current-product` |
| "Improve/iterate/refine this existing app" and affected current behavior is not evidenced | `map-current-product` (next: `define-outcomes`) |
| Existing-product improvement with weak or disputed evidence | `validate-demand` using active-product evidence (next if Green: `define-outcomes`) |
| Existing-product improvement with baseline and evidence already clear | `define-outcomes` |
| Existing-product improvement but solution shape is unclear or unduly constrained | `shape-solution` first, then `define-outcomes` |
| Architecture refactor, cleanup, or internal redesign with no user outcome | `design/technical/harden-architecture` or `design/technical/audit-architecture` |

| Situation | Route to |
| --- | --- |
| No candidate idea, exploring a space | `generate-product-ideas` |
| Idea exists, the struggle isn't articulated | `brainstorm` |
| Struggle named, demand unproven or disputed | `validate-demand` |
| Demand just graded Green, nothing in the tracked layer yet | `write-prd` (early mode), then `shape-solution` |
| Demand verdict Green, no solution shape | `shape-solution` |
| Solution shape exists, outcomes not committed | `define-outcomes` |
| Specific assumption needs cheap validation before committing | `design-experiment` |
| Current product mapped, increment undefined | `define-outcomes` |
| Outcomes defined, risks unexamined | `run-premortem` |
| Accepted conclusions are unpromoted, or the PRD needs reconciliation after an increment | `write-prd` to extend it |
| Demand evidence is assumption-only | back to `validate-demand` |
| A scope change was accepted in premortem | `define-outcomes` to update outcome contracts |
| Effort shipped but its PRD was never written | `write-prd`, or `sync-context` for the wider sweep |

Two cases override the table:

- **User asks to skip a stage.** State which question is still open and what it costs to
  proceed without it, then follow their decision. They may have evidence outside the artifacts.
- **A stage looks complete but its evidence is weak.** An artifact can exist and still not close
  its question — an assumption-only demand assessment, proposed journeys with no first-use moment, a
  commitment set that needs an "and also" to describe. Route back rather than forward.

## Step 3: Report and hand off

State the diagnosis in three lines, then invoke the skill:

```text
Stage:    [Greenfield demand/solution/scope or Existing-product baseline/validation/increment]
Open:     [the specific question that is not answered]
Evidence: [which artifacts exist and what they establish]
→ /[skill-name]
```

Hand off once. Do not chain multiple skills in one turn — each stage produces a decision the
user should see before the next stage consumes it.

---

## Support skills

Available at any stage, outside the three-stage line:

- `research` — trace a claim to primary sources when evidence is disputed
- `engineer-domain-model` — resolve vocabulary when terms are used inconsistently
- `explore-unknowns` — use instead of this router when the route spans more than one session

## Key Principles

- The questions in each lane are ordered because each answer is an input to the next. A solution
  designed against unvalidated demand, or an increment scoped without a baseline, is precise and wrong.
- Route to the earliest open question, not the most interesting one.
- An artifact existing is not the same as its question being closed. Check the evidence.
- This skill's output is a route, not an analysis. Producing content here means the routing
  failed.
