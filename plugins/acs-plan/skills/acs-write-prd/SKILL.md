---
name: acs-write-prd
description: Consolidate shared product knowledge into a durable HTML product document with a PRD reading view, or reconcile an accepted increment into it. Use when the user asks to write a PRD, preserve validated product intent, consolidate requirements, or update an existing PRD without regenerating it.
disable-model-invocation: true
---

# PRD Writer

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [product.accepted_intent]
  retrieves: [product.evidence, product.current_behavior, change.existing_requirements, design.relevant_decisions]
  produces: [change.canonical_spec, product.reading_index]
  updates: [product.durable_records, change.requirements]
  invalidates: [design.requirement_dependents, verification.criteria]
  handoff_to: [design, delivery_planning]
```

Shared semantics: [shared protocol](../../protocols/skill-declarations.md); shared execution: [Coordination](../../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Preserve accepted product intent so the project still knows what it is building and why after working memory is deleted. Consolidate canonical records rather than retelling each skill's report into a second copy.

## Shared Memory Contract

Read [the product memory contract](../../protocols/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy migration. Read [PRD principles](references/prd-principles.md) for the requirements framework and examples; the shared HTML contract governs storage and updates.


Resolve the product through user paths, `docs/agents/memory.md`, and active `state.md`. Reuse its existing durable home for increments; the effort slug does not create a new product identity. Default to `docs/product/<product-slug>/product.html` only when no existing home conflicts. Read legacy `prd.md` when it remains canonical; migrate only within authorized scope, never maintain a competing HTML truth.

## One change, one requirements source

Reuse the coordinator's canonical ticket ID and spec reference. If a spec already exists, including one created by engineering `spec`, reconcile that same document and preserve its requirement/criterion IDs. Create a spec only when none exists. Preserve established homes; new local-only changes use tracked `docs/changes/<change-id>/`. Product indexes and capability records link change-specific normative text rather than restating it. The canonical tracker owns ticket status; a roadmap summary references that source and revision.

## Read and assess

Accept explicit `--doc <path>` / `-d <path>` inputs, including legacy documents. Without flags, follow state pointers to durable product records and relevant working records. Read prototype decisions when they settle a product question; architectural rationale belongs in an ADR and is linked from product memory.

Use established answers regardless of the producing skill. A standalone run can consolidate explicit requirements, evidence, and user decisions without requiring earlier skill files. Missing facts remain questions; supplied requirements do not imply validated demand or accepted scope beyond the user's authorization.

| Knowledge | PRD use |
| --- | --- |
| Personas, problems, demand assessments | Product purpose, who benefits, why it matters, strength of supporting evidence |
| Vision records | Product identity and purpose framing in Part 0/1; user-confirmed visions promote to `overview`, inferred candidates stay working with their open question linked |
| Current capability evidence | Context for the change, with observed behavior distinct from intended behavior |
| Proposed capabilities and journeys | Desired outcomes, scenarios, flows, and interaction states |
| Accepted scope and deltas | Included/excluded requirements, priorities, acceptance, and rationale |
| Risks, constraints, measures | Edge cases, mitigation decisions, NFRs, instrumentation, success thresholds |
| Decisions and unresolved questions | Decision basis, remaining blockers, launch and design handoffs |

Check for conflicting claims, duplicate subjects, and conclusions marked `needs review`. Reconcile by evidence and recorded authority, not recency. An accepted decision remains recorded while its applicability is disputed; do not silently rewrite it. Do not grade demand, rescope features, invent solution behavior, or accept a mitigation proposal just because it appears in a premortem.

Ask only for unknown information needed for the current result. Product title, platform, timeline, stakeholders, and NFRs may already be answered anywhere in shared memory or the supplied context. Never ask again solely because no particular skill owns the field. Consolidate blocking questions in one user message; continue independent consolidation and record the remaining unknowns with their blocking effects.

## Promote and reconcile

1. Identify accepted or otherwise established durable conclusions. On Green demand, preserve the core problem, persona, job, verdict, and necessary evidence early; solution and scope can remain unresolved. Later runs extend those same records.
2. Match existing durable records by product, actor, outcome, surface, and scenario. Preserve their IDs and user-authored content. New records retain their working IDs unless a collision requires an explicit mapping and link repair.
3. For an accepted increment, apply ADDED / MODIFIED / REMOVED to the relevant intended behavior and scope only. Preserve current observation, unrelated requirements, and rejected alternatives with lasting rationale. A removed behavior remains identifiable for references; record that the intent was superseded instead of reusing its ID.
4. Bring the minimum supporting rationale and evidence into durable storage, or link stable sources. Necessary evidence must not depend on an effort directory scheduled for deletion. Keep raw code inventories and execution narratives in working memory.
5. Build or update the PRD reading index over the canonical records. Add a dated change note with affected record links and the decision/source basis. Do not duplicate normative requirements into the index or a separate PRD file.
6. Verify durable content and links before replacing promoted working conclusions with pointers. Repair cross-record links, record any amendment-to-canonical ID mapping, then return routing updates to the coordinator. Do not erase evidence or unresolved analysis that the active effort still needs.

Promotion does not change a claim's evidence strength. A proposed commitment remains proposed; an open question stays open until answered. A **user-confirmed** vision promotes into `product.html` `overview` with its ID, confirmation date, and links preserved; an **inferred** candidate vision stays in working memory and the PRD links its open confirmation question instead. Never invent a vision or upgrade one by promotion. If a relevant premise changes, mark affected conclusions for review and route the unresolved assessment to the appropriate skill.

## Decompose the roadmap

The roadmap is the `roadmap` section of `product.html`: accepted research findings decomposed into prioritized concrete changes. Decompose only when the effort's `research-coverage` record states research is ready for roadmap; when it says not ready, promote settled records as usual and record what blocks decomposition. Early promotion (a Green verdict, a confirmed vision) never waits on roadmap readiness.

1. Map every committed and reduced finding to at least one `roadmap-ticket`; review overlap between tickets (MECE as judgment, not automation). A ticket that answers no recorded finding needs an explicit user decision as its basis.
2. Every ticket records priority (`p0`/`p1`/`p2`/`deferred`), status, its research basis (links to the gap/opportunity/problem records that justify it), and alignment links to at least one mission or vision.
3. Assign the ticket type:
   - **Spec ticket** (`data-ticket-type="spec"`): requirements are settled. Reuse the canonical spec when present; otherwise create it in the resolved change home (existing product layout may use `specs/<spec-slug>.md`) — problem, solution, requirements with acceptance criteria, explicit out-of-scope, success measures for that one change — opening with a link back to its ticket. The spec is canonical for its change; the ticket is canonical for priority and status. A loose spec another skill drafted may be linked provisionally with a note that this skill should tighten it.
   - **Prototype ticket** (`data-ticket-type="prototype"`): a design question blocks specification. The ticket carries a one-or-two-sentence prototype request as the handoff to `design/ux/acs-validate-prototype` and stays `blocked` until the decision lands; then convert it to a spec ticket linking the decision, or close it.
4. A ticket is intent, not implementation: it never closes a behavior gap, and completing it requires evidence of the resulting behavior. Reruns enrich existing tickets by subject match; they do not duplicate them.

## HTML output and PRD reading order

Durable outputs are shared `product.html` records and the single linked spec per change, structured by the Product contract. Keep existing styling. Add a `<nav id="prd" aria-label="PRD reading order">` linking to actual records or shared sections in this order:

| Reading part | Content to establish or link |
| --- | --- |
| Part 0 — Document info | Product identity, product vision (confirmed, or candidate with its open question linked), stage/readiness, version if used, update date, stakeholders, change notes |
| Part 1 — Problem and goals | Persona, usage scenario, pain, job, demand evidence, user outcomes, requirements index, scope and exclusions |
| Part 2 — Solution overview | Relevant current context, desired business flow, information architecture, linked journeys and capabilities |
| Part 3 — Detailed solution | Per-capability acceptance and initial/trigger/success/error/empty states where relevant; edge/recovery behavior, constraints, NFRs, analytics |
| Part 4 — Roadmap and launch | Link to the `roadmap` section (never a copy of it), milestone decisions, target dates when known, success thresholds, monitoring, remaining launch blockers |

The Part labels provide a familiar reading order, not additional copies of records. A requirement index links capability and scope IDs with brief labels; the full requirement and its acceptance live once. Render tables, lists, and diagrams inside their relevant records. Use semantic HTML and inline CSS; diagrams have adjacent textual meaning and do not require JavaScript to understand the requirements.

For partial or early runs, show which questions prevent a part from being ready and link to them. Do not fill unknown fields with fictional answers or mark the whole document complete because every section exists. Do not add arbitrary edge cases, exclusions, dates, stakeholders, or thresholds to satisfy a template.

## Verification and handoff

Before saving or reporting readiness:

- Confirm problem, persona, and outcomes are specific; demand strength and commitment are accurately represented.
- Check intended behavior, scope/exclusions, flows, relevant edge and recovery cases, and necessary NFRs against the actual effort. Record missing answers as questions with blocking effects.
- Ensure accepted increments trace to affected capabilities and evidence; preserve unrelated records and user edits.
- Verify unique IDs and resolving file/anchor links, including promotion pointers. No essential durable link may rely on disposable discovery.
- Verify every record `<article>` carries a closed-list `data-kind` (see the contract's kind table) and sits inside one of the shared sections; every `roadmap-ticket` also carries `data-ticket-type`, links at least one research-basis record and one mission or vision, and its spec or prototype-decision links resolve. Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.
- Check a repeated consolidation would enrich the same records rather than create duplicates. Check HTML facts remain readable without JavaScript.
- Update the document's visible date and changed record dates. Return the durable path, affected anchors, consumed revisions, unresolved blockers, and next action for the coordinator to update run routing.

Report the HTML path and the conclusions promoted, amended, or still unresolved. Before
claiming the PRD is ready, state what was promoted versus what remains open and ask the user
to confirm that reading (the close in `references/shared-understanding.md`); readiness is
claimed only after confirmation. In a non-interactive run, record the unconfirmed reading as
an open question instead. A PRD can be useful and durable while design or launch questions
remain open.

## Design and delivery handoff

Once the user has confirmed scope for a concrete change and its canonical records are saved, invoke `acs-plan-delivery` as the default handoff. Supply the change ID, accepted outcomes/priorities, spec and decision references/revisions, and remaining questions. It generates and opens `docs/changes/<change-id>/delivery-plan.html` with the plan and embedded DAG. Reuse existing confirmation; a second request to draw the graph is unnecessary. For consolidation-only requests or unsettled product scope, return the Product report and open questions. Planning does not imply execution readiness.

The PRD fixes *what* to build. The delivery plan exposes missing design as blockers and routes affected scope through the specialists below. Resolve broad uncertainty first when useful slices cannot yet be identified. Pick the row that matches the largest remaining open question:

| Open question after the PRD | Route to |
| --- | --- |
| Part 3 five-state specs are thin because layout, information hierarchy, or the visual system is undecided — or the effort is frontend-heavy with no design system | `design/ux/acs-design-context` (then the UX pipeline — see `workflows/design.md`) |
| The destination is known but the route is foggy — multiple interdependent decisions, larger than one session | `plan/acs-explore-unknowns` |
| PRD terms have no agreed meaning, or a hard-to-reverse trade-off needs an ADR | `craft/context/acs-engineer-domain-model` |
| The feature strains existing module boundaries, or it is unclear where behavior belongs | `design/technical/acs-design-architecture` |
| The product is an agent system | `design/technical/acs-design-architecture`, plus `design-agent-architecture` when available (ships outside this plugin) |
| The product is an operational decision loop | `craft/context/acs-engineer-domain-model`, plus `design-operational-ontology` when available (ships outside this plugin) |
| Only delivery boundaries and sequencing remain open | `build/acs-plan-delivery` |
| Behavior or testable criteria are missing | `design/requirements/acs-settle-requirements` |
| None of the above | `build/acs-plan-delivery` |

**Skip test** — skip design entirely when all three hold: the Part 2 flowchart and Part 3 five-state blocks are complete; vocabulary is settled (glossary exists or terms are unambiguous); the change fits the existing architecture. What remains then is implementation choices, handled by `acs-plan-delivery` and `acs-implement`.

More than one row may apply — UX and technical design can both run. UX output additionally feeds frontend implementation via `design/ux/acs-design-implement` and the delivery graph. A design question that the criteria and conversation cannot settle goes to `design/ux/acs-validate-prototype`: throwaway variants, draft decision recorded in `prototypes/<slug>/decision.md`, consequential verdict and basis retained in Change Context at acceptance, control returns to the skill that raised it.

---

## Boundaries

- Consolidates the problem, demand assessment, solution, and scope; does not invent or silently reclassify them.
- Can add shared questions and resolve them from supplied evidence or user answers within this task.
- Preserves accepted intent and essential rationale; implementation plans remain working memory.
- Produces product requirements and a design/engineering handoff, not implementation code.
