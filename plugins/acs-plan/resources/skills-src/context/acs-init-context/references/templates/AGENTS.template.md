# {{PROJECT_NAME}} — Agent Guide

<!-- Keep this file under 200 lines. It is an index, not an encyclopedia.
     Anything that grows past a few lines belongs in docs/ with a pointer here. -->

Last updated: 2026-09-25

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

Route Persistent Intent, Current and Changes plus Working recovery here. Current summaries cite executable evidence; human reports and indexes are derived views.

| I want to know... | Read |
| --- | --- |
| What a domain term means, and which word to avoid | {{terminology doc}} |
| Why a hard-to-reverse choice was made | {{decision-record directory}} |
| What problem the product solves, and what is out of scope | {{product-intent directory}} |
| A constraint that binds the project from outside | {{whichever of the above owns it}} |
| Requirements, accepted decisions, and final evidence for this change | {{canonical change/ticket/spec}} |
| Applicable system boundaries and operational constraints | {{current-state docs and source evidence}} |
| What is happening right now | {{configured recovery entry}} |

<!-- Every path here must resolve. Delete rows whose target you did not create. -->

## Code index

<!-- Delete this section if no index is built. -->

This repo is indexed with {{tool}}; the index lives at `{{path}}`.
Query it with `{{command}}` or the `{{mcp-tool}}` MCP tool before grepping for
symbols, callers, or change impact. Refresh with `{{refresh-command}}`.

## Session start

<!-- Delete this section if working memory is not set up. -->

1. Run `{{init script}}` to verify the environment.
2. Read `git log --oneline -10` for recent history.
3. Read `{{configured recovery entry}}` for canonical change/status pointers and the next action, then follow its pointers.

## Working rules

<!-- Genuine constraints only. Generic advice earns no place here. -->

1. **Read the code for structure.** Derive module boundaries and patterns from the
   source or a source-verified index; Persistent Current explains applicable boundaries.
2. **Verify before claiming.** Confirm a relationship against the code, never
   against another document.
3. **Record a decision where decisions live.** When a change settles a
   consequential trade-off, retain its rationale and update applicable Persistent Current.
4. {{Project-specific rule.}}

## Do not

<!-- Real prohibitions with real consequences. Delete this section rather than pad it. -->

- {{e.g. Do not edit generated/ by hand — it is regenerated on build.}}
- {{e.g. Do not import UI components in the service layer — it breaks the build.}}
