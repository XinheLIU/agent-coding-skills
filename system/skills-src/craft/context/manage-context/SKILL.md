---
name: manage-context
description: Set up or sync the shared memory protocol for a repository. Phase A (setup) runs on a fresh repo with no memory routing — it writes the configuration, initialises the working-memory layer, and routes to Human- and Wiki-layer skills for anything still missing. Phase B (sync) runs after code changes — it detects drift across all three layers and either repairs it directly or invokes the owning skill. Use Phase A when starting context management for the first time or after the routing config is lost; use Phase B after a merge, before a handoff, or whenever docs feel stale.
---

# Manage Context

Last updated: 2026-08-10

Read `docs/agents/memory.md`. If absent → **Phase A (Setup)**. If present → **Phase B (Sync)**.

The full ownership registry and read/write rules live in [`references/PROTOCOL.md`](references/PROTOCOL.md).

Four layers, each defined by the question it answers:

| Layer | Answers | Lifetime | Git |
| --- | --- | --- | --- |
| Core | What words and constraints bind this project | Project | Tracked |
| Human | What we are building, why, and how it works | Project | Tracked |
| Wiki | Where the code for X lives | Rebuildable | Either |
| Working | How the current effort is going and what happens next | Effort | Ignored |

**The durability test** decides the layer: *if the work root were deleted today, would the project have lost a fact it still needs?* If yes, it is Human or Core. If no, it is working memory. Promotion runs one way — Working → Human or Core, never back.

---

## Phase A — Setup

Configure shared memory without creating empty content. This phase is the entry point to the context-management collection and the owner of `docs/agents/memory.md`.

### A1. Inspect

Read existing `AGENTS.md` or `CLAUDE.md`, `docs/agents/`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `docs/wiki/`, `specs/`, `.scratch/`, tracker configuration, monorepo signals, and the installed roadmap renderer. Check for an existing code index (`.codemap/`, `.codegraph/`, `graphify-out/`, `.gitnexus/`) before proposing one.

### A2. Resolve choices

Reuse established conventions. Otherwise recommend:

- local Markdown tracker and `.scratch/` work root;
- single-context domain memory;
- repository `docs/` as human memory, with `docs/product/` as the product-docs home;
- wiki disabled unless the codebase is large enough to need a code map;
- Markdown dependency sources with `roadmap.md` and `roadmap.html` projections.

Ask only about choices that materially branch. Present the complete draft before writing.

If the repository already keeps product intent somewhere else — `product/`, `docs/specs/`, a wiki page — configure that path instead of relocating it. The config records where intent lives; it does not impose a move.

### A3. Write routing

Create or update `docs/agents/memory.md`:

```markdown
# Agent Memory

Last updated: YYYY-MM-DD

## Configuration
- Work root: `.scratch/` (git-ignored) — working memory, discarded with the effort
- Issue tracker: local Markdown
- Domain memory: single-context (`CONTEXT.md`, `docs/adr/`)
- Human docs: `docs/`
- Product docs: `docs/product/<slug>/prd.md` — product intent, git-tracked
- Design docs: `docs/design/` — design system and component docs, git-tracked
- Wiki: disabled | `<tool>` at `<path>`, git-tracked
- Roadmap sources: `<work-root>/<effort>/issues/*.md`
- Roadmap views: `roadmap.md`, `roadmap.html`

## Protocol
Read configuration, relevant domain memory, the PRD for the area under change, active `state.md`, then pointed-to artifacts. Write each fact once into the layer it belongs to, update only owned artifacts, refresh derived HTML, and record transitions in `state.md`.

Layer boundary: the work root answers *how* the current effort is going and is disposable. Product docs, design system, architecture docs, and ADRs answer *what* we are building, *why*, and *how the system works* — they are tracked and outlive the effort. Before writing persistent state, ask whether deleting the work root would lose a fact the project still needs; if so, it belongs in a tracked layer. Facts move up only.

## Design Workflow

Design work produces artifacts in two layers:

**Human layer (tracked, outlives effort):**
- `docs/design/system.md` — canonical design system (typography, colors, spacing, component foundations)
- `docs/design/components/<name>.md` — component documentation with API, accessibility, usage

**Working layer (ignored, disposable):**
- `.scratch/<effort>/designs/` — variant exploration, approved designs, decision records

Design system and component docs persist as reference material; HTML variants are scaffolding and become obsolete once production code ships.
```

Add one concise `## Shared memory` pointer to the existing agent context file.

### A4. Initialize only earned structure

Create directories required by an enabled capability, such as `docs/wiki/`. Create `CONTEXT.md`, ADRs, effort folders, issue files, or product docs only when they have real content.

If the repository already has product intent scattered across working directories — a PRD under `.scratch/`, a vision doc in a scratch folder — note it for promotion in A7 rather than moving it silently.

### A5. Bootstrap the working-memory layer

Read start/test/lint commands from the package manifest, `Makefile`, or CI config.

Create an init script at the repo root (`init.sh` or the project's idiomatic equivalent) that verifies the environment is workable — not a full suite. It should confirm the working directory, install dependencies when missing, and run the fastest meaningful smoke check. Target under 30 seconds. Fill in real commands; leave no example comments. Run it once and confirm it exits clean.

Under the configured work root (`.scratch/<effort>/`), create `state.md`:

```markdown
# <Effort> — State

Last updated: YYYY-MM-DD

## Status
<Where this effort stands in one or two sentences.>

## Next action
<The single next concrete step, specific enough to start without re-deriving it.>

## Blockers
<What is preventing progress, or "none".>

## Pointers
<Links to the spec, plan, issues, diagnosis, or handoff that hold the detail.>
```

`state.md` routes; it does not store. Facts live in the artifact that owns them. Create `spec.md`, `plan.md`, `issues/`, or `handoffs/` only when a workflow earns them — empty scaffolds are not memory.

Create `progress.md` in the work root as an append-only log, newest entry on top, one entry per session. Never rewrite history.

Confirm the work root is gitignored — add to `.gitignore` or `.git/info/exclude`.

Add a short startup-sequence section to `AGENTS.md`: run init script → read `git log` → read `state.md` → follow its pointers → update `state.md` and append to `progress.md` before moving on.

### A6. Verify

Simulate a cold start: run the init script, read the recent git log, read `state.md`, confirm its pointers resolve. If a fresh session could not tell what to do next from those alone, `state.md` is underspecified.

### A7. Report and route

Report the chosen paths, enabled layers, and which skills consume each surface. State which paths are tracked and which are disposable, so the boundary is explicit from the first session. Do not commit.

Route to layer skills for anything still missing:

| Missing | Run |
| --- | --- |
| `AGENTS.md` and `docs/` structure | `scaffold-agent-docs` |
| Root `README.md` | `create-readme` |
| Agent-behavior rules and coding conventions | `extract-rules` |
| Architecture, data-model, or API docs | `document-codebase` |
| A queryable code index | `index-codebase` |
| Product intent found only in a disposable location | `write-prd`, to promote it into the product-docs home |
| Layers already exist but have drifted | Phase B below |

---

## Phase B — Sync

Reconcile the three context layers when they drift. Detect drift and orchestrate repairs — make narrow factual corrections directly; invoke the owning skill for structural work.

### B1. Establish what changed

Find the boundary since the last sync — the merge, the release, or the date on the docs — and read the actual diff. `git log --oneline` plus `git diff --stat` against that point is the ground truth. Note especially: moved or deleted files, renamed symbols, new or dropped dependencies.

### B2. Detect drift in each layer

**Wiki layer.** Compare index freshness against the diff. Verify by querying one symbol you know moved; don't assume a watcher kept it current.

**Human layer.** Verify each claim against the code, not against another doc:

- Paths, commands, and flags in `AGENTS.md` and `README.md` still resolve and work.
- `ARCHITECTURE.md` boundaries and dependency rules match current imports. Grep before believing a stated relationship.
- `TECH_DECISIONS.md` covers dependencies actually in the manifest.
- `CONVENTIONS.md` patterns still match the prevailing code.
- The index table in `AGENTS.md` points only at files that exist.
- The PRD's requirement list and Not-To-Do list match what shipped. A feature built while the PRD still lists it out-of-scope is a promotion that never happened, not a doc typo.

**Working layer.** Check whether `state.md` describes work that has since landed, whether issues reference merged or abandoned tickets, and whether the recorded next action is still the real one.

**Layer misplacement.** Independent of staleness, check whether anything sits in the wrong layer:

- Durable product intent — persona, job, demand verdict, scope commitments — living only under the work root, where deleting the effort loses it.
- A settled architectural decision recorded in a `decision.md` or `map.md` but never promoted to an ADR.
- The inverse: task status, claims, or session progress written into a tracked doc, where every status change becomes a commit.

Misplacement is the more expensive failure. Stale docs mislead; misplaced facts vanish.

### B3. Promote what has settled

A decision qualifies for promotion when it is settled, hard to reverse, and would surprise someone who did not watch it happen. Route by owner:

| Settled in working memory | Promote to | Via |
| --- | --- | --- |
| Product intent — persona, job, demand verdict, scope, Not-To-Do | `<product-docs>/<slug>/prd.md` | `write-prd` |
| Architectural constraint or boundary rule | `ARCHITECTURE.md` | `document-codebase` |
| Technology choice and rationale | `TECH_DECISIONS.md` | `document-codebase` |
| Durable trade-off with alternatives considered | An ADR | `domain-modeling` |
| Pattern the next contributor must follow | `CONVENTIONS.md` | `extract-rules` |

Move the decision and leave a link — do not copy into both layers. An effort that shipped without its intent ever reaching the Human layer is the case to flag most loudly: the code exists, the reason for it is one `rm -rf` away.

Completed efforts move to `exec-plans/completed/`. Debt discovered along the way goes to `tech-debt-tracker.md`.

### B4. Reconcile

Fix narrow factual errors directly: a wrong path, a renamed command, a dependency missing from the list. Update `Last updated:` on every file touched. When code and doc disagree, the code wins — unless the doc records an intended constraint the code violates (that is a defect, not drift; report it as one).

For structural work, invoke the owning skill:

| Drift type | Skill | Notes |
| --- | --- | --- |
| Human-layer docs scattered or wrong homes | `scaffold-agent-docs` | update mode |
| Architecture or API docs materially wrong | `document-codebase` | targeted-doc, one call per surface |
| `AGENTS.md` / `CLAUDE.md` structurally wrong, over budget, or no longer routing to memory | `review-agent-instructions` | Also the intake path when a regression should become a rule |
| README no longer describes the project | `create-readme` | — |
| Agent-behavior rules undocumented or misrouted | `extract-rules` | — |
| Wiki index stale or missing | `index-codebase` | — |
| Terminology conflicts or decision needs an ADR | `domain-modeling` | — |
| Product intent stuck in working memory, or PRD contradicts what shipped | `write-prd` | Promotes into the product-docs home; does not relocate discovery drafts |

Dispatch independent skill invocations in parallel when they do not depend on each other.

### B5. Report

Present findings before applying anything beyond trivial factual fixes:

```text
## Context Sync Report

Compared against: <ref or date>

### Wiki layer
<Index freshness, what a refresh would change.>

### Human layer
| File | Claim | Actual | Fix |

### Working layer
<Stale state, efforts ready to complete.>

### Layer misplacement
| Fact | Currently in | Belongs in | Lost if work root is deleted? |

### Constraint violations
<Docs stating a rule the code now breaks — defects, not drift.>

### Orchestration plan
<Skill, invocation mode, and what it will address — listed in dispatch order.>
```

Then ask: **"Apply factual fixes and invoke listed skills? (yes / yes but skip #N / no)"**

## Guardrails

- Verify against code, never against another doc.
- Never delete unique rationale to resolve a conflict — move it to its canonical home.
- Preserve user-authored sections and unrelated state.
- Write each fact once; link rather than copy across layers.
- Promote upward only. Never move a fact from a tracked layer into the work root.
- Route promotion through the owning skill. This skill detects misplacement; it does not author product intent.
- Never record credentials, tokens, personal data, or large raw logs in shared memory.
- Do not commit.
