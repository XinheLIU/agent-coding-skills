# Product Memory Contract

Last updated: 2026-09-08

Product skills contribute to shared product knowledge. A skill owns its reasoning method, not a file or an exclusive section. Read this contract before reading or updating product memory. It also applies when a skill runs standalone.

## Documents and routing

- Working: `<work-root>/<effort>/discovery.html` — findings, alternatives, assessments, and unresolved analysis for one effort.
- Human: `<product-docs>/<product-slug>/product.html` — durable product understanding and accepted intent, including the PRD reading view.
- Routing stays in `docs/agents/memory.md` and `<work-root>/<effort>/state.md`. Record the product identity, both document paths when they exist, and the record anchors needed next. Do not create empty documents just to satisfy routing.

Resolve explicit user paths first, then memory configuration and active-state pointers. Reuse the existing product identity for an increment; do not create a new product document for every feature branch. Default product-docs home is `docs/product/`. If product identity or an existing canonical home is ambiguous, ask before choosing it. With no routing and no unambiguous user-specified destination, work in conversation and recommend `init-context` before persistence.

Both HTML documents are semantic sources, not generated views of Markdown or hidden JSON. Other memory formats, including engineering task Markdown and its generated roadmap, retain their contracts. Read durable records first, then relevant working records and their links, including active review findings that challenge a durable premise. A record in the durable document may be an unresolved question or a proposed amendment: its location alone does not make it accepted.

## Shared concepts

Create only sections and records supported by this run. Navigation groups are shared, not skill-owned:

| Section ID | Records and content |
| --- | --- |
| `overview` | Product identity, concise purpose, vision, assessed scope and exclusions |
| `users-problems` | Personas, jobs, struggling moments, desired outcomes, demand assessments |
| `capabilities-journeys` | Capabilities, current and desired behavior, stories, scenarios, flows, acceptance criteria |
| `gaps-opportunities` | Observed behavior gaps and opportunities, affected records, consequences |
| `questions-assumptions` | Open or answered questions, testable assumptions, evidence gaps |
| `evidence` | Source references and observations reused by other records |
| `scope-decisions` | Proposed and accepted scope, alternatives, exclusions, behavior deltas, rationale |
| `risks-measures` | Failure scenarios, mitigations, constraints, NFRs, metrics, thresholds, monitoring |

Use `<article id="gap-export-feedback" data-kind="gap">` for an addressable record within a semantic `<section>`. The `data-kind` vocabulary is a **closed list**:

| Kind | One meaningful subject | Typical section |
| --- | --- | --- |
| `persona` | A specific user or actor | `users-problems` |
| `problem` | A struggling moment or pain, layered surface/deep/fundamental | `users-problems` |
| `demand-assessment` | A graded demand claim with verdict and evidence level | `users-problems` |
| `vision` | The larger intent a set of problems and stories implies | `overview` |
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

Do not invent a kind. If genuinely none fits, add a `data-kind-reason` attribute on the record stating why, so the validator flags it for review instead of failing. Skill names are contributor provenance, never record kinds or navigation boundaries.

One record describes one meaningful subject in a stated context. Use stable, document-unique IDs; preserve them across edits and promotion. Match by product, actor, outcome, surface, and relevant version or scenario before creating a record. Similar titles alone do not establish identity. Link related records with ordinary `<a href="#record-id">` or relative file-and-anchor links. Promotion pointers retain the old ID and link to the new canonical home. Do not reuse retired IDs for different subjects.

A `problem` record may state its need at three layers — surface (the stated ask), deep (the motivation the ask serves), fundamental (the instinct-level need, a noun) — each with its own inferred/confirmed/evidenced status and source. Adding or revising layers enriches the record and does not change its identity. A `vision` record in `overview` states the larger intent a set of problems and stories implies, linking the records that imply it. Any product skill may create or enrich it as an inference; it becomes confirmed only through the user's own statement, recorded with its date. Match a vision by product and the outcome it names; competing candidates are separate linked records with an open question.

Record only metadata that changes interpretation: source/contributor and date, relevant context, evidence versus inference, unresolved conflicts, and decision basis. A source citation should identify the path plus symbol/test or an external reference and observation date/revision when available. Evidence levels belong to the claim being assessed, not globally to a source: a code path can prove behavior exists without proving users need it.

## Meaning and authority

Keep these independent; do not compress them into a single `complete` status:

- Current behavior: observed implemented, partial, absent within assessed coverage, or not assessed.
- Demand: the scoped claim, evidence level, and assessment verdict.
- Commitment: proposed, accepted, rejected, or deferred, with decision basis and scope.
- Review: current, disputed, or needs review after a relevant input changed.

A gap is an evidenced shortfall against a named expectation. An opportunity improves an outcome that already works. A question lacks an answer; an assumption provisionally supplies one; a risk describes a possible failure. Link them when related rather than merging these meanings. Missing evidence does not prove missing behavior. A proposed remedy, accepted scope, or deferred feature does not close a behavior gap. Closure requires evidence of the resulting behavior. Answered questions retain their answer, basis, and ID; new evidence can reopen them. An empty section means nothing was recorded, not that no issues exist. A vision stays an inference until the user confirms it, and a confirmed vision is intent, not accepted scope.

Any product skill can add relevant observations, evidence, gaps, questions, and proposed answers or remedies. It can resolve a question when its evidence and competence answer that exact question. Specialized assessments remain explicit: `validate-demand` grades demand; scope skills assess scope; `run-premortem` assesses risks; `write-prd` promotes and reconciles accepted intent. Any skill may refresh its own assessment when new evidence warrants it, preserving the previous verdict and reason when they explain a decision. No skill silently reclassifies another assessment or changes an accepted decision. User authorization already present in the task or recorded decisions counts; do not ask for the same approval again.

## Read–match–enrich–verify

1. Resolve the product and effort. Inspect document navigation and relevant record IDs, then read the target records and their evidence, decisions, and dependencies. Do not load every record merely because they share a file.
2. Match existing subjects before adding records. Follow promotion pointers. Reuse established answers regardless of which skill supplied them. For an existing durable subject, working analysis links to it and records only new evidence, a proposed amendment, or a disagreement; it does not copy the canonical description.
3. Create missing records or minimally enrich existing ones: add evidence, refine a finding with its basis, link an assessment, answer a question, or propose a decision. Preserve unrelated fields, user edits, IDs, and layout. Repeating the same run without new information must not duplicate records or evidence.
4. Preserve conflicting claims and their evidence; explain the disputed scope. Do not use last-writer-wins or average incompatible judgments. If the conflict affects an authorized action, resolve it with evidence or ask the decision-maker.
5. When changing a premise, inspect records in both active documents that cite it. Mark materially affected conclusions `needs review`, naming the changed premise. Follow affected conclusions onward only where the change matters. Do not invalidate the whole document or silently recompute another skill's assessment. Existing accepted decisions stay recorded while their applicability is reviewed. Working contributors flag affected durable records through linked review findings in discovery and state, then route reconciliation to `write-prd`; they do not acquire write authority over durable intent. Readers inspect these active review findings before relying on the affected durable conclusions.
6. Record assessed coverage and omissions. A standalone run creates only the useful partial knowledge it can establish from supplied context, code, or evidence. Missing prior skill files never force a pipeline rerun; missing substantive evidence may still block a verdict or commitment. Record the precise question and continue independent analysis.
7. Verify before reporting:
   - Every record `<article>` has a document-unique id, a closed-list `data-kind`, and sits inside one of the shared sections.
   - Local record links (`#anchor`) resolve; promotion pointers resolve.
   - Observed, proposed, and accepted meanings stay distinct; closures are supported by evidence.
   - Unrelated records, user edits, and IDs are preserved.
   - Visible `Last updated` dates are current on changed records and the document.
   - `state.md` carries changed anchors and a concrete next action; report added, enriched, resolved, disputed, or review-needed records rather than another full report.
   - Run `python3 scripts/validate-product-memory.py <file>` from the repo root when the script is available; fix errors before reporting.

Section tags do not provide concurrency control. Serialize writes to each shared file. Concurrent analyses may prepare proposed edits separately, but one coordinator applies them against the latest file. Immediately before applying a patch, reread its target and referenced premises; if they changed, reconcile first. Never overwrite a shared file from a stale whole-document snapshot.

## Promotion and the PRD

`write-prd` consolidates durable knowledge into `product.html`; the PRD is its reading order over canonical records, not another maintained document. It can run early, incrementally, or from explicit standalone inputs. It does not validate demand, invent scope, or turn unresolved analysis into accepted requirements.

Promote settled product intent with the minimum evidence and rationale needed to understand it. Preserve stable IDs when moving new records. When amending an existing durable subject, reconcile the accepted amendment into that record rather than creating a duplicate. Link supporting records once; an overview or requirements index links to them rather than repeating their normative text. Keep current code inventories in working memory; promote only context necessary to explain lasting intent and point to code for implementation facts.

Promotion order: write and verify the durable record and its essential supporting evidence; repair links among promoted records; replace working conclusions with pointers; update routing. Durable records must not depend on disposable effort files for essential rationale or evidence. Preserve required observations in the durable evidence record when their only source was working notes; link stable external/code sources where available. A working amendment ID can become a pointer to the durable record it amended. Before effort deletion, verify the durable document remains understandable and its necessary links resolve without that effort.

PRD navigation uses `prd` for the reading index, and anchors to actual records for problem, users, goals, capabilities, scope, acceptance, risks, measures, and launch decisions. Keep partial readiness explicit: list outstanding questions and what they block. Green demand can justify early promotion without pretending solution or scope is settled. Reassess readiness after conflicting evidence or changed premises; document existence is never a gate.

## HTML presentation

Use a readable, self-contained document: UTF-8, responsive viewport, title, visible update date, inline shared CSS once, semantic headings, lists, tables, links, and native `<details>`. All product facts must be readable from source HTML with JavaScript disabled. IDs and `data-kind` are the reading contract; visual classes are not. Never store a second semantic copy in Markdown, embedded JSON, JavaScript state, or browser storage.

Navigation and concise summaries help humans. Collapsing content does not reduce agent context; agents locate relevant records before reading. Keep source formatted for targeted patches, with one record per readable block. Charts or diagrams must have adjacent textual meaning; render graph diagrams as inline SVG when available, or retain their readable diagram source with a text explanation. No remote dependency is required to read the document. Reuse its existing visual style instead of redesigning it on each skill run. Product mockups are separate, explicitly illustrative prototype artifacts, not a second memory store.

```html
<!doctype html>
<html lang="en" data-product-memory="1">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Export service — discovery</title>
  <style>body{max-width:72rem;margin:auto;padding:2rem;font:1rem/1.6 system-ui} article{margin:2rem 0} dt{font-weight:600}</style>
</head>
<body>
  <header><h1>Export service — discovery</h1><p>Last updated: <time datetime="2026-09-08">2026-09-08</time></p></header>
  <nav aria-label="Product knowledge"><a href="#overview">Overview</a> <a href="#gaps-opportunities">Gaps and opportunities</a> <a href="#questions-assumptions">Questions</a></nav>
  <main>
    <section id="overview">
      <h2>Overview</h2>
      <article id="vision-context-first-org" data-kind="vision">
        <h3>Candidate vision: shared context anyone can act on</h3>
        <p>Last updated: <time datetime="2026-09-08">2026-09-08</time> · Contributor: map-current-product · Status: inferred</p>
        <p>Implied by <a href="#gap-export-feedback">export feedback</a> and other linked story clusters; awaiting user confirmation via <a href="#question-vision-confirm">the open question</a>.</p>
      </article>
    </section>
    <section id="gaps-opportunities">
      <h2>Gaps and opportunities</h2>
      <article id="gap-export-feedback" data-kind="gap">
        <h3>Export completion is invisible</h3>
        <p>Last updated: <time datetime="2026-09-08">2026-09-08</time> · Contributor: map-current-product</p>
        <dl>
          <dt>Expectation and observation</dt><dd>Users need a completion signal; inspected web routes show none.</dd>
          <dt>Coverage</dt><dd>Web export flow only; mobile not assessed.</dd>
          <dt>Evidence</dt><dd>Attach the actual inspected path and symbol before recording this finding.</dd>
          <dt>Resolution</dt><dd>Open; a proposed notification would not establish implementation.</dd>
        </dl>
      </article>
    </section>
    <section id="questions-assumptions">
      <h2>Questions and assumptions</h2>
      <article id="question-vision-confirm" data-kind="question">
        <h3>Does the user confirm the candidate vision?</h3>
        <p>Last updated: <time datetime="2026-09-08">2026-09-08</time> · Blocks: promoting <a href="#vision-context-first-org">the candidate vision</a>.</p>
      </article>
    </section>
  </main>
</body>
</html>
```

The example illustrates structure, not evidence to copy. Fill only source-supported records.

## Existing documents

Read existing `prd.md`, per-skill discovery Markdown, and `discovery/current-product.html` as legacy inputs when configuration or user paths point to them. Do not treat missing HTML as missing knowledge. Keep legacy documents canonical until an authorized migration reconciles their content; do not silently create a competing HTML truth or rename user files.

When migrating, inventory unique facts, user edits, evidence, unresolved questions, and links. Map them to shared records, preserve their authority and dates, verify the new document and handoffs, then update routing and replace superseded content with pointers or remove it only within the authorized scope. If old and new documents conflict, resolve the conflict before retiring either. New product memory uses the HTML contract. Do not maintain dual Markdown/HTML outputs after migration.
