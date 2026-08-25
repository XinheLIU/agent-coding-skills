---
name: sync-context
description: >
  Maintenance skill for shared agent memory. Detects and repairs drift across
  Human layer (WHY docs) and working memory. Two modes: fast (routing check only,
  ~30s, for post-commit hooks) and full (all layers including working memory, for
  weekly cron or pre-handoff). Reads docs/agents/memory.md for configuration. Run
  init-context first if the repo has no memory routing.
---

# Sync Context

Last updated: 2026-08-26

**Announce at start:** "I'm using the sync-context skill to detect and repair context drift."

Ongoing maintenance. Detects drift since the last sync and either fixes it directly (narrow factual corrections) or invokes the owning skill for structural work. Presents a report before applying anything beyond trivial fixes.

**Prerequisite:** `docs/agents/memory.md` must exist. If absent, run `init-context` first.

Layer contract, ownership registry, and read/write protocol: [`references/PROTOCOL.md`](references/PROTOCOL.md).

Canonical document layout, layer-by-layer structural invariants, and classification protocol: [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md).

---

## Modes

| Mode | When to use | What it checks |
|---|---|---|
| **Fast** (default) | Post-commit hook, quick check | Human-layer routing only (~30 s) |
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

Hook output: exit 0 when no blocking issues; exit 1 with a brief summary when blocking issues exist (broken paths, missing required docs). Warnings do not block.

---

## Step 1 — Establish baseline

Read `docs/agents/memory.md`. Resolve Human, Code Index, and Working roots. Find the sync boundary — the merge, the release, or the `Last updated:` date on the most recently touched doc.

```bash
git log --oneline --since="<boundary>"
git diff --stat <boundary>
```

Note moved or deleted files, renamed symbols, new or dropped dependencies. This is the ground truth for all three jobs.

---

## Job A — Human-layer routing (fast + full)

Load [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md). Run two passes:

**Pass 1 — Structural invariants (gate).** Check Human-layer invariants 1–4 from `canonical-doc-layout.md` against what exists. If `docs/agents/memory.md` is missing, stop and recommend `init-context` Phase 1 before continuing — the rest of this skill depends on it. Flag each violated invariant as `STRUCTURAL`.

**Pass 2 — Routing check.** Verify routing documents against reality.

**In scope:** `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/agents/memory.md`, `CONTEXT.md`, `docs/adr/`, `docs/product/`.

**Out of scope:** `.claude/`, skill trees, vendored, generated, cache, and build-output directories.

For every in-scope doc:

- **Paths and commands** — check they resolve and still work.
- **Routing table links** — every entry in `AGENTS.md` must point to an existing file.
- **`Last updated:` currency** — flag docs not touched since the boundary if the diff shows relevant changes.
- **Canonical home** — apply the three classification tests from `canonical-doc-layout.md`. A doc in the wrong location is `MOVE`, not `UPDATE`.

When code and doc disagree, the code wins — unless the doc records an intended constraint the code violates. That is a defect, not drift; report it as one.

Classify each doc using the protocol in `canonical-doc-layout.md`: `OK`, `UPDATE`, `STRUCTURAL`, `MISSING`, `MOVE`, `PROMOTE`, `COMPACT`, or `DELETE`. Apply precedence: `MISSING` > `MOVE` > `PROMOTE` > `COMPACT` > `UPDATE` > `OK`.

**Unify Human-layer docs that fail the source test.** Any doc whose content an agent could derive from code, manifests, or the index is drift, whatever it is named. Extract its unique rationale into a decision record or the terminology doc first, then `DELETE` the doc. A doc that mixes durable rationale with derivable state is `MOVE`: split the rationale out and drop the rest. Never delete rationale that exists nowhere else.

Docs tracking backlog, plans, or in-flight status belong to the working layer, not the Human layer — those are `MOVE`.

---

## Job B — Code index freshness (full only)

Check code index invariants 5–6 from `canonical-doc-layout.md` first: is the code index status (enabled/disabled) declared in `docs/agents/memory.md`? If enabled, does `AGENTS.md` have a `## Code index` section with tool, path, query command, and refresh command? Flag missing declaration or missing section as `STRUCTURAL`.

Then verify freshness: compare index against the diff. Query one symbol you know moved since the boundary — do not assume a watcher kept it current.

Load [`references/index-tools/external-tools.md`](references/index-tools/external-tools.md) only if you need to identify which tool is in use or interpret its output.

If stale: refresh with the tool's own refresh command; re-query the moved symbol; update `Last updated:` in `docs/agents/memory.md`.

If missing and code index is enabled: note as a `STRUCTURAL` gap, recommend `init-context` Phase 3.

If code index is disabled in memory config: skip freshness check; confirm invariant 6 is satisfied.

---

## Job C — Working-memory maintenance (full only)

Check working-layer invariants 7–8 from `canonical-doc-layout.md` first: is the work root gitignored? Does the active effort's `state.md` have a `## Next action` that is specific enough to start without re-deriving context? Flag violations as `STRUCTURAL`.

**If you are only maintaining working memory** (no Human docs or index involved), load [`references/working-memory.md`](references/working-memory.md) for the full protocol. The steps below are the summary; the reference has the detail.

Three checks:

**C1. Working-memory health.** For the active effort:
- Does `state.md` describe work that has since landed? If yes, update `## Status` and `## Next action`.
- Do spec files (`specs/NNN-slug.md`) or task files (`tasks/NNN-slug.md`) have stale states — work marked `in-progress` that has since landed or been abandoned? Update the `state:` field and append a note to `progress.md`.
- Are all pointers in `state.md` resolving to files with real content?
- Is `progress.md` append-only and current?

**C2. Promotion scan.** Check for facts that pass the durability test: *if the work root were deleted today, would the project lose a fact it still needs?*

| Found in working memory | Belongs in |
|---|---|
| Product intent, problem framing, scope and non-goals, MVP definition | The Human layer's product-doc home |
| A settled constraint or trade-off someone would otherwise re-litigate | A decision record |
| Terminology the project must use consistently | The terminology doc |

**A spec is not automatically working-layer.** Split it by question type: the part explaining why the shape was chosen and what it deliberately excludes is durable and gets promoted; the step-by-step build sequence stays in the work root and dies with the effort.

A decision qualifies when it is settled, hard to reverse, and would surprise someone who did not watch it happen. Where the repo already has a home for such facts, promote into it rather than opening a parallel one.

**C3. Completion compaction.** Efforts whose code has merged or been abandoned and whose `state.md` shows no outstanding blockers are `COMPACT` candidates, not archive candidates. Scan the work root and tracked documentation locations for implemented specs, completed plans, closed task files, obsolete handoffs, generated working views, and scratch notes. For each finished effort, propose one compaction action:
- rationale and meaningful rejected alternatives → the existing decision-record home;
- reader-relevant shipped outcome → the existing changelog or release-history home;
- current behavior and verification → pointers to code, tests, configuration, issues, or releases;
- remaining execution narrative → delete after confirming it contains no unique durable fact.

Do not propose an archive unless an explicit retention rule requires it. Do not create a changelog merely to preserve working history. Flag compaction for approval before deletion.

**Never move facts silently.** Flag all promotion candidates and completion candidates in the report. Promote only after confirmation.

---

## Step 2 — Report

Present findings before applying anything beyond trivial factual fixes (wrong path, renamed command, broken link):

```text
## Sync Context Report

Compared against: <ref or date>
Mode: fast | full

### Structural invariants
| # | Invariant | Status | Action |
| 1 | Root agent context file exists with routing content, readable in full | OK / STRUCTURAL | — |
| 2 | Memory config records work root, issue tracker, code index status | OK / STRUCTURAL | — |
| 3 | Every path referenced from a routing file resolves | OK / STRUCTURAL | — |
| 4 | No two documents claim the same fact as their own | OK / STRUCTURAL | — |
| 5 | If enabled: index exists and routing names tool, path, query, refresh | OK / STRUCTURAL | — |
| 6 | If disabled: memory config says so explicitly | OK / STRUCTURAL | — |
| 7 | Work root git-ignored | OK / STRUCTURAL | — |
| 8 | Each active effort has a state file with a specific next action | OK / STRUCTURAL | — |

### Human-layer routing
| File | Status | Issue | Fix |
| README.md | UPDATE | install command references `npm start`, manifest uses `npm run dev` | correct command |
| AGENTS.md | OK | — | — |
| &lt;doc restating current module layout&gt; | DELETE | Derivable from code — fails the source test | extract rationale to an ADR first, then delete |
| &lt;doc holding in-flight plan status&gt; | MOVE | Working-layer content in the Human layer | move to the work root |

### Code index  [full only]
<Invariant check result, index freshness, what a refresh would change, or SKIP if disabled.>

### Working-memory health  [full only]
<Invariant check result, state.md posture, stale issues, broken pointers.>

### Promotion candidates  [full only]
| Fact | Currently in | Belongs in | Lost if work root deleted? |

### Effort completion candidates  [full only]
| Effort / artifact | Status | Durable residue | Action |

### Constraint violations
<Docs stating a rule the code now breaks — defects, not drift.>

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
- Refresh stale code index (Job B).
- Update `state.md` fields when current facts have changed.
- Delete docs that fail the source test, after their unique rationale is saved to a canonical home.

**Invoke owning skill for structural work:**

| Drift type | Owning skill |
|---|---|
| Human docs structurally wrong or missing | `init-context` Phase 2 |
| `AGENTS.md` / `CLAUDE.md` structurally wrong or over budget | `review-agent-instructions` |
| README no longer describes the project | `init-context` Phase 2c |
| Code index stale or missing | `init-context` Phase 3 |
| Terminology conflict, or a decision that needs authoring | the skill that owns decisions and terminology, if one is installed |
| Product intent stuck in working memory | the skill that owns product docs, if one is installed |
| Reader-relevant completed change | the workflow that owns the existing changelog or release history, else the user |

Where no such skill is installed, report the promotion candidate and let the user author it. This skill detects misplacement; it does not author decisions.

Dispatch independent skill invocations in parallel when they do not share state.

---

## Guardrails

- Verify against code, never against another doc.
- Never delete unique rationale — move it to its canonical Human-layer home first.
- Compact completed execution artifacts into canonical decisions and, when warranted, one changelog entry; remove the execution narrative after approval.
- Preserve user-authored sections and unrelated state.
- Write each fact once; link rather than copy.
- Promote upward only — never move durable facts from the Human layer into the work root.
- Promote into the home the repo already uses; do not open a parallel one because it matches a convention this skill prefers.
- Never record credentials, tokens, or personal data in shared memory.
- Do not commit.
