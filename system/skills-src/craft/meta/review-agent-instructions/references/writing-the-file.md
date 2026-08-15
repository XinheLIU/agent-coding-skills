# Writing the File

Last updated: 2026-08-06

Load during a Mode 2 rewrite. This is guidance on what each section is *for*, not a template to fill — a section with nothing non-obvious to say should be omitted, not padded.

## Section order

The order below front-loads orientation and pushes reference material to the back, which is the order an agent needs it in. Keep it unless the project has a reason to differ.

```text
Project Overview          what this is, in a sentence or two
Tech Stack                languages, frameworks, datastores, test tooling
Project Structure         directory → responsibility
Architecture Decisions    the non-obvious ones, with reasons
Coding Standards          pointer to rules files, not rule bodies
Workflow                  commands, branch and commit conventions
Special Constraints       security, performance, compliance — non-negotiable
Key Extension Points      goal → file and function to edit
Agent Surface             AGENTS.md only: path | runtime | owner | when to edit
Shared Memory             startup sequence + pointer to docs/agents/memory.md
Context Files             path | the trigger that should make an agent read it
```

Earned when the project has them, usually near the back: **Danger Zones** (code that breaks things when touched) and **Historical Baggage** (designs that look wrong but have reasons). On a legacy codebase these are the most valuable sections in the file and deserve real space — they are also where post-incident lessons land.

## What each section is for

**Project Overview.** Enough for an agent to know what domain it is in. Not the origin story, not the roadmap.

**Tech Stack.** Exists to stop the agent suggesting mismatched technology. Name versions only where the version genuinely constrains what you can write.

**Project Structure.** A small table, one sentence of responsibility per module. The detailed dependency graph belongs in the code index — link it, never restate it as prose.

**Architecture Decisions.** WHY plus WHAT, no implementation detail. One paragraph and a link to the diagram. A decision with no reason recorded is not a decision, it is a description of the current state.

**Coding Standards.** Prefer a pointer to `.claude/rules/*.md` or `docs/conventions/*.md` (owned by `extract-rules`) over inlining. Anything inlined here should be a hard rule with no rationale needed — "all REST responses are wrapped in `Result`", "DB columns snake_case, Java fields camelCase". Cut anything generic: standards that are not specific to this project only dilute the ones that are.

**Workflow.** Literal commands the agent can run — start, test, lint. One sentence plus a link for anything longer than a command. Include commit, branch, or PR conventions only where the repo actually diverges from the default.

**Special Constraints.** Non-negotiable rules, each stated so something could check it. Name the frozen contract and the test that covers it, not "be careful".

**Key Extension Points.** A table from intent to location: "add a new payment provider" → the file and function. This is the section that saves the most agent search time per line spent.

**Agent Surface** (AGENTS.md only). Table of every agent-facing path: `path | runtime | owner | purpose | when to edit`. `runtime` is `neutral` for anything every agent should respect (`AGENTS.md`, `agents/`, `tools/`, scripts) and a specific runtime (`claude`, `codex`, `cursor`, …) only when that file is genuinely consumed by that runtime alone. Never inline full prompt bodies here — they belong in `agents/`. Agent roles are not portable by copying; when a role needs to work across runtimes, flag it for `translate-agent-context` rather than porting the mechanism here.

**Shared Memory.** The startup sequence plus a pointer to `docs/agents/memory.md`. Never restate that file's configuration; it is owned by `manage-context`.

**Context Files.** Path plus trigger. The trigger is the load-bearing half: "read before changing any API response shape" earns the row, "background information" does not.

## The recurring failure

Writing too much. Prose restatements of the architecture diagram, the whole interface inventory, every table and column — thousands of lines loaded on every startup, crowding out the few facts that would actually have changed the agent's behavior.

| Include | How to write it |
| --- | --- |
| What the project is | One sentence |
| Core architecture | One paragraph plus a link to the diagram |
| Key modules | Small table, one sentence each |
| Key conventions | Hard rules, no rationale |
| How to run it | Literal commands, or one sentence plus a link |
| Danger zones and historical baggage | The sections worth real space |

Leave out entirely: full architecture detail, the full interface inventory, the full data model — all three already live in `docs/`. Also leave out generic coding standards and project backstory.

## Reject these

- Prose that restates an asset which already exists as a diagram, list, or schema
- Unverifiable constraints — "keep it clean", "be careful", "use good judgment"
- Speculative rules with no incident behind them, written to look thorough
- Headings with a single orphan bullet that belongs in a neighboring section
- Intro lines like "This file provides guidance to Claude Code"
- The same warning repeated in several sections
- Large prompt bodies that belong in `agents/`
- Runtime-specific rules presented as neutral (AGENTS.md)
- The same rule copied across several runtime folders with no canonical home named
- Raising the line budget instead of evicting content
