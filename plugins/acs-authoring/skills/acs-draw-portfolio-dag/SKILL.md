---
name: acs-draw-portfolio-dag
description: Render Markdown workstreams and dependency tickets as an interactive HTML DAG or Mermaid flowchart. Use for portfolio sequencing, frontier visibility, cross-cutting ticket tags, or live progress rendering during an implement run.
---

# Draw Portfolio DAG

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [change.tickets]
  retrieves: [change.dependencies]
  produces: [change.roadmap_view]
  updates: [run.derived_views]
  invalidates: []
  handoff_to: [coordinator]
```

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.


Resolve `SKILL_DIR` as this skill's directory and call its scripts by absolute path.

## Input contract

For canonical delivery tickets from `acs-plan-delivery`, scan one change directory or `docs/changes/`:

```bash
python3 "$SKILL_DIR/scripts/scan_tasks.py" docs/changes/<change-id> -o manifest.json
```

The [ticket template](../../resources/skills-src/build/acs-plan-delivery/templates/ticket.md) defines this local format: `tasks/<task-id>.md`, an H1 `<task-id>: <title>`, and plain `Type:`, `Status:`, `Readiness:`, `depends_on:` fields. Dependencies are comma-separated local task IDs or `change/task` IDs; `none` means no dependencies. To resolve cross-change edges, scan the common changes directory including prerequisite tickets. Other tracker schemas need a derived manifest rather than conversion of canonical documents.

The adapter preserves qualified canonical IDs, source paths and SHA-256 revisions. It rejects missing prerequisite IDs and cycles, flags unknown fields, and keeps design tickets, failed/superseded tickets, unresolved dependencies, and unready inputs off the implementation frontier. A historical done ticket with stale readiness remains visible but cannot satisfy downstream prerequisites. The renderer labels type/readiness/status as tags and validates final edges after overlays are applied.

For legacy workstreams, `scan_specs.py` accepts one folder per workstream:

```text
<root>/
  <workstream>/
    map.md or spec.md
    issues/
      NN-<slug>.md
```

Each issue uses an H1 plus `**Status:**` and `**Blocked by:**` fields. The scanner resolves same-workstream blockers written as `NN - title`. It reports prose and cross-workstream blockers in `nodes[*].unresolved_dep_text` for explicit resolution.

The legacy scanner supports only that shape. For other tracker schemas, supply a derived manifest/overlay matching the existing renderer schema from canonical IDs, status, dependencies, and source revisions; validate every node against its source. Do not rewrite tracker documents to fit the scanner or silently omit unsupported sources. Scanner aliases are view IDs only; retain canonical IDs in labels/source references.

## Procedure

1. **Scan.** Use the canonical adapter above for delivery tickets. For legacy inputs:

   ```bash
   python3 "$SKILL_DIR/scripts/scan_specs.py" <root> -o manifest.json
   ```

   Read the warnings and every non-empty `unresolved_dep_text`. Scanning is complete when the manifest contains every intended workstream and ticket exactly once.

2. **Resolve ambiguity.** Verify cross-ticket edges against the canonical ticket relationships; ask the coordinator to reconcile missing relationships there first. An optional derived overlay can encode verified edges and presentation labels for rendering:

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

   For `acs-plan-delivery`, pass `--plan plan.json -o docs/changes/<change-id>/delivery-plan.html` to embed the plan and DAG in one self-contained HTML file. Follow its [delivery report contract](../../resources/skills-src/build/acs-plan-delivery/references/delivery-report.md) for the derived summary, canonical ticket details, opening, and refresh behavior. The renderer derives the frontier and design-blocker list from the same ticket nodes as the graph.

4. **Verify.** Compare output workstream, node, and dependency counts with the manifest; open HTML output when browser control is available. The graph is done when all verified dependencies render, completed tickets with current evidence are green, execution-ready frontier tickets are orange, design/unready/blocked tickets are blue, and displayed status matches canonical tickets without becoming independently editable.

## Source and view

Canonical tickets own status, readiness, and dependency text. The overlay projects verified canonical edges the scanner cannot parse, plus presentation tags; it never owns dependency truth. Record input revisions and rederive the overlay when premises change. Generated HTML and Mermaid are views.

Re-scan after ticket changes, then re-render. HTML drag positions persist in browser `localStorage`; `--storage-key` controls whether multiple outputs share that layout.

## Live execution view

`acs-plan-delivery` renders and opens the combined report after planning or graph reconciliation. An orchestrating run (`build/acs-implement`) re-scans and re-renders the same report on ticket transitions, refreshing the summary's next action and preserving `--plan`. Reload the open browser tab to show progress. Canonical scans emit `in_progress` and `execution_ready`; legacy/other derived manifests can supply them too. Execution overlays may add `agent: "<ref>"`, which renders a small agent label beside the node id. Keep the output path and `--storage-key` fixed so the user's drag layout survives reloads.
