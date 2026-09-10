# Product

Last updated: 2026-09-09

From raw idea or existing codebase to durable product intent an engineer can build against. Nine skills contribute to one shared product model through two lanes: greenfield creation and existing-product improvement.

Read [the product memory contract](../craft/context/init-context/references/product-memory.md) for the record schema and update rules. The source contract lives with context initialization; each product skill exposes the same file through a local `references/product-memory.md` symlink so packaged copies can materialize it without separate maintained versions. The shared need-layering framework (surface / deep / fundamental needs, vision synthesis, module fit) lives canonically at [`discovery/validate-demand/references/need-layers.md`](discovery/validate-demand/references/need-layers.md) and is symlinked into the skills that apply it. The shared-understanding protocol (question blocks of 4–5 with recommended answers, facts-vs-decisions, and the confirm-before-final close) lives canonically at [`discovery/validate-demand/references/shared-understanding.md`](discovery/validate-demand/references/shared-understanding.md) and is symlinked the same way into every interactive product skill.

## The lanes

Product work answers the earliest open question. Greenfield work starts with demand; existing
product work starts with current behavior.

```mermaid
flowchart LR
    subgraph GF["Greenfield lane"]
        BR[brainstorm] --> VD{validate-demand}
        VD -->|Green| DS[shape-solution] --> SM[scope-mvp]
        VD -->|Red| STOP([stop / re-frame])
    end
    subgraph EP["Existing-product lane"]
        MCP[map-current-product] --> VDI{validate-demand}
        VDI -->|Green or already evidenced| SPI[scope-product-increment]
        VDI -->|Red| STOP2([stop / re-frame])
    end
    SM --> PM[run-premortem]
    SPI --> PM
    PM --> PRD[write-prd] --> ENG(["design gate → engineering/feature/spec"])
    IP[ideate-product] -.->|routes| GF & EP
```

`validate-demand` is the kill switch when demand or improvement value is disputed: a Red verdict
here is the cheapest possible outcome. It is also the first promotion point — a Green verdict is
where the core idea earns its place in the tracked product docs, via an early `write-prd` run.
`write-prd` is then the exit: it consolidates accepted shared knowledge into the product document
`engineering/feature/spec` consumes — directly, or through the optional `design/` phase when the
PRD leaves experience or structure open (see the Design Gate in `write-prd`).

## Where to start

| You have | Start with |
| --- | --- |
| A vague idea or problem statement | `brainstorm` |
| A specific idea and you want a go/no-go | `validate-demand` |
| An existing codebase/app and you want to know what it already does | `map-current-product` |
| User stories from existing code | `map-current-product` |
| A validated greenfield demand with no solution shape | `shape-solution` |
| A designed solution with too many features | `scope-mvp` |
| An existing-product improvement to scope | `scope-product-increment` |
| A scoped plan you want to stress-test | `run-premortem` |
| A Green demand verdict and nothing tracked yet | `write-prd` — early mode, Part 1 only |
| A scoped existing-product increment and an existing PRD | `write-prd` — delta mode |
| Completed artifacts and you need the spec | `write-prd` |
| No idea which of the above applies | `ideate-product` — it diagnoses and routes |

Skills can also run standalone: `validate-demand` works as a reality check on any claim,
`run-premortem` stress-tests any plan, and `map-current-product` can reverse-engineer user
stories from an existing codebase with no prior discovery.

## The skills

### Discovery (`discovery/`) — is this problem worth solving?

**`brainstorm`** — turns an ambiguous idea into a Jobs-to-be-Done brief through Socratic
dialogue: who the user is, what job they hire the product for, how they solve it today,
and what constrains any solution. Asks questions in small blocks, keeps it conversational,
and stops before feature scoping. Enriches shared personas, problems, constraints, assumptions, and questions. **Credit: adapted from
[Jesse Hattabaugh's superpowers brainstorming skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md)
for the Socratic conversation pattern.**

**`validate-demand`** — the gate. Grades the evidence behind the demand claim on a
five-level scale, scores the Three Soul Questions (who is the user, where is the pain, why
choose you), classifies the demand as painkiller / reward / vitamin, slices to a beachhead
segment, and issues a traffic-light verdict with three concrete next steps. Green promotes the
core idea via an early `write-prd` run and then proceeds to `shape-solution` for greenfield
work, or `scope-product-increment` for active-product improvements; Red stops the effort or
sends it back to `brainstorm`, promoting nothing. Enriches scoped demand assessments and evidence, including existing gaps and questions.

For active-product improvements, it grades support tickets, analytics, usage funnels, churn,
lost-deal notes, stakeholder evidence, and observed sessions before an increment is scoped.

The verdict is per-claim. When multiple validated claims accumulate for one product, or the
user states a larger mission, it synthesizes a candidate `vision` record (greenfield Vision
Synthesis rules in `references/need-layers.md`) — inferred, linked to its claims, and paired
with an open confirmation question. It never confirms the vision or lets a Green stand in for
whole-product validation.

**`map-current-product`** — the existing-product baseline. Reads product docs and code to
extract product-facing roles, routes/flows, implemented user stories with layered needs
(surface / deep / fundamental), candidate product visions synthesized from the story set and
confirmed with the user in one consolidated message, module need-fit and vision-resilience
verdicts, in-progress work, planned work, gaps, and source evidence. It does not scope future
changes; it gives
`scope-product-increment`, `shape-solution`, and `write-prd` a reliable picture of what exists
today. Enriches source-backed current capabilities, journeys, gaps, questions, and coverage. **Credit: adapts PM-Skills user-story discipline,
OpenSpec brownfield-first exploration, and the prior `shape-solution` codebase inventory into a
standalone analysis.**

**`run-premortem`** — assumes the project has already failed 6 months out, then works
backward to root causes, scored risks, and prevention strategies. Before enumerating causes
it grills the product thread with the user — vision, demand verdict, MVP fit, and the
discovery behind them — and its Mission / Coherence
dimension reads any vision record and asks how the product could ship its wedge yet fail its
mission. Lives in `discovery/`
but runs late in the pipeline: it reads the MVP scope and demand evidence, so it is most
effective after `scope-mvp` and immediately before `write-prd`. Also works standalone on
any plan. Enriches shared risks, mitigation proposals, assumptions, and monitoring measures.

**`ideate-product`** — the router. Diagnoses which question is actually open across the
greenfield and existing-product lanes by reading the effort state and existing artifacts, then
routes to the owning skill. It performs no analysis and owns no artifact; readiness comes from relevant evidence, decisions, and unresolved questions, not file existence.

### Definition (`definition/`) — what exactly are we building?

**`shape-solution`** — turns a validated demand or current-product baseline into a concrete
solution shape: a 3D Persona, a 4-Act Narrative, a 4-Stage User Journey, and the scenarios the
solution must cover. Output depth adapts to complexity within shared HTML; complex systems may need diagrams and illustrative demos. It enriches existing personas, desired capabilities, journeys, gaps, and questions while preserving observed behavior.

**`scope-mvp`** — resolves the three scope axes (scenario × product form × data
availability), then triages features into P0 (build now), P1/P2 (not yet), and Not-To-Do
(never for this MVP), anchored to one falsifiable core assumption. Includes an ambition
review that challenges whether the scope is the right bet, not just a complete one — reading
the product's vision record as the 12-month ideal, or persisting its own ideal as a candidate
vision when none exists. It stays
greenfield/MVP-focused; existing-product iteration routes to `scope-product-increment`. Enriches shared scope decisions, capability priorities, assumptions, and measures.

**`scope-product-increment`** — scopes active-product improvement as an explicit
`ADDED / MODIFIED / REMOVED` behavior delta against source-backed current capabilities or accepted product intent. It records
P0/P1/out-of-scope, acceptance criteria, edge cases and recovery, instrumentation, success
metrics, and refinement notes. Enriches capability deltas, acceptance, scope decisions, questions, and measures. **Credit: adapts PM-Skills
acceptance criteria, edge-case, instrumentation, and refinement-note patterns; OpenSpec delta
language; and gstack scope postures with explicit opt-in for scope changes.**

**`write-prd`** — consolidates durable product knowledge in `<product-docs>/<product-slug>/product.html`. Its PRD reading index links canonical records instead of maintaining a separate summary document. It promotes accepted conclusions with necessary rationale and evidence, preserves IDs and user edits, and replaces working conclusions with pointers. A user-confirmed vision promotes to `overview`; an inferred candidate stays working with its confirmation question linked. Run early after Green demand, then again as scope settles or an increment is accepted. It can also consolidate explicit standalone inputs without inventing missing validation or scope.

## Handoff to design

The PRD fixes *what* to build. When *how it looks* or *how the system is shaped* is still
open, `write-prd` routes through the `design/` phase before `engineering/feature/spec`.

For UX questions — layout, information hierarchy, visual system, interaction states — the
entry point is `design/ux/design-context`, which establishes design authority (the root
`DESIGN.md`). From there the UX pipeline builds the canonical prototype
(`docs/design/prototype.html`), with each stage linking its surfaces back to `product.html`
capability records:

```
design-context → interaction-design → visual-design-variants → design-implement
```

When a design question surfaces during product work that conversation cannot settle — how a
state transition should feel, what a layout should look like — the loop goes to
`design/ux/prototype`: throwaway variants, decision recorded, control returns to the product
skill that raised it. The prototype code is disposable; the decision it bought is not.

For technical design questions — domain model, module boundaries, system architecture — the
entry point is `design/technical/`.

Both branches may run for the same effort. See `design/README.md` for the full routing table.

## The two handoff deliverables

The pipeline's final handoff is **research** plus **roadmap**, aligned with the product's missions and visions:

- **Research** is the full analysis: current behavior, personas, layered needs, gaps, evidence, and coverage. It accumulates in `discovery.html` while working and its accepted conclusions live as durable records in `product.html`.
- **Roadmap** is the `roadmap` section of `product.html`: research findings decomposed into prioritized concrete changes. Each ticket links its research basis, its mission/vision alignment, and either a standalone spec file (`specs/<spec-slug>.md`) or a prototype request.

## Shared knowledge and lifecycle

The [shared protocol](../craft/context/init-context/references/PROTOCOL.md) defines four lifecycles. `discovery.html` holds Run Context analysis; `product.html` can contain North Star, Current State, and Change Context records. A linked Markdown spec is the single canonical requirements source for its change. Existing paths remain valid; new local-only change records use tracked `docs/changes/<change-id>/`.

Retain requirements, accepted decisions, compact verification, and release references after completion. Canonical ticket status lives once in its tracker or roadmap article; other views reference it. Engineering `spec` consumes existing requirements, and `tasks` creates child tickets only for independently deliverable slices.

`state.md` points to the relevant records and maps the effort to its product. Increments reuse the product identity. Existing Markdown product documents remain readable and canonical until an authorized migration reconciles their content and updates routing; do not create a competing HTML copy.

HTML is the semantic source for discovery and product documents. Spec files are Markdown. Skill instructions and engineering task state retain their existing formats. There is no Markdown or hidden JSON twin of the HTML documents. Native headings, tables, `<details>`, stable IDs, and links serve both human reading and targeted agent edits.

## How skills enrich the same model

Navigation groups cover users/problems, capabilities/journeys, gaps/opportunities, questions/assumptions, evidence, scope/decisions, risks/measures, roadmap (product.html only), and research (discovery.html only). Groups are not exclusive skill territories. Records use stable subject IDs, such as `capability-export`, `gap-export-feedback`, `question-export-channel`, or `ticket-export-notification`.

Every product skill can contribute relevant observations, evidence, gaps, and questions. Specialized methods determine assessment authority: demand validation grades demand; scope skills assess commitments; premortem assesses risks; PRD consolidation promotes accepted intent. No contributor silently overrides another assessment or a user decision.

For example:

| Run | Shared contribution |
| --- | --- |
| Map current product | Creates a gap: export completion is invisible; records inspected web routes and code evidence |
| Validate demand | Adds support evidence of repeated retries to that same gap; assesses importance for the affected users |
| Shape solution | Links a proposed notification and an unanswered channel question |
| Scope increment | Adds the authorized in-app notification decision and acceptance criteria; email stays deferred |
| Premortem | Adds a linked lost-notification risk and recovery proposal |
| Write PRD | Promotes accepted intent and essential evidence, leaving working pointers |

The gap stays open until observed implementation resolves it. A deferred feature is not disproved demand, an inferred persona is not an observed user, and a hypothetical risk is not incident evidence.

Standalone runs create only the useful partial records they can establish. Later skills match subjects before enriching them; reruns do not multiply records. Questions retain answers and evidence when resolved. A changed premise marks materially dependent conclusions for review. Record inspected coverage so missing content is not mistaken for absent behavior.

Shared files require serialized writes: concurrent analysis may prepare patches, but one coordinator applies them against current records. Tags provide identity, not locking.

## Promotion and handoff

Apply the durability test: if deleting the effort would lose needed product intent or rationale, promote it. `write-prd` moves or reconciles accepted conclusions into durable records, preserves essential evidence there, verifies links, then replaces working conclusions with pointers. No necessary durable link may depend on a disposable effort file.

**Roadmap decomposition** is part of promotion: when the `research-coverage` record says research is ready, `write-prd` decomposes accepted findings into roadmap tickets. Every P0 finding maps to at least one ticket; every ticket links its research basis and its mission/vision alignment. For each ticket it assigns the type:

- **Spec ticket** (`data-ticket-type="spec"`): settled requirements become a ticket with a generated `specs/<spec-slug>.md` file
- **Prototype ticket** (`data-ticket-type="prototype"`): an open design question becomes a ticket whose short request hands off to `design/ux/prototype`

The PRD is a reading order over durable records: document info → problem/goals → solution overview → detailed requirements → roadmap → launch. The roadmap section is the PRD's forward-looking view. Partial readiness is expressed through specific open questions and their blocking effects. Design and engineering consume the configured product path and relevant anchors; they do not require a particular prior skill to have run.

## Behavioral checks

[Shared-memory regression scenarios](evals/shared-memory.json) cover standalone partial analysis, repeated enrichment, context-sensitive identity, changed premises, durable promotion, legacy migration, and stale patches. They define behavioral acceptance cases for isolated skill evaluations; they are not an automated runner.

## Credit

The `brainstorm` skill adapts the Socratic conversation pattern from [Jesse Hattabaugh's superpowers brainstorming skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md), which pioneered the one-question-at-a-time exploration flow and the hard gate before design.

The existing-product lane adapts principles from PM-Skills, OpenSpec, and gstack while keeping
their reference snapshots read-only. See [`../../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

## Typical workflows

**Greenfield, full run** — a new idea taken all the way to a spec:
`brainstorm` → `validate-demand` → `shape-solution` → `scope-mvp` → `run-premortem` →
`write-prd`. Expect the gate to send weak ideas back — that is the pipeline working, not
failing. After `write-prd`, the Design Gate routes to `spec` directly or through the
optional `design/` phase.

**Reality check** — someone asks "is this worth building?" about an existing idea:
run `validate-demand` alone. It grades whatever evidence exists and issues a verdict
without requiring upstream artifacts.

**Existing codebase** — inherit or revisit a product that already has code:
`map-current-product` extracts implemented user stories, in-progress features, planned work, and
gaps directly from the code. If the user asks for the next improvement, validate the evidence if
needed, then run `scope-product-increment` and `write-prd` in delta mode.

**Improve existing product** — a live app has a known problem:
`map-current-product` if no baseline exists → `validate-demand` when the evidence is weak or
disputed → `scope-product-increment` → optional `run-premortem` → `write-prd` delta mode.

**Stalled effort** — discovery started weeks ago and nobody remembers the state:
`ideate-product` reads `state.md` and the artifacts, reports which question is open, and
routes there.

**Plan stress-test** — a plan exists (from this pipeline or anywhere else) and needs a
devil's-advocate pass before commitment: run `run-premortem` alone on the plan.
