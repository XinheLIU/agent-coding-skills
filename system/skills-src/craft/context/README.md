# Craft · Context

Last updated: 2026-08-16

Managing the shared knowledge an agent needs to work effectively in a codebase. Covers one-time setup and ongoing maintenance, across all runtimes.

## Skills

### setup/ — run once per repo

| Skill | When |
| --- | --- |
| `init-context` | New repo or lost routing config. Writes memory routing, Human-layer docs, code index, and rule files in one sequential flow. |
| `translate-agent-context` | Cross-runtime migration. Port Claude-specific surfaces (rules, slash commands, hooks, orchestrators) to Codex / OpenCode / Cursor equivalents. |

### maintain/ — run on hooks or periodically

| Skill | When |
| --- | --- |
| `sync-context` | After a merge, before a handoff, or on a schedule. Detects drift across Human docs, wiki index, and working memory. |

---

## Design

### Four-layer memory model

Every artifact an agent reads belongs to one layer, defined by the question it answers and how long the answer stays true:

| Layer | Answers | Lifetime | Git |
| --- | --- | --- | --- |
| Core | What words and constraints bind this project | Project | Tracked |
| Human | What we are building, why, and how it works | Project | Tracked |
| Wiki | Where the code for X lives | Rebuildable | Either |
| Working | How the current effort is going and what happens next | Effort | Ignored |

**The durability test.** Before writing persistent state: *if the work root were deleted today, would the project have lost a fact it still needs?* Yes → Human or Core layer. No → working memory.

**Promotion is one-way: Working → Human or Core.** Promote a decision when it is settled, hard to reverse, and would surprise someone who did not watch it happen. Nothing is ever demoted from a tracked layer into working memory.

Full contract and ownership registry: [`setup/init-context/references/PROTOCOL.md`](setup/init-context/references/PROTOCOL.md).

### Skill roles

Each skill declares one of three roles before it writes anything:

| Role | Contract |
| --- | --- |
| **Owner** | Reads configured inputs, writes exactly one canonical artifact, declares `Layer / Owns / Promotes` |
| **Consumer** | Reads canonical artifacts, may report findings — never rewrites their facts |
| **Transient** | In-session operation only, writes no persistent memory |

### init-context phases

Four sequential phases. Each skips if its output already exists — re-running is safe.

| Phase | Output | Skip if |
| --- | --- | --- |
| 1 — Routing + working memory | `docs/agents/memory.md`, `init.sh`, `.scratch/<effort>/state.md` | `docs/agents/memory.md` present |
| 2 — Human-layer docs | `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/TECH_DECISIONS.md`, `docs/QUALITY.md`, `README.md` | All listed docs present |
| 3 — Code index (wiki layer) | Index at configured path + `AGENTS.md` pointer | Wiki disabled or index fresh |
| 4 — Agent-behavior rules | `.claude/rules/*.md`, `docs/spec.md` | Rule files have content |

One confirmation gate before any writes. Agent proposes a consolidated file list; user approves or skips individual phases.

### sync-context modes

| Mode | Invoke | Checks | Typical use |
| --- | --- | --- | --- |
| Fast (default) | `/sync-context` | Human-layer docs only, ~30 s | Post-commit hook |
| Full | `/sync-context --full` | All three layers | Weekly cron, pre-handoff |

Fast mode checks paths, commands, relationships, and index-table links. Full mode additionally checks wiki freshness, working-memory health, and promotion candidates (decisions stuck in working memory that belong in a tracked layer).

### Working-memory hierarchy

Working memory uses a three-level hierarchy: **Effort → Spec → Task**.

- **Effort**: the top-level goal. One `state.md` + `progress.md`.
- **Spec** (`specs/NNN-slug.md`): earned when an effort requires multiple coordinated tasks. Carries `topology: workflow | dag`.
- **Task** (`tasks/NNN-slug.md`): a single unit of work with a state machine and a `verify` command.

Task state machine: `backlog → ready → claimed → in-progress → review → done` (plus `blocked`, `abandoned`). Agents claim before editing; `review → done` requires the `verify` command to pass — agents never self-declare done.

Detail: [`setup/init-context/references/working-memory.md`](setup/init-context/references/working-memory.md).

---

## The Context Protocol

### Read order

Before acting, a memory-aware skill reads:

1. `docs/agents/memory.md` — routing config (work root, issue tracker, wiki status)
2. Relevant `CONTEXT.md` and ADRs — terminology and constraints
3. Active effort's `state.md` — current status, next action, blockers, pointers
4. Artifacts pointed to by `state.md` — minimum set needed for the current work

Generated HTML (e.g., `roadmap.html`) is a view. Use the linked Markdown when reasoning about state.

### Write rules

1. Write each fact in exactly one canonical artifact. Link elsewhere; never copy.
2. Update only artifacts owned by the active skill, or explicitly delegated.
3. Preserve user-authored sections and unrelated state.
4. Add or update `Last updated: YYYY-MM-DD` on every edited Markdown file.
5. Update `state.md` after every workflow transition.
6. Never record credentials, tokens, or personal data in shared memory.

---

## Team Integration

### Quickstart on a new repo

```bash
# 1. Run init-context once — safe to re-run on an existing repo
/init-context

# 2. Bind the post-commit hook (fast sync after every commit)
cat > .git/hooks/post-commit << 'EOF'
#!/bin/sh
claude --skill sync-context
EOF
chmod +x .git/hooks/post-commit

# 3. Add a weekly full sync (cron — every Monday at 09:00)
# 0 9 * * 1 cd /path/to/repo && claude --skill sync-context --full
```

### Distributing the hook across the team

`.git/hooks/` is not committed. Use `pre-commit` to ship the hook with the repo:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: sync-context
        name: Sync agent context (fast)
        entry: claude --skill sync-context
        language: system
        always_run: true
        pass_filenames: false
```

```bash
# each clone, once
pre-commit install
```

The hook exits 0 when there are no blocking issues. It exits 1 with a one-line summary when broken paths or misplaced durable facts are found — those block the commit until repaired.

### Onboarding a new team member

```bash
git clone <repo>
/init-context   # idempotent — skips phases that already exist, verifies cold-start
```

Phase 1 ends with a cold-start verification: can a fresh agent session derive what to do next from `state.md` alone? If not, `state.md` is underspecified and the skill flags it.

### Pre-handoff

Before handing off context to another agent or developer, run a full sync to surface everything that needs attention:

```bash
/sync-context --full
```

The report will show: broken doc paths, stale code index, uncommitted architectural decisions stuck in working memory, and effort completion candidates.

---

## Agent Setup

### Claude Code

Skills are loaded from `.claude/skills/`. After `init-context` Phase 4:

```
.claude/
├── rules/        ← static agent-behavior rules (auto-loaded each session)
└── skills/       ← symlink to shared skills/ or a local copy
```

Invoke via slash commands:

```
/init-context
/sync-context
/sync-context --full
/translate-agent-context
```

To bind `sync-context` to Claude's own tool lifecycle (runs automatically after file writes), add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "claude --skill sync-context" }]
      }
    ]
  }
}
```

### Codex / OpenCode

Skills go in `.codex/skills/` (Codex) or `.config/opencode/agents/` (OpenCode). Use `translate-agent-context` to migrate from a Claude-first setup:

```bash
/translate-agent-context
```

The skill produces a translation map per artifact:

| Claude surface | Codex / OpenCode equivalent |
| --- | --- |
| `.claude/rules/*.md` | Inline `AGENTS.md` (short) or `docs/conventions/<name>.md` referenced from `AGENTS.md` (long) |
| Slash commands | Shell scripts in `tools/<name>.sh` + documented trigger in `AGENTS.md` |
| Hooks (PostToolUse) | Documented rule + CI check |
| Orchestrator skills | User-selected from 4-strategy menu: native dispatch / subprocess fanout / serialized / runtime-only |

For shared skills across runtimes, use a symlinked layout:

```
skills/                    ← canonical shared library
  craft/context/…

.claude/skills -> ../skills    ← Claude reads here
.codex/skills  -> ../skills    ← Codex reads here
```

`AGENTS.md` carries the read protocol for runtimes that load it automatically (Codex, OpenCode, Cursor, aider).

### Cursor and other agents

Most agents load `AGENTS.md`. After `init-context`, `AGENTS.md` contains:

- **Startup sequence**: run init script → read `state.md` → follow pointers → update `state.md` before closing
- **Routing table**: "I want to know X" → the exact file that answers it
- **Static rules**: inline or linked from `docs/conventions/`

For agents without a skill-loading mechanism, the Human-layer docs (`docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, etc.) serve as the context surface — they are agent-agnostic by design. The init-context skill writes them in plain Markdown with no tool-specific directives.

---

## Key references

| File | What it contains |
| --- | --- |
| `setup/init-context/references/PROTOCOL.md` | Full layer contract, ownership registry, read/write protocol |
| `setup/init-context/references/working-memory.md` | Effort→Spec→Task hierarchy, task state machine, triage rules |
| `setup/init-context/references/canonical-doc-layout.md` | Structural invariants for all tracked docs |
| `setup/init-context/references/templates/` | Starter files for AGENTS.md, ARCHITECTURE, spec, task |
| `setup/translate-agent-context/references/agent-surface.md` | Surface inventory per runtime |
| `setup/translate-agent-context/references/runtime-parity-translation.md` | Mechanism-translation map + orchestrator decomposition strategies |

---

## scripts/

`scripts/gen-roadmap.py` generates `roadmap.html` from task and spec frontmatter in an effort directory:

```bash
python3 scripts/gen-roadmap.py .scratch/<effort>/
# writes .scratch/<effort>/roadmap.html
```

One lane per spec. `topology: workflow` renders as a horizontal strip; `topology: dag` as a layered column graph (longest-path depth for column assignment). Standalone tasks get their own lane. Cross-spec `depends_on` edges appear as dashed overlay arrows. Click any node for a side panel with full detail.
