---
name: init-context
description: >
  One-time setup for shared agent memory on a new or unmaintained repo. Runs three
  sequential phases — routing config, Human-layer docs (WHY only), optional code
  index — skipping any phase whose output already exists. Writes docs/agents/memory.md,
  AGENTS.md, CONTEXT.md, and optional code index. Run once before engineering skills;
  re-run after routing config is lost. Use sync-context for ongoing maintenance.
---

# Init Context

Last updated: 2026-08-25

**Announce at start:** "I'm using the init-context skill to set up shared agent memory."

One-time setup. Runs three phases in order; skips any phase whose output already exists. Presents one confirmation gate before writing.

---

## The memory model

Three layers, each defined by the question it answers:

| Layer | Answers | Lifetime | Git |
| --- | --- | --- | --- |
| Human | Why: decisions, constraints, terminology, product intent | Project | Tracked |
| Code Index | What/How: where code lives, what calls what | Rebuildable | Either |
| Working | Now: current effort state, next actions, drafts | Effort | Ignored |

**Human layer documents WHY only** — decisions code cannot show, constraints that bind the project, terminology that must stay consistent. Agents discover WHAT and HOW by reading code or querying an optional index.

Full layer contract, ownership registry, and read/write rules: [`references/PROTOCOL.md`](references/PROTOCOL.md).

---

## Phase 0 — Inspect

Read what exists before proposing anything:

- `AGENTS.md` or `CLAUDE.md` — present? routing already there?
- `docs/agents/memory.md` — present → **skip to per-phase checks below**
- `CONTEXT.md`, `docs/adr/`, `docs/product/`
- Package manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`)
- Monorepo signals — `pnpm-workspace.yaml`, `workspaces` in `package.json`, populated `packages/*`
- Code index — any existing index directory or database, and whatever tool the repo already uses
- Start/test/lint commands from manifest, `Makefile`, or CI config

If `docs/agents/memory.md` is present and all three phase outputs exist, report the repo as already initialized and stop. If it is present but some phases are incomplete, run only the missing phases.

---

## Phase 1 — Routing config and working memory

**Output:** `docs/agents/memory.md` + `init.sh` + `.scratch/<effort>/state.md` + `## Shared memory` pointer in the agent context file.

**Skip if:** `docs/agents/memory.md` already exists.

**If you are only bootstrapping working memory** (no Human docs, no index), read [`references/working-memory.md`](references/working-memory.md) and follow only the working-memory bootstrap steps below.

Resolve these choices; skip any already settled by inspection:

**A. Issue tracker** — where issues live. Default: GitHub if `git remote` points there; local Markdown (`.scratch/`) otherwise. Options: GitHub (`gh`), GitLab (`glab`), local Markdown, other (ask for a one-paragraph description).

**B. Domain memory layout** — single-context (`CONTEXT.md` + `docs/adr/`) or multi-context (`CONTEXT-MAP.md` + per-context files). Default: single-context. Offer multi-context only when monorepo signals were found.

**C. Code index** — disabled by default. Enable only when the codebase is large enough that grepping is slower than querying an index. Tool choice is deferred to Phase 3.

Write `docs/agents/memory.md`:

```markdown
# Agent Memory

Last updated: YYYY-MM-DD

## Configuration
- Work root: `.scratch/` (git-ignored)
- Issue tracker: <A>
- Domain memory: <B>
- Product docs: `docs/product/<slug>/prd.md`
- Code index: disabled | <tool> at <path>

## Protocol
Read memory.md, the relevant CONTEXT.md and ADRs, active state.md, then pointed-to
artifacts. Write each fact once into the layer it belongs to. Promote upward only.
```

**Working memory bootstrap** (load [`references/working-memory.md`](references/working-memory.md) for full detail):

- Read start/test/lint commands from the manifest or CI config.
- Write `init.sh` at the repo root: verifies environment, installs dependencies if missing, runs the fastest smoke check. Real commands only; no example placeholders. Target under 30 seconds. Run it once and confirm it exits 0.
- Create `.scratch/<effort>/state.md` with `## Status`, `## Next action`, `## Blockers`, `## Pointers`.
- Confirm the work root is gitignored.
- Add a `## Startup sequence` to `AGENTS.md`: run init script → `git log` → read `state.md` → follow pointers → update `state.md` before closing context.

**Verify (cold start):** run init script, read recent git log, read `state.md`, confirm pointers resolve. If a fresh session could not tell what to do next from those alone, `state.md` is underspecified.

---

## Phase 2 — Human-layer docs (WHY only)

**Output:** `AGENTS.md`, `CONTEXT.md`, `docs/adr/` (lazy), `docs/product/` (lazy), `README.md`.

**Skip if:** `AGENTS.md` (or `CLAUDE.md`) already has routing content and `docs/agents/memory.md` exists.

**What the agent cannot see does not exist.** Decisions, constraints, and terminology only count once they live in a file.

### 2a — Scaffold minimal structure

Load [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md) for the canonical `docs/` layout. Read before writing; reuse what exists.

Create only what the repo has earned:

```text
AGENTS.md                    ← routing index, under 200 lines
docs/
├── agents/
│   └── memory.md
├── adr/                     ← lazy: created on first ADR
│   └── .gitkeep
└── product/                 ← lazy: created on first PRD
    └── .gitkeep
```

**Do NOT create a doc when the fact fails the source test** — anything an agent can derive from code, manifests, or an index. That rules out docs describing current structure, docs listing patterns the code already demonstrates, technology lists without rationale, generic engineering guidance, and backlog or plan trackers (working memory owns those).

When the repo already has such docs, do not extend them: extract any unique rationale into a decision record or the terminology doc, then unify per [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md).

### 2b — AGENTS.md (routing index only)

Load the AGENTS template from [`references/templates/AGENTS.template.md`](references/templates/AGENTS.template.md).

`AGENTS.md` is a routing index, not documentation. Keep it under 200 lines:

- One paragraph: what the project is
- Tech stack: language, framework, database, infra (literal list, not prose)
- Commands: `Run:`, `Test:`, `Lint:` as literal runnable commands
- Routing table: "I want to know X" → file that answers it
- Working rules: genuine constraints only (no generic advice)
- Prohibitions: real prohibitions with real consequences (delete section if none)

**Verify every command** against the manifest. No placeholders, no "see the docs."

### 2c — README.md

Three questions a stranger can answer in under a minute:

1. What is this? — one-sentence definition + why it exists
2. How do I run it? — prerequisites, install, first success
3. Where next? — usage, structure, links to deeper docs

Keep it minimal. Verify every command against the manifest. No placeholders, no marketing fluff.

### 2d — CONTEXT.md (lazy)

Load Matt Pocock's CONTEXT format from [`references/CONTEXT-FORMAT.md`](references/CONTEXT-FORMAT.md).

**Create lazily** — only when the first term needs definition. Don't scaffold an empty file.

Structure:
```markdown
# {Context Name}

{One or two sentence description.}

## Language

**Order**:
{One or two sentence definition}
_Avoid_: Purchase, transaction

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer
```

Rules:
- Be opinionated: pick one term, list alternatives under `_Avoid_`
- Keep definitions tight: 1-2 sentences, define what it IS
- Only terms specific to this project's domain (not general programming concepts)

### 2e — ADR template (lazy)

Load Matt Pocock's ADR format from [`references/ADR-FORMAT.md`](references/ADR-FORMAT.md).

**Create `docs/adr/` lazily** — only when the first ADR is needed.

ADR format: 1-3 sentences stating what was decided and why. Optional sections only when they add value. No mandatory sections.

When to offer an ADR (all three must be true):
1. Hard to reverse
2. Surprising without context
3. Result of a real trade-off

---

## Phase 3 — Code index (optional)

**Output:** code index at the configured path + pointer in `AGENTS.md`.

**Skip if:** code index is disabled in `docs/agents/memory.md`, or an index already exists and is fresh.

**If the repo already indexes its code, keep that tool.** Record how to query and refresh it; do not replace a working index with a different one.

Otherwise load [`references/index-tools/external-tools.md`](references/index-tools/external-tools.md) for candidate tools, their trade-offs, install commands, and hardening flags. Recommend one from what this repo actually needs — index freshness, non-code sources, multi-repo scope, query depth — state the reason, and **confirm before installing**, since every option adds a dependency.

Build the index, then verify by querying one symbol you can confirm in the source. Decide git policy (track by default; keep it local when the index is large or churns). Add a short `## Code index` section to `AGENTS.md` naming the tool, path, query command, and refresh command.

Do not run a tool's editor- or MCP-wiring setup subcommand unless the user explicitly asked — those edit files outside the index.

---

## Confirmation gate

Before writing anything in any phase, present a single consolidated plan:

```text
## Init Context — Setup Plan

### Phase 1 — Routing config and working memory
  CREATE  docs/agents/memory.md
  CREATE  init.sh
  CREATE  .scratch/<effort>/state.md
  UPDATE  AGENTS.md  (## Shared memory pointer + startup sequence)

### Phase 2 — Human-layer docs (WHY only)
  CREATE  AGENTS.md  (routing index)
  CREATE  README.md
  CREATE  docs/adr/.gitkeep  (lazy)
  CREATE  docs/product/.gitkeep  (lazy)
  (CONTEXT.md created lazily when first term is defined)

### Phase 3 — Code index
  SKIP  (code index disabled)
  — or —
  INSTALL <tool>; CREATE index at <path>; UPDATE AGENTS.md

Skipped (already exists): <list>
```

Ask: **"Proceed with setup? (yes / yes but skip phase N / no)"**

Apply only after confirmation. Do not commit.

---

## Guardrails

- Never create a doc for a fact an agent can derive from code, manifests, or an index.
- Human layer = WHY only (decisions, constraints, terminology, product intent).
- Agents discover WHAT/HOW by reading code or querying optional index.
- Verify every relationship claim against code, never against another doc.
- Never delete unique rationale — move it to its canonical home.
- Preserve user-authored sections.
- Write each fact once; link rather than copy across layers.
- Do not create watchers, daemons, or git hooks unless the user asked.
- Never record credentials, tokens, or personal data in shared memory.
- Do not commit.
