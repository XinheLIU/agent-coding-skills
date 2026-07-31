# Agent Surface Checklist

Last updated: 2026-04-19

Use this for `audit`, `translate`, or `normalize` work before proposing any rewrite or migration.

Reading this file does **not** imply normalization work. Audit and translation can stop without any folder changes.

## Two-Layer Model

The agent context in a repo splits into two layers:

- **Runtime-specific** — files consumed by one agent runtime: `.claude/`, `.codex/`, `.cursor/`, `.continue/`, `.aider*`, etc. Each runtime only reads its own folder.
- **Runtime-neutral** — files every agent should respect: `AGENTS.md` (entry point), subdirectory `AGENTS.md`, `agents/*.md` (role prompts), `tools/` (executables), scripts, CI checks.

The skill's job is to inventory the runtime-specific layer and extract still-needed behavior into the runtime-neutral layer so every agent the repo uses can follow the same rules.

## What to Inventory

### Runtime-neutral surfaces (these should own most shared behavior)

- `AGENTS.md` as the canonical entry-point context file
- subdirectory `AGENTS.md` files for scoped instructions
- files referenced directly by `AGENTS.md`
- `agents/` for repo-owned agent role or prompt files
- `tools/` for repo-owned executors, wrappers, or integrations
- scripts and CI checks that enforce behavior

### Runtime-specific surfaces (inventory, then translate)

- `.claude/CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, `.claude/commands/`, `.claude/agents/*.md` (subagent definitions), Claude hook definitions in `.claude/settings*.json`
- `.codex/config.toml` and anything else under `.codex/`
- `.cursor/rules/*.mdc`, legacy `.cursorrules`
- `.continue/` config and prompt files
- `.aider.conf.yml`, `.aider.model.settings.yml`, and similar tool configs
- any other `.xxx/` folder a runtime uses to discover its own config

### Likely duplication sites

- root-level docs that duplicate agent guidance already covered above
- multiple runtime configs that encode the same rule in different dialects

## Skills Copy, Subagents Don't

Skills (`.claude/skills/`, other runtime equivalents) are usually folders of self-contained prose + references and can be copied between runtimes or repos almost as-is.

Subagent / multi-agent mechanisms do **not** transfer by copying files. They are runtime-specific in form:

- Claude: `.claude/agents/*.md` — auto-discovered by frontmatter, invoked via the Agent tool in one session.
- Codex: `[profiles.X]` in `.codex/config.toml` + prompt section in `AGENTS.md` — invoked as a separate process with `codex exec --profile X`; parallelism = multiple processes (often tmux).
- Cursor / Continue / Aider: each has its own (or no) convention.

Translation requires splitting the role into (a) a runtime-neutral prompt in `agents/<role>.md` and (b) a small per-runtime binding that points at it plus the runtime's invocation mechanism. The audit only flags the gap; the concrete translation pattern lives in the `translate-agent-context` skill.

## Runtime-Specific vs Runtime-Neutral — What Goes Where

- Rules every agent must follow → `AGENTS.md` (root for cross-cutting, subdirectory for scoped).
- Role-specific prompts or long-lived agent instructions → `agents/*.md`.
- Executable integrations, wrappers, and tool surfaces → `tools/` or scripts.
- Enforced checks (formerly hooks) → scripts + CI or pre-commit.
- True runtime toggles that only one runtime consumes → stay in that runtime's config (`.codex/config.toml`, `.cursor/rules/*.mdc`, etc.).
- Runtime-specific automation the repo intentionally keeps (e.g. a Claude skill) → stay under its `.xxx/` folder and be labeled optional.

Do not invent new `.xxx/` subtrees just to hold content that belongs in `agents/` or `tools/`.

## Behavioral Parity Rule

Do not frame the audit as "what features does runtime X not support?" Frame it as "what repo behavior must still happen regardless of which runtime the user runs today?"

For every runtime-specific surface:

1. Name the behavior it created.
2. Decide whether the behavior is still required across runtimes.
3. Translate it into one explicit runtime-neutral home.
4. Mark whether the replacement is `equivalent`, `partial`, or `missing`.

The audit is incomplete until every still-needed runtime-specific behavior has a runtime-neutral destination (or is explicitly marked runtime-specific on purpose).

## Folder Layout to Consider

Use this as a common pattern, not a forced template:

```text
AGENTS.md
agents/
  <role>.md             # runtime-neutral role prompts
skills/                 # runtime-neutral shared skills, category-organized
  prompt/<name>/SKILL.md
  coding/<name>/SKILL.md
  data/<name>/SKILL.md
tools/
  <workflow>/run.sh     # runtime-neutral executable bindings

.claude/
  skills -> ../skills   # symlink (unless skill has a Claude-specific version below)
  skills/<name>/        # only when skill has a runtime-specific Claude flavor
  agents/<role>.md      # Claude role bindings (mirror agents/<role>.md)
.codex/
  skills -> ../skills   # symlink (unless skill has a Codex-specific version below)
  skills/<name>/        # only when skill has a runtime-specific Codex flavor
  config.toml           # Codex profile bindings for roles
.cursor/
  rules/                # Cursor-only rules, keep minimal
```

Rule: when a skill's behavior is identical across runtimes, put it under `skills/<category>/<name>/` and symlink. When a skill has runtime-specific flavors (e.g. orchestrators with different dispatch primitives), keep each version under `.claude/skills/<name>/` or `.codex/skills/<name>/` and share the contract via `docs/<workflow>-playbook.md`.

## Migration Rules

- If a runtime-specific artifact matters only because that runtime is still supported, classify it as `keep` and mark the consumer explicitly.
- If the behavior matters to every agent the repo supports, classify it as `translate` and give it a runtime-neutral home.
- If a runtime-specific artifact is obsolete, classify it as `archive` or `delete`, but only remove it on confirmation.
- If `AGENTS.md` duplicates content that belongs in `agents/`, subdirectory `AGENTS.md`, or `tools/`, move the detail out and keep `AGENTS.md` as the entry point.
- If agent prompts, scripts, and configs are scattered across unrelated folders, propose a cleanup plan that gives each artifact one obvious home.
- Do not delete a runtime's rules, hooks, or commands until their behavior has either been translated or explicitly marked unnecessary.
