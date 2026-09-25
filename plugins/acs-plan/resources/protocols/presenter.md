---
protocol: acs:presenter
version: 1.1.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/presenter.md
---

# Presenter and Human Review

Last updated: 2026-09-26

Use this contract when preparing a human reading/review view, receiving feedback on a view, or retaining reviewed evidence. It specializes the [memory and ownership protocol](skill-declarations.md); it adds neither a service nor an approval gate.

## Interface and ownership

```text
present(references, focus) -> view_reference
```

`references` identify accessible canonical records and consumed revisions. `focus` names what the reader needs to understand or decide. Domain skills supply conclusions, evidence, options, recommendations and unresolved questions. The coordinator resolves sources and saves necessary records. Presenter controls reading order, information density, comparison and visual expression.

Presenter preserves substantive meaning, recommendation order, uncertainty, blocking effects and domain status. Missing reasoning returns to its domain owner. It cannot accept a proposal, change ticket status or infer authorization. No separate Presenter skill is required for domain work or text delivery.

## Templates

Simple results use text/Markdown; use HTML when diagrams, comparisons or progress benefit from it. All shared display templates live under `skills-src/authoring/references/`:

| Template | Use when |
| --- | --- |
| [Visual report](../../skills/acs-map-current-product/references/visual-report.md) | The default derived HTML companion: header, overview, finding cards, evidence, footer |
| [Tabbed discovery report](../skills-src/authoring/references/tabbed-discovery-report.md) | Complex multi-dimensional analysis: 3+ major concerns, revision history, nested options, multi-dimension before/after |

Per-skill `HTML-REPORT.md` references only add that skill's content requirements; display rules stay in these shared templates. Canonical memory documents (`product.html`, `prototype.html`) are not Presenter views; their serialization is the [HTML record format](html-records.md).

## Generate a view

1. Resolve only the relevant records and revisions. Before formal review or downstream reliance, save the minimum proposal and evidence in Persistent Memory with its actual status, including `proposed`.
2. Organize existing conclusions around the focus. Mark any Working-only execution information as provisional run state and link its checkpoint. Keep rendering intermediates in Working; no persistent parallel ViewModel is required.
3. Show source references and revisions, domain status and applicable review findings. A view contains no unique domain conclusion or hidden second copy of canonical state. Retain the existing renderer/template where suitable.
4. Verify that links and the visible meaning agree with the sources. The delivered view represents the listed revisions. Refresh by rereading sources; rendering never mutates them. A static offline page cannot automatically detect later source changes.

Generated reports, delivery roadmaps and DAGs can be removed and rebuilt without changing facts or decisions. Canonical `product.html` records and design prototypes are Persistent artifacts, even when human-readable: their contents and accepted visuals must not be discarded as derived presentation.

## Review reconciliation

Review applies when the task, a domain rule or an unresolved decision calls for it; ordinary factual updates need no extra approval. Conversation feedback is sufficient; static HTML needs no approval buttons.

The coordinator reconciles actual feedback in this order:

1. Identify the subject, reviewed revision, scope and actual feedback source. Recheck current source and consumed premise revisions before writing; if changed, preserve the feedback against the reviewed version and route affected current conclusions for reassessment. Never apply old acceptance automatically to new content.
2. Ensure the exact reviewed content remains retrievable. A retained immutable repository/tracker revision is sufficient; otherwise preserve a snapshot. If visual presentation affected the decision, retain that page/prototype and its necessary assets as Persistent evidence.
3. Reread existing decision records. Match a feedback contribution by subject record ID and actual feedback source, then reconcile its explicit scope and reviewed revision. Preserve multiple scoped outcomes within that contribution; matching an event must not discard another scope or version. Repeated processing of unchanged feedback is a no-op. Reconcile parallel feedback under the shared serialized writer, preserving disagreements. If identity or scope is ambiguous, resolve it before recording a decision.
4. Record the outcome in the existing change/decision home, using only the actual feedback as its basis. Keep prior decisions and route requested content revisions to their domain owner.
5. Update affected freshness and the configured recovery entry, then refresh the view when useful. Downstream work consumes canonical references and decisions, not page state.

Minimum decision content (existing Markdown/HTML/tracker fields suffice):

```yaml
id: D-12
subject: DESIGN-7
reviewed_revision: <immutable revision or digest with retrievable content reference>
outcome: accepted
scope: export interaction
basis: <reason supported by the actual feedback>
source: <durable feedback reference or faithfully retained user response>
```

Acceptance is scoped to that subject and revision, not every proposal displayed together. Design acceptance and authorization to implement, commit or publish are distinct; existing explicit authorization persists. Material changes to content or dependencies mark affected applicability `needs review`, retaining the historical decision. Cosmetic report changes do not invalidate a domain decision; layout is material when visual design itself was reviewed.

Critical comments and revision requests belong in canonical records. Browser localStorage may store UI preferences only, never decisions or sole feedback copies. A retained review snapshot is historical evidence, not a second current fact source.
