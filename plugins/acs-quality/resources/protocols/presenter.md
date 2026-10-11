---
protocol: acs:presenter
version: 1.3.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/presenter.md
---

# Presenter and Human Review

Last updated: 2026-10-11

Use this contract to prepare a view for human reading or review, to receive feedback on a view, or to keep reviewed evidence. It specializes the [memory and ownership protocol](skill-declarations.md). It adds no service and no approval gate.

## Interface and ownership

```text
present(references, focus) -> view_reference
```

- `references` identify the canonical records and the revisions consumed.
- `focus` names what the reader must understand or decide.

| Role | Owns |
| --- | --- |
| Domain skills | conclusions, evidence, options, recommendations, open questions |
| Coordinator | resolving sources, saving necessary records |
| Presenter | reading order, information density, comparison, visual expression |

Presenter keeps the meaning, the recommendation order, the uncertainty, the blocking effects and the domain status. If reasoning is missing, Presenter returns the gap to its domain owner. Presenter cannot accept a proposal, change a ticket status or infer authorization. Domain work and text delivery need no separate Presenter skill.

## Templates

Use text or Markdown for simple results. Use HTML when diagrams, comparisons or progress help the reader. All shared display templates live in `skills-src/authoring/references/`:

| Template | Use when |
| --- | --- |
| [Visual report](../../skills/acs-refactor-code/references/visual-report.md) | The default derived HTML companion: header, overview, finding cards, evidence, footer. It also holds the Writing rules for every view and HTML record. |
| [Tabbed discovery report](../skills-src/authoring/references/tabbed-discovery-report.md) | Complex analysis: 3 or more major concerns, revision history, nested options, before/after across several dimensions |

A per-skill `HTML-REPORT.md` adds only that skill's content requirements. Display and writing rules stay in the shared templates. Canonical memory documents (`product.html`, `prototype.html`) are not Presenter views. The [HTML record format](html-records.md) defines their serialization.

## Generate a view

1. Resolve only the relevant records and revisions. Before formal review or downstream use, save the minimum proposal and evidence in Persistent Memory with its actual status, `proposed` included.
2. Arrange existing conclusions around the focus. Put the conclusion first and write to the [Writing rules](../../skills/acs-refactor-code/references/visual-report.md#writing). Mark Working-only execution information as provisional run state and link its checkpoint. Keep rendering intermediates in Working; a persistent parallel ViewModel is not necessary.
3. Show source references and revisions, domain status and applicable review findings. A view holds no unique domain conclusion and no hidden second copy of canonical state. Keep the existing renderer or template when it fits.
4. Verify that links and the visible meaning agree with the sources. The delivered view represents the listed revisions. To refresh, reread the sources; rendering never changes them. A static offline page cannot detect later source changes.

## Date and version

Every human-readable HTML file an ACS skill writes tells a later reader which day and which source it represents. This includes views, roadmaps, delivery plans, design previews and the canonical records under the [HTML record format](html-records.md):

```html
<meta name="generated" content="YYYY-MM-DD">
<meta name="source-revision" content="<git short sha, record revision, or untracked>">
```

A visible line near the top shows the same date and revision.

- **One-off report:** name it `<slug>-YYYY-MM-DD.html`.
- **File rebuilt or edited at a fixed path** (`technical-design.html`, `roadmap.html`, `delivery-plan.html`, `product.html`, `prototype.html`): keep the path and add `<meta name="view-kind" content="living">`.

Before handover, run the [validator](../skills-src/authoring/scripts/validate-report-html.py). Finding reports run it plainly, as the [visual report](../../skills/acs-refactor-code/references/visual-report.md) contract requires. Every other HTML file runs it with `--version-only`. Fix every error.

You can delete and rebuild generated reports, delivery roadmaps and DAGs; no fact or decision changes. Canonical `product.html` records and design prototypes are Persistent artifacts, even when people read them. Do not discard their contents or accepted visuals as derived presentation.

## Review reconciliation

Review applies when the task, a domain rule or an open decision asks for it. Ordinary factual updates need no extra approval. Conversation feedback is sufficient; static HTML needs no approval buttons.

The coordinator reconciles actual feedback in this order:

1. **Identify** the subject, the reviewed revision, the scope and the actual feedback source. Before writing, recheck the current source and the consumed premise revisions. If they changed, keep the feedback against the reviewed version and send the affected current conclusions back for reassessment. Never apply an old acceptance to new content.
2. **Keep the reviewed content retrievable.** A retained immutable repository or tracker revision is sufficient; otherwise keep a snapshot. If the visual presentation affected the decision, keep that page or prototype and its necessary assets as Persistent evidence.
3. **Match existing decisions.** Reread the decision records. Match a feedback contribution by subject record ID and actual feedback source, then reconcile its explicit scope and reviewed revision.
   - Keep each scoped outcome in a contribution. A match on one event must not discard another scope or version.
   - Processing unchanged feedback again changes nothing.
   - Reconcile parallel feedback under the shared serialized writer, and keep disagreements.
   - If identity or scope is unclear, resolve it before you record a decision.
4. **Record** the outcome in the existing change or decision home. Base it only on the actual feedback. Keep prior decisions, and send requested content revisions to their domain owner.
5. **Update** the affected freshness and the configured recovery entry, then refresh the view when useful. Downstream work consumes canonical references and decisions, not page state.

Minimum decision content (existing Markdown, HTML or tracker fields are sufficient):

```yaml
id: D-12
subject: DESIGN-7
reviewed_revision: <immutable revision or digest with retrievable content reference>
outcome: accepted
scope: export interaction
basis: <reason supported by the actual feedback>
source: <durable feedback reference or faithfully retained user response>
```

- An acceptance covers that subject and revision only, not every proposal shown with it.
- Design acceptance is not authorization to implement, commit or publish. Existing explicit authorization stays valid.
- A material change to content or dependencies marks the affected applicability `needs review` and keeps the historical decision.
- A cosmetic report change does not invalidate a domain decision. Layout is material when the review assessed the visual design.

Critical comments and revision requests go in canonical records. Browser localStorage holds UI preferences only, never decisions or the only copy of feedback. A retained review snapshot is historical evidence, not a second current source of facts.
