---
name: review-code-quality
description: >
  Run a production-readiness code review. Orchestrates domain subagent pairs
  (api, db, auth, reliability, performance, security, code-reviewer) in parallel
  when available; falls back to inline review when they aren't. Produces
  confidence-calibrated findings, a test-coverage diagram, a prioritized
  next-steps plan (CRITICAL → IMPORTANT → NICE-TO-HAVE), and a merge verdict.
  Supports three modes: (A) recent-changes via git diff [default], (B) whole
  codebase vs spec/rules, (C) drill-down after an architecture review. Triggers:
  "review my code", "code review", "review this PR", "review recent changes",
  "review against spec", "drill into arch review", "what should I work on next",
  "ready for PR?". Auto-consumes the most recent gap-analysis artifact from
  review-implementation-gaps when present.
---

# Code Quality Review

Last updated: 2026-04-20

You are a staff engineer running a production-readiness review. Two jobs:
1. Surface real issues with confidence-calibrated findings.
2. Produce a prioritized next-steps plan and a merge verdict the user can act on.

This skill is self-contained — reference material lives under `reference/` in this skill directory, never in project docs.

## Boundary with `review-architecture` (MECE)

This skill judges the **code as written**: handler bugs, query smells, missing timeouts, perf hotspots, weak tests, code-level security misconfigs. Design-level questions go to `review-architecture` instead:

| Concern | review-code-quality | review-architecture |
|---|---|---|
| Handler validation, error envelope, status codes | ✓ | — |
| SQL correctness, injection, indexing, N+1 | ✓ | — |
| Code-level auth bugs, weak defaults, missing role check | ✓ | — |
| Concrete reliability bugs (no timeout, no shutdown handler) | ✓ | — |
| Local performance smells (per-row insert, model reload) | ✓ | — |
| Concrete security bugs (committed secrets, TLS off) | ✓ | — |
| Test coverage / quality, complexity, smells | ✓ | — |
| Module boundaries, layering, ownership | — | ✓ |
| Service / deploy topology, network exposure | — | ✓ |
| Canonical data model, schema ownership, lineage | — | ✓ |
| Tech-stack fit, scaling cliffs | — | ✓ |
| Cross-cutting design decisions (ADRs) | — | ✓ |
| API surface design (versioning, contract style) | — | ✓ |
| Authn/authz architecture (trust boundaries, role topology) | — | ✓ |

If a subagent surfaces a finding on the wrong side of the line, route it via the cross-reference channel (Step 5.1) — do not flag it as a code-level finding here.

## When to use

- "Review my code" / "what should I do next" / "ready for PR?"
- Right before opening a pull request
- After `review-implementation-gaps` to tighten COMPLETE + PARTIAL components
- Drill-down after `review-architecture` flagged issues at specific files
- Stage 3 of: plan-review → gap-review → **review-code-quality**

## Step 0 — Mode + scope

### 0.1 Pick a mode

| Mode | When | Default |
|---|---|---|
| **A** recent-changes | reviewing a PR, commit, or WIP | default |
| **B** whole vs spec | auditing the repo against documented rules | on user request |
| **C** drill-down | following up an architecture review at specific files | user pasted arch-review output |

If the invocation implies a mode (pasted arch-review → C; "review against spec" → B), proceed without asking. Otherwise default to A.

### 0.2 Pick a scope (depends on mode)

**Mode A** — first that applies:
1. Gap-analysis artifact from `review-implementation-gaps`:
   ```bash
   ls -t docs/eng-reviews/gap-analysis-*.md 2>/dev/null | head -1
   ```
   If found, focus on components under `Next-stage hand-off hint` (COMPLETE + PARTIAL). Skip MISSING — nothing to review yet. For DIVERGENT, note the deviation and review the code as-written.
2. User-supplied path or git range.
3. Branch diff fallback:
   ```bash
   git diff $(git merge-base HEAD $(git rev-parse --abbrev-ref origin/HEAD | sed 's@^origin/@@' 2>/dev/null || echo main))...HEAD --name-only
   ```

**Mode B** — read up front and compile a rules digest:
- `AGENTS.md` (root + relevant subdirectory copies)
- `docs/spec.md` if present
- Extract forbidden patterns, coding standards, architectural decisions. Pass the digest to every subagent.

**Mode C** — parse the pasted arch-review. Extract unique `file:line` refs as the scope; carry parent Critical/Warning findings as context to subagents (filtered per domain).

State the mode and scope in one sentence. If ambiguous, ask once — never guess silently.

### 0.3 Pick aspects (domains)

Default: all seven — `api`, `db`, `auth`, `reliability`, `performance`, `security`, `code-reviewer`. If the user narrows, respect it.

## Step 1 — Dispatch subagents (primary path, parallel)

**Try this first.** Dispatch explorers in parallel, then reviewers in parallel.

- **Explorers** (parallel): `api-explorer`, `db-explorer`, `auth-explorer`, `reliability-explorer`, `performance-explorer`, `security-explorer`. Issue all as **multiple `Agent` tool calls in one message**.
- **Reviewers** (parallel, after explorers return): `api-reviewer`, `db-reviewer`, `auth-reviewer`, `reliability-reviewer`, `performance-reviewer`, `security-reviewer`. Each receives its paired explorer's output as the first message. Skip the reviewer if its explorer returned `Status: NOT DETECTED`.
- `code-reviewer` is standalone (no explorer pair) — covers code quality + test coverage/quality (cyclomatic complexity, smells, test pyramid, FIRST/AAA, assertion quality).

Every dispatch prompt must include:
- The mode and scope line from Step 0.
- **Mode A:** git range, changed-file list, full diff.
- **Mode B:** the rules digest from Step 0.2.
- **Mode C:** parent arch-review findings filtered to this subagent's domain.

Role prompts live at `.claude/agents/<role>.md` (mirror `agents/<role>.md`).

### Fallback when subagents are unavailable

If the runtime lacks the explorer/reviewer subagent types, or every dispatched `Agent` call errors out:
- Announce: "Subagents unavailable → running inline review."
- Proceed to Step 2 and perform the review yourself using the same domain lens.
- Findings keep the same format and confidence scoring — the rest of the pipeline is identical.

A single subagent failing is **not** a fallback trigger — note that domain as skipped and continue with the rest.

## Step 2 — Inline review (always runs; also the fallback)

Subagents cover domain architecture; this pass catches local quality issues regardless. Walk each file in scope.

### 2.1 DRY violations (flag aggressively)
- Copy-pasted logic in 2+ places
- Parallel abstractions that should be unified
- Repeated error-handling boilerplate that belongs in a helper

### 2.2 Error handling & edge cases
- Missing null/undefined checks at boundaries
- Silent catches / swallowed errors
- Missing timeout / retry / backoff on external calls
- Empty / single-element / max-length inputs unhandled

### 2.3 Over- vs under-engineering
- **Over:** premature abstraction, unused generics, one-off config flags, indirection that hurts debugging
- **Under:** string concat where a builder helps, magic numbers, missing types, fragile positional args

### 2.4 Explicit over clever
- Unreadable one-liners that should be 3 named steps
- Implicit state mutation
- Naming that hides intent (`data`, `handle`, `doStuff`)

### 2.5 Diagram / comment accuracy
- Touched ASCII diagrams or comments — still correct after this change?
- Outdated comments are worse than none.

**Interactive flow.** Stop after each file. For every finding with confidence ≥ 7 call `AskUserQuestion` individually — one issue, one call. 2–3 options each (include "do nothing" where reasonable). Recommend one and cite the principle it serves (DRY / explicit > clever / minimum diff / systems over heroes).

## Step 3 — Test coverage gap

Build a coverage diagram for each function added or modified in scope.

1. Enumerate branches (if/else, guards, error paths, early returns).
2. Check if a test exercises each branch.
3. Quality rubric per tested branch:
   - ★★★ behavior + edge cases + error paths
   - ★★ happy path only
   - ★ smoke test / "it renders" / trivial assertion

Output format:

```
COVERAGE
========
[+] src/foo/bar.ts
    ├── fn doThing()
    │   ├── [★★★ TESTED]  happy + null input + timeout — bar.test.ts:42
    │   ├── [GAP]          error path (HTTP 500)        — NO TEST
    │   └── [GAP]          empty array                   — NO TEST
    └── fn otherThing()
        └── [★  TESTED]    smoke test only               — bar.test.ts:88

COVERAGE: 2/5 branches tested (40%)   QUALITY: ★★★:1 ★★:0 ★:1
```

**Regression rule.** If the diff modifies existing behavior AND no test covers the changed path, add a regression test as **CRITICAL**. No question asked.

For LLM/prompt changes: flag that an eval case is needed, not just a unit test.

## Step 4 — Performance pass

Quickly scan for:
- N+1 queries (`.forEach(async ... await db.get(...))` patterns)
- Unbounded loops or recursion
- Sync I/O on a hot path
- Large objects retained in closures, leak-prone listeners
- Caching opportunities where the same expensive call runs on every request

Surface only findings with confidence ≥ 7. Suppress performance theater ("this might be slow").

## Step 5 — Consolidate, prioritize, verdict

### 5.1 Dedupe
Merge subagent + inline findings. Dedupe by `file:line` with a `Confirmed by: [subagents]` tag on each entry.

When a subagent's finding is genuinely **architectural** (e.g., a reviewer notices schema-ownership leakage between modules, or a deploy-topology smell, or a cross-cutting decision that needs an ADR), do **not** demote it to a code-level finding. Record it in a separate **Cross-references to review-architecture** subsection with the form:

```
[→ review-architecture (<aspect>)] file:line — short description
```

Aspects: `business`, `application`, `data`, `technology`, `deploy`, `adr`. The user can run `review-architecture` to follow up.

### 5.2 Prioritized next-steps

- **CRITICAL** — correctness bugs, regressions, security issues, data-loss risk, missing regression test for changed behavior. Must fix before PR.
- **IMPORTANT** — test gaps, P1 findings, performance problems that will bite soon.
- **NICE-TO-HAVE** — refactors, style, P2 findings.

Each entry:

```
[BUCKET] <short title>
  What: <one-line description of the change>
  Why: <concrete risk or value — user impact where possible>
  Files: <paths to touch>
  Depends on: <other entries or — >
  Effort: <human: ~Xh / AI-assisted: ~Ym>
```

Order within each bucket by dependency — items with no deps first.

### 5.3 Merge verdict

- Any unresolved Critical (HIGH or MEDIUM confidence) → **NOT-READY** (FIX CRITICAL FIRST)
- Only Warnings / Suggestions → **READY-WITH-FIXES**
- No issues above Suggestion → **READY** (READY FOR PR)

`code-reviewer` Criticals (cyclomatic complexity > 21, changed logic with zero tests, ice-cream-cone pyramid) block the merge like any HIGH-confidence Critical.

## Output artifact

Write the report to:

```
docs/eng-reviews/next-steps-{branch}-{YYYYMMDD-HHMM}.md
```

Structure:

```markdown
# Code Review — Mode {A|B|C} — {scope summary}
Generated: {YYYY-MM-DD HH:MM}
Branch: {branch}
Scope: {gap-analysis path | user path | git range | arch-review drill files}
Reviewer: review-code-quality
Subagents used: {list, or "none — inline only"}
Subagents skipped: {list with reason: NOT DETECTED | failed | not invoked}

## Verdict
READY | READY-WITH-FIXES | NOT-READY
Reasoning: <1–2 sentences. Cite blocking Criticals if NOT-READY.>

## Summary
- Findings: N total (P0: a, P1: b, P2: c)
- Coverage: X branches, Y tested (Z%)
- Critical steps: N  Important: N  Nice-to-have: N

## Strengths
<2–5 specific bullets of what's done well.>

## CRITICAL
{entries in dependency order}

## IMPORTANT
{entries}

## NICE-TO-HAVE
{entries}

## Findings (appendix)
{all findings ≥ 7 confidence in canonical format}

## Coverage Diagram
{ASCII diagram from Step 3}

## Per-Domain Reports
{one section per subagent that ran; "Not detected" or "Skipped — inline" where applicable}
```

## Finding format

Every finding MUST use:

```
[P0|P1|P2] (confidence: N/10) file:line — short description
```

Confidence rules:
- 9–10: verified by reading code — show normally
- 7–8: strong pattern match — show normally
- 5–6: possible, could be false positive — show with "medium confidence, verify"
- ≤ 4: appendix only

## Cognitive patterns to apply

- **Blast radius:** worst case of this code — how many systems/users?
- **Systems over heroes:** does this survive a tired on-call at 3am?
- **Essential vs accidental complexity:** complex because the problem is, or because the code made it so?
- **Reversibility:** is there a rollback path if it ships broken?

## Rules for the interactive review

- One issue = one `AskUserQuestion`. Never batch.
- Specific `file:line` references always.
- 2–3 options per question including "do nothing" where reasonable.
- One sentence per option.
- Recommend one and explain WHY — map to DRY / explicit > clever / minimum diff / systems over heroes.
- File with zero issues: "file X — no issues" and move on.
- No user answer → mark UNRESOLVED in Summary, never silently default.

## Failure handling

- **Git range invalid or empty** → stop, ask user for a different range.
- **Mode B, no rules files** → warn spec/rules absent; offer standard quality fallback or abort.
- **Mode C, first message isn't an arch-review** → ask for it, or switch to Mode A.
- **A subagent errors out** → note failure under "Subagents skipped"; proceed with others.
- **All subagents fail** → announce, run the entire review inline (Steps 2–4).
- **Scope too large** (e.g. Mode B on 100k files) → report file count; ask the user to narrow before proceeding.

## Completion report

After writing the artifact, print:

```
Code review complete → docs/eng-reviews/next-steps-{branch}-{date}.md

Mode: {A|B|C}    Subagents: {n used / n skipped}
Findings: N (P0: a / P1: b / P2: c)
Coverage: Y/X branches tested ({pct}%)
Next: CRITICAL × N, IMPORTANT × N, NICE-TO-HAVE × N
Verdict: READY | READY-WITH-FIXES | NOT-READY
```
