---
name: review-agent-instructions
description: >
  Audit and restructure CLAUDE.md or AGENTS.md and every file they reference.
  Detects which file is present and applies the appropriate canonical skeleton:
  9-section + Context Files for CLAUDE.md (200-line ceiling); 9-section + Agent
  Surface + Context Files for AGENTS.md (220-line ceiling). Produces a MECE
  rewrite and a concrete change list. Also handles post-incident intake — folding
  a regression, a bad agent edit, or a repeated correction into the file as one
  checkable rule, so the file accumulates knowledge as the codebase evolves.
  Use when the user asks to "review CLAUDE.md", "review AGENTS.md", "audit context
  files", "shrink CLAUDE.md / AGENTS.md", "deduplicate context docs", "restructure
  to canonical form", or "add this lesson to CLAUDE.md / AGENTS.md". Does NOT
  extract or document agent-behavior rules or coding conventions — see
  `extract-rules`. Does NOT translate Claude-specific surfaces to agent-agnostic
  form — see `translate-agent-context`. Does NOT detect staleness against the code
  — see `manage-context` Phase B.
---

# Review Agent Instructions

Last updated: 2026-08-06

**Announce at start:** "I'm using the review-agent-instructions skill to audit your `CLAUDE.md` / `AGENTS.md`."

## Where This Skill Sits

Two vocabularies overlap here. Keep them separate.

**Collection layer.** Human layer of the context-management collection. Owner of `CLAUDE.md` and `AGENTS.md` structure. The canonical index shapes are the templates shipped by `scaffold-agent-docs`; this skill keeps them canonical and under their line ceilings.

Preserve, and verify the accuracy of, any section pointing to the code index (written by `index-codebase`) or the session-start sequence (written by `manage-context` Phase A). Removing those pointers to save lines makes the wiki and working layers invisible — if the file is over its ceiling, move the detail into `docs/` and keep the pointer.

**Reliability chain.** Agent reliability rests on three links: comprehension (make the agent *see*), constraint (make it *obey*), verification (make it *checkable*). This skill owns the **constraint** link. It owns neither of the others, but is bounded by both:

| Chain relation | Audit consequence |
| --- | --- |
| **Comprehension determines constraint** — a constraint is only as precise as the understanding behind it. You cannot write "this module must not depend on that one" before the module graph is untangled. | Step 0: verify the comprehension assets exist. Without them the rewrite invents structure instead of recording it. |
| **Constraint determines verification** — verification only checks what the constraint names. "Core endpoint response shapes must not change" gets checked; "keep the code clean" never does. | Principle 13: every constraint stated so something could check it. |
| **Verification feeds comprehension** — each regression teaches what the docs did not say, and that lesson becomes a new line here. | Principle 14 and [Accumulation](#accumulation): the file must be able to grow. |

The chain is why a context file is never finished. Comprehension assets, agent runtime, and CI gates are all replaceable; the chain between them is not.

## Goal

Audit the target file and every file it references. Produce a concrete change list, then apply on user confirmation. This skill owns the **content shape** of the file — its canonical structure, section ordering, the docs it links to, and dedup across that set. It does not own rules extraction or cross-runtime translation.

## Detect: Mode, Then File

**Mode.** Two entry paths — pick before reading anything:

- The user brings a **specific lesson** (a regression, a bad agent edit, a correction they keep repeating) → [Post-incident intake](#post-incident-intake). Append one line, update `Last updated`, report headroom. Do not restructure.
- The user asks for a **review, audit, shrink, or restructure** → the full workflow below.

**File.** Then check which is present:

- **`CLAUDE.md` present** → apply CLAUDE.md rules (200-line ceiling, 9-section skeleton without Agent Surface).
- **`AGENTS.md` present** → apply AGENTS.md rules (220-line ceiling, 9-section skeleton with Agent Surface table).
- **Both present** → ask the user which to audit first, or audit both in sequence.
- **Neither present** → recommend `scaffold-agent-docs` to create them from templates.

## Scope

| In scope (this skill) | Out of scope — handoff |
|---|---|
| File structure & content audit | Cross-runtime translation (CLAUDE.md ↔ AGENTS.md) → `translate-agent-context` |
| Canonical skeleton + line ceiling | Rule extraction & routing (static / dynamic / implicit) → `extract-rules` |
| Post-incident intake (fold a lesson into one checkable rule) | Building the comprehension assets → `document-codebase`, `index-codebase` |
| Accumulation health: headroom, landing zones, churn | Drift detection against live code → `manage-context` Phase B |
| Subdirectory `AGENTS.md` / scoped `CLAUDE.md` cleanup | Orchestrator decomposition → `translate-agent-context` |
| `agents/`, `tools/` placement clarity (AGENTS.md only) | Slash command / hook portage → `translate-agent-context` |
| MECE dedup across the file and its referenced docs | Writing the verification gates themselves (tests, CI) |
| `Context Files` table shape | — |
| Agent Surface table shape (AGENTS.md only) | — |

If the audit surfaces rule-shaped content embedded in prose, **flag it** for eviction — do not rewrite the rule body here. Recommend `extract-rules`.

## Workflow

### Step 0 — Comprehension Precondition

Only for a codebase the user did not write, or one whose decisions they cannot yet explain — a legacy project, an inherited service, a repo joined mid-flight. Skip for a greenfield repo where the author sets the rules.

A context file distilled from scattered impressions comes out vacuous, wrong, or incomplete. Check which of the five comprehension assets exist before rewriting:

| Asset | Typical home | Constraints it makes writable |
| --- | --- | --- |
| Architecture diagram | `docs/architecture.svg` | Core architecture paragraph, layering rules |
| Module graph | `docs/module-deps.svg` | "Module A must not depend on B" |
| Dependency graph | code index or generated | Danger zones, blast radius |
| Interface inventory | `docs/api-list.md` | "Response shape of these endpoints is frozen" |
| Data model | `docs/data-model.md` | Column/field naming conventions |

Missing assets are not a blocker — they are a scope boundary. Rewrite what the existing assets support and flag the rest, rather than inventing structure. Recommend `document-codebase` for architecture/API/data-model assets and `index-codebase` for the dependency graph. If **no** asset exists, say so plainly: the rewrite will be conventions plus prohibitions only, and the architecture sections will stay thin until comprehension catches up.

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

### Step 3 — Per-File Analysis Against the 14 Principles

For the target file and each referenced file, record each issue as:

- `File`, `line range`, `principle #`, `problem` (one sentence), `fix` (concrete action)

Load [common-audit-workflow.md](references/common-audit-workflow.md) for the full 14-principle list, the "index plus common sense" content rule, and audit step detail.

### Step 4 — Audit Report

Produce the report using this template (substitute the actual filename for `<FILE>`):

```markdown
## <FILE> Audit Report

### Summary
- <FILE>: <N> lines / <ceiling> ceiling — <N> lines headroom
- Referenced files: <list — exists/missing>
- Subdirectory AGENTS.md files: <list> [AGENTS.md audits only]
- Comprehension assets present: <list> / missing: <list>
- MECE violations: <count>
- Unverifiable constraints (principle 13): <count>
- Unjustified rules (principle 14): <count>
- Other issues: <count>
- Rule-shaped content to evict (handoff to extract-rules): <count>
- Cross-runtime parity gaps (handoff to translate-agent-context): <count> [AGENTS.md audits only]

### Comprehension Gaps
| Missing asset | Constraints it would unlock | Skill to run |
|---|---|---|

### Accumulation Health
| Check | Status | Note |
|---|---|---|
| Headroom | | |
| Landing zone for incidents | | |
| Recency vs. last significant merge | | |
| Churn (commits to this file over project life) | | |

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
6. Report remaining headroom against the ceiling — the next lesson has to fit somewhere.

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

## Accumulation

A context file is not written once and maintained thereafter. It is the **only** link in the reliability chain that learns. Comprehension assets are regenerated from code; verification gates are written against known failure modes. The context file is where a failure that nobody anticipated turns into a rule that prevents its recurrence.

That loop is the source of everything worth keeping in the file. Each regression teaches that some code also governs some scenario, and that lesson becomes a new line here. A file that never grows records only what its author guessed on day one.

### Audit for accumulation capacity

Every audit checks whether the file *can* grow, not just whether it is currently correct:

| Check | Failing symptom | Fix |
| --- | --- | --- |
| **Headroom** | At or over ceiling, no obvious extraction candidate | Extract detail to `docs/` now, so the next lesson has somewhere to land |
| **Landing zone** | No section owns "things that broke" | Add `## Danger Zones` / `## Historical Baggage` |
| **Recency** | `Last updated` far behind the last significant merge | Flag as drift; recommend `manage-context` Phase B |
| **Provenance** | Constraints with no traceable origin | Ask the user which are load-bearing; delete the speculation (principle 14) |
| **Churn** | File unchanged across many incidents in the git log | The loop is broken — the team learns and the file does not. Say so in the report |

Read the file's own git history when available (`git log --follow`). A file with three commits after a year of development is not stable, it is abandoned.

### The ceiling forces the discipline

Growth under a hard ceiling means every addition displaces something. That is the intended pressure, not a problem to route around. When a new lesson does not fit, in order: delete rules principle 14 cannot justify → compress a prose section into an index row → move subtree-scoped rules into a subdirectory file → only then ask whether the lesson belongs in `docs/` instead.

Never raise the ceiling. A file over its ceiling is a file that stopped being read.

### Post-incident intake

When the user brings a specific failure — a regression, a bad agent edit, a repeated correction — write **one** line, in the section that owns it, phrased so verification could check it (principle 13):

```markdown
<!-- Bad: unverifiable, no alternative, no reason -->
- Be careful when modifying the order service.

<!-- Good: reason, rule, alternative, checkable -->
- `OrderService.calculateTotal` is called by the settlement batch job, which has no
  test coverage. Changing its signature breaks settlement silently — add a
  characterization test in `tests/settlement/` before touching it.
```

Do not run a full restructure for a one-line addition. Add the line, update `Last updated`, and note the remaining headroom.

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
- Prose restatements of an asset that already exists — the architecture diagram, the API list, the schema
- Unverifiable constraints ("keep it clean", "be careful", "use good judgment") — nothing can check them
- Speculative rules with no incident behind them, written to look thorough
- Raising the ceiling instead of evicting content

## Restructure Rules

1. Rewrite from scratch. Do not incrementally preserve the old structure.
2. Keep the canonical section order exactly as listed above.
3. Consolidate duplicates ruthlessly — a fact appears once, in the best section.
4. Move scoped rules into subdirectory files; move long procedures to `docs/` or scripts.
5. Kill filler: repetitive intros, decorative separators, prose that does not change behavior.
6. Hard ceilings: 200 lines for CLAUDE.md, 220 for AGENTS.md. Anything over belongs in a doc.
7. Leave headroom. A rewrite that lands exactly at the ceiling has nowhere to put the next lesson.

## Guardrails

- **Never delete** content encoding non-obvious decisions or historical rationale — move it instead.
- **Never shorten** a file without confirming its unique content is preserved somewhere.
- **Never create** a new file if the content fits cleanly into an existing one.
- **Never absorb** a doc into the target file if doing so would breach the ceiling.
- **Never raise the ceiling** — evict content instead.
- **Never invent structure** the comprehension assets do not support — flag the gap and leave the section thin.
- **Never full-restructure for a one-line addition** — post-incident intake is an append, not an audit.
- **Always rewrite to canonical structure** — incremental edits that preserve old layout defeat the purpose.
- **Dedup is mandatory** — if the audit finds the same fact in 3 places, the rewrite has it in exactly 1.
- **Never rewrite rule bodies** — flag for eviction and recommend `extract-rules`.
- **Never port mechanisms** — cross-runtime translation is `translate-agent-context`'s job.

## Handoffs

**→ `document-codebase` / `index-codebase`:** when Step 0 finds comprehension assets missing. The constraints those assets would unlock stay unwritten until they exist; list them in the "Comprehension Gaps" section.

**→ `extract-rules`:** when the audit surfaces rule-shaped content (naming, formatting, API patterns, dynamic per-task guardrails, implicit "do not delete" markers). List each in the "Rule-Shaped Content" section of the audit report; recommend `extract-rules` after this skill finishes.

**→ `manage-context` (Phase B):** when the file is stale relative to the code rather than structurally wrong. Drift detection and cross-layer reconciliation are that skill's job; this skill fixes shape, not currency.

**→ `translate-agent-context`:** when the audit reveals cross-runtime parity gaps — behaviors carried only by Claude-specific surfaces, or CLAUDE.md and AGENTS.md drifted out of parity. List each gap in the "Cross-Runtime Parity Gaps" section.

**→ `review-agent-instructions` (the other file):** if auditing CLAUDE.md reveals AGENTS.md needs work, or vice versa, note it and recommend running this skill again on the other file.
