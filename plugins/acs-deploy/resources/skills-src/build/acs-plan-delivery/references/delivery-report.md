# HTML Delivery Report

Last updated: 2026-10-11

After `acs-plan-delivery` decomposes the accepted scope, the user receives one `docs/changes/<change-id>/delivery-plan.html`. On resumed work, keep an established report location.

| Owner | Owns |
| --- | --- |
| `acs-plan-delivery` | domain scope, decomposition, blockers, recommendations |
| [Presenter](../../../../protocols/presenter.md) | display and review semantics |
| `acs-draw-portfolio-dag` | rendering the derived view; refreshing progress without planning again |

## Generate

1. Scan canonical tickets with `acs-draw-portfolio-dag/scripts/scan_tasks.py`. Include prerequisite changes for cross-change edges, and keep qualified IDs. For an existing tracker, derive the same manifest from its canonical records. Report nodes keep `ticket_type`, `readiness`, `scope`, `inputs`, `verification`, `blockers` and `evidence` as plain text, next to IDs, dependencies, status and source revisions.
2. Prepare a derived `plan.json` in the configured Working Memory. Summarize the accepted source records. Keep scope and substantive decisions in their canonical homes. Required fields:

   ```json
   {
     "scope": "Let members edit profile details; account deletion is outside this change.",
     "outcomes": ["Members can edit their display name", "Members can replace their avatar"],
     "next_action": "Resolve avatar storage with technical design; display-name editing is ready for implementation.",
     "sources": [
       {"label": "Accepted profile scope", "href": "../../product/accounts/product.html#profile-scope", "revision": "<consumed source revision>"}
     ]
   }
   ```

   Source links resolve relative to the final HTML file, or use an established tracker URL. The next action reflects current authorization and blockers; readiness alone does not authorize execution. Keep the reasons for changed edges in canonical tickets. Summarize consequential changes in the handoff.
3. Resolve `DAG_DIR` to the installed `acs-draw-portfolio-dag` skill directory and render with its existing CLI:

   ```bash
   python3 "$DAG_DIR/scripts/render_dag.py" "$RUN_DIR/manifest.json" \
     --plan "$RUN_DIR/plan.json" --format html \
     --storage-key "delivery-<change-id>" \
     --title "<Change title> — delivery plan" \
     -o "docs/changes/<change-id>/delivery-plan.html"
   ```

   `RUN_DIR` is the resolved Working Memory directory. The renderer embeds the report, graph, styles and scripts in one file; it needs no server or network. Ticket details stay readable without JavaScript. Mermaid and graph-only HTML stay available for other callers.

The HTML is a Human Review View, not a memory source. Before formal review, save proposed plan decisions in canonical records. Use those records and their revisions for feedback. Keep a reviewed snapshot only when its presentation influenced the decision.

## Present and refresh

Open the HTML with the available browser capability and return a clickable file link. If you cannot open it, return the link and say that it was generated but not opened.

Inspect the scope and outcomes, next action, ready work, design blockers, graph, ticket checks and evidence, and source links. Verify graph and ticket counts, dependencies, readiness and links against the manifest and canonical sources. The graph's colours, legend and node labels follow the [task graph contract](../../../../protocols/task-graph.md). Confirm each ticket's view status there; do not read the colours as a new vocabulary.

After a ticket transition:

1. Scan again and refresh the derived next action.
2. Render the **same HTML path** again, with `--plan` and the same storage key.
3. Reload an open tab to show the update. Regenerating the file does not update a loaded page.

Refresh ordinary execution status directly. Send scope or dependency changes back to `acs-plan-delivery`. If run files are missing, recreate them from canonical sources; never treat the HTML or JSON as authoritative.
