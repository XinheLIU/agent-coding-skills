---
protocol: acs:product-memory
version: 1.2.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/product-memory.md
---

# Product Memory Contract

Last updated: 2026-09-26

Product skills contribute to shared product knowledge. A skill owns its reasoning method, not a file or an exclusive section. Read this contract before reading or updating product memory. It also applies when a skill runs standalone. Product documents serialize under the [HTML record format](../../../../protocols/html-records.md); this contract defines which records exist, what they mean, and who may change them.

## Lifecycle and change identity

The [shared protocol](../../../../protocols/skill-declarations.md) owns the two memory classes, relationships, freshness and handoffs. In Persistent `product.html`, mission/vision/principles are Intent; evidenced capabilities are Current; tickets, proposed or accepted scope and decisions are Changes. Exploratory `discovery.html` is Working until needed for formal review, cross-run handoff or downstream reliance; save those conclusions and evidence as proposed Persistent records before that boundary. Classify records independently of format or acceptance.

Use the canonical ticket ID across all domains. Requirements and acceptance criteria live once in the ticket's canonical spec, with stable requirement/criterion IDs. Product reading indexes, capability records, designs, and child tickets link that normative source. `spec` consumes it; it creates requirements under this contract only when none exist. Preserve existing spec/tracker locations; new local-only change records default to tracked `docs/changes/<change-id>/`. A product-backed ticket and its existing `specs/<spec-slug>.md` remain valid homes.

The coordinator owns path/identity resolution, serialized contributions, run state, runtime calls, and cross-domain freshness propagation. Product skills own subject matching, evidence interpretation, scope and demand authority. The contribution rules below apply within that boundary, including standalone runs.

## Documents and routing

- Working Memory: `<work-root>/<effort>/discovery.html` — findings, alternatives, assessments, unresolved analysis, and research completeness tracking for one effort.
- Durable records: `<product-docs>/<product-slug>/product.html` — durable product understanding, accepted intent, the roadmap, and the PRD reading view.
- Specs: preserve the existing canonical requirement home (for example `<product-docs>/<product-slug>/specs/<spec-slug>.md`); new local-only changes use `docs/changes/<change-id>/spec.md`. `acs-write-prd` authors or reconciles that same source, linked from the canonical ticket. A loose spec can be tightened in place before engineering consumes it.
- Routing stays in `docs/agents/memory.md` and the single configured run recovery entry (default `<work-root>/<run-id>/state.md`). Record the product identity, document paths when they exist, and the record anchors needed next. Do not create empty documents just to satisfy routing.

Resolve explicit user paths first, then memory configuration and active-state pointers. Reuse the existing product identity for an increment; do not create a new product document for every feature branch. Default product-docs home is `docs/product/`. If product identity or an existing canonical home is ambiguous, ask before choosing it. Without routing configuration, use explicit inputs and an unambiguous established home, or the defaults above for authorized persistence. Use `acs-init-context` only when routing remains ambiguous; configuration absence alone does not block standalone work.

Canonical product HTML owns Persistent records; discovery HTML owns temporary Working analysis. Neither is a generated twin of Markdown or hidden JSON. Derived reports use [Presenter](../../../../protocols/presenter.md), while product record semantics stay here. Other memory formats, including engineering task Markdown and its generated roadmap, retain their contracts. Read durable records first, then relevant working records and their links, including active review findings that challenge a durable premise. A record in the durable document may be an unresolved question or a proposed amendment: its location alone does not make it accepted.

## The two handoff deliverables

The pipeline's final handoff is **research** plus **roadmap**, aligned with the product's missions and visions:

- **Research** is the full analysis: current behavior, personas, layered needs, gaps, evidence, and coverage. It accumulates in `discovery.html` while working and its accepted conclusions live as durable records in `product.html`.
- **Roadmap** is the `roadmap` section of `product.html`: research findings decomposed into prioritized concrete changes. Each ticket links its research basis, its mission/vision alignment, and either a standalone spec file or a prototype request.

MECE guides the boundary, not a hard constraint: analysis in progress stays in discovery. Proposals needed for review or downstream reliance, accepted requirements, decisions and essential evidence must reach their canonical Persistent homes before that use, not wait for run cleanup. The handoff is product records plus linked Persistent Changes; no essential fact may depend on disposable discovery.

## Shared concepts

Create only sections and records supported by this run. Navigation groups are shared, not skill-owned:

| Section ID | Records and content |
| --- | --- |
| `overview` | Product identity, concise purpose, missions, visions, assessed scope and exclusions |
| `users-problems` | Personas, jobs, struggling moments, desired outcomes, demand assessments |
| `capabilities-journeys` | Capabilities, current and desired behavior, stories, scenarios, flows, acceptance criteria |
| `gaps-opportunities` | Observed behavior gaps and opportunities, affected records, consequences |
| `questions-assumptions` | Open or answered questions, testable assumptions, evidence gaps |
| `evidence` | Source references and observations reused by other records |
| `scope-decisions` | Proposed and accepted scope, alternatives, exclusions, behavior deltas, rationale |
| `risks-measures` | Failure scenarios, mitigations, constraints, NFRs, metrics, thresholds, monitoring |
| `roadmap` | Prioritized tickets decomposing research into concrete changes (`product.html` only) |
| `research` | Research coverage and readiness tracking (`discovery.html` only) |

Use `<article id="gap-export-feedback" data-kind="gap">` for an addressable record within a semantic `<section>`, per the [HTML record format](../../../../protocols/html-records.md). The `data-kind` vocabulary is a **closed list**:

| Kind | One meaningful subject | Typical section |
| --- | --- | --- |
| `mission` | A measurable product objective; multiple allowed | `overview` |
| `vision` | The larger intent a set of problems and stories implies | `overview` |
| `persona` | A specific user or actor | `users-problems` |
| `problem` | A struggling moment or pain, layered surface/deep/fundamental | `users-problems` |
| `demand-assessment` | A graded demand claim with verdict and evidence level | `users-problems` |
| `capability` | A current or desired behavior of the product | `capabilities-journeys` |
| `journey` | A story, scenario, or flow through capabilities | `capabilities-journeys` |
| `gap` | An evidenced shortfall against a named expectation | `gaps-opportunities` |
| `opportunity` | An improvement to an outcome that already works | `gaps-opportunities` |
| `question` | Something unanswered, with what it blocks | `questions-assumptions` |
| `assumption` | A provisional answer awaiting evidence | `questions-assumptions` |
| `evidence` | A source reference or observation reused by other records | `evidence` |
| `decision` | A proposed or accepted scope/choice with basis | `scope-decisions` |
| `constraint` | A limit the product must respect | `risks-measures` |
| `risk` | A possible failure with score and mitigation | `risks-measures` |
| `metric` | A measure, threshold, or monitoring signal | `risks-measures` |
| `roadmap-ticket` | A prioritized concrete change with spec or prototype handoff | `roadmap` |
| `research-coverage` | Aggregated coverage and roadmap-readiness for the research phase | `research` |

Skill names are contributor provenance, never record kinds or navigation boundaries.

### Capability commitment attributes

A `capability` record set by `acs-define-outcomes` carries two further closed-list attributes. They are orthogonal: commitment says whether the capability is part of what the product promises, depth says how far it goes. Priority numbers are not a substitute — they cannot express a capability that ships narrower than shaped.

| `data-commitment` | Meaning |
| --- | --- |
| `committed` | An outcome's verification fails without it |
| `reduced` | Committed, at a named lower depth |
| `deferred` | Accepted intent, not in this commitment; carries a re-entry trigger |
| `excluded` | Decided against, resting on a constraint or evidenced non-need |
| `open` | Unresolved and blocking; carries a linked question |

| `data-depth` | Meaning |
| --- | --- |
| `full` | The capability as shaped in the target experience |
| `narrowed` | Full behavior over a restricted set of inputs, cases, or actors |
| `fixed` | Behavior whose tunable policy is frozen to one choice |
| `manual` | The user-visible outcome produced by a human behind the interface |

`data-depth` applies only to `committed` and `reduced` records, and may carry more than one value (`data-depth="narrowed fixed"`). The basis for each decision — verification link, lost user capability, constraint, or re-entry trigger — lives in the record body, never in the attribute.

```html
<article id="cap-private-doc-retrieval" data-kind="capability"
         data-commitment="reduced" data-depth="narrowed fixed">
```

Only `acs-define-outcomes` sets these. Downstream skills read them: a proposal that drops a `committed` capability or lowers a recorded depth returns to product rather than resolving locally.

### Record identity

One record describes one meaningful subject in a stated context. Match by product, actor, outcome, surface, and relevant version or scenario before creating a record. Similar titles alone do not establish identity. ID stability, promotion pointers, and linking rules follow the [HTML record format](../../../../protocols/html-records.md).

A `problem` record may state its need at three layers — surface (the stated ask), deep (the motivation the ask serves), fundamental (the instinct-level need, a noun) — each with its own inferred/confirmed/evidenced status and source. Adding or revising layers enriches the record and does not change its identity.

Record only metadata that changes interpretation: source/contributor and date, relevant context, evidence versus inference, unresolved conflicts, and decision basis. A source citation should identify the path plus symbol/test or an external reference and observation date/revision when available. Evidence levels belong to the claim being assessed, not globally to a source: a code path can prove behavior exists without proving users need it.

## Mission and vision

A `mission` record states a measurable product objective. Multiple missions per product are allowed; each carries a status (proposed / accepted / retired), the date accepted when accepted, and its measurement. Missions are objectives; visions are direction.

A `vision` record in `overview` states the larger intent a set of problems and stories implies, linking the records that imply it. Any product skill may create or enrich it as an inference; it becomes confirmed only through the user's own statement, recorded with its date. Match a vision by product and the outcome it names; competing candidates are separate linked records with an open question. A vision may link the missions it serves.

```html
<article id="mission-actionable-context" data-kind="mission">
  <h3>Mission: Make internal context instantly actionable</h3>
  <p>Status: accepted · <time datetime="2026-09-01">2026-09-01</time> · Measure: time from context creation to first team action</p>
  <p>Serves <a href="#vision-context-first-org">context-first collaboration</a>.</p>
</article>
```

## Roadmap

The `roadmap` section exists only in `product.html`. It decomposes accepted research findings into prioritized, concrete changes. Every ticket is one `roadmap-ticket` record with `data-ticket-type` of `spec` or `prototype`:

- **Spec ticket** (`data-ticket-type="spec"`): requirements are settled enough to specify. Links the canonical Markdown spec at its resolved home, authored or reconciled by `acs-write-prd`. A loose spec drafted by another skill may be linked provisionally; the ticket notes that `acs-write-prd` should tighten it.
- **Prototype ticket** (`data-ticket-type="prototype"`): a design question blocks specification. The ticket carries a short prototype request — one or two sentences stating what needs prototyping — as the handoff to `design/ux/prototype`. It is not a spec and does not go through `acs-write-prd` until the prototype decision lands.

When an external or existing local tracker owns the ticket, the roadmap record links that canonical ID/status instead of maintaining its own execution status. When the roadmap article is the canonical ticket, it owns status once. Any rendered status names its source revision. Child tickets reference this parent; completing children does not by itself complete the parent.

Every canonical ticket records: priority (`p0` / `p1` / `p2` / `deferred`), status (`proposed` / `accepted` / `in-progress` / `blocked` / `completed` / `abandoned`), its research basis (links to the gap/opportunity/problem records that justify it), and its alignment (links to at least one mission or vision).

```html
<article id="ticket-export-notification" data-kind="roadmap-ticket" data-ticket-type="spec">
  <h3>Add export completion notification</h3>
  <p>p0 · accepted · Spec: <a href="specs/export-notification.md">export-notification.md</a></p>
  <p>Basis: <a href="#gap-export-feedback">export feedback gap</a> · Aligns: <a href="#mission-actionable-context">actionable-context mission</a></p>
</article>
```

Ticket lifecycle: `proposed → accepted → in-progress → completed`, with `blocked` for unmet prerequisites (including prototype decisions) and `abandoned` as an exit. `deferred` is a priority choice, not another status source. When a prototype decision is accepted, preserve its consequential verdict and basis in Persistent Changes immediately; the ticket links that durable decision and either converts to a spec ticket (via `acs-write-prd`) or closes. A ticket does not close a behavior gap; only evidence of the resulting behavior does.

The same ticket identifies the change across domains. `engineering/feature/spec` consumes its spec without copying requirements; `tasks` adds child tickets only for independent delivery slices. Roadmaps and session state reference canonical ticket status.

## Research completeness

The `research` section exists only in `discovery.html`. One `research-coverage` record aggregates what the research phase has and has not assessed — platforms, roles, flows, data sources — and states explicitly whether the research is ready to decompose into a roadmap, naming the blocking gaps or questions when it is not.

Readiness means: assessed coverage is explicit, P0 findings have source-backed evidence, primary personas have mapped journeys, known omissions are recorded with their impact, and no open question would invalidate a P0 priority. `acs-write-prd` checks this record before decomposing research into roadmap tickets; when it says not ready, promotion of the roadmap waits — early promotion of settled records (a Green demand verdict, a confirmed vision) still proceeds.

## Meaning and authority

Keep these independent; do not compress them into a single `complete` status:

- Current behavior: observed implemented, partial, absent within assessed coverage, or not assessed.
- Demand: the scoped claim, evidence level, and assessment verdict.
- Commitment: proposed, accepted, rejected, or deferred, with decision basis and scope.
- Review: current, disputed, or needs review after a relevant input changed.

A gap is an evidenced shortfall against a named expectation. An opportunity improves an outcome that already works. A question lacks an answer; an assumption provisionally supplies one; a risk describes a possible failure. Link them when related rather than merging these meanings. Missing evidence does not prove missing behavior. A proposed remedy, accepted scope, deferred feature, or roadmap ticket does not close a behavior gap. Closure requires evidence of the resulting behavior. Answered questions retain their answer, basis, and ID; new evidence can reopen them. An empty section means nothing was recorded, not that no issues exist. A vision stays an inference until the user confirms it, and a confirmed vision is intent, not accepted scope. An accepted mission is an objective, not evidence that any ticket serves it — alignment links carry that claim, per ticket.

Any product skill can add relevant observations, evidence, gaps, questions, and proposed answers or remedies. It can resolve a question when its evidence and competence answer that exact question. Specialized assessments remain explicit: `acs-validate-demand` grades demand; scope skills assess scope; `acs-run-premortem` assesses risks; `acs-write-prd` promotes and reconciles accepted intent, owns roadmap decomposition, and generates spec files. Any skill may refresh its own assessment when new evidence warrants it, preserving the previous verdict and reason when they explain a decision. No skill silently reclassifies another assessment or changes an accepted decision. User authorization already present in the task or recorded decisions counts; do not ask for the same approval again.

## Read–match–enrich–verify

1. Resolve the product and effort. Read the document `<nav>`, then fetch only the target records and their evidence, decisions, and dependencies using the [retrieval patterns](../../../../protocols/html-records.md#targeted-retrieval). Do not load every record merely because they share a file.
2. Match existing subjects before adding records. Follow promotion pointers. Reuse established answers regardless of which skill supplied them. For an existing durable subject, working analysis links to it and records only new evidence, a proposed amendment, or a disagreement; it does not copy the canonical description.
3. Create missing records or minimally enrich existing ones: add evidence, refine a finding with its basis, link an assessment, answer a question, or propose a decision. Preserve unrelated fields, user edits, IDs, and layout. Repeating the same run without new information must not duplicate records or evidence.
4. Preserve conflicting claims and their evidence; explain the disputed scope. Do not use last-writer-wins or average incompatible judgments. If the conflict affects an authorized action, resolve it with evidence or ask the decision-maker.
5. When changing a premise, inspect records in both active documents that cite it. Mark materially affected conclusions `needs review`, naming the changed premise. Follow affected conclusions onward only where the change matters — including roadmap tickets whose research basis changed. Do not invalidate the whole document or silently recompute another skill's assessment. Existing accepted decisions stay recorded while their applicability is reviewed. Working contributors flag affected durable records through linked review findings in discovery and state, then route reconciliation to `acs-write-prd`; they do not acquire write authority over durable intent. Readers inspect these active review findings before relying on the affected durable conclusions.
6. Record assessed coverage and omissions — per record, and aggregated in the `research-coverage` record when the run contributes research. A standalone run creates only the useful partial knowledge it can establish from supplied context, code, or evidence. Missing prior skill files never force a pipeline rerun; missing substantive evidence may still block a verdict or commitment. Record the precise question and continue independent analysis.
7. Verify before reporting:
   - Every record satisfies the [HTML record format](../../../../protocols/html-records.md): unique `<kind>-<slug>` ID, closed-list `data-kind` inside a shared section, complete `<nav>` index, resolving links and promotion pointers, current `Last updated` dates.
   - Roadmap tickets carry `data-ticket-type`; committed capabilities carry `data-commitment` (plus `data-depth` where it applies); every roadmap ticket links at least one research-basis record and at least one mission or vision.
   - Observed, proposed, and accepted meanings stay distinct; closures are supported by evidence.
   - Unrelated records, user edits, and IDs are preserved.
   - The configured recovery entry carries changed anchors and a concrete next action; report added, enriched, resolved, disputed, or review-needed records rather than another full report.
   - Run `python3 scripts/validate-product-memory.py <file>` from the repo root when the script is available; fix errors before reporting.

Serialization of shared writes follows the [HTML record format](../../../../protocols/html-records.md#writing) and the shared protocol's coordinated-writes rules.

## Promotion and the PRD

`acs-write-prd` consolidates durable knowledge into `product.html`; the PRD is its reading order over canonical records, not another maintained document. It owns promotion, roadmap decomposition, and spec generation; the workflow lives in its `references/promotion-and-roadmap.md`. The authority rules stand regardless of workflow:

- Save proposals required for review or downstream reliance with `proposed` status and the minimum evidence; saving them does not accept scope or bypass product ownership.
- A contributing skill without authority to amend durable product intent saves an addressable proposal in the canonical change home, linking the product subject and consumed revision; the coordinator routes intent reconciliation to `acs-write-prd`. It does not edit accepted product intent merely to make its proposal Persistent.
- Durable records must not depend on disposable effort files for essential rationale or evidence; promotion preserves stable IDs and reconciles amendments into existing records rather than duplicating them.
- The spec is canonical for its change; the canonical ticket (roadmap article or linked tracker record) owns priority and status.
- Keep raw code inventories in Working Memory; maintain useful observed product summaries in Persistent Current with source revision and coverage. Historical deltas and rationale belong to Persistent Changes; point to code for executable facts.

## HTML presentation

Product documents follow the [HTML record format](../../../../protocols/html-records.md) for structure, self-containment, retrieval, and write discipline. Human review and derived companions follow [Presenter](../../../../protocols/presenter.md), including version-scoped decisions, deduplication and retrievable reviewed content. Product-specific additions: `data-kind`, `data-ticket-type`, `data-commitment`, and `data-depth` are part of the reading contract, and product mockups are separate, explicitly illustrative prototype artifacts, not a second memory store.

## Existing documents

Read existing `prd.md`, per-skill discovery Markdown, and `discovery/current-product.html` as legacy inputs when configuration or user paths point to them. Do not treat missing HTML as missing knowledge. Keep legacy documents canonical until an authorized migration reconciles their content; do not silently create a competing HTML truth or rename user files.

When migrating, inventory unique facts, user edits, evidence, unresolved questions, and links. Map them to shared records, preserve their authority and dates, verify the new document and handoffs, then update routing and replace superseded content with pointers or remove it only within the authorized scope. If old and new documents conflict, resolve the conflict before retiring either. New product memory uses the HTML contract. Do not maintain dual Markdown/HTML outputs after migration.
