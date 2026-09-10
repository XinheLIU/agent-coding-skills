# Engineering Setup

Last updated: 2026-09-09

**Lifecycle stage 3.** Engineering Setup covers everything needed to make a codebase ready for reliable agent-assisted delivery. Its scope spans three sub-areas:

- **Context management** *(current)* — curating the minimal, high-signal information an agent needs. Detailed below.
- **Project skeleton** — standardized project framework scaffolding (e.g. Django Project/Apps layering, settings tiers, middleware, unified response/exception, auth).
- **Roadmap planning** *(planned)* — phased rollout with per-phase manual-test gates and base-infra bring-up.

---

## Context Management

Context Management is the art and science of curating the minimal, high-signal information an AI agent needs to understand a codebase, follow conventions, and execute tasks with high precision.

In agentic coding, **context is the bottleneck**. Too little context leads to hallucinations and errors; too much context wastes tokens, increases latency, and confuses the agent with noise.

## The Core Framework

The [shared protocol](../skills-src/craft/context/init-context/references/PROTOCOL.md) defines North Star, Current State, Change Context, and Run Context. Code indexes are derived views. The [coordinator](../workflows/context-coordination.md) owns context assembly, runtime bindings, claims, transitions, and cleanup; domain skills own facts and judgments.

`sync-context` reconciles drift and routes affected conclusions to their owners. Keep accepted requirements/designs and compact final evidence after completion; remove only reconciled execution material. Current-state summaries explain applicable behavior/boundaries with source revisions, while ADRs and change records retain historical rationale.

Instruction-file content is maintained by `review-agent-instructions`; runtime parity by `translate-agent-context`. Other documentation capabilities are optional and must be available before invocation.

---

## Skills

### [init-context](../skills/init-context/SKILL.md)

The one-time setup entry point for the whole collection. Writes `docs/agents/memory.md` and initializes the configured memory layers.

**Phase A (setup)** — runs when routing is absent. Configures the shared memory layers, work root, issue tracker, and optional wiki; writes `docs/agents/memory.md`; and bootstraps the Run Context. Broader documentation, rule extraction, and indexing are separate capabilities.

**Phase B (sync)** — runs when routing exists. Detects drift across domain records, derived indexes, and Run Context, then makes narrow factual corrections or reports structural work for the owning capability. Distinguishes drift (fix the doc) from a constraint violation (fix the code).

Protocol spec at [`init-context/references/PROTOCOL.md`](../skills/init-context/references/PROTOCOL.md). Triggers: "set up context management", "the docs are stale", "sync the context", run after a merge or before a handoff.

### Documentation and indexing capabilities

Documentation-tree scaffolding is separate from this small context set. `init-context` initializes routing and `sync-context` reports drift without claiming ownership of project documentation.

### Code indexing

Code indexing is also separate. The context set records the configured index location and checks whether it has drifted.

### llm-wiki-init · llm-wiki-ingest · llm-wiki-lint (learning-os)

The prose wiki skills live in [learning-os](https://github.com/XinheLIU/learning-os). `llm-wiki-init` scaffolds the schema, index, and append-only log; `llm-wiki-ingest` distills one source through capture → extract → discuss → write, keeping raw files immutable and hashed; `llm-wiki-lint` audits broken wikilinks, orphans, source drift, contested claims, and tag sprawl. Triggers: "start a knowledge base", "ingest this into my wiki", "lint the wiki".

### [review-agent-instructions](../skills/review-agent-instructions/SKILL.md)

Write and maintain the repository's agent instruction file — `CLAUDE.md` or `AGENTS.md`, whichever is present — and keep it wired to the memory system. Triages before reading: **intake** folds one post-incident lesson into the section that owns it, **review** rewrites a file whose shape has decayed, **wire memory** restores the startup sequence, memory-routing pointer, and Context Files triggers. Judges against five principles (index plus common sense, earned by experience, checkable, alternatives not just prohibitions, room to grow) under a ~200/220-line budget. Triggers: "review CLAUDE.md", "review AGENTS.md", "shrink CLAUDE.md / AGENTS.md", "add this lesson to CLAUDE.md", "the agent keeps ignoring CLAUDE.md".

### [translate-agent-context](../skills/translate-agent-context/SKILL.md)

Cross-runtime parity. Preserves behavior while translating instructions, skills, commands, hooks, roles, and context between any agent runtimes or host applications. Classifies each target by its actual discovery, tool, delegation, persistence, permission, enforcement, and timing capabilities before choosing a native binding. Triggers: "port agent setup", "sync runtime instructions", "translate slash commands", "make these skills work in another agent", "set up cross-runtime parity".

### Rule extraction

Discover, classify, and runtime-route agent-behavior rules. Auto-detects runtime (Claude / AGENTS.md-only / multi-runtime) and writes static rules to `.claude/rules/*.md`, inline AGENTS.md, or `docs/conventions/*.md`; dynamic per-task patterns to `docs/spec.md` Workflow Norms; implicit conventions stay inline + indexed. Triggers: "extract project rules", "create spec.md", "find hidden conventions", "set up rules in AGENTS.md".

### Technical documentation

Author technical docs — READMEs, C4 architecture diagrams (Mermaid), API references, configuration docs. Scales deliverables to project complexity. Always audits and proposes a diff before writing. Triggers: "write README", "document architecture", "create C4 diagram".

### README authoring

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
