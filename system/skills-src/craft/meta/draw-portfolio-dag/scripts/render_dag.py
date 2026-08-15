#!/usr/bin/env python3
"""Render a portfolio DAG manifest (from scan_specs.py) into HTML or Mermaid.

Usage:
    python3 render_dag.py manifest.json --overlay overlay.json --format html -o dag.html
    python3 render_dag.py manifest.json --overlay overlay.json --format mermaid -o dag.md

The overlay file supplies anything the mechanical scan cannot infer:
  - extra_deps:  {node_id: [dep_id, ...]}   merged with scanned deps
  - tags:        {node_id: ["data", "deploy", ...]}  arbitrary small labels
  - tag_styles:  {tag_key: {"label": "DATA", "bg": "#5b21b6", "fg": "#fff"}}
It is optional — omit --overlay to render the mechanically-scanned graph as-is.
"""
import argparse
import json
from pathlib import Path

DEFAULT_TAG_STYLES = {
    "data": {"label": "DATA", "bg": "#5b21b6", "fg": "#fff"},
    "deploy": {"label": "DEPLOY", "bg": "#b45309", "fg": "#fff"},
}


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
        n["tags"] = overlay["tags"].get(n["id"], [])
        nodes.append(n)
    return manifest["workstreams"], nodes


def render_mermaid(workstreams, nodes, title):
    tag_styles = {}  # unused in mermaid output; kept for signature symmetry
    lines = [f"# {title}", "", "```mermaid", "flowchart TB"]
    by_row = {}
    for n in nodes:
        by_row.setdefault(n["row"], []).append(n)
    for ws in workstreams:
        rn = by_row.get(ws["key"], [])
        if not rn:
            continue
        lines.append(f"    subgraph {ws['key']}[\"{ws['label']}\"]")
        for n in rn:
            label = n["title"].replace('"', "'")
            tagstr = (" " + " ".join(f"[{t}]" for t in n["tags"])) if n["tags"] else ""
            lines.append(f'        {n["id"]}["{n["id"]} {label}{tagstr}"]')
        lines.append("    end")
    for n in nodes:
        for d in n["deps"]:
            lines.append(f"    {d} --> {n['id']}")
    done_ids = [n["id"] for n in nodes if n["done"]]
    if done_ids:
        lines.append(f"    classDef done fill:#d1e7dd,stroke:#0f5132,color:#111;")
        lines.append(f"    class {','.join(done_ids)} done;")
    lines.append("```")
    return "\n".join(lines)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--done-bg:#d1e7dd;--done-bd:#0f5132;--frontier-bg:#ffe3c2;--frontier-bd:#c2540c;--todo-bg:#dbeafe;--todo-bd:#1d4ed8;}
*{box-sizing:border-box;}
body{margin:0;font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;background:#f4f5f7;color:#111;}
#toolbar{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid #d8dbe0;padding:10px 16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
#toolbar h1{font-size:15px;margin:0;font-weight:600;}
#toolbar .sub{font-size:11px;color:#666;}
.legend{display:flex;gap:10px;font-size:11px;align-items:center;}
.swatch{width:12px;height:12px;border-radius:3px;display:inline-block;margin-right:4px;vertical-align:-1px;}
button{font-size:11px;padding:5px 10px;border:1px solid #c7cad1;background:#fff;border-radius:6px;cursor:pointer;}
button:hover{background:#f0f1f3;}
#stage{position:relative;overflow:auto;height:calc(100vh - 54px);}
#canvas{position:relative;}
svg#edges{position:absolute;top:0;left:0;pointer-events:none;overflow:visible;}
.row-label{position:absolute;left:14px;font-size:12px;font-weight:600;color:#444;}
.row-label .count{font-weight:400;color:#888;margin-left:6px;font-size:11px;}
.node{position:absolute;width:190px;min-height:60px;border-radius:8px;padding:7px 9px 8px;
  border:2px solid;cursor:grab;user-select:none;font-size:12px;line-height:1.32;
  box-shadow:0 1px 2px rgba(0,0,0,.08);}
.node:active{cursor:grabbing;box-shadow:0 5px 14px rgba(0,0,0,.2);z-index:10;}
.node .nid{font-weight:700;font-size:10px;letter-spacing:.03em;opacity:.6;}
.node .ntitle{margin-top:2px;}
.node .tags{margin-top:4px;display:flex;gap:4px;flex-wrap:wrap;}
.tag{font-size:9px;font-weight:700;letter-spacing:.02em;padding:1px 5px;border-radius:8px;line-height:1.4;}
.node.done{background:var(--done-bg);border-color:var(--done-bd);}
.node.frontier{background:var(--frontier-bg);border-color:var(--frontier-bd);}
.node.todo{background:var(--todo-bg);border-color:var(--todo-bd);}
</style>
</head>
<body>
<div id="toolbar">
  <h1>__TITLE__</h1>
  <span class="sub">__WS_COUNT__ workstreams &middot; __NODE_COUNT__ tickets &middot; status from Markdown &middot; drag to rearrange</span>
  <div class="legend">
    <span><span class="swatch" style="background:var(--done-bg);border:1px solid var(--done-bd)"></span>Finished</span>
    <span><span class="swatch" style="background:var(--frontier-bg);border:1px solid var(--frontier-bd)"></span>Frontier (ready now)</span>
    <span><span class="swatch" style="background:var(--todo-bg);border:1px solid var(--todo-bd)"></span>Todo (blocked)</span>
  </div>
  <div class="legend" id="tagLegend"></div>
  <button id="resetLayout">Reset layout</button>
</div>
<div id="stage"><div id="canvas"><svg id="edges"></svg></div></div>
<script>
const STORAGE_KEY = __STORAGE_KEY__;
const ROWS = __ROWS_JSON__;
const NODES = __NODES_JSON__;
const TAG_STYLES = __TAG_STYLES_JSON__;
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

function isDone(node){
  return !!node.done;
}

function computeStatus(){
  const doneSet = new Set(NODES.filter(isDone).map(n=>n.id));
  const status = {};
  NODES.forEach(n=>{
    if (doneSet.has(n.id)) { status[n.id]="done"; return; }
    const ready = n.deps.every(d=>doneSet.has(d));
    status[n.id] = ready ? "frontier" : "todo";
  });
  return status;
}

const NODE_W = 190, NODE_H = 62, COL_GAP = 40, ROW_GAP = 100, ROW_HEAD = 40, LEFT_PAD = 150, TOP_PAD = 16;

function defaultLayout(){
  const pos = {};
  let y = TOP_PAD;
  ROWS.forEach(r=>{
    const rowNodes = NODES.filter(n=>n.row===r.key);
    let x = LEFT_PAD;
    rowNodes.forEach(n=>{
      pos[n.id] = {x, y: y + ROW_HEAD};
      x += NODE_W + COL_GAP;
    });
    y += ROW_HEAD + NODE_H + ROW_GAP;
  });
  return pos;
}
const defaultPos = defaultLayout();
function currentPos(id){ return posOverride[id] || defaultPos[id]; }

const canvas = document.getElementById("canvas");
const svg = document.getElementById("edges");

function totalSize(){
  let maxX=0, maxY=0;
  NODES.forEach(n=>{
    const p = currentPos(n.id);
    maxX = Math.max(maxX, p.x + NODE_W + 40);
    maxY = Math.max(maxY, p.y + NODE_H + 40);
  });
  return {w:maxX, h:maxY};
}

function renderTagLegend(){
  const el = document.getElementById("tagLegend");
  el.innerHTML = Object.keys(TAG_STYLES).map(k=>{
    const s = TAG_STYLES[k];
    return `<span><span class="tag" style="background:${s.bg};color:${s.fg};position:static;">${s.label}</span></span>`;
  }).join("");
}

function render(){
  const status = computeStatus();
  canvas.querySelectorAll(".node, .row-label").forEach(el=>el.remove());

  let y = TOP_PAD;
  ROWS.forEach(r=>{
    const lbl = document.createElement("div");
    lbl.className = "row-label";
    const count = NODES.filter(n=>n.row===r.key).length;
    lbl.style.top = (y + 8) + "px";
    lbl.innerHTML = r.label + ' <span class="count">' + (r.note||"") + " &middot; " + count + " tickets</span>";
    canvas.appendChild(lbl);
    y += ROW_HEAD + NODE_H + ROW_GAP;
  });

  NODES.forEach(n=>{
    const p = currentPos(n.id);
    const el = document.createElement("div");
    el.className = "node " + status[n.id];
    el.style.left = p.x + "px";
    el.style.top = p.y + "px";
    el.style.width = NODE_W + "px";
    el.dataset.id = n.id;
    const tags = (n.tags||[]).map(t=>{
      const s = TAG_STYLES[t] || {label:t, bg:"#666", fg:"#fff"};
      return `<span class="tag" style="background:${s.bg};color:${s.fg};">${s.label}</span>`;
    }).join("");
    el.innerHTML = '<div class="nid">'+n.id+'</div><div class="ntitle">'+n.title+'</div>'
      + (tags ? '<div class="tags">'+tags+'</div>' : '');
    el.title = "Status comes from Markdown. Drag to move.";
    canvas.appendChild(el);
    attachDrag(el, n.id);
  });

  const size = totalSize();
  canvas.style.width = size.w + "px";
  canvas.style.height = size.h + "px";
  svg.setAttribute("width", size.w);
  svg.setAttribute("height", size.h);
  drawEdges(status);
}

function drawEdges(status){
  svg.innerHTML = '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa1ab"/></marker></defs>';
  NODES.forEach(n=>{
    const toP = currentPos(n.id);
    n.deps.forEach(dep=>{
      const fromP = currentPos(dep);
      if (!fromP) return;
      const x1 = fromP.x + NODE_W/2, y1 = fromP.y + NODE_H;
      const x2 = toP.x + NODE_W/2, y2 = toP.y;
      let d;
      if (Math.abs(y2-y1) < 4 && x2 < x1) {
        d = `M ${fromP.x+NODE_W} ${fromP.y+NODE_H/2} C ${fromP.x+NODE_W+40} ${fromP.y+NODE_H/2}, ${toP.x-40} ${toP.y+NODE_H/2}, ${toP.x} ${toP.y+NODE_H/2}`;
      } else {
        const midY = (y1+y2)/2;
        d = `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;
      }
      const path = document.createElementNS("http://www.w3.org/2000/svg","path");
      path.setAttribute("d", d);
      path.setAttribute("fill","none");
      path.setAttribute("stroke", status[dep]==="done" ? "#8fbfa4" : "#c3c8d1");
      path.setAttribute("stroke-width","1.6");
      path.setAttribute("marker-end","url(#arrow)");
      svg.appendChild(path);
    });
  });
}

function attachDrag(el, id){
  let sx, sy, ox, oy, dragging=false;
  el.addEventListener("mousedown", (ev)=>{
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
renderTagLegend();
render();
"""


def render_html(workstreams, nodes, title, storage_key, tag_styles_all):
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
                "tags": n["tags"],
            }
            for n in nodes
        ],
        ensure_ascii=False,
    )
    used_tags = {t for n in nodes for t in n["tags"]}
    tag_styles = {k: v for k, v in tag_styles_all.items() if k in used_tags}
    html = HTML_TEMPLATE
    html = html.replace("__TITLE__", title)
    html = html.replace("__WS_COUNT__", str(len(workstreams)))
    html = html.replace("__NODE_COUNT__", str(len(nodes)))
    html = html.replace("__STORAGE_KEY__", json.dumps(storage_key))
    html = html.replace("__ROWS_JSON__", rows_json)
    html = html.replace("__NODES_JSON__", nodes_json)
    html = html.replace("__TAG_STYLES_JSON__", json.dumps(tag_styles, ensure_ascii=False))
    html = html.replace("__RENDER_JS__", RENDER_JS)
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--overlay", type=Path, default=None)
    ap.add_argument("--format", choices=["html", "mermaid"], default="html")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--title", default="Portfolio DAG")
    ap.add_argument(
        "--storage-key",
        default=None,
        help="localStorage key prefix for HTML output (default: derived from output filename)",
    )
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    overlay = load_overlay(args.overlay)
    tag_styles_all = {**DEFAULT_TAG_STYLES, **overlay.get("tag_styles", {})}
    workstreams, nodes = merge(manifest, overlay)

    if args.format == "mermaid":
        out = render_mermaid(workstreams, nodes, args.title)
    else:
        storage_key = args.storage_key or ("dag_" + args.out.stem)
        out = render_html(workstreams, nodes, args.title, storage_key, tag_styles_all)

    args.out.write_text(out, encoding="utf-8")
    print(f"Wrote {args.format} DAG ({len(nodes)} nodes, {len(workstreams)} workstreams) -> {args.out}")


if __name__ == "__main__":
    main()
