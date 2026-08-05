---
name: translate-agent-context
description: >
  Port Claude-specific surfaces (CLAUDE.md, .claude/rules/, slash commands, hooks,
  .claude/skills/, orchestrator subagents) into agent-agnostic equivalents that
  Codex / OpenCode / Cursor can consume. Owns the orchestrator decomposition
  4-strategy menu, shared skills/ symlink layout, and mechanism-translation map.
  Use when the user asks to "port Claude setup to Codex", "sync Claude and AGENTS.md",
  "translate slash commands", "make my Claude skills work in OpenCode", or "set up
  cross-runtime parity". Does NOT audit AGENTS.md or CLAUDE.md content shape — see
  `review-agent-instructions`. Does NOT discover or classify rules
  from code — see `extract-rules`.
---

# Translate Agent Context

Last updated: 2026-08-02

**Announce at start:** "I'm using the translate-agent-context skill."

## Goal

Port Claude-specific surfaces into agent-agnostic equivalents so Codex / OpenCode / Cursor users get the same behavior. The source artifact stays where it is until its replacement exists; nothing is silently downgraded. When a Claude mechanism has no clean equivalent (e.g., orchestrators that depend on the `Agent` tool), surface the trade-off and let the user pick a strategy.

This skill is the only home for cross-runtime mechanism translation, orchestrator decomposition, and shared `skills/` layout. It does not rewrite content shape — that's `review-agent-instructions`. It does not discover rules from code — that's `extract-rules`.

## Scope: What This Skill Owns

| In scope (this skill) | Out of scope — handoff |
|---|---|
| Translate `.claude/rules/*.md` → AGENTS.md inline / `docs/conventions/*.md` | AGENTS.md structure audit → `review-agent-instructions` |
| Translate slash commands → shell scripts in `tools/` | CLAUDE.md content audit → `review-agent-instructions` |
| Translate hooks → documented rules or CI check | Initial rule discovery from code → `extract-rules` |
| Orchestrator decomposition (4-strategy menu) | — |
| Shared `skills/` layout + cross-runtime symlinks | — |
| Mechanism-translation map across runtimes | — |

## When to Use

Run this skill when at least one of the following holds:

- Repo has both `CLAUDE.md` and `AGENTS.md` and they have drifted out of parity.
- Want to introduce `AGENTS.md` to a Claude-first repo (or vice versa) without losing behaviors.
- Skills exist in `.claude/skills/` and a Codex / OpenCode user wants the same library available.
- A Claude orchestrator skill (uses the `Agent` tool with `subagent_type`) needs an equivalent in another runtime.
- Slash commands or hooks encode behavior that another runtime should respect — typically as a documented rule, a `tools/` script, or a CI check.

Do not run this skill just to clean up AGENTS.md or CLAUDE.md prose — use `review-agent-instructions`. Do not run it to discover what rules the codebase already enforces — use `extract-rules`.

## Workflow

### Step 1 — Surface Inventory

Load [agent-surface.md](references/agent-surface.md). Inventory every context surface in the repo: `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.claude/`, `.codex/`, `.config/opencode/`, `agents/`, `tools/`, `skills/`, `.claude/skills/`, slash-command directories, hook scripts. For each, record:

- Path
- Owning runtime (`claude`, `codex`, `opencode`, `cursor`, `neutral`)
- Current consumer (auto-loaded? referenced from where?)
- Whether the behavior it carries needs to exist in target runtimes

### Step 2 — Translation Map

Mechanism-by-mechanism, decide the target form. For each source artifact, name the destination type and path:

| Source (Claude) | Translation target | Notes |
|---|---|---|
| `.claude/rules/<name>.md` (auto-loaded) | Inline AGENTS.md (short) or `docs/conventions/<name>.md` referenced from AGENTS.md (long) | Keep one canonical body — single-source rule via reference |
| `.claude/commands/<name>.md` (slash command) | Script in `tools/<name>.sh` invocable from any runtime; document trigger in AGENTS.md | If command was Claude-side LLM logic, may need to live as a documented prompt the user pastes |
| `.claude/settings.json` hook (PreToolUse / PostToolUse) | Documented rule + CI check (when enforcement matters) or `tools/` script run via repo's existing pre-commit framework | A hook becoming "advisory prose" is a downgrade — flag it |
| `.claude/skills/<name>/` | Move shared skills to `skills/<category>/<name>/`; keep runtime-specific skills under each runtime's dir | See Step 4 for the symlink layout |
| Subagent / orchestrator skill (uses `Agent` tool) | See Step 3 — requires user choice from 4-strategy menu | Never copy the body verbatim |

Default parity: `equivalent`. If a target runtime cannot match a behavior (e.g., a hook can't be enforced without that runtime owning the lifecycle), drop to `partial` only with explicit user approval per artifact.

### Step 3 — Orchestrator Detection

Grep each candidate skill body for orchestrator markers: `Agent(`, `subagent_type`, `parallel`, `Explore + reviewer`, `dispatch`, `fanout`. If any are present, treat the skill as an orchestrator and load [runtime-parity-translation.md](references/runtime-parity-translation.md) → "Orchestrator Skill Translation".

Present the 4-strategy menu to the user, per target runtime:

- **A. Native** — target runtime has its own subagent dispatch (e.g., Codex profiles). Wire to native primitive.
- **B. Subprocess fanout** — runtime lacks native dispatch; orchestrator shells out to itself or to runtime CLIs to fanout work.
- **C. Serialized** — flatten the parallel work into sequential phases. Simpler, slower, no parallelism.
- **D. Runtime-only** — keep the orchestrator under `.claude/skills/`; do not port. Document the gap in AGENTS.md.

Get explicit user approval per skill, per target runtime. No silent downgrade.

### Step 4 — Shared Skills Layout

When `.claude/skills/` contains skills the user wants in other runtimes, lay out a shared library and symlink each runtime's discovery path at it:

```
skills/                   # canonical shared library, category-organized
  prompt/<name>/SKILL.md
  coding/<name>/SKILL.md
  data/<name>/SKILL.md

.claude/skills -> ../skills    # Claude reads the shared library
.codex/skills  -> ../skills    # Codex reads the shared library
```

Apply at repo level (`<repo>/skills/`) or user level (`~/skills/` + `~/.claude/skills` + `~/.codex/skills`).

When a skill has runtime-specific versions (orchestrators with different dispatch primitives — see Step 3 outcomes), **do not** symlink it into the shared `skills/` dir. Keep each version under its runtime dir and let a shared playbook in `docs/` capture the contract both versions follow:

```
.claude/skills/<name>/SKILL.md   # Claude version (uses Agent tool)
.codex/skills/<name>/            # Codex version (uses subprocess fanout)
docs/<workflow>-playbook.md      # shared contract both versions follow
```

Before replacing `.claude/skills/` or `.codex/skills/` with a symlink, verify the target is writable and contents have been moved — stage the migration, do not force.

### Step 5 — Apply

Confirm before each write step. Approving the plan is not a blanket write approval. Order:

1. Create the new neutral artifacts (`tools/`, `agents/`, `skills/`, `docs/conventions/`).
2. Update AGENTS.md `Agent Surface` table to reflect new surfaces.
3. Stage symlinks for shared `skills/` only after target dirs are populated.
4. Verify each translated behavior has a working destination.
5. Only then delete the original Claude-specific artifact, and only when the user has confirmed.

## Parity Guardrails

- Default parity is `equivalent`. `partial` requires explicit user approval per artifact.
- Never delete the original runtime-specific artifact until its replacement exists and works.
- No opportunistic folder cleanup — that belongs to `review-agent-instructions`.
- Orchestrator skills: never copy the body verbatim across runtimes. Always decompose first (content / roles / control flow).
- Mechanism downgrades (enforced → advisory) are flagged, not silent. The audit report names every downgrade.

## Handoff to review-agent-instructions

After translation produces or modifies AGENTS.md, recommend `review-agent-instructions` to clean up structure (canonical 9-section skeleton, Agent Surface table, 220-line ceiling). This skill makes mechanism-level changes, not structural ones.

## Handoff to extract-rules

If translation surfaces rule-shaped content (e.g., a `.claude/rules/` file that should be re-derived from code rather than ported verbatim, or a hook whose intent is a static rule the codebase doesn't yet document), recommend `extract-rules` for routing.

## Handoff to review-agent-instructions

After translation produces or modifies AGENTS.md or CLAUDE.md, recommend `review-agent-instructions` to clean up structure (canonical 9-section skeleton, Agent Surface table, line ceilings). This skill makes mechanism-level changes, not structural ones.
