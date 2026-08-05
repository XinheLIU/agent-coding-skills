---
name: review-agent-instructions
description: >
  Audit and restructure CLAUDE.md or AGENTS.md and every file they reference.
  Detects which file is present and applies the appropriate canonical skeleton:
  9-section + Context Files for CLAUDE.md (200-line ceiling); 9-section + Agent
  Surface + Context Files for AGENTS.md (220-line ceiling). Produces a MECE
  rewrite and a concrete change list. Use when the user asks to "review CLAUDE.md",
  "review AGENTS.md", "audit context files", "shrink CLAUDE.md / AGENTS.md",
  "deduplicate context docs", or "restructure to canonical form". Does NOT extract
  or document agent-behavior rules or coding conventions — see `extract-rules`.
  Does NOT translate Claude-specific surfaces to agent-agnostic form — see
  `translate-agent-context`.
---

# Review Agent Instructions

Last updated: 2026-08-05

**Announce at start:** "I'm using the review-agent-instructions skill to audit your `CLAUDE.md` / `AGENTS.md`."

## Layer

Human layer of the context-management collection. Owner of `CLAUDE.md` and `AGENTS.md` structure. The canonical index shapes are the templates shipped by `scaffold-agent-docs`; this skill keeps them canonical and under their line ceilings.

Preserve, and verify the accuracy of, any section pointing to the code index (written by `index-codebase`) or the session-start sequence (written by `manage-context` Phase A). Removing those pointers to save lines makes the wiki and working layers invisible — if the file is over its ceiling, move the detail into `docs/` and keep the pointer.

## Goal

Audit the target file and every file it references. Produce a concrete change list, then apply on user confirmation. This skill owns the **content shape** of the file — its canonical structure, section ordering, the docs it links to, and dedup across that set. It does not own rules extraction or cross-runtime translation.

## Detect: CLAUDE.md or AGENTS.md

At the start, check which file is present:

- **`CLAUDE.md` present** → apply CLAUDE.md rules (200-line ceiling, 9-section skeleton without Agent Surface).
- **`AGENTS.md` present** → apply AGENTS.md rules (220-line ceiling, 9-section skeleton with Agent Surface table).
- **Both present** → ask the user which to audit first, or audit both in sequence.
- **Neither present** → recommend `scaffold-agent-docs` to create them from templates.

## Scope

| In scope (this skill) | Out of scope — handoff |
|---|---|
| File structure & content audit | Cross-runtime translation (CLAUDE.md ↔ AGENTS.md) → `translate-agent-context` |
| Canonical skeleton + line ceiling | Rule extraction & routing (static / dynamic / implicit) → `extract-rules` |
| Subdirectory `AGENTS.md` / scoped `CLAUDE.md` cleanup | Orchestrator decomposition → `translate-agent-context` |
| `agents/`, `tools/` placement clarity (AGENTS.md only) | Slash command / hook portage → `translate-agent-context` |
| MECE dedup across the file and its referenced docs | — |
| `Context Files` table shape | — |
| Agent Surface table shape (AGENTS.md only) | — |

If the audit surfaces rule-shaped content embedded in prose, **flag it** for eviction — do not rewrite the rule body here. Recommend `extract-rules`.

## Workflow

### Step 1 — Inventory

1. Read the target file in full.
2. Collect every file path mentioned anywhere: inline code paths, links, tables, comments, examples.
3. Read each collected file in full.
4. Record `exists`, `missing`, or `empty` for each path.
5. For AGENTS.md audits: also record subdirectory `AGENTS.md` files (subtree-scoped rules are part of the audit surface).

### Step 2 — Cross-File MECE Analysis

Map the full content landscape across the target file and every referenced file. For each piece of information, ask: is this the single canonical home, or does it duplicate another file?

Build a content ownership map:

```text
Topic -> owned by <file> | duplicated in <file-a>, <file-b>
```

Common MECE violations:

- Same commands appear in both the target file and a referenced doc.
- Architecture described in both the target file and a doc file.
- Setup steps split across multiple files without clear ownership.
- Two doc files cover overlapping subsystems with no clear boundary.
- A doc file is two unrelated topics stapled together.
- Rules duplicated across the target file and runtime-specific dirs without naming a canonical home (AGENTS.md audits).

### Step 3 — Per-File Analysis Against the 12 Principles

For the target file and each referenced file, record each issue as:

- `File`, `line range`, `principle #`, `problem` (one sentence), `fix` (concrete action)

Load [common-audit-workflow.md](references/common-audit-workflow.md) for the full 12-principle list and audit step detail.

### Step 4 — Audit Report

Produce the report using this template (substitute the actual filename for `<FILE>`):

```markdown
## <FILE> Audit Report

### Summary
- <FILE>: <N> lines
- Referenced files: <list — exists/missing>
- Subdirectory AGENTS.md files: <list> [AGENTS.md audits only]
- MECE violations: <count>
- Other issues: <count>
- Rule-shaped content to evict (handoff to extract-rules): <count>
- Cross-runtime parity gaps (handoff to translate-agent-context): <count> [AGENTS.md audits only]

### Content Ownership Map
| Topic | Canonical Home | Also appears in |
|---|---|---|

### MECE Violations
| # | Topic | Files | Problem | Fix |
|---|---|---|---|---|

### Per-File Issues
#### <FILE>
| # | Lines | Principle | Problem | Fix |
|---|---|---|---|---|

### Rule-Shaped Content (handoff to extract-rules)
| Lines | Content type | Suggested home |
|---|---|---|

### Cross-Runtime Parity Gaps (handoff to translate-agent-context) [AGENTS.md only]
| Source surface | Behavior | Missing in |
|---|---|---|

### Proposed File Operations
- CREATE: <path> — <reason>
- DELETE: <path> — <reason>
- RENAME: <old> → <new> — <reason>
- MERGE: <file-a> + <file-b> → <target> — <reason>
- SPLIT: <file> → <file-a> + <file-b> — <reason>
```

For AGENTS.md rewrites, load [agent-md-rewrite-target.md](references/agent-md-rewrite-target.md) for the Agent Surface table rules and anti-patterns. For surface inventory, load [agent-surface.md](references/agent-surface.md).

### Step 5 — Confirm and Apply

Ask: **"Apply all changes? (yes / yes but skip #N,M / no)"**

On confirmation, execute in this order:

1. Apply file operations: merges, splits, deletes, renames of referenced docs.
2. Rewrite the target file with full new content (see Canonical Structures below).
3. Update all cross-references across Markdown files.
4. Verify referenced paths still exist; verify Agent Surface table matches the repo (AGENTS.md only).
5. Check the final line count; flag anything that should be extracted if still too long.

## Canonical Structures

Rewrite from scratch — do not patch the old structure.

### CLAUDE.md (200-line ceiling)

Read the exact blueprint from [claude-md-template.md](references/claude-md-template.md).

Sections (omit only when nothing non-obvious to say):

```markdown
## Project Overview
## Tech Stack
## Project Structure
## Architecture Decisions
## Coding Standards        ← link to .claude/rules/*.md; don't inline rule bodies
## Workflow
## Special Constraints
## Key Extension Points    ← table: goal → file/function
## Context Files           ← table: file path | read-when trigger
```

Optional when the project earns them: `## Danger Zones`, `## Historical Baggage`.

### AGENTS.md (220-line ceiling)

Same base skeleton as CLAUDE.md plus one section for the agent surface:

```markdown
## Project Overview
## Tech Stack
## Project Structure
## Architecture Decisions
## Coding Standards        ← inline (short) or link to docs/conventions/*.md (long)
## Workflow
## Special Constraints
## Key Extension Points    ← table: goal → file/function
## Agent Surface           ← table: path | runtime | owner | purpose | when to edit
## Context Files           ← table: file path | read-when trigger
```

`runtime` in the Agent Surface table is one of `neutral`, `claude`, `codex`, `cursor`, `continue`, `aider`, etc. For agent roles (subagents), record the runtime-neutral prompt file, per-runtime binding file, and invocation command per supported runtime. Agent roles are not portable by copy — see `translate-agent-context` for the decomposition pattern.

## Content Constraints

### What belongs

- Project overview, tech stack, module responsibilities, architecture decisions (WHY+WHAT, no implementation detail)
- Key conventions as pointers, not prose rule bodies
- How to run: one-sentence summary + link to docs
- Danger zones and historical baggage (legacy projects)
- Entry-point pointers only — every cross-reference says *when* to read the target

### What must not be inlined

- Full architecture details, full API lists, full data models → move to `docs/`
- Generic coding standards → link to `.claude/rules/*.md` or `docs/conventions/*.md`
- Backstory, origin story, organizational context

## Anti-Patterns to Reject

- Heading-plus-one-bullet sections that belong in a neighbor
- Intro lines like "This file provides guidance to Claude Code"
- Repeating the same warning in multiple sections
- Embedding large prompt bodies when they belong in `agents/`
- Runtime-specific rules pretending to be neutral (AGENTS.md)
- Parallel copies of the same rule across multiple runtime folders without naming a canonical home

## Restructure Rules

1. Rewrite from scratch. Do not incrementally preserve the old structure.
2. Keep the canonical section order exactly as listed above.
3. Consolidate duplicates ruthlessly — a fact appears once, in the best section.
4. Move scoped rules into subdirectory files; move long procedures to `docs/` or scripts.
5. Kill filler: repetitive intros, decorative separators, prose that does not change behavior.
6. Hard ceilings: 200 lines for CLAUDE.md, 220 for AGENTS.md. Anything over belongs in a doc.

## Guardrails

- **Never delete** content encoding non-obvious decisions or historical rationale — move it instead.
- **Never shorten** a file without confirming its unique content is preserved somewhere.
- **Never create** a new file if the content fits cleanly into an existing one.
- **Never absorb** a doc into the target file if doing so would breach the ceiling.
- **Always rewrite to canonical structure** — incremental edits that preserve old layout defeat the purpose.
- **Dedup is mandatory** — if the audit finds the same fact in 3 places, the rewrite has it in exactly 1.
- **Never rewrite rule bodies** — flag for eviction and recommend `extract-rules`.
- **Never port mechanisms** — cross-runtime translation is `translate-agent-context`'s job.

## Handoffs

**→ `extract-rules`:** when the audit surfaces rule-shaped content (naming, formatting, API patterns, dynamic per-task guardrails, implicit "do not delete" markers). List each in the "Rule-Shaped Content" section of the audit report; recommend `extract-rules` after this skill finishes.

**→ `translate-agent-context`:** when the audit reveals cross-runtime parity gaps — behaviors carried only by Claude-specific surfaces, or CLAUDE.md and AGENTS.md drifted out of parity. List each gap in the "Cross-Runtime Parity Gaps" section.

**→ `review-agent-instructions` (the other file):** if auditing CLAUDE.md reveals AGENTS.md needs work, or vice versa, note it and recommend running this skill again on the other file.
