---
name: init-context
description: >
  One-time setup for shared agent memory on a new or unmaintained repo. Runs four
  sequential phases — routing config, Human-layer docs, code index, agent-behavior
  rules — skipping any phase whose output already exists. Writes docs/agents/memory.md,
  AGENTS.md, docs/, an optional code index, and rule files. Run once before the
  engineering skills; re-run after a routing config is lost. Use sync-context for
  ongoing maintenance after setup.
---

# Init Context

Last updated: 2026-08-15

**Announce at start:** "I'm using the init-context skill to set up shared agent memory."

One-time setup. Runs four phases in order; skips any phase whose output already exists. Presents one confirmation gate before writing.

---

## The memory model

Four layers, each defined by the question it answers:

| Layer | Answers | Lifetime | Git |
| --- | --- | --- | --- |
| Core | What words and constraints bind this project | Project | Tracked |
| Human | What we are building, why, and how it works | Project | Tracked |
| Wiki | Where the code for X lives | Rebuildable | Either |
| Working | How the current effort is going and what happens next | Effort | Ignored |

Full layer contract, ownership registry, and read/write rules: [`references/PROTOCOL.md`](references/PROTOCOL.md).

---

## Phase 0 — Inspect

Read what exists before proposing anything:

- `AGENTS.md` or `CLAUDE.md` — present? routing already there?
- `docs/agents/memory.md` — present → **skip to per-phase checks below**
- `docs/`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `.scratch/`
- Package manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`)
- Monorepo signals — `pnpm-workspace.yaml`, `workspaces` in `package.json`, populated `packages/*`
- Code index — `.codemap/`, `.codegraph/`, `graphify-out/`, `.gitnexus/`, `docs/wiki/`
- Start/test/lint commands from manifest, `Makefile`, or CI config

If `docs/agents/memory.md` is present and all four phase outputs exist, report the repo as already initialized and stop. If it is present but some phases are incomplete, run only the missing phases.

---

## Phase 1 — Routing config and working memory

**Output:** `docs/agents/memory.md` + `init.sh` + `.scratch/<effort>/state.md` + `## Shared memory` pointer in the agent context file.

**Skip if:** `docs/agents/memory.md` already exists.

**If you are only bootstrapping working memory** (no Human docs, no index, no rules), read [`references/working-memory.md`](references/working-memory.md) and follow only the working-memory bootstrap steps below. You do not need to read any other reference.

Resolve these choices; skip any already settled by inspection:

**A. Issue tracker** — where issues live. Default: GitHub if `git remote` points there; local Markdown (`.scratch/`) otherwise. Options: GitHub (`gh`), GitLab (`glab`), local Markdown, other (ask for a one-paragraph description).

**B. Domain memory layout** — single-context (`CONTEXT.md` + `docs/adr/`) or multi-context (`CONTEXT-MAP.md` + per-context files). Default: single-context. Offer multi-context only when monorepo signals were found.

**C. Wiki layer** — disabled by default. Enable only when the codebase is large enough that grepping is slower than querying an index. Tool choice is deferred to Phase 3.

Write `docs/agents/memory.md`:

```markdown
# Agent Memory

Last updated: YYYY-MM-DD

## Configuration
- Work root: `.scratch/` (git-ignored)
- Issue tracker: <A>
- Domain memory: <B>
- Human docs: `docs/`
- Product docs: `docs/product/<slug>/prd.md`
- Wiki: disabled | <tool> at <path>

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

## Phase 2 — Human-layer docs

**Output:** `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/TECH_DECISIONS.md`, `docs/QUALITY.md`, `docs/exec-plans/`, `README.md`, and optional architecture diagrams.

**Skip if:** `AGENTS.md` (or `CLAUDE.md`) already has routing content and all listed docs are present.

**What the agent cannot see does not exist.** Architecture decisions, conventions, and technology choices only count once they live in a file.

### 2a — Scaffold structure

Load [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md) for the canonical `docs/` layout. Read before writing; reuse what exists.

Create only what the repo has earned:

```text
AGENTS.md                    ← index file, under 200 lines
docs/
├── ARCHITECTURE.md
├── CONVENTIONS.md
├── TECH_DECISIONS.md
├── QUALITY.md
└── exec-plans/
    ├── active/.gitkeep
    ├── completed/.gitkeep
    ├── backlog.md
    └── tech-debt-tracker.md
```

Templates for each file: [`references/templates/`](references/templates/). Read the template before writing its target; replace every `{{placeholder}}`; delete sections the project has not earned.

`AGENTS.md` is an index: what the project is in a few sentences; tech stack, entry point, start command, test command as literal commands; a table mapping "I want to know X" to the file that answers it; working rules; genuine prohibitions. Everything else is a link.

### 2b — Fill from code

Before writing, be able to answer: which modules exist and what each is for, what the call chain looks like, which libraries matter, what the naming patterns are.

**Verify every relationship claim with a grep.** No import found → mark `[VERIFY: no import found]`, not a stated fact.

- **ARCHITECTURE.md** — module responsibilities, dependency direction rules, core data flows. Every constraint carries its reason.
- **CONVENTIONS.md** — patterns induced from the code, each with an observed example. Where inconsistent, say so and propose the target.
- **TECH_DECISIONS.md** — frameworks, libraries, and why each was chosen. Mark unknowns `TO BE ADDED`.
- **QUALITY.md** — definition of done, review checklist, test requirements. Project-specific; no generic advice.
- **backlog.md** — ask the user; rarely derivable from code.
- **tech-debt-tracker.md** — TODO/FIXMEs, duplicated logic, oversized files, untested core modules. An honest empty list beats invented debt.

### 2c — README

Load [`references/docs-playbooks/readme-template.md`](references/docs-playbooks/readme-template.md) before writing. Three questions a stranger can answer in under a minute:

1. What is this? — one-sentence definition + why it exists
2. How do I run it? — prerequisites, install, first success
3. Where next? — usage, structure, links

Tier the README to project size: Minimal (script/lib/internal tool) → Standard (typical app/library) → Full (OSS seeking contributors). Verify every command against the manifest. No placeholders, no marketing fluff.

### 2d — Architecture and onboarding docs

Detect codebase shape (service / library / CLI / pipeline / ML-repo / mixed) and complexity tier:

| Tier | Signals |
|---|---|
| Simple | <2k LOC, single module, no external services |
| Medium | 2k–20k LOC, or 3–10 modules, or 1–2 external integrations |
| Complex | >20k LOC, or microservices, or async workflows |

**Progressive-disclosure references — load on demand, not all at once:**

| When generating… | Load |
|---|---|
| Entry-point trace (`docs/architecture/entry-points.md`) | [`references/docs-playbooks/entry-points-playbook.md`](references/docs-playbooks/entry-points-playbook.md) |
| Module dependency diagram | [`references/docs-playbooks/module-deps-playbook.md`](references/docs-playbooks/module-deps-playbook.md) |
| External dependency diagram | [`references/docs-playbooks/external-deps-playbook.md`](references/docs-playbooks/external-deps-playbook.md) |
| Data model / ER diagram | [`references/docs-playbooks/data-model-playbook.md`](references/docs-playbooks/data-model-playbook.md) |
| Any C4 diagram | [`references/docs-playbooks/c4-syntax.md`](references/docs-playbooks/c4-syntax.md) + [`references/docs-playbooks/c4-anti-patterns.md`](references/docs-playbooks/c4-anti-patterns.md) |
| C4 on a microservice / event-driven / multi-region system | additionally [`references/docs-playbooks/c4-advanced-patterns.md`](references/docs-playbooks/c4-advanced-patterns.md) |
| Any prose-heavy doc (architecture overview, conventions, runbooks) | [`references/docs-playbooks/doc-types-playbook.md`](references/docs-playbooks/doc-types-playbook.md) |

C4 hard rules (apply without loading the reference):
- ≤15 elements per diagram. Split by bounded context if over.
- Unidirectional arrows only. `BiRel` is banned.
- Label every arrow: verb + protocol/technology, ≤40 chars.
- `UpdateLayoutConfig` mandatory for ≥5 elements.
- Before producing any diagram: *would a new engineer learn something non-obvious from this?* If not, skip it.

**Phase 2 verify:**
- `AGENTS.md` under 200 lines, with literal commands.
- Every path in the index table resolves to an existing file.
- No empty placeholder sections.
- Every unverifiable claim marked, not guessed.

---

## Phase 3 — Code index (wiki layer)

**Output:** code index at the configured path + pointer in `AGENTS.md`.

**Skip if:** wiki is disabled in `docs/agents/memory.md`, or an index already exists and is fresh.

Load [`references/index-tools/external-tools.md`](references/index-tools/external-tools.md) for the full tool comparison (codemap / codegraph / graphify / GitNexus), install commands, and hardening flags.

**Default tool: codemap** — fastest, no runtime, covers structure, dependency flow, blast radius. Choose codegraph when staleness is the main problem; graphify for mixed-media corpora; GitNexus for multi-repo groups.

State the recommendation and reason, then **confirm before installing** — every option adds a dependency.

Build the index; verify by querying one symbol you can confirm in the source. Determine git policy (track by default; use `.git/info/exclude` if large or noisy). Add a short `## Code index` section to `AGENTS.md` naming the tool, path, query command, and refresh command.

Do not run MCP-wiring subcommands (`codemap setup`, `gitnexus setup`) unless the user explicitly asked.

---

## Phase 4 — Agent-behavior rules

**Output:** `.claude/rules/*.md` and/or `docs/conventions/*.md` and/or AGENTS.md rules section + `docs/spec.md`.

**Skip if:** `docs/spec.md` exists and rule files have content.

**Detect runtime** from `.claude/` (Claude), `AGENTS.md`/`.codex/` (Codex/OpenCode), `.cursorrules` (Cursor). This determines routing: `claude-only`, `agents-md-only`, or `multi-runtime`.

**Progressive-disclosure references — load on demand:**

| When… | Load |
|---|---|
| Classifying whether a finding is static / dynamic / implicit | [`references/rules/constraint-taxonomy.md`](references/rules/constraint-taxonomy.md) |
| Running the 10-category scan | [`references/rules/scan-checklist.md`](references/rules/scan-checklist.md) |
| Presenting gap options to the user | [`references/rules/gap-consultation-format.md`](references/rules/gap-consultation-format.md) |
| Writing `.claude/rules/*.md` files | [`references/rules/rules-file-format.md`](references/rules/rules-file-format.md) |
| Writing or updating `docs/spec.md` | [`references/rules/spec-template.md`](references/rules/spec-template.md) |

**Three constraint types** (classify each finding before routing):
- **Static** — permanent rules that apply across all tasks. Route to `.claude/rules/*.md` (Claude) or `docs/conventions/*.md` / inline AGENTS.md (Codex). For multi-runtime: write body once, reference from both.
- **Dynamic** — per-task guardrails re-stated each invocation. Document the meta-pattern in `docs/spec.md §Workflow Norms` only; never encode in static rule files.
- **Implicit** — undocumented norms in HTML comments or file markers. Leave marker in place; index in `docs/spec.md §Implicit Conventions`. Promote to explicit rule when generalizable.

Scan 10 categories: file/directory structure, API conventions, code formatting, naming, database conventions, logging, security, version control, comments/documentation, environment/config. Sample 3–5 representative files per category — do not exhaustively read. For `Partial` or `Missing` categories, present gap options and wait for the user's decision.

Add rows to the `Context Files` table in `AGENTS.md` or `CLAUDE.md`. Do not restructure those files — if structural rewrite is needed, recommend `review-agent-instructions`.

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

### Phase 2 — Human-layer docs
  CREATE  AGENTS.md
  CREATE  docs/ARCHITECTURE.md
  CREATE  docs/CONVENTIONS.md
  CREATE  docs/TECH_DECISIONS.md
  CREATE  docs/QUALITY.md
  CREATE  docs/exec-plans/  (structure only)
  CREATE  README.md
  [additional architecture docs scaled to complexity tier]

### Phase 3 — Code index
  SKIP  (wiki disabled)
  — or —
  INSTALL <tool>; CREATE index at <path>; UPDATE AGENTS.md

### Phase 4 — Agent-behavior rules
  CREATE  .claude/rules/<topic>.md  (or docs/conventions/<topic>.md)
  CREATE  docs/spec.md

Skipped (already exists): <list>
```

Ask: **"Proceed with setup? (yes / yes but skip phase N / no)"**

Apply only after confirmation. Do not commit.

---

## Guardrails

- Verify every relationship claim against code, never against another doc.
- Never delete unique rationale — move it to its canonical home.
- Preserve user-authored sections.
- Write each fact once; link rather than copy across layers.
- Do not create watchers, daemons, or git hooks unless the user asked.
- Never record credentials, tokens, or personal data in shared memory.
- Do not commit.
