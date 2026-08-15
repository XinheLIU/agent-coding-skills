# {{PROJECT_NAME}} — Agent Guide

<!-- Keep this file under 200 lines. It is an index, not an encyclopedia.
     Anything that grows past a few lines belongs in docs/ with a pointer here. -->

Last updated: {{YYYY-MM-DD}}

## What this project is

{{One to three sentences: what it does, who it serves, why it exists.}}

## Orientation

- **Tech stack**: {{language}} + {{framework}} + {{key tools}}
- **Entry point**: {{e.g. src/main.ts, app/main.py}}
- **Start**: `{{literal command}}`
- **Test**: `{{literal command}}`
- **Lint / typecheck**: `{{literal command}}`

<!-- Literal commands only. "See the docs" is not a command. -->

## Knowledge map

Read the relevant file before changing anything.

| I want to know... | Read |
| --- | --- |
| Module boundaries, dependency direction | `docs/ARCHITECTURE.md` |
| Naming rules, code style | `docs/CONVENTIONS.md` |
| Why a technology was chosen | `docs/TECH_DECISIONS.md` |
| What counts as done | `docs/QUALITY.md` |
| Plans in flight | `docs/exec-plans/active/` |
| Known but unscheduled work | `docs/exec-plans/backlog.md` |
| Known technical debt | `docs/exec-plans/tech-debt-tracker.md` |

<!-- Every path here must resolve to a file that exists. Delete rows you did not create. -->

## Code index

<!-- Delete this section if no index is built. Written by `index-codebase`. -->

This repo is indexed with {{tool}}; the index lives at `{{path}}`.
Query it with `{{command}}` or the `{{mcp-tool}}` MCP tool before grepping for
symbols, callers, or change impact. Refresh with `{{refresh-command}}`.

## Session start

<!-- Delete this section if working memory is not set up. Written by `manage-context` Phase A. -->

1. Run `{{init script}}` to verify the environment.
2. Read `git log --oneline -10` for recent history.
3. Read `{{work-root}}/state.md` for status and the next action, then follow its pointers.

## Working rules

1. **Read before changing.** Consult the architecture doc before modifying a module.
2. **Verify before claiming.** Confirm a relationship with a grep rather than inferring it from file layout.
3. **Keep docs current.** If a change alters architecture or conventions, update `docs/` in the same pass.
4. **Ask rather than guess.** When the docs do not answer it, ask.
5. {{Project-specific rule.}}

## Do not

<!-- Real prohibitions with real consequences. Delete this section rather than pad it. -->

- {{e.g. Do not edit generated/ by hand — it is regenerated on build.}}
- {{e.g. Do not import UI components in the service layer — see docs/ARCHITECTURE.md.}}
