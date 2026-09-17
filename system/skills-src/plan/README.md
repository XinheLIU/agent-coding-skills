# Plan

Last updated: 2026-09-17

From raw idea or existing codebase to durable product intent an engineer can build against. Ten skills contribute to one shared product model through two lanes: greenfield creation and existing-product improvement.

Read [the product memory contract](../craft/context/acs-init-context/references/product-memory.md) for the record schema and update rules. The source contract lives with context initialization; each product skill exposes the same file through a local `references/product-memory.md` symlink so packaged copies can materialize it without separate maintained versions.

## The lanes

Product work answers the earliest open question. Greenfield work starts with demand; existing product work starts with current behavior.

```mermaid
flowchart LR
    subgraph GF["Greenfield lane"]
        BR[acs-brainstorm] --> VD{acs-validate-demand}
        VD -->|Green| DS[acs-shape-solution] --> DO[acs-define-outcomes]
        VD -->|Red| STOP([stop / re-frame])
    end
    subgraph EP["Existing-product lane"]
        MCP[acs-map-current-product] --> VDI{acs-validate-demand}
        VDI -->|Green or already evidenced| DOI[acs-define-outcomes]
        VDI -->|Red| STOP2([stop / re-frame])
    end
    DE[acs-design-experiment] -.->|optional: resolve uncertainty| DS
    DO --> PM[acs-run-premortem]
    DOI --> PM
    PM --> PRD[acs-write-prd] --> DESIGN(["design gate → design/requirements/acs-settle-requirements"])
    IP[acs-ideate-product] -.->|routes| GF & EP
```

`acs-validate-demand` is the kill switch: a Red verdict here is the cheapest possible outcome. `acs-write-prd` is the exit: it consolidates accepted intent into the product document that `design/requirements/acs-settle-requirements` consumes — directly, or through the optional UX and technical design sub-phases when the PRD leaves experience or structure open.

## Where to start

| You have | Start with |
| --- | --- |
| A vague idea or problem statement | `acs-brainstorm` |
| A specific idea and you want a go/no-go | `acs-validate-demand` |
| An existing codebase and you want to know what it already does | `acs-map-current-product` |
| A validated greenfield demand with no solution shape | `acs-shape-solution` |
| A solution shape that needs verifiable commitments | `acs-define-outcomes` |
| An existing-product improvement to scope | `acs-define-outcomes` |
| A feature list to prioritize, cut, or reduce to an MVP | `acs-define-outcomes` — commitment and depth |
| A specific assumption to validate cheaply before committing | `acs-design-experiment` |
| A scoped plan you want to stress-test | `acs-run-premortem` |
| A multi-session effort with interdependent open decisions | `acs-explore-unknowns` |
| A Green demand verdict and nothing tracked yet | `acs-write-prd` — early mode, Part 1 only |
| No idea which of the above applies | `acs-ideate-product` — it diagnoses and routes |

## The skills

### Discovery — is this problem worth solving?

**`acs-brainstorm`** — turns an ambiguous idea into a Jobs-to-be-Done brief through Socratic dialogue: who the user is, what job they hire the product for, how they solve it today, and what constrains any solution. Asks questions in small blocks and stops before feature scoping. Enriches shared personas, problems, constraints, assumptions, and questions.

**`acs-validate-demand`** — the gate. Grades evidence behind a demand claim on a five-level scale, scores the Three Soul Questions (who is the user, where is the pain, why choose you), issues a traffic-light verdict with three concrete next steps. Green promotes the core idea via an early `acs-write-prd` run; Red stops or sends back to `acs-brainstorm`. Also grades active-product improvement evidence: support tickets, analytics, usage funnels, churn, lost-deal notes.

**`acs-map-current-product`** — the existing-product baseline. Reads product docs and code to extract product-facing roles, routes/flows, implemented user stories with layered needs, module need-fit verdicts, in-progress work, planned work, gaps, and source evidence. Does not scope future changes; gives `acs-shape-solution`, `acs-define-outcomes`, and `acs-write-prd` a reliable picture of what exists today.

**`acs-run-premortem`** — assumes the project has failed 6 months out, then works backward to root causes, scored risks, and prevention strategies. Lives in discovery but runs late in the pipeline — most effective after `acs-define-outcomes` and immediately before `acs-write-prd`. Also works standalone on any plan.

**`acs-ideate-product`** — the router. Diagnoses which question is actually open by reading the effort state and existing artifacts, then routes to the owning skill. Performs no analysis and owns no artifact.

**`acs-explore-unknowns`** — maps a multi-session effort into dependency-ordered decision tickets when the destination is known but the route is not. It coordinates decisions; domain skills still own their answers.

### Definition — what exactly are we building?

**`acs-shape-solution`** — turns a validated demand or current-product baseline into a concrete solution shape: target experience, connected journeys, required capabilities, and the scope space they sit in (primary scenario × product form × data grade).

**`acs-define-outcomes`** — turns a chosen solution into verifiable product commitments: outcome-oriented user stories with observable success states, end-to-end verification scenarios, and a commitment level and depth for every capability. Commitment (`committed` / `reduced` / `deferred` / `excluded` / `open`) says whether the product promises it; depth (`full` / `narrowed` / `fixed` / `manual`) says how far it goes. The two axes are what a P0/P1 ladder cannot express — a capability that ships, but narrower than shaped. Delivery sequencing stays downstream.

**`acs-design-experiment`** — designs a bounded experiment to resolve a named, falsifiable uncertainty cheaply before full commitment. The experiment returns evidence to `acs-shape-solution` (if the target experience changes) or `acs-define-outcomes` (if a commitment needs adjustment). The experiment's scope never becomes the product's scope.

**`acs-write-prd`** — consolidates durable product knowledge in `docs/product/<product-slug>/product.html`. Promotes accepted conclusions with necessary rationale and evidence, preserves IDs and user edits. Runs early after Green demand, then again as scope settles or an increment is accepted.

## Handoff to design

`acs-write-prd` fixes *what* to build. The design gate routes to `design` when *how it looks* or *how the system is shaped* is still open. Entry is `design/requirements/acs-settle-requirements`, which defines testable acceptance criteria before UX or technical design begins.

## Typical workflows

**Greenfield, full run:**
`acs-brainstorm` → `acs-validate-demand` → `acs-shape-solution` → `acs-define-outcomes` → `acs-run-premortem` → `acs-write-prd`

**Reality check on an existing idea:**
`acs-validate-demand` alone — grades whatever evidence exists and issues a verdict without requiring upstream artifacts.

**Existing codebase:**
`acs-map-current-product` → `acs-define-outcomes` → `acs-write-prd` delta mode

**Stalled effort:**
`acs-ideate-product` reads `state.md` and artifacts, reports which question is open, routes there.
