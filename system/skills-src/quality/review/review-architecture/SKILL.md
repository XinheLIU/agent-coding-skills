---
name: review-architecture
description: >
  Run a comprehensive architecture review across TOGAF 4A (Business / Application / Data /
  Technology), Deploy, and ADR aspects, by orchestrating per-aspect explore/review subagent
  pairs in parallel. Asks the user which aspects and scope to cover, then consolidates
  findings into one design-level report with per-aspect detail and an ADR ledger.
  Use when the user says "architecture review", "arch review", "audit architecture",
  "review the design", or wants a holistic design-quality read on the codebase.
  Boundary: this skill judges the system's design. Code-level defects (handler bugs,
  query smells, missing timeouts, perf hotspots, test gaps) belong to `review-code-quality`.
---

# Architecture Review

Last updated: 2026-08-02

You are running a holistic architecture review. Your job is **not** to do the reviews yourself — per-aspect explore/review subagent pairs do. Your job is to collect user intent, dispatch subagents in parallel, and consolidate findings into a design-level report.

This skill is **self-contained.** Everything you need is in this file.

## Boundary with `review-code-quality` (MECE)

| Concern | review-architecture | review-code-quality |
|---|---|---|
| Module boundaries, layering, ownership | ✓ | — |
| Service topology, deploy units, network/exposure model | ✓ | — |
| Canonical data model, ODS→DWD→APP layering, lineage | ✓ | — |
| Tech stack fit (DB, scheduler, runtime, observability) | ✓ | — |
| Cross-cutting design decisions (ADRs) | ✓ | — |
| API surface design (versioning, contract style, evolution) | ✓ | — |
| Authn/authz architecture (trust boundaries, role topology) | ✓ | — |
| Handler-level input validation, error envelope, status codes | — | ✓ |
| SQL correctness, injection, indexing, N+1 | — | ✓ |
| Code-level auth bugs (missing role check, weak defaults) | — | ✓ |
| Concrete reliability bugs (no timeout, no shutdown handler) | — | ✓ |
| Local performance smells (per-row insert, model reload) | — | ✓ |
| Concrete security bugs (committed secrets, TLS off) | — | ✓ |
| Test coverage / quality, complexity, smells | — | ✓ |

Rule of thumb: *review-architecture judges the system's design; review-code-quality judges the code that implements it.* When a subagent surfaces something on the wrong side of the line, route it via the cross-reference channel — do not silently flag it as a finding here.

## Aspects

| Aspect | Question it answers | Primary subagents |
|---|---|---|
| `business` | Do the modules and CLIs deliver the documented capabilities? Are personas and end-to-end flows complete? | `business-explorer` → `business-reviewer` |
| `application` | Is the module / service decomposition coherent? Are layering, contracts, and runtime ownership aligned with stated decisions? | `application-explorer` → `application-reviewer` |
| `data` | Are schema ownership, layered data model (ODS / DWD / APP), dataset contracts, and lineage explicit and respected? | `data-architecture-explorer` → `data-architecture-reviewer` |
| `technology` | Do the language / runtime / DB / scheduler / observability choices fit the workload? Where are the scaling cliffs? | `technology-explorer` → `technology-reviewer` |
| `deploy` | Is the Compose topology, network segmentation, host exposure, env-var contract, and prod-vs-dev variant model sound? | `deploy-explorer` → `deploy-reviewer` |
| `adr` | What cross-cutting decisions does the system rest on? Sound, Reconsider, Missing-but-needed, Drifted, or Stale? | `adr-explorer` → `adr-reviewer` |

## Orchestration

### Step 1 — Pick aspects

Multi-select from `business`, `application`, `data`, `technology`, `deploy`, `adr`. Default suggestion: all 6.

If the invocation includes args like `business,data,deploy`, skip the prompt and use the args.

### Step 2 — Pick scope

Options:

1. **Whole codebase** — full glob scans; reviewers see the whole surface. Default for architecture review.
2. **Subtree** — user supplies a directory (e.g., `services/biz_data/`).
3. **Recent changes — last commit** (`HEAD~1..HEAD`).
4. **Recent changes — last N commits** (ask user for N).
5. **Branch diff** (`origin/main..HEAD`).
6. **Working tree** (unstaged + staged).
7. **Custom range** — user supplies base/head refs or a file list.

For scoped runs, capture the file list via `git diff --name-only <range>` (or `find <subtree>`) **before dispatch** and pass it to every subagent. Whole-codebase runs do not need a file list — the explorers glob the codebase themselves.

Note: architecture-level findings often need surrounding context that a narrow diff cannot show. Prefer **Whole codebase** or **Subtree** unless the user specifically wants change-scoped review. For change-scoped questions tied to a PR, `review-code-quality` (Mode A) is usually the better fit.

### Step 3 — Dispatch all selected explorers in parallel

Issue all explorer invocations as **multiple `Agent` tool calls in one message**. Sequential dispatch is a bug.

Explorer prompt template:

```
You are being invoked as part of a parallel architecture review.

Aspect: <aspect>
Scope: <whole codebase | files listed below>

[If scoped] Focus your analysis on these files (you may read siblings for context):
<file list>

Produce your standard <aspect>-explorer output. It will be handed to <aspect>-reviewer
in the next step, so structure it per your Output Format. If your aspect is not detected
in the scope, return Status: NOT DETECTED per your Failure Modes section.
```

### Step 4 — Dispatch reviewers in parallel

For each completed explorer, launch its paired reviewer. Skip the reviewer for any explorer that returned `Status: NOT DETECTED` and note the skip in the consolidated report.

Issue all reviewer invocations as **multiple `Agent` tool calls in one message**.

Reviewer prompt template (the explorer output is passed verbatim — the reviewer requires it as the first message):

```
[Paste the full explorer output here — required as your first message.]

Review scope: <whole codebase | files listed in explorer output>
Produce your standard <aspect>-reviewer output with Confidence levels on every finding.
```

### Step 5 — Consolidate

Build the consolidated report using the template below. Rules:

- **Dedupe by `file:line`** (or `doc:line`). When two reviewers flag the same anchor, merge into one entry tagged `Confirmed by: [aspect-1, aspect-2]`.
- **Rank** by severity first, then by confidence (HIGH > MEDIUM > LOW). Never promote a LOW-confidence finding to Critical.
- **Do not paraphrase** reviewer findings — paraphrasing loses evidence. Quote with file:line anchors intact.
- **ADR ledger** is its own section, sourced from `adr-reviewer`.
- **Cross-reference recommendations** to `review-code-quality` go in their own section, not as findings here.

## Consolidated Report Template

```markdown
# Architecture Review — <scope summary>
Generated: <YYYY-MM-DD HH:MM>
Aspects reviewed: <list>
Aspects skipped (NOT DETECTED): <list, if any>

## Executive Summary

- **Verdict:** HEALTHY | NEEDS ATTENTION | AT RISK
- **Total issues:** <N> (Critical: X | Warnings: Y | Suggestions: Z)
- **Confidence distribution:** HIGH: X | MEDIUM: Y | LOW: Z
- **Top 3 design risks:** <bullets, each linking to its aspect section>
- **Cross-aspect themes:** <2–4 patterns observed across aspects>
- **Decisions to ratify (from ADR):** <count + brief>

## Aspect Scorecard

| Aspect | Risk | Critical | Warnings | Suggestions | Notes |
|--------|------|----------|----------|-------------|-------|
| Business | … | | | | |
| Application | … | | | | |
| Data | … | | | | |
| Technology | … | | | | |
| Deploy | … | | | | |
| ADR | … | | | | |

## Cross-Aspect Findings

Findings flagged at the same anchor by 2+ aspects — these are the highest-signal items.

- [file:line] <description>
  - Confirmed by: [aspect-1, aspect-2]
  - Severity: Critical | Warning | Suggestion
  - Confidence: HIGH | MEDIUM
  - Consolidated fix direction: …

## Per-Aspect Findings

### Business
<paste business-reviewer report verbatim, or "Skipped — NOT DETECTED">

### Application
<…>

### Data
<…>

### Technology
<…>

### Deploy
<…>

### ADR
<…>

## ADR Ledger

| # | Decision | Status | Stated at | Enforced at | Recommendation |

Status legend: Sound | Reconsider | Missing-but-needed | Drifted | Stale

## Recommendations

- **Docs to write or update:** <list>
- **Boundaries to tighten:** <list>
- **Decisions to ratify as ADRs:** <list>
- **Code-level follow-ups (route to `review-code-quality`):** <list with file paths and reason>

## Appendix — Run Details

- Aspects invoked: <list>
- Aspects skipped: <list with reason>
- Scope: <whole | subtree | git range | file list summary>
- Dispatch transcript hint: explorers in 1 message, reviewers in 1 message.
```

## Output artifact

Write the consolidated report to:

```
docs/eng-reviews/review-architecture-<YYYYMMDD-HHMM>.md
```

Print the path back to the user when complete.

## Failure handling

- **No aspects selected** — stop and ask again.
- **User aborts mid-flow** — summarize partial results and exit cleanly.
- **Explorer errors out** — note the failure under "Aspects skipped" with reason `failed`; proceed with the rest.
- **Reviewer missing its explorer output** — orchestration bug; do not retry blindly.
- **Empty scope (0 files)** — do not dispatch; report the empty scope and stop.
- **Subagent type unavailable in runtime** — announce "Subagents unavailable for aspect X — running inline review with the same lens." Inline reviews keep the same output structure and confidence rules.

## Critical rules

**DO:**
- Dispatch all selected explorers in parallel (one message, multiple `Agent` calls).
- Dispatch all reviewers in parallel after their explorers return.
- Pass the file list to each subagent when scope is restricted.
- Consolidate before presenting — never dump 6 raw reports at the user.
- Preserve each reviewer's Confidence levels and `file:line` anchors verbatim.
- Tag cross-aspect overlaps with `Confirmed by: [..]`.
- Route code-level findings to `review-code-quality` via the cross-reference channel.

**DON'T:**
- Run reviews yourself when subagents are available.
- Promote LOW-confidence findings to Critical.
- Paraphrase reviewer findings.
- Skip the Executive Summary or the ADR Ledger.
- Dispatch reviewers sequentially when they can go in parallel.
- Flag code-level defects (handler bugs, perf smells, query injection) here — those are `review-code-quality`'s job.
