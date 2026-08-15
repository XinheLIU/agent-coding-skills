---
name: draw-portfolio-dag
description: Turn a portfolio of spec/ticket folders (each with spec.md + issues/NN-*.md) into a dependency DAG — interactive draggable HTML or a Mermaid flowchart — colored by finished/frontier/todo, with small tag badges (data change, deploy/build impact, or any custom tag).
---

# Draw Portfolio DAG

Last updated: 2026-08-02

Mechanically scans a folder of workstreams (each `<workstream>/map.md` or `spec.md` +
`<workstream>/issues/NN-slug.md`) and renders their ticket dependency graph.
Built for the pattern used in `.scratch/` here: several spec folders, each
with numbered tickets that reference other tickets via a `**Blocked by:**`
field.

## When to use

- User asks to draw/update a DAG, dependency graph, or portfolio map of
  specs/tickets/tasks.
- User wants ticket status visualized as finished / ready-to-start / blocked.
- User wants to mark which tickets touch production data, migrations, or
  deploys (or any other cross-cutting property) with small labels.

## Expected input shape

```
<some-folder>/
  workstream-a/
    map.md or spec.md
    issues/
      01-do-the-thing.md
      02-do-another-thing.md
  workstream-b/
    spec.md
    issues/
      01-....md
```

Each issue file should have:
- An H1 title: `# 01 Do the thing` (number + slug from the filename is fine
  too if there's no H1).
- A `**Status:**` line — anything containing "done"/"completed"/"merged"/a
  commit hash reads as finished; anything else is not-finished.
- A `**Blocked by:**` line — free text. The scanner auto-resolves clauses
  shaped like `NN — Title of ticket NN in the same workstream`. Anything else
  (cross-workstream refs, external preconditions, prose) is left unresolved
  and reported — do **not** guess at these; read them and add them to the
  overlay file's `extra_deps` by hand, or leave them out if they're not
  actually a ticket dependency.

If a real project's tickets look different (different field names, no `Blocked
by` field, dependencies as a YAML frontmatter list, etc.), adjust
`scripts/scan_specs.py`'s regexes rather than reshaping the project's docs to
fit the tool.

## Workflow

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Use absolute
script paths so the commands work from the target repository.

1. **Scan**: `python3 "$SKILL_DIR/scripts/scan_specs.py" <root> -o manifest.json`
   Prints how many unresolved "Blocked by" clauses it found. Read
   `manifest.json`'s `nodes[*].unresolved_dep_text` for each one.

2. **Resolve by hand into an overlay** (`overlay.json`, gitignore-able or
   commit it — your call):
   ```json
   {
     "extra_deps": { "AOM01": ["ASR07"] },
     "tags": { "SPR04": ["data", "deploy"] },
     "tag_styles": {
       "data":   {"label": "DATA",   "bg": "#5b21b6", "fg": "#fff"},
       "deploy": {"label": "DEPLOY", "bg": "#b45309", "fg": "#fff"}
     }
   }
   ```
   `tags`/`tag_styles` are open-ended — use whatever small labels the task
   calls for (e.g. `breaking`, `external-dep`, `needs-review`). Only add an
   entry to `extra_deps` for a genuine ticket-to-ticket dependency; free-text
   preconditions ("an external team must ship X first") aren't edges — leave
   them out.

3. **Render**:
   ```bash
   # interactive, draggable HTML
   python3 "$SKILL_DIR/scripts/render_dag.py" manifest.json --overlay overlay.json \
     --format html -o roadmap.html --title "My Roadmap"

   # or a Mermaid flowchart (for embedding in a markdown doc / PR description)
   python3 "$SKILL_DIR/scripts/render_dag.py" manifest.json --overlay overlay.json \
     --format mermaid -o roadmap.md --title "My Roadmap"
   ```

## HTML output behavior

- One row per workstream; one card per ticket.
- Color is **derived**, not stored: green = finished, orange = frontier (all
  deps finished, not itself finished — i.e. ready to start now), light blue =
  todo (blocked). Frontier/todo are derived from Markdown status and dependencies.
- Drag a card to reposition. Layout persists in `localStorage` (keyed by output filename by default —
  override with `--storage-key` if rendering multiple DAGs that should share
  or not share state).
- "Reset layout" clears the layout override.
- Tags render as small colored pills under the title, styled per
  `overlay.json`'s `tag_styles`.
- Self-contained single file — no build step, no network dependency, opens
  directly in a browser.

## Re-running after tickets change

Re-run step 1 whenever ticket files change (status flips, new tickets added,
dependencies edited). The overlay file is stable across re-scans as long as
node IDs (`{workstream_prefix}{NN}`) don't change — only add to it when the
scanner reports new unresolved dependencies. Re-run step 3 to regenerate the
output. Manual drag positions live in that browser's `localStorage`, so
regenerating HTML keeps the layout when the storage key is unchanged. Status
and dependency state always come from Markdown; HTML does not write them back
or override them.

## Adjusting for a different tool/output

The two scripts are decoupled deliberately:
- `scan_specs.py` only knows about reading markdown into a JSON manifest
  (`{workstreams: [...], nodes: [...]}`). Change this if the ticket file
  format differs.
- `render_dag.py` only knows about turning that JSON manifest (+ optional
  overlay) into HTML or Mermaid. Add a new `--format` branch here for another
  output (e.g. Graphviz DOT, a JSON export for some other viewer) without
  touching the scanner.
