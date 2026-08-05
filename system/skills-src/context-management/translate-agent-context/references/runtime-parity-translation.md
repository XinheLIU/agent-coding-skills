# Runtime-to-Neutral Parity Translation

Last updated: 2026-08-02

Use this for `translate`. Translation is a separate decision from normalizing `AGENTS.md`, creating `agents/`, or cleaning up repo structure.

The goal is not to preserve runtime-specific mechanisms as artifacts. The goal is to preserve the behavior they created so every agent the repo supports — Claude, Codex, Cursor, Continue, Aider, or whatever comes next — can follow the same rules and complete the same workflows.

Default to the smallest edit surface that achieves parity.

## Core Rule

For every runtime-specific surface you find, answer two questions:

1. What behavior did this enforce, remind, or automate?
2. Where should that behavior live so every agent the repo supports can still follow it?

Never stop at "runtime X does not support this." Translate the behavior.

## Translation Matrix

| Runtime-specific surface | What it usually means | Preferred runtime-neutral home |
|---|---|---|
| `CLAUDE.md` root guidance | Cross-cutting repo instructions for Claude | `AGENTS.md` |
| `.claude/rules/*.md` | Directory- or topic-scoped Claude rules | root `AGENTS.md` for cross-cutting rules, or subdirectory `AGENTS.md` for scoped rules |
| Claude hooks (`.claude/settings*.json`) | Automatic checks, setup, guardrails, or generated context | scripts or `tools/` plus explicit invocation rules in `AGENTS.md`, plus CI or pre-commit when enforcement matters |
| Claude slash commands (`.claude/commands/`) | Reusable multi-step workflows | scripts, `tools/`, skills, or `agents/*.md` workflow docs depending on whether the behavior is executable or instructional |
| `.claude/skills/` | Claude-specific automation | keep if Claude is still supported; port shared logic into repo-owned docs, scripts, or `tools/` when other agents also need it |
| `.claude/agents/*.md` | Claude subagents — auto-discovered role prompts invoked via the Agent tool inside one Claude session | **does not copy** to other runtimes. Split into: (1) role prompt in `agents/<role>.md` (neutral) + (2) per-runtime binding (see "Multi-Agent Orchestration" below) |
| `.cursor/rules/*.mdc`, `.cursorrules` | Cursor-scoped rules (often `@`-scoped globs) | root or subdirectory `AGENTS.md` when the rule is behavioral; keep in `.cursor/` only if the rule is genuinely Cursor-only (e.g. IDE hints) |
| `.continue/` config and prompts | Continue.dev assistants, slash commands, prompts | `agents/*.md` for role prompts, `tools/` or scripts for executable flows, `AGENTS.md` for cross-cutting rules |
| `.aider.conf.yml`, `.aider.model.settings.yml` | Aider runtime + model settings | stay in the aider config file (true runtime toggles); move any prose guidance into `AGENTS.md` |
| Runtime settings files (e.g. `.codex/config.toml`) | Runtime or behavior toggles | stay in that runtime's config only for true runtime settings; otherwise move guidance into `AGENTS.md` or executable surfaces |

## Multi-Agent Orchestration

Subagent / multi-agent mechanisms are **fundamentally different across runtimes**. They do not copy. Skills copy; subagents do not.

For every agent role the repo wants, translate into three pieces:

1. **Role prompt** → `agents/<role>.md` (runtime-neutral, "how this agent thinks"). This is the shared home.
2. **Per-runtime binding** — one tiny file per supported runtime, pointing at or mirroring the neutral prompt:
   - Claude: `.claude/agents/<role>.md` with frontmatter (`name`, `description`, `model`). Auto-discovered, invoked via the Agent tool inside one Claude session.
   - Codex: `[profiles.<role>]` block in `.codex/config.toml` (model, `sandbox_mode`, approval policy) **plus** a `## <role>` section in `AGENTS.md` that states the role's rules. No auto-discovery. Invoked as a separate process: `codex exec --profile <role> "…"`. Multi-agent = multi-process (e.g. tmux panes).
   - Cursor: no standard subagent format. The closest equivalents are `.cursor/rules/*.mdc` (scoped rules) or Composer/Agent-mode prompts. If the repo wants a named role, document it in `AGENTS.md` and/or point Cursor at `agents/<role>.md`.
   - Continue: a custom assistant / model entry in `.continue/config.json` (or `.continue/prompts/<role>.prompt`) whose system prompt pulls from `agents/<role>.md`.
   - Aider: a launch wrapper script that sets the system prompt (`--message-file agents/<role>.md`) and runtime flags. No in-tool subagent concept — multi-agent = multiple `aider` processes.
3. **Invocation documentation** → the `Agent Surface` table in `AGENTS.md` should record, for each role, the command or mechanism each supported runtime uses. Without this, users cannot reproduce the multi-agent workflow across runtimes.

**Concrete example — Claude subagent → Codex:**

```toml
# .codex/config.toml
[profiles.explorer]
model = "gpt-5"
sandbox_mode = "read-only"
```

```markdown
# AGENTS.md
## explorer
Explore repo, do NOT modify files.
```

```bash
codex exec --profile explorer "Explore repo"
```

Run multiple roles in parallel by launching multiple `codex exec` processes (one per tmux pane).

## Orchestrator Skill Translation

Some skills are **orchestrators** — their body dispatches multiple subagents in parallel and consolidates results (e.g. `.claude/skills/code-review/`, `.claude/skills/review-architecture/`). Copying the body verbatim produces a broken workflow on runtimes without a native agent primitive.

### Decomposition

Split the orchestrator into three layers:

| Layer | Runtime-specific? | Canonical home |
|---|---|---|
| Content — prompts, domain checks, report templates | No | `docs/<workflow>-playbook.md` |
| Roles — per-subagent persona prompts | No | `agents/<role>.md` (see Multi-Agent Orchestration above) |
| Control flow — parallel dispatch + consolidation | **Yes** | per-runtime binding |

### Control-flow strategies

Pick per target runtime. Rank by parity; do not silently downgrade.

| Strategy | Parity | Mechanism | Target fit |
|---|---|---|---|
| A. Native agent primitive | `equivalent` | Target has a subagent tool | Claude only today |
| B. Subprocess fanout | `equivalent` with caveats | Shell spawns N `codex exec --profile X` in parallel, collects output, runs a consolidator process | Codex, Aider |
| C. Serialized playbook | `partial` | Main agent walks single-threaded through `docs/<workflow>-playbook.md` | Cursor, Continue |
| D. Declared runtime-only | `missing` | `AGENTS.md` states "workflow X only supported on runtime Y" | When translation isn't worth the infra |

### Discovery & collisions

| Runtime | Auto-discovers | Needs explicit pointer |
|---|---|---|
| Claude | `.claude/skills/`, `.claude/agents/` | `agents/`, `docs/`, `tools/` |
| Codex | `.codex/config.toml`, `AGENTS.md` | everything else |
| Cursor | `.cursor/rules/`, `AGENTS.md` | everything else |
| Continue | `.continue/`, `AGENTS.md` | everything else |
| Aider | `.aider*`, `AGENTS.md` | everything else |

Same workflow name across runtimes is fine — different folders eliminate collision. `agents/` is never auto-discovered; `AGENTS.md` routes every runtime to the right binding.

### DRY convention

When a role file must exist in both `agents/<role>.md` (canonical) and `.claude/agents/<role>.md` (Claude binding), duplicate the body and append a footer to the binding:

```
<!-- Canonical source: agents/<role>.md — keep in sync. -->
```

Symlinks break on Windows; build-script inlining adds infra. Duplication + periodic lint is the minimum viable approach.

### Example layout (code-review)

```text
docs/code-review-playbook.md          # neutral content: prompts, checks, report template
agents/<role>.md                      # neutral role prompts (x12)
.claude/skills/code-review/SKILL.md   # Claude binding: uses Agent tool, references playbook
.claude/agents/<role>.md              # mirrors agents/<role>.md (+ footer)
.codex/config.toml                    # [profiles.<role>] per role
tools/code-review/run.sh              # Codex subprocess fanout orchestrator
AGENTS.md                             # workflow routing table
```

## Scoping Rules

- Put cross-cutting rules in root `AGENTS.md`.
- Put directory-specific rules in the nearest subdirectory `AGENTS.md`.
- Put role-specific prompts or long-lived agent instructions in `agents/`.
- Put executable behavior in `tools/` or scripts, not in prose.
- Put runtime controls in a runtime's own config file only when they are actually runtime controls, not behavioral rules in disguise.

## Enforcement Rules

- If a runtime-specific hook or check prevented bad states, prose alone is a downgrade. Translate it into an executable check where possible.
- If a runtime-specific rule changed how files in one subtree should be edited, a subdirectory `AGENTS.md` is usually the cleanest replacement.
- If a runtime-specific command bundled a repeatable procedure, prefer a script or tool wrapper over a long natural-language recipe.
- If no executable replacement is possible, document the workflow in the narrowest relevant `AGENTS.md` and make the trigger condition explicit.

## Audit Questions

- Which runtime-specific surfaces exist in the repo today, and for which runtimes?
- What exact behavior does each one create?
- Is that behavior still needed across every runtime the repo supports?
- What is the single canonical runtime-neutral home for that behavior?
- Is the replacement equally enforceable, or did it degrade from executable to advisory?
- For surfaces that stay runtime-specific on purpose, which runtime owns them, and why can't they be neutralized?
