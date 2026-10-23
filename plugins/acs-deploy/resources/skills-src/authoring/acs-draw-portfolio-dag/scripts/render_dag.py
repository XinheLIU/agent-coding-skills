#!/usr/bin/env python3
"""Render a scanned ticket manifest into HTML or Mermaid.

Usage:
    python3 render_dag.py manifest.json --overlay overlay.json --format html -o dag.html
    python3 render_dag.py manifest.json --overlay overlay.json --format mermaid -o dag.md
    python3 render_dag.py manifest.json --plan plan.json -o delivery-plan.html

View status, palette, layout, and the critical path come from the shared
contract in system/protocols/task-graph.md. This script implements it; change
the contract before changing the rendering rules.

The overlay file supplies anything the mechanical scan cannot infer:
  - extra_deps:  {node_id: [dep_id, ...]}   merged with scanned deps
  - tags:        {node_id: ["data", "deploy", ...]}  arbitrary small labels
  - tag_styles:  {tag_key: {"label": "DATA"}}  pill label override
It is optional — omit --overlay to render the mechanically-scanned graph as-is.

Canonical scans and derived manifests may add per-node fields:
  - in_progress: true      renders the node as in progress
  - execution_ready: false keeps unready design/criteria tickets off the frontier
  - agent: "ref"           renders a small agent label beside the node id
"""
import argparse
import json
import os
import re
import subprocess
from datetime import date
from html import escape
from pathlib import Path
from typing import TypedDict
from urllib.parse import quote, urlsplit

from scan_tasks import TicketNode, validate_graph

# One palette definition, consumed by the CSS tokens, the Mermaid classes, and
# the status rules. Adding a view status means adding a row here.
PALETTE: dict[str, dict[str, str]] = {
    "done": {"bg": "#e6f5ec", "bd": "#4a9d6e", "fg": "#1e6b45", "label": "Done"},
    "in_progress": {"bg": "#fdf2df", "bd": "#cf9a35", "fg": "#7c5510", "label": "In progress"},
    "failed": {"bg": "#fbe8e5", "bd": "#c85a49", "fg": "#8a2f22", "label": "Failed"},
    "ready": {"bg": "#e8f1fc", "bd": "#4b82c9", "fg": "#1e4a8a", "label": "Ready now"},
    "needs_design": {"bg": "#efecfb", "bd": "#7766cd", "fg": "#443789", "label": "Needs design or review"},
    "waiting": {"bg": "#f2f3f6", "bd": "#a9b0bb", "fg": "#4c5361", "label": "Waiting on prerequisites"},
    "superseded": {"bg": "#f2f3f6", "bd": "#a9b0bb", "fg": "#6b7280", "label": "Superseded"},
}
DARK_PALETTE: dict[str, dict[str, str]] = {
    "done": {"bg": "#14301f", "bd": "#4fae7d", "fg": "#9fe0bd"},
    "in_progress": {"bg": "#33290f", "bd": "#c9922f", "fg": "#f0cf8a"},
    "failed": {"bg": "#3a1d19", "bd": "#d4715f", "fg": "#f2b0a4"},
    "ready": {"bg": "#14263f", "bd": "#5b93d9", "fg": "#a8c9f0"},
    "needs_design": {"bg": "#241f3d", "bd": "#8b7ce0", "fg": "#c4b8f5"},
    "waiting": {"bg": "#21242b", "bd": "#4a515e", "fg": "#b6bdc9"},
    "superseded": {"bg": "#21242b", "bd": "#4a515e", "fg": "#8a919e"},
}
SURFACE = {
    "light": {"page": "#f6f7f9", "panel": "#ffffff", "line": "#e2e5ea", "ink": "#1f2430",
              "muted": "#6b7280", "link": "#3b6db5", "shadow": "rgba(31,36,48,.08)",
              "edge": "#c3c8d1", "edge-done": "#9ecbb1", "edge-critical": "#343b48"},
    "dark": {"page": "#14161a", "panel": "#1c1f25", "line": "#2c313a", "ink": "#e7eaf0",
             "muted": "#9aa3b2", "link": "#8fb4e8", "shadow": "rgba(0,0,0,.5)",
             "edge": "#464d59", "edge-done": "#4a7d5f", "edge-critical": "#d7dce5"},
}
STATUS_ORDER = list(PALETTE)
DEFAULT_TAG_STYLES = {"data": {"label": "DATA"}, "deploy": {"label": "DEPLOY"}}
# Bumped when the layout algorithm changes, so stale drag positions do not
# reinterpret themselves against a different grid.
LAYOUT_VERSION = "grid-v1"


class PlanSource(TypedDict):
    label: str
    href: str
    revision: str


class DeliveryPlan(TypedDict):
    scope: str
    outcomes: list[str]
    next_action: str
    sources: list[PlanSource]


def view_status(node: TicketNode, done: set[str]) -> str:
    """Derive the one display status for a ticket. First match wins."""
    raw = (node.get("status_raw") or "").strip().lower()
    if node["done"]:
        return "done"
    if "superseded" in raw:
        return "superseded"
    if "failed" in raw:
        return "failed"
    if node.get("in_progress") or re.search(r"in[ _-]?progress", raw):
        return "in_progress"
    if not node.get("execution_ready", True):
        return "needs_design"
    if all(dep in done for dep in node["deps"]):
        return "ready"
    return "waiting"


def compute_waves(nodes: list[TicketNode]) -> dict[str, int]:
    """Column per ticket: 1 + the deepest prerequisite chain below it."""
    ids = {node["id"] for node in nodes}
    deps = {node["id"]: [dep for dep in node["deps"] if dep in ids] for node in nodes}
    dependents: dict[str, list[str]] = {node_id: [] for node_id in ids}
    for node_id, prerequisites in deps.items():
        for prerequisite in prerequisites:
            dependents[prerequisite].append(node_id)
    waves = {node_id: 1 for node_id in ids}
    remaining = {node_id: len(prerequisites) for node_id, prerequisites in deps.items()}
    queue = sorted(node_id for node_id, count in remaining.items() if count == 0)
    while queue:
        node_id = queue.pop(0)
        for dependent in dependents[node_id]:
            waves[dependent] = max(waves[dependent], waves[node_id] + 1)
            remaining[dependent] -= 1
            if remaining[dependent] == 0:
                queue.append(dependent)
    return waves


def critical_path(nodes: list[TicketNode], statuses: dict[str, str], waves: dict[str, int]) -> list[str]:
    """Longest chain of remaining tickets, prerequisite first.

    Remaining excludes done and superseded: a failed or unready ticket is still
    work the chain must traverse. Length is counted in tickets, because tickets
    carry no duration estimate.
    """
    by_id = {node["id"]: node for node in nodes}
    depth: dict[str, int] = {}
    parent: dict[str, str | None] = {}
    for node_id in sorted(by_id, key=lambda node: (waves[node], node)):
        if statuses[node_id] in {"done", "superseded"}:
            continue
        best, best_dep = 1, None
        for prerequisite in by_id[node_id]["deps"]:
            if prerequisite in depth and depth[prerequisite] + 1 > best:
                best, best_dep = depth[prerequisite] + 1, prerequisite
        depth[node_id], parent[node_id] = best, best_dep
    if not depth:
        return []
    chain: list[str] = [min(sorted(depth), key=lambda node: (-depth[node], node))]
    while parent[chain[-1]]:
        chain.append(parent[chain[-1]])  # type: ignore[arg-type]
    chain.reverse()
    return chain


def critical_summary(nodes: list[TicketNode], statuses: dict[str, str], chain: list[str],
                     waves: dict[str, int]) -> str:
    wave_count = max(waves.values(), default=0)
    done_count = sum(1 for status in statuses.values() if status == "done")
    if not chain:
        return f"All {len(nodes)} tickets done · {wave_count} waves"
    return (f"Remaining critical path: {' → '.join(chain)} · {wave_count} waves · "
            f"{done_count}/{len(nodes)} done")


def palette_css() -> str:
    """Tokens plus the per-status rules, so the two can never disagree."""
    def tokens(surface: dict[str, str], colors: dict[str, dict[str, str]]) -> str:
        parts = [f"--{name}:{value};" for name, value in surface.items()]
        for status, color in colors.items():
            parts += [f"--{status}-bg:{color['bg']};", f"--{status}-bd:{color['bd']};",
                      f"--{status}-fg:{color['fg']};"]
        return "".join(parts)

    rules = "".join(
        f".node.{status}{{background:var(--{status}-bg);border-color:var(--{status}-bd);color:var(--{status}-fg);}}\n"
        f".ticket-card.{status}{{border-left-color:var(--{status}-bd);}}\n"
        f".ticket-card.{status} .card-status{{color:var(--{status}-fg);}}\n"
        for status in PALETTE
    )
    return (f"/* palette:start */\n"
            f":root{{color-scheme:light dark;{tokens(SURFACE['light'], PALETTE)}}}\n"
            f"@media (prefers-color-scheme: dark){{:root{{{tokens(SURFACE['dark'], DARK_PALETTE)}}}}}\n"
            f"/* palette:end */\n"
            f".node.superseded{{border-style:dashed;opacity:.55;}}\n"
            f"{rules}")


def legend_edges_html() -> str:
    samples = (("critical", "Critical path"), ("satisfied", "Prerequisite done"),
               ("dependency", "Dependency"))
    return "".join(
        f'<span class="item"><svg class="edge-sample {kind}" viewBox="0 0 44 10" width="44" height="10" '
        f'aria-hidden="true"><path class="line" d="M0 5 H34"/><path class="head" d="M33 1.5 L42 5 L33 8.5 Z"/></svg>'
        f'{label}</span>'
        for kind, label in samples
    )


def safe_href(href: str) -> str:
    if urlsplit(href).scheme.lower() not in {"", "http", "https", "file"}:
        raise ValueError(f"Unsupported source link: {href}")
    return escape(href, quote=True)


def render_plan(plan: DeliveryPlan, nodes: list[TicketNode], statuses: dict[str, str],
                output_dir: Path) -> tuple[str, str]:
    """Render the reading view from the same nodes used by the graph."""
    anchors = {node["id"]: "ticket-" + node["id"] for node in nodes}

    def ticket_link(node_id: str) -> str:
        return f'<a href="#{quote(anchors[node_id], safe="")}">{escape(node_id)}</a>'

    def ticket_list(selected: list[TicketNode]) -> str:
        if not selected:
            return "<p>None.</p>"
        return "<ul>" + "".join(
            f'<li>{ticket_link(node["id"])} — {escape(node["title"])}</li>' for node in selected
        ) + "</ul>"

    ready = [node for node in nodes if statuses[node["id"]] == "ready"]
    design = [node for node in nodes if node.get("ticket_type") == "design"
              and not node["done"] and node.get("status_raw") != "superseded"]
    done_count = sum(1 for status in statuses.values() if status == "done")
    outcomes = "".join(f"<li>{escape(outcome)}</li>" for outcome in plan["outcomes"])
    overview = f'''<main id="delivery-plan">
<header><p class="eyebrow">Delivery plan · {date.today().isoformat()}</p>
<p class="plan-counts">{len(nodes)} tickets · {len(ready)} ready · {len(design)} design blockers · {done_count} complete</p>
<nav aria-label="Plan sections"><a href="#scope">Scope</a> <a href="#ready">Ready work</a>
<a href="#design-blockers">Design blockers</a> <a href="#stage">DAG</a> <a href="#tickets">Tickets &amp; evidence</a></nav></header>
<section id="next-action"><h2>Next action</h2><p>{escape(plan["next_action"])}</p></section>
<section id="scope"><h2>Accepted scope</h2><p>{escape(plan["scope"])}</p>
<h3>Outcomes</h3><ul>{outcomes}</ul></section>
<div class="plan-grid"><section id="ready"><h2>Ready to implement</h2>{ticket_list(ready)}</section>
<section id="design-blockers"><h2>Design blockers</h2>{ticket_list(design)}</section></div>
<h2 id="dag-heading">Delivery dependencies</h2></main>'''
    cards: list[str] = []
    for node in nodes:
        status = statuses[node["id"]]
        details = "".join(
            f'<h4>{label}</h4><pre>{escape(node.get(key, ""))}</pre>'
            for key, label in (("inputs", "Inputs"), ("verification", "Verification / decision owner"),
                               ("blockers", "Blockers"), ("evidence", "Evidence")) if node.get(key)
        )
        source = node.get("source_file", "")
        source_link = ""
        if source:
            href = source if urlsplit(source).scheme else quote(os.path.relpath(Path(source).resolve(), output_dir))
            source_link = f'<a href="{safe_href(href)}">Canonical ticket</a>'
        dependencies = ", ".join(ticket_link(dep) for dep in node["deps"]) or "None"
        metadata = " · ".join(value for value in (node.get("ticket_type"), node.get("status_raw"), node.get("readiness")) if value)
        cards.append(f'''<article id="{escape(anchors[node["id"]])}" class="ticket-card {status}">
<h3>{escape(node["id"])} — {escape(node["title"])}</h3>
<p class="card-status">{PALETTE[status]["label"]} · {escape(metadata)}</p>
<p class="ticket-scope">{escape(node.get("scope", ""))}</p><p>Prerequisites: {dependencies}</p>
<details><summary>Checks, blockers &amp; evidence</summary>{details}
<p>{source_link}</p><code>{escape(node.get("source_revision") or "Revision unavailable — re-scan before review")}</code></details></article>''')
    sources = "".join(
        f'<li><a href="{safe_href(source["href"])}">{escape(source["label"])}</a> '
        f'<code>{escape(source["revision"])}</code></li>' for source in plan["sources"]
    )
    appendix = f'''<div class="plan-appendix"><section id="tickets"><h2>Tickets &amp; evidence</h2>{"".join(cards)}</section>
<footer><h2>Source artifacts</h2><ul>{sources}</ul>
<p>Generated reading view. Scope and decisions remain in the linked sources; ticket status and dependencies come from canonical tickets.</p></footer></div>'''
    return overview, appendix


def load_overlay(path):
    if not path:
        return {"extra_deps": {}, "tags": {}, "tag_styles": {}}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    data.setdefault("extra_deps", {})
    data.setdefault("tags", {})
    data.setdefault("tag_styles", {})
    return data


def merge(manifest, overlay):
    nodes = []
    for n in manifest["nodes"]:
        n = dict(n)
        n["deps"] = sorted(set(n["deps"]) | set(overlay["extra_deps"].get(n["id"], [])))
        n["tags"] = list(dict.fromkeys(n.get("tags", []) + overlay["tags"].get(n["id"], [])))
        nodes.append(n)
    validate_graph(nodes)
    return manifest["workstreams"], nodes


def render_mermaid(workstreams, nodes, title):
    done = {node["id"] for node in nodes if node["done"]}
    statuses = {node["id"]: view_status(node, done) for node in nodes}
    waves = compute_waves(nodes)
    chain = critical_path(nodes, statuses, waves)
    critical = set(zip(chain, chain[1:]))
    lines = [f"# {title}", "", f"Last updated: {date.today().isoformat()}", "", "```mermaid", "flowchart LR"]
    aliases = {node["id"]: f"n{index}" for index, node in enumerate(nodes)}
    by_row: dict[str, list] = {}
    for n in nodes:
        by_row.setdefault(n["row"], []).append(n)
    for row_index, ws in enumerate(workstreams):
        row_nodes = by_row.get(ws["key"], [])
        if not row_nodes:
            continue
        lines.append(f'    subgraph row{row_index}["{ws["label"]}"]')
        for n in row_nodes:
            label = n["title"].replace('"', "'")
            tagstr = (" " + " ".join(f"[{t}]" for t in n["tags"])) if n["tags"] else ""
            lines.append(f'        {aliases[n["id"]]}["{n["id"]} {label}{tagstr}"]')
        lines.append("    end")
    edge_index = 0
    critical_links: list[int] = []
    for n in nodes:
        for dependency in n["deps"]:
            lines.append(f"    {aliases[dependency]} --> {aliases[n['id']]}")
            if (dependency, n["id"]) in critical:
                critical_links.append(edge_index)
            edge_index += 1
    for status in STATUS_ORDER:
        members = [aliases[node_id] for node_id, value in statuses.items() if value == status]
        if not members:
            continue
        color = PALETTE[status]
        lines.append(f"    classDef {status} fill:{color['bg']},stroke:{color['bd']},color:{color['fg']};")
        lines.append(f"    class {','.join(members)} {status};")
    if critical_links:
        lines.append(f"    linkStyle {','.join(str(index) for index in critical_links)} "
                     f"stroke:{SURFACE['light']['edge-critical']},stroke-width:2.5px;")
    lines += ["```", "", critical_summary(nodes, statuses, chain, waves)]
    return "\n".join(lines)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generated" content="__GENERATED__">
<meta name="source-revision" content="__SOURCE_REVISION__">
<meta name="view-kind" content="living">
<title>__TITLE__</title>
<style>
__PALETTE_CSS__
*{box-sizing:border-box;}
body{margin:0;font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;background:var(--page);color:var(--ink);}
body:not(.delivery-plan){display:flex;flex-direction:column;min-height:100vh;}
#toolbar{position:sticky;top:0;z-index:20;background:var(--panel);border-bottom:1px solid var(--line);padding:10px 18px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
#toolbar h1{font-size:15px;margin:0;font-weight:600;}
#toolbar .sub{font-size:11px;color:var(--muted);}
button{font-size:11px;padding:5px 10px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:6px;cursor:pointer;margin-left:auto;}
button:hover{background:var(--page);}
#stage{position:relative;overflow:auto;}
body:not(.delivery-plan) #stage{flex:0 1 auto;min-height:180px;max-height:calc(100vh - 190px);}
.delivery-plan #stage{height:460px;min-height:280px;border-block:1px solid var(--line);background:var(--panel);}
#canvas{position:relative;}
svg#edges{position:absolute;top:0;left:0;pointer-events:none;overflow:visible;}
.edge{fill:none;stroke:var(--edge);stroke-width:1.2;}
.edge.satisfied{stroke:var(--edge-done);}
.edge.critical{stroke:var(--edge-critical);stroke-width:2.5;}
#arrow path{fill:var(--edge);}
#arrowDone path{fill:var(--edge-done);}
#arrowCritical path{fill:var(--edge-critical);}
.wave-head,.lane-label{position:absolute;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
.wave-head{font-weight:600;}
.column-rule{position:absolute;border-left:1px dashed var(--line);}
.lane-label{left:16px;width:138px;font-weight:600;color:var(--ink);text-transform:none;letter-spacing:0;font-size:12px;}
.lane-label .count{display:block;font-weight:400;color:var(--muted);font-size:11px;margin-top:2px;}
.node{position:absolute;width:190px;height:86px;border-radius:10px;border:1.5px solid;padding:8px 10px;
  cursor:grab;user-select:none;font-size:12px;line-height:1.3;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
  box-shadow:0 1px 2px var(--shadow);}
.node:active{cursor:grabbing;box-shadow:0 6px 16px var(--shadow);z-index:10;}
.node .nid{font-weight:700;font-size:10px;letter-spacing:.04em;opacity:.75;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.node .ntitle{margin-top:3px;max-width:100%;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.node .tags{margin-top:4px;display:flex;gap:4px;justify-content:center;flex-wrap:nowrap;overflow:hidden;max-width:100%;}
.tag{font-size:9px;font-weight:600;letter-spacing:.03em;padding:1px 6px;border-radius:9px;line-height:1.5;
  border:1px solid var(--line);color:var(--muted);background:transparent;white-space:nowrap;}
.node .agent{font-weight:600;font-size:9px;opacity:.75;margin-left:5px;}
#legend{background:var(--panel);border-top:1px solid var(--line);padding:14px 18px;font-size:12px;color:var(--ink);}
#legend h2{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 10px;font-weight:600;}
.legend-row{display:flex;gap:20px;flex-wrap:wrap;margin-bottom:9px;}
#legend .item{display:inline-flex;align-items:center;gap:7px;}
#legend .item svg{display:block;}
.swatch{width:14px;height:14px;border-radius:4px;border:1.5px solid;display:inline-block;}
.edge-sample .line{fill:none;stroke:var(--edge);stroke-width:1.2;}
.edge-sample.satisfied .line{stroke:var(--edge-done);}
.edge-sample.critical .line{stroke:var(--edge-critical);stroke-width:2.5;}
.edge-sample .head{fill:var(--edge);}
.edge-sample.satisfied .head{fill:var(--edge-done);}
.edge-sample.critical .head{fill:var(--edge-critical);}
.legend-summary{margin:0;color:var(--muted);font-size:12px;}
a{color:var(--link);overflow-wrap:anywhere;}
.node a{color:inherit;}
#delivery-plan,.plan-appendix{max-width:1120px;margin:auto;padding:24px;line-height:1.6;}
#delivery-plan h2,.plan-appendix h2{font-size:20px;margin:20px 0 8px;}
#delivery-plan h3,.ticket-card h3{font-size:16px;margin:8px 0;}
#delivery-plan p{white-space:pre-wrap;}
.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);}
.plan-counts{font-weight:600;}
nav{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;}
#next-action{padding:8px 20px;background:var(--panel);border:1px solid var(--line);border-radius:10px;}
.plan-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;}
.ticket-card{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--waiting-bd);border-radius:8px;padding:16px 20px;margin:12px 0;}
.ticket-card p{margin:6px 0;}
.card-status{font-weight:600;}
.ticket-scope,pre{white-space:pre-wrap;overflow-wrap:anywhere;}
pre{font:inherit;font-size:14px;}
code{font-size:12px;overflow-wrap:anywhere;}
summary{cursor:pointer;}
[id]{scroll-margin-top:110px;}
@media(max-width:640px){.plan-grid{grid-template-columns:1fr;}#delivery-plan,.plan-appendix{padding:16px;}}
</style>
</head>
<body class="__BODY_CLASS__">
<div id="toolbar">
  <h1>__TITLE__</h1>
  <span class="sub">__GENERATED__ &middot; __SOURCE_REVISION__ &middot; __WS_COUNT__ workstreams &middot; __NODE_COUNT__ tickets &middot; status from Markdown &middot; drag to rearrange</span>
  <button id="resetLayout">Reset layout</button>
</div>
__PLAN_OVERVIEW__
<div id="stage" role="region" aria-label="Dependency graph"><div id="canvas"><svg id="edges"></svg></div></div>
__PLAN_APPENDIX__
<footer id="legend">
  <h2>Legend</h2>
  <div class="legend-row" id="statusLegend"></div>
  <div class="legend-row">__LEGEND_EDGES__</div>
  <p class="legend-summary">__CRITICAL_SUMMARY__</p>
</footer>
<script>
const STORAGE_KEY = __STORAGE_KEY__;
const ROWS = __ROWS_JSON__;
const NODES = __NODES_JSON__;
const TAG_STYLES = __TAG_STYLES_JSON__;
const STATUS_META = __STATUS_META_JSON__;
__RENDER_JS__
</script>
</body>
</html>
"""

RENDER_JS = r"""
const LS_POS    = STORAGE_KEY + "_pos";

function loadJSON(key, fallback){
  try{ const v = JSON.parse(localStorage.getItem(key)); return v || fallback; }
  catch(e){ return fallback; }
}
let posOverride = loadJSON(LS_POS, {});

function esc(value){
  return String(value).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}

function computeStatus(){
  const done = new Set(NODES.filter(n=>n.done).map(n=>n.id));
  const status = {};
  NODES.forEach(n=>{
    const raw = String(n.status_raw||"").toLowerCase();
    if (n.done) status[n.id] = "done";
    else if (raw.indexOf("superseded") !== -1) status[n.id] = "superseded";
    else if (raw.indexOf("failed") !== -1) status[n.id] = "failed";
    else if (n.in_progress || /in[ _-]?progress/.test(raw)) status[n.id] = "in_progress";
    else if (!n.execution_ready) status[n.id] = "needs_design";
    else if (n.deps.every(d=>done.has(d))) status[n.id] = "ready";
    else status[n.id] = "waiting";
  });
  return status;
}

const NODE_W = 190, NODE_H = 86, COL_GAP = 68, LANE_GAP = 46, STACK_GAP = 18,
      LANE_TOP = 58, TOP_PAD = 14, LEFT_PAD = 172;

const LANES = ROWS.map((r,index)=>({...r, index}));
const LANE_OF = Object.fromEntries(LANES.map(l=>[l.key, l.index]));
const MAX_WAVE = NODES.reduce((m,n)=>Math.max(m, n.wave), 1);

// A lane's height is set by its busiest wave, so stacked cells never overlap.
function laneHeights(){
  return LANES.map(l=>{
    const counts = {};
    NODES.filter(n=>n.row===l.key).forEach(n=>{ counts[n.wave] = (counts[n.wave]||0) + 1; });
    const rows = Math.max(1, ...Object.values(counts));
    return rows * (NODE_H + STACK_GAP) - STACK_GAP;
  });
}
const LANE_H = laneHeights();
const LANE_TOP_AT = LANE_H.map((_,index)=>LANE_TOP + LANE_H.slice(0,index).reduce((a,b)=>a+b + LANE_GAP, 0));
function columnX(wave){ return LEFT_PAD + (wave-1) * (NODE_W + COL_GAP); }

function defaultLayout(){
  const pos = {};
  const used = {};
  NODES.forEach(n=>{
    const lane = LANE_OF[n.row] ?? 0;
    const cell = (n.row + "|" + n.wave);
    const slot = used[cell] || 0;
    used[cell] = slot + 1;
    pos[n.id] = {x: columnX(n.wave), y: LANE_TOP_AT[lane] + slot * (NODE_H + STACK_GAP)};
  });
  return pos;
}
const defaultPos = defaultLayout();
function currentPos(id){ return posOverride[id] || defaultPos[id]; }

const canvas = document.getElementById("canvas");
const svg = document.getElementById("edges");

function totalSize(){
  let maxX = LEFT_PAD + MAX_WAVE * (NODE_W + COL_GAP), maxY = 0;
  NODES.forEach(n=>{
    const p = currentPos(n.id);
    maxX = Math.max(maxX, p.x + NODE_W + 40);
    maxY = Math.max(maxY, p.y + NODE_H + 40);
  });
  return {w:maxX, h:maxY};
}

function renderStatusLegend(status){
  const present = STATUS_META.order.filter(s=>Object.values(status).includes(s));
  document.getElementById("statusLegend").innerHTML = present.map(s=>{
    const meta = STATUS_META.labels[s];
    return `<span class="item"><span class="swatch" style="background:var(--${s}-bg);border-color:var(--${s}-bd)"></span>${esc(meta)}</span>`;
  }).join("");
}

function render(){
  const status = computeStatus();
  canvas.querySelectorAll(".node, .lane-label, .wave-head, .column-rule").forEach(el=>el.remove());

  for (let wave = 1; wave <= MAX_WAVE; wave++){
    const head = document.createElement("div");
    head.className = "wave-head";
    head.style.left = columnX(wave) + "px";
    head.style.top = TOP_PAD + "px";
    head.style.width = NODE_W + "px";
    head.style.textAlign = "center";
    head.textContent = "Wave " + wave;
    canvas.appendChild(head);
    if (wave > 1){
      const rule = document.createElement("div");
      rule.className = "column-rule";
      rule.style.left = (columnX(wave) - COL_GAP/2) + "px";
      rule.style.top = TOP_PAD + "px";
      rule.style.height = Math.max(...LANE_TOP_AT.map((top,i)=>top + LANE_H[i]), LANE_TOP) + "px";
      canvas.appendChild(rule);
    }
  }

  LANES.forEach((lane,index)=>{
    const members = NODES.filter(n=>n.row===lane.key);
    if (!members.length) return;
    const lbl = document.createElement("div");
    lbl.className = "lane-label";
    lbl.style.top = (LANE_TOP_AT[index] + NODE_H/2 - 14) + "px";
    lbl.innerHTML = esc(lane.label) + '<span class="count">' + esc(lane.note||"") +
      (lane.note ? " · " : "") + members.length + " tickets</span>";
    canvas.appendChild(lbl);
  });

  NODES.forEach(n=>{
    const p = currentPos(n.id);
    const el = document.createElement("div");
    el.className = "node " + status[n.id];
    el.style.left = p.x + "px";
    el.style.top = p.y + "px";
    el.dataset.id = n.id;
    const tags = (n.tags||[]).slice(0,3).map(t=>{
      const style = TAG_STYLES[t];
      return `<span class="tag">${esc((style && style.label) || t)}</span>`;
    }).join("");
    const shortId = n.id.indexOf("/") === -1 ? n.id : n.id.slice(n.id.lastIndexOf("/") + 1);
    const label = n.report_anchor
      ? `<a href="#${esc(encodeURIComponent(n.report_anchor))}" title="${esc(n.id)}">${esc(shortId)}</a>`
      : esc(shortId);
    el.innerHTML = '<div class="nid">'+label
      + (n.agent ? '<span class="agent">&#9881; '+esc(n.agent)+'</span>' : '')
      + '</div><div class="ntitle">'+esc(n.title)+'</div>'
      + (tags ? '<div class="tags">'+tags+'</div>' : '');
    el.title = n.id + " — " + STATUS_META.labels[status[n.id]] + "\n"
      + "Source: " + (n.source_file || "manifest") + "\n"
      + (n.source_revision || "Revision unavailable — re-scan before review") + "\n" + (n.status_raw || "")
      + (n.unresolved_dep_text ? "\nUnresolved: " + n.unresolved_dep_text : "");
    canvas.appendChild(el);
    attachDrag(el, n.id);
  });

  const size = totalSize();
  canvas.style.width = size.w + "px";
  canvas.style.height = size.h + "px";
  svg.setAttribute("width", size.w);
  svg.setAttribute("height", size.h);
  drawEdges(status);
  renderStatusLegend(status);
}

// Orthogonal elbow with rounded corners; falls back to a curve when the two
// nodes are too close or the target sits behind the source after a drag.
function elbowPath(x1,y1,x2,y2){
  const r = 9, dx = x2 - x1, dy = y2 - y1;
  if (Math.abs(dy) < 2) return `M ${x1} ${y1} H ${x2}`;
  if (dx < 3*r) return `M ${x1} ${y1} C ${x1 + 40} ${y1}, ${x2 - 40} ${y2}, ${x2} ${y2}`;
  const mx = x1 + dx/2, sy = dy > 0 ? 1 : -1;
  return `M ${x1} ${y1} H ${mx - r} Q ${mx} ${y1} ${mx} ${y1 + sy*r} V ${y2 - sy*r} Q ${mx} ${y2} ${mx + r} ${y2} H ${x2}`;
}

function drawEdges(status){
  svg.innerHTML = '<defs>'
    + '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>'
    + '<marker id="arrowDone" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>'
    + '<marker id="arrowCritical" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>'
    + '</defs>';
  const draw = (n, dep, critical) => {
    const fromP = currentPos(dep), toP = currentPos(n.id);
    if (!fromP || !toP) return;
    const satisfied = status[dep] === "done";
    const path = document.createElementNS("http://www.w3.org/2000/svg","path");
    path.setAttribute("d", elbowPath(fromP.x + NODE_W, fromP.y + NODE_H/2, toP.x, toP.y + NODE_H/2));
    path.setAttribute("class", "edge" + (critical ? " critical" : (satisfied ? " satisfied" : "")));
    path.setAttribute("marker-end", critical ? "url(#arrowCritical)" : (satisfied ? "url(#arrowDone)" : "url(#arrow)"));
    svg.appendChild(path);
  };
  NODES.forEach(n=>{
    (n.deps||[]).filter(dep=>(n.critical_deps||[]).indexOf(dep) === -1).forEach(dep=>draw(n, dep, false));
  });
  NODES.forEach(n=>{
    (n.critical_deps||[]).forEach(dep=>draw(n, dep, true));
  });
}

function attachDrag(el, id){
  let sx, sy, ox, oy, dragging=false;
  el.addEventListener("mousedown", (ev)=>{
    if (ev.target.closest("a")) return;
    dragging = true;
    el.dataset.dragged = "0";
    sx = ev.clientX; sy = ev.clientY;
    const p = currentPos(id);
    ox = p.x; oy = p.y;
    ev.preventDefault();
  });
  window.addEventListener("mousemove", (ev)=>{
    if (!dragging) return;
    const dx = ev.clientX - sx, dy = ev.clientY - sy;
    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) el.dataset.dragged = "1";
    const nx = Math.max(0, ox + dx), ny = Math.max(0, oy + dy);
    posOverride[id] = {x:nx, y:ny};
    el.style.left = nx + "px";
    el.style.top = ny + "px";
    drawEdges(computeStatus());
    const size = totalSize();
    canvas.style.width = size.w + "px";
    canvas.style.height = size.h + "px";
    svg.setAttribute("width", size.w);
    svg.setAttribute("height", size.h);
  });
  window.addEventListener("mouseup", ()=>{
    if (!dragging) return;
    dragging = false;
    if (el.dataset.dragged === "1") {
      localStorage.setItem(LS_POS, JSON.stringify(posOverride));
    }
  });
}

document.getElementById("resetLayout").addEventListener("click", ()=>{
  posOverride = {};
  localStorage.removeItem(LS_POS);
  render();
});
render();
"""


def repository_revision(directory: Path) -> str:
    """Short HEAD of the repository holding the output; "untracked" outside git."""
    result = subprocess.run(["git", "-C", str(directory), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "untracked"


def display_tags(node: TicketNode) -> list[str]:
    """Node pills, minus the scanner's own type/readiness/status triple.

    Those three are already carried by the node colour and stated in full in the
    tooltip, so repeating them as pills only costs width. Overlay tags such as
    `data` or `deploy` say something the colour does not, and stay.
    """
    derived = {node.get("ticket_type"), node.get("readiness"), node.get("status_raw")}
    return [tag for tag in node["tags"] if tag not in derived]


def render_html(workstreams, nodes, title, storage_key, tag_styles_all,
                plan: DeliveryPlan | None = None, output_dir: Path = Path("."),
                *, generated: str, source_revision: str):
    done = {node["id"] for node in nodes if node["done"]}
    statuses = {node["id"]: view_status(node, done) for node in nodes}
    waves = compute_waves(nodes)
    chain = critical_path(nodes, statuses, waves)
    critical_edges = set(zip(chain, chain[1:]))
    shown_tags = {node["id"]: display_tags(node) for node in nodes}
    rows_json = json.dumps(
        [{"key": w["key"], "label": w["label"], "note": w.get("note", "")} for w in workstreams],
        ensure_ascii=False,
    )
    nodes_json = json.dumps(
        [
            {
                "id": n["id"],
                "row": n["row"],
                "title": n["title"],
                "deps": n["deps"],
                "done": n["done"],
                "in_progress": n.get("in_progress", False),
                "execution_ready": n.get("execution_ready", True),
                "unresolved_dep_text": n.get("unresolved_dep_text", ""),
                "status_raw": n.get("status_raw", ""),
                "source_file": n.get("source_file", ""),
                "source_revision": n.get("source_revision", ""),
                "agent": n.get("agent", ""),
                "tags": shown_tags[n["id"]],
                "wave": waves[n["id"]],
                "critical_deps": [d for d in n["deps"] if (d, n["id"]) in critical_edges],
                "view_status": statuses[n["id"]],
                "report_anchor": "ticket-" + n["id"] if plan else "",
            }
            for n in nodes
        ],
        ensure_ascii=False,
    )
    status_meta = {"order": STATUS_ORDER, "labels": {k: v["label"] for k, v in PALETTE.items()}}
    used_tags = {tag for tags in shown_tags.values() for tag in tags}
    tag_styles = {k: v for k, v in tag_styles_all.items() if k in used_tags}
    html = HTML_TEMPLATE
    html = html.replace("__PALETTE_CSS__", palette_css())
    html = html.replace("__TITLE__", escape(title))
    html = html.replace("__GENERATED__", generated)
    html = html.replace("__SOURCE_REVISION__", escape(source_revision))
    html = html.replace("__WS_COUNT__", str(len(workstreams)))
    html = html.replace("__NODE_COUNT__", str(len(nodes)))
    html = html.replace("__LEGEND_EDGES__", legend_edges_html())
    html = html.replace("__CRITICAL_SUMMARY__", escape(critical_summary(nodes, statuses, chain, waves)))
    html = html.replace("__STORAGE_KEY__", json.dumps(f"{storage_key}_{LAYOUT_VERSION}").replace("<", "\\u003c"))
    html = html.replace("__ROWS_JSON__", rows_json.replace("<", "\\u003c"))
    html = html.replace("__NODES_JSON__", nodes_json.replace("<", "\\u003c"))
    html = html.replace("__STATUS_META_JSON__", json.dumps(status_meta, ensure_ascii=False).replace("<", "\\u003c"))
    html = html.replace("__TAG_STYLES_JSON__", json.dumps(tag_styles, ensure_ascii=False).replace("<", "\\u003c"))
    html = html.replace("__RENDER_JS__", RENDER_JS)
    overview, appendix = render_plan(plan, nodes, statuses, output_dir) if plan else ("", "")
    html = html.replace("__BODY_CLASS__", "delivery-plan" if plan else "")
    html = html.replace("__PLAN_OVERVIEW__", overview)
    html = html.replace("__PLAN_APPENDIX__", appendix)
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--overlay", type=Path, default=None)
    ap.add_argument("--plan", type=Path, help="Derived scope, outcomes, next action, and sources JSON for an HTML delivery plan")
    ap.add_argument("--format", choices=["html", "mermaid"], default="html")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--title", default="Portfolio DAG")
    ap.add_argument(
        "--storage-key",
        default=None,
        help="localStorage key prefix for HTML output (default: derived from output filename)",
    )
    ap.add_argument(
        "--source-revision",
        default=None,
        help="Revision shown in the header and <meta name=\"source-revision\"> (default: git HEAD of the output directory)",
    )
    args = ap.parse_args()
    if args.plan and args.format != "html":
        ap.error("--plan requires --format html")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    overlay = load_overlay(args.overlay)
    tag_styles_all = {**DEFAULT_TAG_STYLES, **overlay.get("tag_styles", {})}
    workstreams, nodes = merge(manifest, overlay)

    if args.format == "mermaid":
        out = render_mermaid(workstreams, nodes, args.title)
    else:
        storage_key = args.storage_key or ("dag_" + args.out.stem)
        plan = json.loads(args.plan.read_text(encoding="utf-8")) if args.plan else None
        output_dir = args.out.resolve().parent
        source_revision = args.source_revision or repository_revision(output_dir)
        out = render_html(workstreams, nodes, args.title, storage_key, tag_styles_all, plan, output_dir,
                          generated=date.today().isoformat(), source_revision=source_revision)

    args.out.write_text(out, encoding="utf-8")
    print(f"Wrote {args.format} DAG ({len(nodes)} nodes, {len(workstreams)} workstreams) -> {args.out}")


if __name__ == "__main__":
    main()
