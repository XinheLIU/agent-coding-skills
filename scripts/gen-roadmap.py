#!/usr/bin/env python3
"""
gen-roadmap.py  Generate a self-contained roadmap.html from specs/ and tasks/.

Usage:
    python3 scripts/gen-roadmap.py <effort-dir> [output.html]

Reads <effort-dir>/specs/*.md and <effort-dir>/tasks/*.md.
Output defaults to <effort-dir>/roadmap.html.
"""
import sys
import json
import re
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    yaml_block = text[4:end].strip()
    body = text[end + 4:].strip()
    return _parse_simple_yaml(yaml_block), body


def _parse_simple_yaml(yaml_text: str) -> dict:
    result: dict = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest in ("~", "null", "Null", "NULL", ""):
            result[key] = None
        elif rest in ("true", "True"):
            result[key] = True
        elif rest in ("false", "False"):
            result[key] = False
        elif rest.startswith("["):
            inner = rest.strip("[]")
            result[key] = (
                [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
                if inner.strip() else []
            )
        else:
            result[key] = rest.strip('"').strip("'")
    return result


def load_specs(specs_dir: Path) -> list[dict]:
    if not specs_dir.exists():
        return []
    specs = []
    for path in sorted(specs_dir.glob("*.md")):
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        fm.setdefault("id", path.stem)
        fm.setdefault("title", path.stem)
        fm.setdefault("state", "in-progress")
        fm.setdefault("topology", "workflow")
        fm["_body"] = body
        fm["_file"] = path.name
        specs.append(fm)
    return specs


def load_tasks(tasks_dir: Path) -> dict[str, dict]:
    tasks: dict[str, dict] = {}
    if not tasks_dir.exists():
        return tasks
    for path in sorted(tasks_dir.glob("*.md")):
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm.get("id"):
            m = re.match(r"^(\d+)", path.stem)
            fm["id"] = m.group(1) if m else path.stem
        fm.setdefault("title", path.stem)
        fm.setdefault("depends_on", [])
        fm.setdefault("type", "agent")
        fm.setdefault("state", "backlog")
        fm.setdefault("spec", None)
        fm.setdefault("claimed_by", None)
        fm.setdefault("verify", "")
        fm["_body"] = body
        fm["_file"] = path.name
        tasks[fm["id"]] = fm
    return tasks


def _topo_sort(ids: list[str], deps: dict[str, list[str]]) -> list[str]:
    id_set = set(ids)
    visited: set[str] = set()
    order: list[str] = []

    def visit(tid: str) -> None:
        if tid in visited:
            return
        visited.add(tid)
        for d in deps.get(tid, []):
            if d in id_set:
                visit(d)
        order.append(tid)

    for tid in ids:
        visit(tid)
    return order


def _assign_columns(ids: list[str], deps: dict[str, list[str]]) -> dict[str, int]:
    id_set = set(ids)
    col: dict[str, int] = {}

    def depth(tid: str) -> int:
        if tid in col:
            return col[tid]
        inner = [d for d in deps.get(tid, []) if d in id_set]
        col[tid] = (max(depth(d) for d in inner) + 1) if inner else 0
        return col[tid]

    for tid in ids:
        depth(tid)
    return col


def _is_workflow(ids: list[str], deps: dict[str, list[str]]) -> bool:
    id_set = set(ids)
    return all(sum(1 for d in deps.get(t, []) if d in id_set) <= 1 for t in ids)


def build_data(effort_dir: Path) -> dict:
    specs = load_specs(effort_dir / "specs")
    tasks = load_tasks(effort_dir / "tasks")

    task_ids_set = set(tasks)
    deps = {tid: [d for d in t["depends_on"] if d in task_ids_set] for tid, t in tasks.items()}

    spec_task_map: dict[str, list[str]] = {s["id"]: [] for s in specs}
    standalone: list[str] = []
    for tid, t in tasks.items():
        sid = t.get("spec")
        if sid and sid in spec_task_map:
            spec_task_map[sid].append(tid)
        else:
            standalone.append(tid)

    lanes = []
    for spec in specs:
        sid = spec["id"]
        stids = sorted(spec_task_map[sid], key=lambda x: x.zfill(10))
        topology = spec.get("topology", "workflow")
        if topology == "dag" and _is_workflow(stids, deps):
            topology = "workflow"

        ordered = _topo_sort(stids, deps)
        if topology == "workflow":
            layout = {tid: {"col": i, "row": 0} for i, tid in enumerate(ordered)}
            cols, rows = len(ordered), 1
        else:
            col_map = _assign_columns(stids, deps)
            row_ctr: dict[int, int] = {}
            layout = {}
            for tid in ordered:
                c = col_map.get(tid, 0)
                r = row_ctr.get(c, 0)
                layout[tid] = {"col": c, "row": r}
                row_ctr[c] = r + 1
            cols = max((v["col"] for v in layout.values()), default=0) + 1
            rows = max((v["row"] for v in layout.values()), default=0) + 1

        lanes.append({
            "spec": spec, "task_ids": stids, "topology": topology,
            "layout": layout, "cols": cols, "rows": rows,
        })

    if standalone:
        sa = sorted(standalone, key=lambda x: x.zfill(10))
        lanes.append({
            "spec": {"id": "__standalone__", "title": "Standalone tasks",
                     "state": "", "topology": "workflow", "_body": "", "_file": ""},
            "task_ids": sa, "topology": "workflow",
            "layout": {tid: {"col": i, "row": 0} for i, tid in enumerate(sa)},
            "cols": len(sa), "rows": 1,
        })

    cross_edges = [
        {"from": dep, "to": tid}
        for tid, t in tasks.items()
        for dep in deps.get(tid, [])
        if tasks[dep].get("spec") != t.get("spec")
    ]
    return {"lanes": lanes, "tasks": tasks, "cross_edges": cross_edges}


# ---------------------------------------------------------------------------
# HTML template — self-contained, no external deps
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Roadmap</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:#0f172a;color:#e2e8f0;min-height:100vh}
#app{padding:24px;max-width:calc(100vw - 360px);overflow-x:hidden}
h1{font-size:1.3rem;font-weight:600;color:#f8fafc;margin-bottom:14px}
.legend{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:22px}
.legend-item{display:flex;align-items:center;gap:5px;font-size:.73rem;color:#94a3b8}
.legend-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.lane{background:#1e293b;border:1px solid #334155;border-radius:10px;margin-bottom:18px}
.lane-header{display:flex;align-items:center;gap:10px;padding:10px 16px;
  border-bottom:1px solid #334155;background:#0f172a;border-radius:10px 10px 0 0;
  cursor:pointer;user-select:none}
.lane-header:hover{background:#1a2538}
.lane-title{font-size:.9rem;font-weight:600;color:#f1f5f9}
.lane-state{font-size:.68rem;padding:2px 8px;border-radius:10px;
  background:#334155;color:#94a3b8;text-transform:uppercase;letter-spacing:.04em}
.lane-topo{font-size:.68rem;color:#475569;margin-left:auto}
.lane-body{overflow-x:auto;padding:14px}
.lane-body svg{display:block}
#panel{position:fixed;top:0;right:0;width:340px;height:100vh;background:#1e293b;
  border-left:1px solid #334155;transform:translateX(100%);
  transition:transform .2s ease;overflow-y:auto;z-index:100}
#panel.open{transform:translateX(0)}
.pi{padding:20px}
.pc{background:none;border:none;color:#94a3b8;cursor:pointer;font-size:1.1rem;
  float:right;padding:0;line-height:1}
.pc:hover{color:#f1f5f9}
.pt{font-size:1rem;font-weight:600;color:#f1f5f9;margin:4px 0 14px;clear:right}
.pr{display:flex;gap:8px;margin-bottom:7px;font-size:.78rem}
.pl{color:#64748b;flex-shrink:0;width:78px}
.pv{color:#e2e8f0;word-break:break-all}
.pb{margin-top:14px;padding-top:14px;border-top:1px solid #334155;
  font-size:.78rem;color:#94a3b8;white-space:pre-wrap;line-height:1.6}
.pf{font-size:.68rem;color:#475569;margin-top:10px}
</style>
</head>
<body>
<div id="app">
  <h1>Roadmap</h1>
  <div class="legend" id="legend"></div>
  <div id="lanes"></div>
</div>
<svg id="ov" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:5;overflow:visible"></svg>
<div id="panel"><div class="pi">
  <button class="pc" onclick="closePanel()">&#x2715;</button>
  <div class="pt" id="pt"></div>
  <div id="pf"></div>
  <div class="pb" id="pb"></div>
  <div class="pf" id="pfile"></div>
</div></div>
<script>
const DATA = __DATA_JSON__;
const SC = {backlog:'#6b7280',ready:'#3b82f6',claimed:'#f59e0b',
  'in-progress':'#f59e0b',blocked:'#ef4444',review:'#a855f7',
  done:'#22c55e',abandoned:'#374151'};
const SSC = {backlog:'#475569','in-progress':'#3b82f6',done:'#22c55e'};
const NW=144,NH=44,HG=52,VG=24,PAD=16;
const nx=c=>PAD+c*(NW+HG), ny=r=>PAD+r*(NH+VG);
const sw=c=>PAD*2+c*NW+Math.max(0,c-1)*HG;
const sh=r=>PAD*2+r*NH+Math.max(0,r-1)*VG;
const NP={};
function svgEl(t,a){
  const e=document.createElementNS('http://www.w3.org/2000/svg',t);
  Object.entries(a).forEach(([k,v])=>e.setAttribute(k,v));return e;}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function drawArrow(svg,x1,y1,x2,y2,dash){
  const id='m'+Math.random().toString(36).slice(2);
  const def=svgEl('defs',{});
  const mk=svgEl('marker',{id,markerWidth:'8',markerHeight:'6',refX:'7',refY:'3',orient:'auto'});
  mk.appendChild(svgEl('polygon',{points:'0 0,8 3,0 6',fill:dash?'#475569':'#475569'}));
  def.appendChild(mk);svg.insertBefore(def,svg.firstChild);
  const cx=(x1+x2)/2;
  svg.appendChild(svgEl('path',{
    d:`M${x1},${y1} C${cx},${y1} ${cx},${y2} ${x2},${y2}`,
    stroke:dash?'#475569':'#2d3f55','stroke-width':'1.5',
    fill:'none','stroke-dasharray':dash?'5,3':'none',
    'marker-end':`url(#${id})`}));}
function renderNode(svg,task,x,y){
  const col=SC[task.state]||'#6b7280';
  const rx=task.type==='human'?'3':'10';
  const r=svgEl('rect',{x,y,width:NW,height:NH,rx,fill:'#1e293b',
    stroke:col,'stroke-width':'1.5',style:'cursor:pointer'});
  const bar=svgEl('rect',{x,y:y+8,width:'3',height:NH-16,rx:'2',fill:col});
  const id=svgEl('text',{x:x+10,y:y+15,fill:col,'font-size':'10',
    'font-weight':'600','font-family':'monospace'});
  id.textContent=`#${task.id}`;
  const mc=17,tt=task.title.length>mc?task.title.slice(0,mc-1)+'…':task.title;
  const tl=svgEl('text',{x:x+10,y:y+31,fill:'#e2e8f0','font-size':'11','font-weight':'500'});
  tl.textContent=tt;
  const ic=svgEl('text',{x:x+NW-16,y:y+31,fill:'#475569','font-size':'11'});
  ic.textContent=task.type==='human'?'H':'A';
  [r,bar,id,tl,ic].forEach(e=>{e.style.cursor='pointer';
    e.addEventListener('click',()=>openTask(task));svg.appendChild(e);});}
function renderLane(lane){
  const wrap=document.createElement('div');
  wrap.className='lane';wrap.id='lane-'+lane.spec.id;
  const sc=SSC[lane.spec.state]||'#475569';
  const hdr=document.createElement('div');hdr.className='lane-header';
  hdr.innerHTML=`<span class="lane-title">${esc(lane.spec.title)}</span>`+
    (lane.spec.state?`<span class="lane-state" style="color:${sc};background:${sc}22">${esc(lane.spec.state)}</span>`:'')+
    `<span class="lane-topo">${esc(lane.topology)}</span>`;
  if(lane.spec.id!=='__standalone__')
    hdr.addEventListener('click',()=>openSpec(lane.spec));
  wrap.appendChild(hdr);
  const body=document.createElement('div');body.className='lane-body';
  const w=sw(lane.cols),h=sh(lane.rows);
  const svg=svgEl('svg',{width:w,height:h,viewBox:`0 0 ${w} ${h}`});
  lane.task_ids.forEach(tid=>{
    const task=DATA.tasks[tid];
    const tp=lane.layout[tid];if(!tp)return;
    (task.depends_on||[]).forEach(dep=>{
      const fp=lane.layout[dep];if(!fp)return;
      drawArrow(svg,nx(fp.col)+NW,ny(fp.row)+NH/2,nx(tp.col),ny(tp.row)+NH/2,false);});});
  lane.task_ids.forEach(tid=>{
    const task=DATA.tasks[tid];const p=lane.layout[tid];if(!p)return;
    renderNode(svg,task,nx(p.col),ny(p.row));
    NP[tid]={laneId:'lane-'+lane.spec.id,col:p.col,row:p.row};});
  body.appendChild(svg);wrap.appendChild(body);return wrap;}
function renderCrossEdges(){
  if(!DATA.cross_edges.length)return;
  requestAnimationFrame(()=>{
    const ov=document.getElementById('ov');ov.innerHTML='';
    DATA.cross_edges.forEach(({from:f,to:t})=>{
      const fi=NP[f],ti=NP[t];if(!fi||!ti)return;
      const fEl=document.querySelector('#'+fi.laneId+' .lane-body svg');
      const tEl=document.querySelector('#'+ti.laneId+' .lane-body svg');
      if(!fEl||!tEl)return;
      const fr=fEl.getBoundingClientRect(),tr=tEl.getBoundingClientRect();
      drawArrow(ov,fr.left+nx(fi.col)+NW,fr.top+ny(fi.row)+NH/2,
        tr.left+nx(ti.col),tr.top+ny(ti.row)+NH/2,true);});});}
function openTask(t){
  document.getElementById('pt').textContent=t.title;
  const rows=[['State',t.state],['Type',t.type],['Spec',t.spec||'—'],
    ['Claimed',t.claimed_by||'—'],['Depends on',(t.depends_on||[]).join(', ')||'—'],
    ['Verify',t.verify||'—']];
  document.getElementById('pf').innerHTML=rows.map(([k,v])=>
    `<div class="pr"><span class="pl">${esc(k)}</span><span class="pv">${esc(String(v))}</span></div>`).join('');
  document.getElementById('pb').textContent=t.body||'';
  document.getElementById('pfile').textContent=t.file?'tasks/'+t.file:'';
  document.getElementById('panel').classList.add('open');}
function openSpec(s){
  document.getElementById('pt').textContent=s.title;
  const rows=[['State',s.state||'—'],['Topology',s.topology||'—']];
  document.getElementById('pf').innerHTML=rows.map(([k,v])=>
    `<div class="pr"><span class="pl">${esc(k)}</span><span class="pv">${esc(v)}</span></div>`).join('');
  document.getElementById('pb').textContent=s.body||'';
  document.getElementById('pfile').textContent=s._file?'specs/'+s._file:'';
  document.getElementById('panel').classList.add('open');}
function closePanel(){document.getElementById('panel').classList.remove('open');}
function buildLegend(){
  const lg=document.getElementById('legend');
  [['backlog','Backlog'],['ready','Ready'],['in-progress','In progress'],
   ['blocked','Blocked'],['review','Review'],['done','Done'],['abandoned','Abandoned']
  ].forEach(([s,l])=>{
    const d=document.createElement('div');d.className='legend-item';
    d.innerHTML=`<div class="legend-dot" style="background:${SC[s]}"></div>${l}`;
    lg.appendChild(d);});}
buildLegend();
const lanesEl=document.getElementById('lanes');
DATA.lanes.forEach(l=>{const el=renderLane(l);if(el)lanesEl.appendChild(el);});
renderCrossEdges();
document.addEventListener('keydown',e=>{if(e.key==='Escape')closePanel();});
</script>
</body>
</html>
"""


def _serialise_lane(lane: dict) -> dict:
    spec = {k: v for k, v in lane["spec"].items() if not k.startswith("_")}
    spec["body"] = lane["spec"].get("_body", "")
    spec["_file"] = lane["spec"].get("_file", "")
    return {
        "spec": spec,
        "task_ids": lane["task_ids"],
        "topology": lane["topology"],
        "layout": lane["layout"],
        "cols": lane["cols"],
        "rows": lane["rows"],
    }


def generate_html(data: dict) -> str:
    tasks_out = {}
    for tid, t in data["tasks"].items():
        tasks_out[tid] = {k: v for k, v in t.items() if not k.startswith("_")}
        tasks_out[tid]["body"] = t.get("_body", "")
        tasks_out[tid]["file"] = t.get("_file", "")

    payload = json.dumps({
        "lanes": [_serialise_lane(l) for l in data["lanes"]],
        "tasks": tasks_out,
        "cross_edges": data["cross_edges"],
    }, ensure_ascii=False)
    return HTML_TEMPLATE.replace("__DATA_JSON__", payload)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    effort_dir = Path(sys.argv[1]).resolve()
    if not effort_dir.is_dir():
        print(f"error: not a directory: {effort_dir}", file=sys.stderr)
        sys.exit(1)
    out_path = (
        Path(sys.argv[2]).resolve() if len(sys.argv) >= 3
        else effort_dir / "roadmap.html"
    )
    data = build_data(effort_dir)
    html = generate_html(data)
    out_path.write_text(html, encoding="utf-8")
    n_specs = sum(1 for l in data["lanes"] if l["spec"]["id"] != "__standalone__")
    print(f"wrote {out_path}")
    print(f"  {n_specs} spec(s), {len(data['tasks'])} task(s), "
          f"{len(data['cross_edges'])} cross-spec edge(s)")


if __name__ == "__main__":
    main()
