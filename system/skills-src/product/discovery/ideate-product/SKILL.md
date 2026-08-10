---
name: ideate-product
description: >
  Entry point and router for product ideation. Diagnoses where a product effort actually
  stands across the three stages — discover the demand, design the solution, scope the MVP —
  then routes to the owning skill instead of running a fixed sequence. Use when the user
  arrives with a product idea, startup concept, feature request, vague problem, or a
  half-finished discovery effort and it isn't obvious which step comes next; or when they ask
  to "work on my product idea", "figure out what to build", or resume a stalled effort.
  Routes to brainstorm, validate-demand, shape-solution, scope-mvp, run-premortem, write-prd.
---

# Ideate Product

Last updated: 2026-08-10

Product ideation is three questions in order. Most efforts fail by skipping one, not by doing
one badly.

```text
1. Is the demand real?      →  brainstorm → validate-demand
2. What is the solution?    →  shape-solution          (key artifact: user stories)
3. What ships first?        →  scope-mvp                (scenario × form × data)
```

This skill diagnoses which question is actually open and routes there. It owns no artifact of
its own and writes no analysis — every substantive output belongs to the skill it routes to.

```text
Layer:    transient — routes state, writes none
Owns:     nothing
Promotes: nothing; it detects unpromoted intent and routes to the owner
```

## Boundary

Routing only. Do not perform the analysis yourself: no demand classification, no user stories,
no feature triage. If you find yourself writing content for a downstream artifact, invoke that
skill instead. Do not route to technical design, architecture, or implementation skills — the
handoff ends at `write-prd`.

---

## Step 1: Read the effort state

Read `docs/agents/memory.md`, the active `state.md`, and the PRD at
`<product-docs>/<slug>/prd.md` when one exists. Read the PRD first: it is the tracked statement
of intent, so anything recorded there is settled, while the working-memory drafts below may be
mid-revision.

| Artifact | Layer | Owner | Complete when |
| --- | --- | --- | --- |
| `discovery/ideas.md` | working | `generate-product-ideas` | Candidates exist, one is selected |
| `discovery/brainstorm.md` | working | `brainstorm` | Struggle is named with a job statement and forces |
| `discovery/demand.md` | working | `validate-demand` | Demand type and evidence grade A/B/C recorded |
| `discovery/solution.md` | working | `shape-solution` | User stories exist with a first-use moment |
| `discovery/mvp.md` | working | `scope-mvp` | Three axes resolved, P0 ≤ 5 items |
| `discovery/premortem.md` | working | `run-premortem` | Failure modes with mitigations |
| `<product-docs>/<slug>/prd.md` | **human** | `write-prd` | Part 1 states persona, pain, and one user story; later parts filled or explicitly `Pending` |

The PRD is the only one in a tracked layer. The rest are drafts under a git-ignored work root —
useful now, gone when the effort ends.

If no artifacts and no memory protocol exist, say so and offer `/manage-context` Phase A first —
without it, each skill has nowhere durable to write.

Check for an unpromoted core idea: a Green `demand.md` with no PRD means the validated reason for
this project exists only in a disposable directory. Route to `/write-prd` before continuing, and
say why.

## Step 2: Diagnose the open question

Route on the **earliest** stage that is not yet closed. Skipping forward is the failure mode
this skill exists to prevent.

| Situation | Route to |
| --- | --- |
| No candidate idea, exploring a space | `/generate-product-ideas` |
| Idea exists, the struggle isn't articulated | `/brainstorm` |
| Struggle named, demand unproven or disputed | `/validate-demand` |
| Demand just graded Green, nothing in the tracked layer yet | `/write-prd` (early mode), then `/shape-solution` |
| Demand graded A/B/C, no solution shape | `/shape-solution` |
| Solution and user stories exist, scope undefined | `/scope-mvp` |
| Scope set, risks unexamined | `/run-premortem` |
| Premortem clear, PRD still `Pending` past Part 1 | `/write-prd` to extend it |
| Evidence grade D on `demand.md` | back to `/validate-demand` |
| Scope change accepted in premortem | back to `/scope-mvp` |
| Effort shipped but its PRD was never written | `/write-prd`, or `/manage-context` Phase B for the wider sweep |

Two cases override the table:

- **User asks to skip a stage.** State which question is still open and what it costs to
  proceed without it, then follow their decision. They may have evidence outside the artifacts.
- **A stage looks complete but its evidence is weak.** An artifact can exist and still not close
  its question — a `demand.md` at grade D, a `solution.md` with no first-use moment, an MVP with
  12 P0 items. Route back rather than forward.

## Step 3: Report and hand off

State the diagnosis in three lines, then invoke the skill:

```text
Stage:    [1 Demand / 2 Solution / 3 Scope]
Open:     [the specific question that is not answered]
Evidence: [which artifacts exist and what they establish]
→ /[skill-name]
```

Hand off once. Do not chain multiple skills in one turn — each stage produces a decision the
user should see before the next stage consumes it.

---

## Support skills

Available at any stage, outside the three-stage line:

- `/research` — trace a claim to primary sources when evidence is disputed
- `/domain-modeling` — resolve vocabulary when terms are used inconsistently
- `/prototype` — build a throwaway artifact when a question needs a demo to answer
- `/wayfinder` — use instead of this router when the route spans more than one session

## Key Principles

- The three questions are ordered because each answer is an input to the next. A solution
  designed against unvalidated demand is precise and wrong.
- Route to the earliest open question, not the most interesting one.
- An artifact existing is not the same as its question being closed. Check the evidence.
- This skill's output is a route, not an analysis. Producing content here means the routing
  failed.

