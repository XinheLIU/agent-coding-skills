---
name: sync-context
description: >
  Maintenance skill for shared agent memory. Detects and repairs drift across
  all three context layers (Human docs, wiki index, working memory). Two modes:
  fast (docs drift check only, ~30s, for post-commit hooks) and full (all three
  layers, for weekly cron or pre-handoff). Reads docs/agents/memory.md for
  configuration. Run init-context first if the repo has no memory routing.
---

# Sync Context

Last updated: 2026-08-15

**Announce at start:** "I'm using the sync-context skill to detect and repair context drift."

Ongoing maintenance. Detects drift since the last sync and either fixes it directly (narrow factual corrections) or invokes the owning skill for structural work. Presents a report before applying anything beyond trivial fixes.

**Prerequisite:** `docs/agents/memory.md` must exist. If absent, run `init-context` first.

Layer contract, ownership registry, and read/write protocol: [`references/PROTOCOL.md`](references/PROTOCOL.md).

Canonical document layout, layer-by-layer structural invariants, and classification protocol: [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md).

---

## Modes

| Mode | When to use | What it checks |
|---|---|---|
| **Fast** (default) | Post-commit hook, quick check | Human-layer docs only (~30 s) |
| **Full** (`--full`) | Weekly cron, pre-handoff, after a merge | All three layers |

Invoke as `/sync-context` (fast) or `/sync-context --full` (full).

---

## Hook and cron recipes

```bash
# .git/hooks/post-commit  (fast mode)
#!/bin/sh
claude --skill sync-context

# weekly full sync — every Monday at 09:00
# 0 9 * * 1 cd /path/to/repo && claude --skill sync-context --full
```

Hook output: exit 0 when no blocking issues; exit 1 with a brief summary when blocking issues exist (broken paths, misplaced durable facts). Warnings do not block.

---

## Step 1 — Establish baseline

Read `docs/agents/memory.md`. Resolve Human, Wiki, and Working roots. Find the sync boundary — the merge, the release, or the `Last updated:` date on the most recently touched doc.

```bash
git log --oneline --since="<boundary>"
git diff --stat <boundary>
```

Note moved or deleted files, renamed symbols, new or dropped dependencies. This is the ground truth for all three jobs.

---

## Job A — Human-layer docs drift (fast + full)

Load [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md). Run two passes:

**Pass 1 — Structural invariants (gate).** Check Human-layer invariants 1–5 from `canonical-doc-layout.md` against what exists. If `docs/agents/memory.md` is missing, stop and recommend `init-context` Phase 1 before continuing — the rest of this skill depends on it. Flag each violated invariant as `STRUCTURAL`.

**Pass 2 — Drift check.** Verify tracked, people-facing docs against live code.

**In scope:** `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/TECH_DECISIONS.md`, `docs/QUALITY.md`, `docs/architecture/`, `docs/data/`, `docs/runbooks/`, module READMEs.

**Out of scope:** `.claude/`, skill trees, vendored, generated, cache, build-output directories.

For every in-scope doc:

- **Paths and commands** — check they resolve and still work.
- **Relationships** — grep before asserting "A uses B". No import found → mark `[VERIFY]`, not a stated fact.
- **Tech stack claims** — cross-check against the package manifest.
- **Index table links** — every entry in `AGENTS.md` must point to an existing file.
- **`Last updated:` currency** — flag docs not touched since the boundary if the diff shows relevant changes.
- **Canonical home** — apply the four classification tests from `canonical-doc-layout.md`. A doc in the wrong location is `MOVE`, not `UPDATE`.

When code and doc disagree, the code wins — unless the doc records an intended constraint the code violates. That is a defect, not drift; report it as one.

Classify each doc using the protocol in `canonical-doc-layout.md`: `OK`, `UPDATE`, `STRUCTURAL`, `MISSING`, `MOVE`, `SPLIT`, `MERGE`, or `DELETE`. Apply precedence: `MISSING` > `MOVE` > `STRUCTURAL` > `UPDATE` > `OK`.

---

## Job B — Wiki layer freshness (full only)

Check wiki-layer invariants 6–7 from `canonical-doc-layout.md` first: is the wiki status (enabled/disabled) declared in `docs/agents/memory.md`? If enabled, does `AGENTS.md` have a `## Code index` section with tool, path, query command, and refresh command? Flag missing declaration or missing section as `STRUCTURAL`.

Then verify freshness: compare index against the diff. Query one symbol you know moved since the boundary — do not assume a watcher kept it current.

Load [`references/index-tools/external-tools.md`](references/index-tools/external-tools.md) only if you need to identify which tool is in use or interpret its output.

If stale: refresh with the tool's own refresh command; re-query the moved symbol; update `Last updated:` in `docs/agents/memory.md`.

If missing and wiki is enabled: note as a `STRUCTURAL` gap, recommend `init-context` Phase 3.

If wiki is disabled in memory config: skip freshness check; confirm invariant 7 is satisfied.

---

## Job C — Working-memory maintenance (full only)

Check working-layer invariants 8–9 from `canonical-doc-layout.md` first: is the work root gitignored? Does the active effort's `state.md` have a `## Next action` that is specific enough to start without re-deriving context? Flag violations as `STRUCTURAL`.

**If you are only maintaining working memory** (no Human docs or index involved), load [`references/working-memory.md`](references/working-memory.md) for the full protocol. The steps below are the summary; the reference has the detail.

Three checks:

**C1. Working-memory health.** For the active effort:
- Does `state.md` describe work that has since landed? If yes, update `## Status` and `## Next action`.
- Do spec files (`specs/NNN-slug.md`) or task files (`tasks/NNN-slug.md`) have stale states — work marked `in-progress` that has since landed or been abandoned? Update the `state:` field and append a note to `progress.md`.
- Are all pointers in `state.md` resolving to files with real content?
- Is `progress.md` append-only and current?

**C2. Promotion scan.** Check for facts that pass the durability test: *if the work root were deleted today, would the project lose a fact it still needs?*

| Found in working memory | Belongs in | Route via |
|---|---|---|
| Durable product intent (persona, scope, Not-To-Do) | `docs/product/<slug>/prd.md` | `write-prd` |
| Settled architectural constraint or boundary rule | `docs/ARCHITECTURE.md` | `document-codebase` |
| Technology choice and rationale | `docs/TECH_DECISIONS.md` | `document-codebase` |
| Durable trade-off with alternatives considered | `docs/adr/` | `domain-modeling` |
| Pattern the next contributor must follow | `docs/CONVENTIONS.md` | `extract-rules` |

A decision qualifies when it is settled, hard to reverse, and would surprise someone who did not watch it happen.

**C3. Effort completion.** Efforts whose code has merged and whose `state.md` shows no outstanding blockers are candidates for archiving to `exec-plans/completed/`. Debt discovered along the way goes to `tech-debt-tracker.md`. Flag both — do not move without confirmation.

**Never move facts silently.** Flag all promotion candidates and completion candidates in the report. Promote only after confirmation.

---

## Step 2 — Report

Present findings before applying anything beyond trivial factual fixes (wrong path, renamed command, broken link):

```text
## Sync Context Report

Compared against: <ref or date>
Mode: fast | full

### Structural invariants  [full only]
| # | Invariant | Status | Action |
| 1 | AGENTS.md exists at root with routing content | OK / STRUCTURAL | — |
| 2 | docs/agents/memory.md exists with all fields | OK / STRUCTURAL | — |
| 3 | Four core docs exist (ARCHITECTURE, CONVENTIONS, TECH_DECISIONS, QUALITY) | OK / STRUCTURAL | — |
| 4 | exec-plans/ with backlog.md and tech-debt-tracker.md | OK / STRUCTURAL | — |
| 5 | AGENTS.md under 200 lines; all routing-table paths resolve | OK / STRUCTURAL | — |
| 6 | Wiki invariant satisfied (enabled+indexed OR explicitly disabled) | OK / STRUCTURAL | — |
| 7 | Work root gitignored | OK / STRUCTURAL | — |

### Human-layer docs
| File | Status | Issue | Fix |
| README.md | UPDATE | install command references `npm start`, manifest uses `npm run dev` | correct command |
| docs/ARCHITECTURE.md | STRUCTURAL | three modules renamed since last update | invoke init-context Phase 2d (targeted) |
| docs/CONVENTIONS.md | OK | — | — |

### Wiki layer  [full only]
<Invariant check result, index freshness, what a refresh would change, or SKIP if disabled.>

### Working-memory health  [full only]
<Invariant check result, state.md posture, stale issues, broken pointers.>

### Promotion candidates  [full only]
| Fact | Currently in | Belongs in | Lost if work root deleted? |

### Effort completion candidates  [full only]
| Effort | Status | Action |

### Constraint violations
<Docs stating a rule the code now breaks — defects, not drift.>

### Content gaps
| Surface | What's missing | Owning skill |

### Orchestration plan
<Skill, invocation mode, what it addresses — listed in dispatch order.>
```

Ask: **"Apply factual fixes and invoke listed skills? (yes / yes but skip #N / no)"**

---

## Step 3 — Apply

After confirmation:

**This skill applies directly:**
- Correct wrong paths, broken links, renamed commands.
- Update `Last updated:` on every touched file.
- Refresh stale wiki index (Job B).
- Update `state.md` fields when current facts have changed.
- Move completed efforts to `exec-plans/completed/`.

**Invoke owning skill for structural work:**

| Drift type | Owning skill |
|---|---|
| Human docs structurally wrong or missing | `init-context` Phase 2 |
| Architecture or API docs materially wrong | `init-context` Phase 2d (targeted surface) |
| `AGENTS.md` / `CLAUDE.md` structurally wrong or over budget | `review-agent-instructions` |
| README no longer describes the project | `init-context` Phase 2c |
| Agent-behavior rules undocumented or misrouted | `init-context` Phase 4 |
| Wiki index stale or missing | `init-context` Phase 3 |
| Terminology conflict or decision needs an ADR | `domain-modeling` |
| Product intent stuck in working memory | `write-prd` |

Dispatch independent skill invocations in parallel when they do not share state.

---

## Guardrails

- Verify against code, never against another doc.
- Never delete unique rationale — move it to its canonical home.
- Preserve user-authored sections and unrelated state.
- Write each fact once; link rather than copy.
- Promote upward only — never move facts from a tracked layer into the work root.
- Route promotion through the owning skill. This skill detects misplacement; it does not author product intent.
- Never record credentials, tokens, or personal data in shared memory.
- Do not commit.
