---
name: draw-portfolio-dag
description: Render Markdown workstreams and dependency tickets as an interactive HTML DAG or Mermaid flowchart. Use for portfolio sequencing, frontier visibility, or cross-cutting ticket tags.
---

# Draw Portfolio DAG

Last updated: 2026-08-25

Resolve `SKILL_DIR` as this skill's directory and call its scripts by absolute path.

## Input contract

The scanner accepts one folder per workstream:

```text
<root>/
  <workstream>/
    map.md or spec.md
    issues/
      NN-<slug>.md
```

Each issue uses an H1 plus `**Status:**` and `**Blocked by:**` fields. The scanner resolves same-workstream blockers written as `NN - title`. It reports prose and cross-workstream blockers in `nodes[*].unresolved_dep_text` for explicit resolution.

When the source uses different fields or YAML frontmatter, adapt `scripts/scan_specs.py` to the source format. Preserve the project's documents as the authority.

## Procedure

1. **Scan.**

   ```bash
   python3 "$SKILL_DIR/scripts/scan_specs.py" <root> -o manifest.json
   ```

   Read the warnings and every non-empty `unresolved_dep_text`. Scanning is complete when the manifest contains every intended workstream and ticket exactly once.

2. **Resolve ambiguity.** Put genuine cross-ticket edges and optional labels in an overlay:

   ```json
   {
     "extra_deps": {"AOM01": ["ASR07"]},
     "tags": {"SPR04": ["data", "deploy"]},
     "tag_styles": {
       "data": {"label": "DATA", "bg": "#5b21b6", "fg": "#fff"},
       "deploy": {"label": "DEPLOY", "bg": "#b45309", "fg": "#fff"}
     }
   }
   ```

   Leave external preconditions as prose. Resolution is complete when each warning is either mapped to a verified ticket ID or deliberately retained as a non-ticket blocker.

3. **Render the requested view.** The overlay is optional.

   ```bash
   python3 "$SKILL_DIR/scripts/render_dag.py" manifest.json --overlay overlay.json \
     --format html -o roadmap.html --title "My Roadmap"

   python3 "$SKILL_DIR/scripts/render_dag.py" manifest.json --overlay overlay.json \
     --format mermaid -o roadmap.md --title "My Roadmap"
   ```

4. **Verify.** Compare output workstream, node, and dependency counts with the manifest; open HTML output when browser control is available. The graph is done when all verified dependencies render, completed tickets are green, frontier tickets are orange, blocked tickets are blue, and the generated views contain no canonical status.

## Source and view

Markdown owns ticket status and dependency text. The overlay owns only explicit edges the scanner cannot infer and optional tags. Generated HTML and Mermaid are views.

Re-scan after ticket changes, then re-render. HTML drag positions persist in browser `localStorage`; `--storage-key` controls whether multiple outputs share that layout.
