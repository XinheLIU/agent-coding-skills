# HTML Delivery Report

Last updated: 2026-09-25

The user receives one `docs/changes/<change-id>/delivery-plan.html` after accepted scope has been decomposed. Preserve an established report location on resumed work. `acs-plan-delivery` owns domain scope, decomposition, blockers, and recommendations; [Presenter](../../../resources/protocols/presenter.md) owns display and review semantics. `acs-draw-portfolio-dag` renders the derived view and can refresh progress without repeating planning.

## Generate

1. Scan canonical tickets with `acs-draw-portfolio-dag/scripts/scan_tasks.py`. Include prerequisite changes for cross-change edges; keep qualified IDs. For an existing tracker, derive the same manifest from its canonical records. Report nodes retain `ticket_type`, `readiness`, `scope`, `inputs`, `verification`, `blockers`, and `evidence` as plain text alongside IDs, dependencies, status, and source revisions.
2. Prepare a derived `plan.json` in the configured Working Memory. Summarize accepted source records; retain scope and substantive decisions in their canonical homes. Required fields:

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

   Source links resolve relative to the final HTML file, or use an established tracker URL. The next action reflects current authorization and blockers; readiness alone does not authorize execution. Keep reasons for changed edges in canonical tickets and summarize consequential changes in the handoff.
3. Resolve `DAG_DIR` to the installed `acs-draw-portfolio-dag` skill directory and render with its existing CLI:

   ```bash
   python3 "$DAG_DIR/scripts/render_dag.py" "$RUN_DIR/manifest.json" \
     --plan "$RUN_DIR/plan.json" --format html \
     --storage-key "delivery-<change-id>" \
     --title "<Change title> — delivery plan" \
     -o "docs/changes/<change-id>/delivery-plan.html"
   ```

   `RUN_DIR` is the resolved Working Memory directory. The renderer embeds the report, graph, styles, and scripts into one file; no server or network dependency is required. Ticket details remain readable without JavaScript. Mermaid and graph-only HTML remain available for other callers.

The HTML is a Human Review View, not a memory source. Preserve proposed plan decisions in canonical records before formal review; use those records and their revisions for feedback. Retain a reviewed snapshot only when its presentation influenced the decision.

## Present and refresh

Open the HTML using the available browser capability and return a clickable file link. If opening is unavailable, return the link and state that it was generated but not opened. Inspect scope/outcomes, next action, frontier, design blockers, graph, ticket checks/evidence, and source links. Verify graph and ticket counts, dependencies, readiness, and links against the manifest and canonical sources.

After a ticket transition, re-scan, refresh the derived next action, and re-render the **same HTML path** with `--plan` and the same storage key. Reload an open tab to show the update; file regeneration alone does not update a loaded page. Refresh ordinary execution status directly; return scope or dependency changes to `acs-plan-delivery`. Recreate missing run files from canonical sources rather than treating the HTML or JSON as authoritative.
