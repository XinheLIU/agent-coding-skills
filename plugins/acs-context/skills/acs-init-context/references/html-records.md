---
protocol: acs:html-records
version: 1.0.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/html-records.md
---

# HTML Record Format

Last updated: 2026-09-26

This is the shared serialization grammar for canonical HTML memory documents — currently product memory (`product.html`, `discovery.html`) and the design prototype (`prototype.html`). It defines *how* records are written and retrieved. Which records exist, who owns them, and what their statuses mean belong to the domain contracts ([Product](../../../resources/protocols/product-memory.md), [Design](../../../resources/protocols/design-memory.md)); derived human views belong to [Presenter](../../../resources/protocols/presenter.md).

## Self-contained document

Use a readable, self-contained document: UTF-8, responsive viewport, title, visible update date, inline shared CSS once, semantic headings, lists, tables, links, and native `<details>`. The document needs no build step and opens from `file://`. All canonical facts must be readable from source HTML with JavaScript disabled. No remote dependency is required to read the document. Reuse the document's existing visual style instead of redesigning it on each skill run.

Record IDs and `data-*` attributes are the reading contract; visual classes are not. Never store a second semantic copy in Markdown, embedded JSON, JavaScript state, or browser storage. Browser localStorage may hold UI preferences only, never decisions or sole feedback copies.

## Records and structure

- Every record is one self-contained `<article>` with a document-unique `id` following `<kind>-<slug>` (e.g. `gap-export-feedback`); no record content lives outside its article.
- An article's `data-kind` comes from its domain contract's **closed list**. Do not invent a kind; if genuinely none fits, add a `data-kind-reason` attribute stating why, so validation flags the record for review instead of failing.
- The same discipline applies to lifecycle attributes: do not invent additional `data-*` attributes; if a record genuinely needs one, add a `data-attr-reason` stating why so review flags it.
- Sections use only the domain contract's closed-list section IDs, in its stated order; empty sections are omitted.
- The `<nav>` block at the top lists each present section and, per section, its record IDs with one-line titles — the document's own index.
- Use stable, document-unique IDs; preserve them across edits and promotion. Promotion pointers retain the old ID and link to the new canonical home. Do not reuse retired IDs for different subjects.
- Link related records with ordinary `<a href="#record-id">` or relative file-and-anchor links. All internal `#anchor` links resolve; file links resolve relative to the document. Express `depends_on`/`affects`/`supersedes` relationships as visible labelled links inside the record; do not add a second metadata store.

## Targeted retrieval

Structure lets an agent fetch what it needs without scanning the whole document. An agent reads `<nav>` first, then extracts only the target `<article>` blocks (e.g. `grep -n 'article id=' file.html` to locate offsets, then read the matching ranges).

| Need | Pattern |
| --- | --- |
| One record | locate `article id="<record-id>"`, read to its closing `</article>` |
| All of one kind | locate every `data-kind="<kind>"` article |
| One section | read from `<section id="<section-id>">` to its closing tag |
| Orientation | read `<nav>` only |

This is why documents must stay concise: one record per subject, links instead of copies, diagrams and tables instead of prose walls. A record too long to read in one grab should link evidence rather than inline it. Prefer a diagram, table, or chip row over prose where it carries the same meaning; every diagram gets an adjacent one-sentence takeaway. Render graph diagrams as inline SVG when available, or retain their readable diagram source with a text explanation. Collapsing content does not reduce agent context; agents locate relevant records before reading. Keep source formatted for targeted patches, with one record per readable block.

## Writing

Section tags do not provide concurrency control. Serialize writes to each shared file under the [shared protocol](../../../resources/protocols/skill-declarations.md#coordinated-writes-and-claims). Immediately before applying a patch, reread its target and referenced premises; if they changed, reconcile first. Never overwrite a shared file from a stale whole-document snapshot. Preserve unrelated fields, user edits, IDs, and layout. Update visible `Last updated` dates on changed records and the document.
