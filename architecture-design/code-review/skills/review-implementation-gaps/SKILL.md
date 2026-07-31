---
name: review-implementation-gaps
description: Compare the current codebase against a design doc (DESIGN.md, docs/plans/*.md) and produce a structured gap analysis — what's complete, partial, missing, divergent, or unexpected scope creep. Use this skill whenever the user asks "what's left to do", "gap analysis", "am I done with the plan", "compare code to the plan", or "what did I miss from the design". Also use when a plan is partway implemented and the user is about to continue — knowing the current gap map prevents re-implementing finished work or skipping unfinished work. Writes a machine-readable-ish artifact that the review-code-quality skill auto-consumes.
---

# Engineering Gap Review

You are comparing the actual state of the codebase to what a design document promised. Your output is a structured gap analysis artifact that (a) tells the user what to build next and (b) feeds into `review-code-quality` as the next pipeline stage.

## When to use this skill

- User asks "what's left to do" or "what did I miss from the design"
- User wants to resume a partially-implemented plan
- Before final PR review — to catch "forgot to build that component" drift
- As Stage 2 of the review pipeline: plan-review → **gap-review** → review-code-quality

## Step 0 — Locate inputs

1. **Design doc:** use the path the user gave, or find the most recent `docs/plans/*.md`. Read it fully.
2. **Codebase root:** assume `git rev-parse --show-toplevel`. Note the current branch — you'll need it for the output filename.
3. If neither exists, STOP and ask.

## Step 1 — Parse the design doc into a checklist

Extract planned items. For each, capture:
- **Name** (short, stable identifier — lowercase with dashes, e.g., `auth-middleware`, `user-schema`)
- **Intent** (one line — what this component is supposed to do)
- **Planned location** (file path if the design names one; a directory hint otherwise)
- **Depends on** (other planned items this one requires)

Aim for 5–30 items. If the design doc is vague (no file paths, no names), say so and work with what's there — note the vagueness as a finding.

## Step 2 — Trace each planned item into the codebase

For every checklist item, investigate:

1. Does the planned file/module exist at the expected path? (`ls`, `Glob`)
2. If renamed or moved, can you find it by name/intent? (`Grep` for key identifiers)
3. Read the actual code. Does the implementation match the planned intent?
4. Are the dependencies the design promised actually wired up?

Classify each item into exactly one status:

| Status | Meaning |
|---|---|
| **COMPLETE** | Found at expected path, implementation matches intent, dependencies wired |
| **PARTIAL** | Found but incomplete — missing branches, missing error handling, stub functions, TODO comments, or missing behaviors from the spec |
| **MISSING** | No code found that implements this item |
| **DIVERGENT** | Code exists but differs meaningfully from the design (different approach, different data model, different API shape) |
| **UNEXPECTED** | (separate list) — code in the codebase that is not in the design at all |

Assign a confidence score 1–10 for each classification. If you can't find a file but the design is ambiguous about location, confidence is lower (5–6) and you flag it.

## Step 3 — Scan for unexpected code

Walk the branch diff (`git diff <base>...HEAD --stat` or simply the recently-modified files). For every changed file not tied to a planned item:
- Is it legitimate infra / existing pattern extension? → note briefly, no action needed
- Is it scope creep / out-of-plan work? → flag as UNEXPECTED with one sentence on why it looks out of scope

## Step 4 — Build the dependency order

From the planned items' `Depends on` edges, produce a topological order. Prioritize items whose completion unblocks the most others. Call out cycles if any (they're a design smell).

## Step 5 — Produce the ASCII gap diagram

Keep it dense and readable. Example shape:

```
PLANNED vs ACTUAL
================
 [COMPLETE]   auth-middleware       src/auth/middleware.ts
 [COMPLETE]   user-schema           src/db/schema/user.ts
 [PARTIAL]    session-store         src/auth/session.ts   (missing: refresh, eviction)
 [PARTIAL]    rate-limiter          src/middleware/rate.ts (happy path only)
 [DIVERGENT]  password-reset        src/auth/reset.ts     (uses JWT, plan said email-token)
 [MISSING]    audit-log             (planned: src/audit/)
 [MISSING]    admin-panel-route     (planned: src/routes/admin.ts)

 [UNEXPECTED] src/utils/csv-export.ts  (not in plan — scope creep?)

DEPENDENCY ORDER (build in this sequence):
 1. audit-log          blocks: admin-panel-route
 2. admin-panel-route  blocks: (leaf)
 -- session-store, rate-limiter can ship independently after their own fixes
```

## Output artifact (this is the handoff — get the schema right)

Write to:

```
docs/eng-reviews/gap-analysis-{branch}-{YYYYMMDD-HHMM}.md
```

Use exactly this structure — `review-code-quality` parses it:

```markdown
# Gap Analysis
Generated: {YYYY-MM-DD HH:MM}
Branch: {branch}
Design doc: {relative path to plan}
Reviewer: review-implementation-gaps

## Summary
- Planned components: N
- COMPLETE: X | PARTIAL: Y | MISSING: Z | DIVERGENT: W | UNEXPECTED: V

## Gap Diagram
{the ASCII diagram from Step 5}

## Components

### <component-name>
- **Status:** COMPLETE | PARTIAL | MISSING | DIVERGENT | UNEXPECTED
- **Planned:** <path or location hint> — "<intent, one line>"
- **Actual:** <path:line-range, or — if missing>
- **Deviation:** <one sentence if PARTIAL or DIVERGENT, else —>
- **Blocks:** <comma-separated component names that depend on this, or —>
- **Confidence:** N/10

(repeat for every planned item)

## Dependency Order
1. <name> (blocks N others)
2. <name> (blocks N others)
...

## Unexpected Code
- <file:path> — <one-line assessment: legit infra | possible scope creep>

## Next-stage hand-off hint
Focus review-code-quality on: <comma-separated list of component names with status COMPLETE or PARTIAL>
```

## Finding format (for issues you surface interactively)

If you notice quality problems during tracing (e.g., "this is implemented but has an obvious bug"), use:

```
[P0|P1|P2] (confidence: N/10) file:line — short description
```

**Suppress findings with confidence ≤ 4** from the main output — the gap analysis is about status, not code quality. Defer quality review to `review-code-quality`.

## What this skill does NOT do

- Does not review code quality in depth (DRY, edge cases, perf) — that's `review-code-quality`.
- Does not challenge the plan itself — that's `review-design-doc`.
- Does not run or write tests.
- Does not touch source files — this skill is read-only on the codebase.

## Interactive behavior

This skill is mostly non-interactive — it reads the plan, reads the code, writes the artifact. Ask the user only if:
- The design doc is so vague that classification is guesswork
- A classification is genuinely ambiguous (DIVERGENT vs UNEXPECTED) and the user's intent matters
- The user-scope-creep detection finds changes that could go either way

One question per ambiguity. Never batch.

## Completion report

After writing the artifact, print a short summary to the user:

```
Gap analysis complete → docs/eng-reviews/gap-analysis-{branch}-{date}.md

Status: COMPLETE {X} / PARTIAL {Y} / MISSING {Z} / DIVERGENT {W} / UNEXPECTED {V}
Next build order: 1) <name>, 2) <name>, 3) <name>
Recommended next skill: /review-code-quality (will consume this artifact and review the COMPLETE+PARTIAL components)
```
