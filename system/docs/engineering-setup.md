# Engineering Setup

Last updated: 2026-08-04

**Lifecycle stage 3.** Engineering Setup covers everything needed to make a codebase ready for reliable agent-assisted delivery. Its scope spans three sub-areas:

- **Context management** *(current)* — curating the minimal, high-signal information an agent needs. Detailed below.
- **Project skeleton** — standardized project framework scaffolding (e.g. Django Project/Apps layering, settings tiers, middleware, unified response/exception, auth).
- **Roadmap planning** *(planned)* — phased rollout with per-phase manual-test gates and base-infra bring-up.

---

## Context Management

Context Management is the art and science of curating the minimal, high-signal information an AI agent needs to understand a codebase, follow conventions, and execute tasks with high precision.

In agentic coding, **context is the bottleneck**. Too little context leads to hallucinations and errors; too much context wastes tokens, increases latency, and confuses the agent with noise.

## The Core Framework

Context lives in **three durable layers**, each with a different lifetime and a different author. The full model, including git-tracking policy and how `AGENTS.md` discovers the code index, is documented in the [`context-management`](../skills-src/context-management/README.md) category README.

| Layer | Question | Lives in | Git | Author |
| --- | --- | --- | --- | --- |
| **Human** | "How is this built, and why?" | `AGENTS.md`, `CLAUDE.md`, `docs/` | Tracked | People, agent-assisted |
| **Wiki** | "Where is X, and what connects to it?" | `docs/wiki/`, `.codemap/`, `graphify/` | Tracked by default | Tools |
| **Working** | "What am I doing, and where did I leave off?" | `.scratch/<effort>/` | Ignored | The active workflow |

`manage-context` Phase B is the single entry point responsible for reconciling the three when they drift.

Within the Human layer, ownership splits further by **content type** and **runtime**:

- **Operational** — *what/why* the project is. Project overview, architecture, modules, interfaces, data tables, test coverage.
  - `CLAUDE.md` / `AGENTS.md` content shape → `review-agent-instructions` (detects which file is present and applies the matching skeleton and line ceiling)
- **Technical** — *how the agent must behave*. Naming, formatting, API patterns, security rules, per-task guardrails, implicit conventions.
  - Discovery, classification, runtime-aware routing → `extract-rules` (writes to `.claude/rules/*.md`, inline AGENTS.md, or `docs/conventions/*.md` based on detected runtime; per-task patterns to `docs/spec.md`)
- **Cross-runtime parity** — port Claude-specific surfaces (slash commands, hooks, `.claude/skills/`, orchestrator subagents) into agent-agnostic equivalents → `translate-agent-context`

---

## Skills

### [manage-context](../skills/manage-context/SKILL.md)

The entry point and orchestrator for the whole collection. Reads `docs/agents/memory.md` and auto-selects a phase.

**Phase A (setup)** — runs when routing is absent. Configures the shared memory layers, work root, issue tracker, and optional wiki; writes `docs/agents/memory.md`; bootstraps the Working layer (init script, `state.md` as the resume entry point, append-only `progress.md`, cold-start sequence in `AGENTS.md`); then routes to `scaffold-agent-docs`, `create-readme`, `extract-rules`, `document-codebase`, and `index-codebase` for whatever is still missing.

**Phase B (sync)** — runs when routing exists. Detects drift across Human docs, Wiki index, and Working memory; makes narrow factual corrections directly; and invokes the owning skill for structural work — `scaffold-agent-docs` (update mode) for Human-layer structure, `document-codebase` (targeted-doc) for stale content, `review-agent-instructions` for oversized context files, `create-readme` for a stale README, `extract-rules` for undocumented conventions, `index-codebase` for a stale wiki index. Distinguishes drift (fix the doc) from a constraint violation (fix the code).

Protocol spec at [`manage-context/references/PROTOCOL.md`](../skills/manage-context/references/PROTOCOL.md). Triggers: "set up context management", "the docs are stale", "sync the context", run after a merge or before a handoff.

### [scaffold-agent-docs](../skills/scaffold-agent-docs/SKILL.md)

Owns the core `AGENTS.md` + `docs/` structure. Mode A (init): create `AGENTS.md` as a short index under 200 lines, plus `docs/ARCHITECTURE.md`, `CONVENTIONS.md`, `TECH_DECISIONS.md`, `QUALITY.md`, and `exec-plans/` from templates, then fill from the code — verifying every relationship claim with a grep. Mode B (update): audit existing Human-layer docs, verify claims against live code, classify each doc, apply structural repairs, and flag content gaps for `manage-context` Phase B to delegate. Templates live at [`scaffold-agent-docs/references/templates/`](../skills/scaffold-agent-docs/references/templates/README.md); canonical layout reference at [`scaffold-agent-docs/references/canonical-doc-layout.md`](../skills/scaffold-agent-docs/references/canonical-doc-layout.md). Triggers: "add agent support to this project", "create AGENTS.md", "set up agent docs", "audit and repair the docs".

### [index-codebase](../skills/index-codebase/SKILL.md)

Own the Wiki layer. Chooses among `codemap` (fastest, default), `codegraph` (SQLite index, auto-syncs), `graphify` (multimodal corpora), and `GitNexus` (multi-repo, browser UI), builds the index, sets the git policy, and writes the query pointer into `AGENTS.md` so the agent actually uses it. Tool comparison in the reference it ships at [`index-codebase/references/external-tools.md`](../skills/index-codebase/references/external-tools.md). Triggers: "index the codebase", "set up a code map", "the agent keeps grepping".

### llm-wiki-init · llm-wiki-ingest · llm-wiki-lint (learning-os)

The prose wiki skills live in [learning-os](https://github.com/XinheLIU/learning-os). `llm-wiki-init` scaffolds the schema, index, and append-only log; `llm-wiki-ingest` distills one source through capture → extract → discuss → write, keeping raw files immutable and hashed; `llm-wiki-lint` audits broken wikilinks, orphans, source drift, contested claims, and tag sprawl. Triggers: "start a knowledge base", "ingest this into my wiki", "lint the wiki".

### [review-agent-instructions](../skills/review-agent-instructions/SKILL.md)

Audit and restructure `CLAUDE.md` or `AGENTS.md` and every file they reference. Detects which file is present and applies the appropriate canonical skeleton: 9-section for `CLAUDE.md` (200-line ceiling); 9-section plus an Agent Surface table for `AGENTS.md` (220-line ceiling). Produces a MECE rewrite and a concrete change list. Triggers: "review CLAUDE.md", "review AGENTS.md", "audit context files", "shrink CLAUDE.md / AGENTS.md", "deduplicate context docs".

### [translate-agent-context](../skills/translate-agent-context/SKILL.md)

Cross-runtime parity. Ports Claude-specific surfaces (`.claude/rules/`, slash commands, hooks, `.claude/skills/`, orchestrator subagents) into agent-agnostic equivalents Codex / OpenCode / Cursor can consume. Owns the orchestrator decomposition 4-strategy menu and shared `skills/` symlink layout. Triggers: "port Claude setup to Codex", "sync Claude and AGENTS.md", "translate slash commands", "set up cross-runtime parity".

### [extract-rules](../skills/extract-rules/SKILL.md)

Discover, classify, and runtime-route agent-behavior rules. Auto-detects runtime (Claude / AGENTS.md-only / multi-runtime) and writes static rules to `.claude/rules/*.md`, inline AGENTS.md, or `docs/conventions/*.md`; dynamic per-task patterns to `docs/spec.md` Workflow Norms; implicit conventions stay inline + indexed. Triggers: "extract project rules", "create spec.md", "find hidden conventions", "set up rules in AGENTS.md".

### [document-codebase](../skills/document-codebase/SKILL.md)

Author technical docs — READMEs, C4 architecture diagrams (Mermaid), API references, configuration docs. Scales deliverables to project complexity. Always audits and proposes a diff before writing. Triggers: "write README", "document architecture", "create C4 diagram".

### [create-readme](../skills/create-readme/SKILL.md)

Create or revamp a project's `README.md`. Audits the codebase first, tiers the README to project size (minimal / standard / full), drafts from a [Best-README-Template](https://github.com/othneildrew/Best-README-Template)-based blueprint, and self-checks against a zero-context-reader checklist. Triggers: "create a README", "write a README", "revamp the README".

---

## Hook Setup — keep context fresh on every commit

Three setup methods. Pick by runtime and how you want to share the hook with your team.

| Method | Scope | Versioned? | Best for |
|---|---|---|---|
| **A. Git `pre-commit` hook** | Per-clone | No (`.git/` is local) | Quick personal setup, any runtime |
| **B. `pre-commit` framework** | Repo-wide | Yes | Team-shared, cross-runtime |
| **C. Claude Code native hook** | Project | Yes | Claude-only, fires only when Claude commits |

### Method A — Git `pre-commit` hook (simplest, runtime-agnostic)

Drop a script at `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
set -e

# Trigger only when context-bearing files are staged.
if git diff --cached --name-only | grep -qE '(CLAUDE\.md|AGENTS\.md|docs/.*\.md)'; then
  # Claude project — review CLAUDE.md
  claude -p "Use review-agent-instructions to audit CLAUDE.md and referenced docs. Report findings only — do not write."

  # Codex / OpenCode project — review AGENTS.md
  # codex exec "Use review-agent-instructions to audit AGENTS.md and referenced docs. Report findings only."
  # opencode run "Use review-agent-instructions to audit AGENTS.md. Report only."
fi
```

`chmod +x .git/hooks/pre-commit`. Per-clone — git hooks are not under version control.

### Method B — `pre-commit` framework (shared with the team)

If your repo uses [`pre-commit`](https://pre-commit.com), add a local hook in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: review-agent-instructions
        name: Claude — audit CLAUDE.md
        entry: claude -p "Use review-agent-instructions to audit and report only."
        language: system
        files: ^(CLAUDE\.md|docs/.*\.md)$
        stages: [pre-commit]

      - id: review-agent-instructions
        name: Codex — audit AGENTS.md
        entry: codex exec "Use review-agent-instructions to audit AGENTS.md and report only."
        language: system
        files: ^(AGENTS\.md|docs/.*\.md)$
        stages: [pre-commit]
```

Run once: `pre-commit install`. Hooks live in the repo and apply to every contributor.

### Method C — Claude Code native hook (`.claude/settings.json`)

Tightest integration for Claude users. Fires only when *Claude itself* runs `git commit` (not when the user runs it from a terminal). Project-scoped — commit `.claude/settings.json`.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(git commit *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-commit.sh"
          }
        ]
      }
    ]
  }
}
```

Hook script at `.claude/hooks/pre-commit.sh` (`chmod +x`):

```bash
#!/usr/bin/env bash
# Stdin is JSON; tool_input.command holds the actual git command.
COMMAND=$(jq -r '.tool_input.command')

claude -p "Use review-agent-instructions to audit CLAUDE.md and referenced docs against the staged commit: $COMMAND. Report only."

# Exit 0 = allow commit. Exit 2 = block. Anything else = non-blocking error.
exit 0
```

Reference: [Claude Code hooks docs](https://code.claude.com/docs/en/hooks.md).

### Recommended pairings

| Runtime | Skill | Method |
|---|---|---|
| Claude (project) | `review-agent-instructions` | C — fires only when Claude commits, no extra latency for human commits |
| Codex / OpenCode | `review-agent-instructions` | A or B — these runtimes lack a native PreToolUse hook surface; use git's |
| Cross-team / shared repos | any | B — versioned with the repo so every contributor shares the hooks |
| Personal-only quick setup | any | A — fastest, no shared config |

`extract-rules` and `translate-agent-context` are **not** good fits for per-commit hooks — both are periodic audits (when conventions drift, when porting between runtimes, when onboarding). Run them manually.

---

## Integration Guide — context surfaces by agent

Copy or symlink skills/instructions to each agent's configuration paths.

| Agent | Global Path (User Level) | Project Path (Workspace Level) |
| :--- | :--- | :--- |
| **Claude (Code/Desktop)** | `~/.claude/CLAUDE.md` | `./CLAUDE.md` |
| **Antigravity** | `<appDataDir>/knowledge/` (KIs) | N/A (Uses KIs) |
| **Cursor** | - | `.cursorrules` / `AGENTS.md` |
| **Windsurf** | `~/.codeium/windsurf/memories/global_rules.md` | `.windsurfrules` / `AGENTS.md` |
| **Trae** | `TRAE/rules/user_rules.md` | `TRAE/rules/project_rules.md` |
| **Codex / OpenCode** | `~/.codex/AGENTS.md` / `~/.config/opencode/AGENTS.md` | `AGENTS.md` |
| **Qwen** | `~/.qwen/settings.json` | `.qwen/QWEN.md` |
| **Quoder** | `~/.qoder/agents/` | `.qoder/rules/` |
| **Gemini CLI** | `~/.gemini/system.md` | `.gemini/system.md` (or `GEMINI_SYSTEM_MD` env) |
| **GitHub Copilot** | - | `.github/copilot-instructions.md` |

> For an AGENTS.md-based runtime, run `review-agent-instructions` to audit content shape and `extract-rules` to extract rules into the right home (inline AGENTS.md or `docs/conventions/`). To port a Claude setup over to one of these runtimes, run `translate-agent-context`.

---

## Setup Examples

- **User Level Setup:** [user-level-claude.md](examples/user-level-claude.md)
  *Credit to [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/EXAMPLES.md) for the initial examples.*
