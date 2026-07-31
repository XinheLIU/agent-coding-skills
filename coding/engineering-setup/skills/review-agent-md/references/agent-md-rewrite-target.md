# AGENTS.md Rewrite Target

Last updated: 2026-04-19

Use this for `normalize` after any translation decisions are settled. Do not use it for translation-only work.

Rewrite `AGENTS.md` from scratch instead of patching the old structure.

## Canonical AGENTS.md Structure

`AGENTS.md` is the runtime-neutral entry point: every agent the repo supports (Claude, Codex, Cursor, Continue, Aider, ...) should be able to read it first and get the cross-cutting rules. Keep the same base skeleton as the CLAUDE review, plus one section for the agent surface. Omit a section only when it has nothing non-obvious to say.

```markdown
## Project Overview
[A concise one-sentence definition of the project’s nature and core objectives (to enable the Agent to establish a holistic understanding of the project)]

## Tech Stack
[Programming languages, frameworks, databases, testing tools, and other relevant technical components (to prevent the Agent from recommending mismatched or inappropriate technologies)]

## Project Structure
[Directory layout and corresponding functional responsibilities (to guide the Agent on the correct placement of code files)]

## Architecture Decisions
[WHY + WHAT for each non-obvious decision. No implementation detail.]

## Coding Standards
[Naming conventions, code style guidelines, and prohibited practices (to unify consistent code style across the team).]

## Workflow
[Commit specifications, branching strategy, CI/CD pipeline rules, key commands, and run/startup instructions (to align with the team’s established working process)]

## Special Constraints
[Security requirements, performance requirements, compliance requirements, and other mandatory rules (to ensure adherence to non-negotiable bottom-line standards)]

## Key Extension Points
[Table: goal -> exact file and function to edit.]

## Agent Surface
[Table: path | runtime | owner | purpose | when to edit]

## Context Files
[Table: file path | read-when trigger condition]
```

`runtime` in the Agent Surface table is one of `neutral`, `claude`, `codex`, `cursor`, `continue`, `aider`, etc. Use `neutral` for anything every agent should respect (`AGENTS.md`, `agents/`, `tools/`, scripts). Use a specific runtime only when the file is genuinely consumed by that runtime alone.

For **agent roles** (subagents), the Agent Surface table must record, for each role:

- the runtime-neutral prompt file (usually `agents/<role>.md`)
- the per-runtime binding file (e.g. `.claude/agents/<role>.md`, `[profiles.<role>]` in `.codex/config.toml`, etc.)
- the invocation command per supported runtime (e.g. `codex exec --profile <role>` for Codex; "Agent tool, subagent=<role>" for Claude)

Agent roles are **not** portable by copy — skills are, subagents are not. The translation pattern (orchestrator decomposition, 4-strategy menu) lives in the `translate-agent-context` skill — flag the gap during audit and recommend that skill, do not port mechanisms here.

## Agent Surface Rules

- `AGENTS.md` is the runtime-neutral entry point, not the place to inline full agent prompts.
- Root `AGENTS.md` should state cross-cutting rules that every supported runtime needs.
- Use subdirectory `AGENTS.md` files for subtree-specific rules that used to live in runtime-scoped rules (`.claude/rules/`, `.cursor/rules/`).
- Repo-owned prompt or role definitions belong in `agents/` when they need their own lifecycle.
- Repo-owned executable integrations belong in `tools/`.
- Runtime-specific settings (`.codex/config.toml`, `.cursor/rules/*.mdc`, `.aider.conf.yml`, ...) stay in their runtime's own folder **only** when they are genuinely runtime toggles, not behavioral rules in disguise.
- Runtime-specific automation the repo intentionally keeps (e.g. `.claude/skills/`) should be labeled as optional unless that runtime is a first-class consumer.
- Do not invent extra `.xxx/` subtrees just to hold content that belongs more clearly in `agents/` or `tools/`.
- If a prior runtime-specific mechanism was executable or enforced, the replacement should usually stay executable or enforced rather than becoming advisory prose.

## Required Translation Output

The final rewrite package must make the replacement surfaces explicit:

- cross-cutting behavioral rules -> root `AGENTS.md`
- directory-scoped rules -> subdirectory `AGENTS.md`
- role-specific prompts -> `agents/*.md`
- executable workflows or hook replacements -> `tools/` or scripts
- runtime toggles -> the runtime's own config file, only when they are actually runtime settings

Include every translated behavior in the audit report's mechanism-translation map before applying changes.

## Anti-Patterns to Reject

- Treating any runtime's `.xxx/` folder as a dumping ground for all agent-related files
- Listing one runtime's mechanism as if every runtime consumes it directly
- Deleting a runtime's rules, hooks, or commands without porting the behavior they carried
- Embedding large prompt bodies in `AGENTS.md` when they belong in `agents/*.md`
- Duplicating tool behavior in both `AGENTS.md` and `tools/` docs
- Keeping parallel copies of the same rule across multiple runtime folders without naming the canonical home
- Replacing an enforced hook with vague prose when a script, tool, or CI check should own it

## Restructure Rules

1. Rewrite the file from scratch. Do not incrementally preserve the old structure.
2. Keep the canonical section order exactly as listed above.
3. Consolidate duplicates ruthlessly. A fact appears once, in the best section, and nowhere else.
4. Keep `AGENTS.md` focused on cross-cutting guidance; move scoped rules into subdirectory `AGENTS.md` and agent-specific detail into `agents/` or `tools/`.
5. Translate still-needed runtime-specific behaviors into runtime-neutral surfaces before deleting their original home.
6. Explicitly label any retained runtime-specific artifacts instead of pretending they are neutral.
7. Kill filler: repetitive intros, decorative separators, and prose that does not change behavior.
8. Keep a hard ceiling of 220 lines. If the rewrite exceeds that, more content belongs elsewhere.
9. Define forbidden patterns ("Don't X -> do Y instead") and detailed rules directly in AGENTS.md or in runtime-neutral rules, as AGENTS.md lacks a `.claude/rules.md` equivalent.

## Execution Order

1. Build the mechanism-translation map for every runtime-specific surface and confirm every still-needed behavior has a destination.
2. Apply folder and file operations first: creates, merges, deletes, renames, and relocations across `AGENTS.md`, subdirectory `AGENTS.md`, `agents/`, `tools/`, and each runtime's `.xxx/` folder.
3. Rewrite `AGENTS.md` with the full new content.
4. Update all cross-references across Markdown files and agent-owned files.
5. Verify referenced paths still exist, the `Agent Surface` table matches the repo, and translated behaviors are represented in their new homes.
6. Check the final line count and flag anything that should be extracted if the file is still too long.
