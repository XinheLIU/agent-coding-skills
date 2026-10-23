# Visual Report Contract

Last updated: 2026-10-11

[Presenter](../../../protocols/presenter.md) uses this display template to render a complex Human Review View. Domain records supply the findings, options, recommendations, evidence and blockers. Arrange that content; do not add conclusions. Use text for simple results. The release builder bundles this file and its references for standalone consumers.

## When to use tabbed layout

Use the [tabbed layout](tabbed-discovery-report.md) instead of flat cards for any of these:

- 3 or more major architectural concerns;
- a long revision history;
- nested options;
- before/after comparisons across several dimensions.

Keep simple findings (1–5 cards, one dimension) as cards without tabs.

## Reading order

- **Header:** a title that names the subject (not a sentence, at most 2rem). One meta line `YYYY-MM-DD · <revision> · <scope>`, the review status and a compact legend. No lede paragraph.
- **Overview:** status and count pills, and the top recommendation or decision.
- **Cards:** one card per finding or capability.
- **Evidence:** source paths and detailed rationale, inside `<details>` where possible.
- **Footer:** provenance, source artifact and generation information.

The first viewport tells the reader what matters and where to look next. Do not start with an essay.

## Card contract

Each finding, candidate, capability, option or module is one `<article class="card">`. Keep this order in every card:

1. short title and status badge;
2. involved files or records, in monospace;
3. a dominant current/target (before/after) visual;
4. the problem, in one sentence;
5. the solution or observed behavior, in one sentence;
6. at most four short wins, each naming the concrete gain;
7. the visual takeaway next to the visual, in one sentence;
8. an optional decision, ADR or uncertainty callout;
9. collapsed evidence with file/line or record anchors.

```html
<article class="card" id="FND-CON-3" data-visual="compare">
  <h3>Short title naming the change</h3>
  <div class="badges"><span class="badge">P1</span><span class="tag">in-process</span></div>
  <pre class="files">src/a.ts:26  ← what this line is
src/b.ts:129 ← what this line is</pre>
  <div class="grid">
    <div class="pane"><h4>Before</h4><svg role="img" viewBox="0 0 400 300"><title>…</title>…</svg></div>
    <div class="pane"><h4>After</h4><svg role="img" viewBox="0 0 400 300"><title>…</title>…</svg></div>
  </div>
  <p class="takeaway">One sentence: what the picture shows.</p>
  <div class="two">
    <div><p><strong>Problem.</strong> …</p><p><strong>Solution.</strong> …</p></div>
    <ul class="wins"><li>…</li></ul>
  </div>
  <div class="callout">Optional decision or ADR line.</div>
  <details><summary>Evidence</summary>…</details>
</article>
```

Never collapse the card body. Only evidence goes inside `<details>`, never the title or the visual.

**Every card has a visual.** `data-visual` states its kind:

| Value | Use for | Requires |
| --- | --- | --- |
| `compare` (default) | Structural change: modules, seams, ownership, options, refactors | two `.pane` elements, Before and After |
| `single` | Table-shaped content: contracts, gates, test layers, traceability | one schematic beside the table, e.g. the path with the enforcement point marked, a failure path, a layer grid |
| `none` | A pure ledger row that only links to a card elsewhere | nothing |

A table never replaces the visual; it sits beside it.

**Diagrams are schematics, not prose.** Labels are names and short phrases: at most 14 words per `<text>` and 90 words per SVG. Put sentences in the takeaway or the problem/solution line. If the diagram needs a paragraph, redraw it. Keep diagrams roughly 320–360px tall. Vary the patterns:

- Mermaid flow or sequence graphs for relationships;
- hand-built boxes and arrows for seams;
- cross-sections for shallow layers;
- mass diagrams for interface versus implementation;
- call-graph collapse for repeated delegation.

## Writing

These rules adapt [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) and the controlled-writing rules of answer-me-with-html. They apply to every visible sentence in a view or HTML record: cards, tables, callouts, summaries and evidence. Diagram labels follow the schematic rule above.

**Logic**

- **Conclusion first.** The header and overview give the answer or the decision. The cards give the evidence.
- **One card, one finding.** One sentence, one statement. One paragraph, one topic: put the topic sentence first, use at most 6 sentences, or use a list.
- **Say each fact once.** Put it at one disclosure level and link to it from other places.
- **Steps:** one action per step, in the imperative. Put the condition first: "If the build fails, rerun the scan."
- **Warnings:** start with the command, then give the risk: "Do not rebuild the record from the view. The view can be stale."

**Words**

- **Sentence length:** a step (an `<ol>` item) has at most 20 words; any other sentence has at most 25. In Chinese, the limits are 35 and 45 characters.
- **Active voice:** name the actor. ✗ "The ticket is closed." ✓ "`acs-plan-delivery` closes the ticket."
- **Simple tenses:** use the present, the past or the future.
- **One term, one meaning:** use the record's own terms and IDs. Do not rename a thing for variety.
- **Short noun clusters:** use at most 3 nouns in a row. ✗ "review feedback reconciliation step" ✓ "the step that reconciles review feedback".
- **Common words:**

  | Write | Not |
  | --- | --- |
  | use | utilize, leverage (verb) |
  | start | commence |
  | before | prior to |
  | to | in order to |
  | help | facilitate |
  | about | with regard to |
  | the number (`4 files`) | a number of, several, various |

- **No filler:** delete "it's worth noting" and "basically". Replace "robust", "better" or "improved" with what improved.
- **Chinese:** do not use light verbs (`进行优化` → `优化`, `加以说明` → `说明`). Do not chain more than 3 `的`. Do not use clichés (`赋能`, `闭环`, `至关重要`).
- **Counter-examples:** write a deliberate bad example inside `<s>` or `<del>`, so the check skips it.

**Card budget:** a card has at most 120 words of prose outside `<svg>`, `<pre>` and `<details>`. This is the card skeleton at its sentence limits. Move more text into evidence.

## Visual and runtime rules

- Use inline CSS and inline SVG as the portability baseline. Mermaid is an optional progressive enhancement for graph-shaped diagrams when the report environment permits network access.
- Keep labels and basic structure in ordinary HTML, so the report stays readable if a CDN or Mermaid render fails.
- Use one accent color. Use red only for leakage and problems, amber only for warnings, and dark emphasis for deep modules or recommendations.
- Editorial, not dashboard: shadows at most `0 1px 2px`, radius at most 12px, serif headings allowed, no hero-sized headline.
- Define colors once as CSS custom properties, with a `prefers-color-scheme: dark` override. SVG `fill`, `stroke` and `stop-color` use `var(--token)`, `none`, `currentColor` or `url(#id)`, never raw hex, so diagrams follow the theme.
- Put long evidence, open questions and implementation detail behind native `<details>` elements.
- Give every diagram an adjacent one-sentence takeaway.
- End every report with one anchored top recommendation or next decision.
- Keep roadmap and implementation sequencing artifacts separate from finding reports. Do not use a roadmap as an audit companion.

## Date and version

Agents and readers must see which snapshot a view shows without opening its sources. Every view carries, in `<head>`:

```html
<meta name="generated" content="YYYY-MM-DD">
<meta name="source-revision" content="<commit sha or record revision>">
```

The header meta line shows the same date and revision.

- **One-off report** (review, audit, refactor report, discovery pass): name the file `<slug>-YYYY-MM-DD.html`. A later run writes a new file; the older one stays as dated evidence.
- **Living view** rebuilt at a fixed path that other records link to (for example `technical-design.html`): keep the path and add `<meta name="view-kind" content="living">`. The date and revision tags are still required.

The same rule covers every other human-readable HTML file: canonical records, roadmaps, delivery plans and prototypes. See [Presenter date and version](../../../protocols/presenter.md#date-and-version). Those files validate with `--version-only`, because the card rules apply only to finding reports.

## Validate before handover

Run [the report validator](../scripts/validate-report-html.py) on every generated view. Fix each error before handover:

```bash
python3 <path of the validator link above> path/to/view.html
```

| Output | Checks | Effect |
| --- | --- | --- |
| Errors | each card's `data-visual` against its panes and SVGs; SVG label density; raw hex colors; accessible titles; collapsed cards; internal links; the top recommendation; the `generated` and `source-revision` tags; the dated filename of a one-off report | A view that fails is not finished. |
| Warnings | the Writing rules: long sentences and steps, long paragraphs, words from the replacement table, Chinese light verbs and `的` chains, card prose over budget | The run does not fail. Fix each one, or keep it only as a deliberate exception. |

## Portability

Consumer `references/visual-report.md` aliases resolve to this single file in the repository. Packaging copies the reference closure with working local links. Keep domain-specific content requirements in the consumer's report reference; keep display and writing rules here. No separate Presenter skill is required.

## Quality gates

- The report validator passes with no errors.
- The wording check prints no warnings, or each remaining warning is a named, deliberate exception.
- Internal card and recommendation links resolve.
- Evidence stays reachable when visible prose is short.
- Domain sources stay authoritative, including canonical product HTML and prototype artifacts. Deleting this derived report loses no unique fact or decision.
- Visible source revisions match the requested snapshot. Refresh and feedback processing recheck the sources under Presenter.
- Review feedback goes in the canonical record, never in browser localStorage. localStorage holds display preferences only.
- Inline SVG includes accessible `<title>` and `<desc>` elements. Ordinary HTML labels keep the meaning if scripts or CDNs fail.
- Changed Markdown files carry a current `Last updated` line near the top.
