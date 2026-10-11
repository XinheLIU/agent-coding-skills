---
protocol: acs:html-records
version: 1.2.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/html-records.md
---

# HTML Record Format

Last updated: 2026-10-11

This is the shared serialization grammar for canonical HTML memory documents: product memory (`product.html`, `discovery.html`) and the design prototype (`prototype.html`). It defines *how* agents write and retrieve records.

- The domain contracts ([Product](product-memory.md), [Design](design-memory.md)) define which records exist, who owns them and what their statuses mean.
- [Presenter](presenter.md) owns derived human views.

## Self-contained document

Write a readable, self-contained document:

- UTF-8, a responsive viewport and a title.
- A visible update date and revision, with matching `generated`, `source-revision` and `view-kind="living"` meta tags (see [Presenter date and version](presenter.md#date-and-version)).
- Shared CSS inlined once; semantic headings, lists, tables, links and native `<details>`.
- No build step; it opens from `file://`. No remote dependency is necessary to read it.
- Every canonical fact is readable from the source HTML with JavaScript disabled.

Reuse the document's existing visual style. Do not redesign it on each skill run.

Record IDs and `data-*` attributes are the reading contract; visual classes are not. Never store a second semantic copy in Markdown, embedded JSON, JavaScript state or browser storage. Browser localStorage holds UI preferences only, never decisions or the only copy of feedback.

## Records and structure

- Every record is one self-contained `<article>` with a document-unique `id` in the form `<kind>-<slug>` (e.g. `gap-export-feedback`). No record content lives outside its article.
- An article's `data-kind` comes from its domain contract's **closed list**. Do not invent a kind. If no kind fits, add a `data-kind-reason` attribute that states why. Validation then flags the record for review instead of failing.
- Lifecycle attributes follow the same rule. Do not invent `data-*` attributes. If a record needs one, add a `data-attr-reason` that states why, so review flags it.
- Sections use only the domain contract's closed-list section IDs, in its stated order. Omit empty sections.
- The `<nav>` block at the top is the document's index. It lists each present section and, per section, its record IDs with one-line titles.
- Keep IDs stable and document-unique across edits and promotion. A promotion pointer keeps the old ID and links to the new canonical home. Do not reuse a retired ID for a different subject.
- Link related records with ordinary `<a href="#record-id">` or relative file-and-anchor links. All internal `#anchor` links resolve; file links resolve relative to the document. Show `depends_on`, `affects` and `supersedes` as visible labelled links inside the record. Do not add a second metadata store.

## Targeted retrieval

An agent reads `<nav>` first, then extracts only the target `<article>` blocks. For example, it runs `grep -n 'article id=' file.html` to find offsets, then reads the matching ranges.

| Need | Pattern |
| --- | --- |
| One record | find `article id="<record-id>"`, read to its closing `</article>` |
| All of one kind | find every `data-kind="<kind>"` article |
| One section | read from `<section id="<section-id>">` to its closing tag |
| Orientation | read `<nav>` only |

Targeted retrieval works only when records stay short:

- One record per subject. Link to other records; do not copy them.
- If a record is too long to read in one extract, link its evidence instead of inlining it.
- Prefer a diagram, table or chip row to prose when it carries the same meaning. Give every diagram an adjacent one-sentence takeaway. Render graph diagrams as inline SVG when available. Otherwise keep their readable diagram source with a text explanation.
- Write visible text to the [Writing rules](../../skills/acs-design-architecture/references/visual-report.md#writing).

Collapsing content does not reduce agent context, because agents find the relevant records before they read. Format the source for targeted patches, with one record per readable block.

## Writing

Section tags do not give concurrency control. Serialize writes to each shared file under the [shared protocol](skill-declarations.md#coordinated-writes-and-claims).

1. Immediately before you apply a patch, reread its target and the premises it references. If they changed, reconcile first.
2. Never overwrite a shared file from a stale whole-document snapshot. Keep unrelated fields, user edits, IDs and layout.
3. Update the visible `Last updated` dates on changed records and on the document. Set the document's `generated` and `source-revision` meta tags to match. A document written before this rule gets the tags on its next write.
4. Run the [validator](../skills-src/authoring/scripts/validate-report-html.py) with `--version-only`. Fix every error.
