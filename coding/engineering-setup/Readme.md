# Engineering Setup

Last updated: 2026-07-18

**Lifecycle stage 3.** Engineering Setup covers everything needed to make a codebase ready for reliable agent-assisted delivery. Its scope spans three sub-areas:

- **Context management** *(current)* — curating the minimal, high-signal information an agent needs. Detailed below.
- **Project skeleton** *(planned — see [`backlog.md`](../backlog.md))* — standardized project framework scaffolding (e.g. Django Project/Apps layering, settings tiers, middleware, unified response/exception, auth).
- **Roadmap planning** *(planned — see [`backlog.md`](../backlog.md))* — phased rollout with per-phase manual-test gates and base-infra bring-up.

---

## Context Management

Context Management is the art and science of curating the minimal, high-signal information an AI agent needs to understand a codebase, follow conventions, and execute tasks with high precision.

In agentic coding, **context is the bottleneck**. Too little context leads to hallucinations and errors; too much context wastes tokens, increases latency, and confuses the agent with noise.

## The Core Framework

Two layers manage agent context, with skill ownership split by **content type** and **runtime**:

- **Operational layer** — *what/why* the project is. Project overview, architecture, modules, interfaces, data tables, test coverage.
  - `CLAUDE.md` content shape → `review-claude-md`
  - `AGENTS.md` content shape (Codex / OpenCode / Cursor) → `review-agent-md`
- **Technical layer** — *how the agent must behave*. Naming, formatting, API patterns, security rules, per-task guardrails, implicit conventions.
  - Discovery, classification, runtime-aware routing → `extract-rules` (writes to `.claude/rules/*.md`, inline AGENTS.md, or `docs/conventions/*.md` based on detected runtime; per-task patterns to `docs/spec.md`)
- **Cross-runtime parity** — port Claude-specific surfaces (slash commands, hooks, `.claude/skills/`, orchestrator subagents) into agent-agnostic equivalents → `translate-agent-context`

---

## Skills

### [review-claude-md](./skills/review-claude-md/SKILL.md)

Audit and restructure `CLAUDE.md` and the docs it references. Produces a MECE rewrite to a canonical 9-section skeleton with a 200-line ceiling. Triggers: "review CLAUDE.md", "shrink CLAUDE.md", "deduplicate context docs".

### [review-agent-md](./skills/review-agent-md/SKILL.md)

Direct parallel to `review-claude-md` but for `AGENTS.md` (Codex / OpenCode / Cursor). Audits AGENTS.md and the docs it references; produces a MECE rewrite to a canonical 9-section skeleton (with an Agent Surface table) and a 220-line ceiling. Triggers: "review AGENTS.md", "audit AGENTS.md", "shrink AGENTS.md".

### [translate-agent-context](./skills/translate-agent-context/SKILL.md)

Cross-runtime parity. Ports Claude-specific surfaces (`.claude/rules/`, slash commands, hooks, `.claude/skills/`, orchestrator subagents) into agent-agnostic equivalents Codex / OpenCode / Cursor can consume. Owns the orchestrator decomposition 4-strategy menu and shared `skills/` symlink layout. Triggers: "port Claude setup to Codex", "sync Claude and AGENTS.md", "translate slash commands", "set up cross-runtime parity".

### [extract-rules](./skills/extract-rules/SKILL.md)

Discover, classify, and runtime-route agent-behavior rules. Auto-detects runtime (Claude / AGENTS.md-only / multi-runtime) and writes static rules to `.claude/rules/*.md`, inline AGENTS.md, or `docs/conventions/*.md`; dynamic per-task patterns to `docs/spec.md` Workflow Norms; implicit conventions stay inline + indexed. Triggers: "extract project rules", "create spec.md", "find hidden conventions", "set up rules in AGENTS.md".

### [codebase-documenter](./skills/codebase-documenter/SKILL.md)

Author technical docs — READMEs, C4 architecture diagrams (Mermaid), API references, configuration docs. Scales deliverables to project complexity. Always audits and proposes a diff before writing. Triggers: "write README", "document architecture", "create C4 diagram".

### [create-readme](./skills/create-readme/SKILL.md)

Create or revamp a project's `README.md`. Audits the codebase first, tiers the README to project size (minimal / standard / full), drafts from a [Best-README-Template](https://github.com/othneildrew/Best-README-Template)-based blueprint, and self-checks against a zero-context-reader checklist. Triggers: "create a README", "write a README", "revamp the README".

### [organize-docs](./skills/organize-docs/)

*(Placeholder — not yet populated.)*

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
  claude -p "Use review-claude-md to audit CLAUDE.md and referenced docs. Report findings only — do not write."

  # Codex / OpenCode project — review AGENTS.md
  # codex exec "Use review-agent-md to audit AGENTS.md and referenced docs. Report findings only."
  # opencode run "Use review-agent-md to audit AGENTS.md. Report only."
fi
```

`chmod +x .git/hooks/pre-commit`. Per-clone — git hooks are not under version control.

### Method B — `pre-commit` framework (shared with the team)

If your repo uses [`pre-commit`](https://pre-commit.com), add a local hook in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: review-claude-md
        name: Claude — audit CLAUDE.md
        entry: claude -p "Use review-claude-md to audit and report only."
        language: system
        files: ^(CLAUDE\.md|docs/.*\.md)$
        stages: [pre-commit]

      - id: review-agent-md
        name: Codex — audit AGENTS.md
        entry: codex exec "Use review-agent-md to audit AGENTS.md and report only."
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

claude -p "Use review-claude-md to audit CLAUDE.md and referenced docs against the staged commit: $COMMAND. Report only."

# Exit 0 = allow commit. Exit 2 = block. Anything else = non-blocking error.
exit 0
```

Reference: [Claude Code hooks docs](https://code.claude.com/docs/en/hooks.md).

### Recommended pairings

| Runtime | Skill | Method |
|---|---|---|
| Claude (project) | `review-claude-md` | C — fires only when Claude commits, no extra latency for human commits |
| Codex / OpenCode | `review-agent-md` | A or B — these runtimes lack a native PreToolUse hook surface; use git's |
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

> For an AGENTS.md-based runtime, run `review-agent-md` to audit content shape and `extract-rules` to extract rules into the right home (inline AGENTS.md or `docs/conventions/`). To port a Claude setup over to one of these runtimes, run `translate-agent-context`.

---

## Setup Examples

- **User Level Setup:** [user-level-Claude-md](./Claude-set-up-Example/user-level-Claude-md)
  *Credit to [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/EXAMPLES.md) for the initial examples.*
