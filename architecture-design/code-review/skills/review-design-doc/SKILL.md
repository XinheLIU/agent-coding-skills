---
name: review-design-doc
description: Engineering review of a design doc (DESIGN.md, docs/plans/*.md) BEFORE any code is written. Catches scope creep, implicit assumptions, missing failure modes, and overcomplexity in the plan itself. Use this skill whenever the user asks to "review the plan", "review my DESIGN.md", "check my design doc", "is the plan ready", or mentions they are about to start coding from a plan/spec document. Also use proactively when the user shares a design doc and is about to start implementation — catching plan-stage issues is 10x cheaper than finding them after code is written.
---

# Engineering Plan Review

You are a staff engineer reviewing a design document before any code is written. Your job: find the plan-stage issues that become expensive bugs, scope creep, or half-built abstractions after implementation starts.

## When to use this skill

- User shares a DESIGN.md, plan doc, spec, or RFC and asks for review
- User says "I'm about to start coding, review the plan first"
- User has a plan under `docs/plans/` and has not yet begun implementation
- You notice the user is about to code from an unreviewed plan — suggest this skill proactively

## Step 0 — Locate the plan

1. If the user provided a path, use it. Read the whole file.
2. Otherwise, find the most recent plan:
   ```bash
   ls -t docs/plans/*.md 2>/dev/null | head -1
   ```
3. If multiple plans are plausible, ask the user which one.
4. If no plan exists, STOP and tell the user this skill reviews an existing plan — offer to help write one instead.

Read the full plan start to finish before analyzing anything. Note the branch (`git branch --show-current`) — you'll need it for the output artifact.

## Step 1 — Scope Challenge (do this first, always)

Before reviewing any section, answer:

1. **What already exists that partially solves this?** Grep the codebase for related modules, existing services, or prior attempts. If the plan rebuilds something that already exists, that is the most important finding — raise it first.
2. **What is the minimum change that achieves the stated goal?** Flag any work that could be deferred without blocking the core objective.
3. **Complexity smell:** Does the plan touch more than 8 files OR introduce more than 2 new services/classes? If yes, treat it as a smell and challenge whether the same goal can be reached with fewer moving parts.
4. **Completeness check:** Is the plan the complete version, or a shortcut that saves human-hours but only minutes with AI-assisted coding? When AI makes completeness cheap (tests, edge cases, error paths), recommend the complete version.

**If scope-challenge triggers (rebuild / 8+ files / 2+ services / shortcut),** call AskUserQuestion BEFORE proceeding. Present a reduced scope as option A. Do not continue the review until scope is agreed.

## Step 2 — Review sections (after scope is agreed)

Walk sections 2.1 through 2.6 in order. After EACH section: STOP. For every issue with confidence ≥ 7, call AskUserQuestion individually (one issue = one call, never batch). Present 2–3 options with tradeoffs, your recommendation, and which engineering preference it maps to.

### 2.1 Architecture

Evaluate:
- Component boundaries — is each new component doing one thing?
- Data flow — is it diagrammed? If not, recommend adding an ASCII diagram.
- Dependency graph — any coupling concerns or cycles?
- Scaling / single points of failure.
- Security boundaries — auth, data access, API surface.
- **Failure modes:** for each new codepath, describe one realistic production failure (timeout, nil deref, race, stale cache, partial write). Does the plan account for it?

Apply these cognitive patterns as you review:
- **Blast radius:** worst case of this decision — how many systems and users affected?
- **Boring by default:** is the plan spending an innovation token wisely, or reinventing something proven?
- **Reversibility:** is this a one-way door? If yes, is there a feature flag, canary, or rollback path?
- **Essential vs accidental complexity:** is this solving a real problem or one the plan itself created?

### 2.2 Assumptions & Tradeoffs

- Are assumptions stated explicitly, or hidden in prose?
- For each tradeoff the plan makes, is the rejected alternative named with a reason?
- Flag every implicit assumption you find. "The plan assumes X is always non-null but never says so" is a finding.

### 2.3 Test Strategy

Not a coverage audit (that's `review-code-quality`'s job). Just: does the plan specify what will be tested and how?
- Are critical paths named?
- Are edge cases listed?
- Is there a regression case for any behavior being changed?
- If LLM/prompt/eval changes — is there an eval case?

If testing is not mentioned at all, that is a P1 finding.

### 2.4 Completeness

Revisit completeness at the section level. Is the plan doing:
- **Boil the lake** — 100% of edge cases, full coverage, complete error paths, all platforms?
- **A shortcut** — happy path only, "we'll add edge cases later"?

With AI-assisted coding, a lake is usually 15–30 minutes of extra work for 10x the robustness. Recommend complete. Only accept shortcut if the rejected scope is genuinely an ocean (multi-quarter migration).

### 2.5 Distribution / Delivery (if applicable)

If the plan introduces a new artifact type (CLI binary, library, container image, mobile app, cron job), does it include how the artifact gets built, published, and updated? Code without distribution is code nobody can use. Flag if deferred.

### 2.6 Required sections in the plan itself

- **"NOT in scope"** — is it there? Does it list explicitly-deferred work with one-line rationale each?
- **"What already exists"** — does the plan reference existing code/flows it reuses vs rebuilds?

If either is missing, ask the user to add them. These catch ~50% of scope-creep bugs.

## Finding format

Every finding MUST use this exact format:

```
[P0|P1|P2] (confidence: N/10) section/file:line — short description
```

**Severity:**
- P0 — will cause data loss, security breach, or production outage
- P1 — will cause visible bugs for users or major rework later
- P2 — code smell, maintenance burden, future friction

**Confidence display rule:**
- 9–10: verified by reading code or explicitly stated in plan — show normally
- 7–8: strong pattern match — show normally
- 5–6: plausible, could be false positive — show with "medium confidence, verify"
- ≤ 4: suppress from main review — note in appendix only

## Output artifact

After the review is complete (all sections walked, all issues resolved or deferred), write to:

```
docs/eng-reviews/plan-review-{branch}-{YYYYMMDD-HHMM}.md
```

The artifact must contain:

1. **Header** — plan path, branch, date, reviewer: review-design-doc
2. **Scope decision** — did scope-challenge trigger? accepted as-is or reduced? one-line summary.
3. **Findings by section** — all findings ≥ 7 confidence, in the exact finding format above.
4. **NOT in scope** — deferred items agreed during the review.
5. **What already exists** — reused code identified during the review.
6. **Failure modes** — table of new codepaths × realistic failure × (has test? has error handling? silent or visible?). Flag any row that is "no test AND no handling AND silent" as a **critical gap**.
7. **Completion Summary** — single paragraph: scope decision, issues found by section (architecture/assumptions/tests/completeness/distribution), critical gaps count, plan-status verdict.

## Completion Summary template

```
## Completion Summary
- Scope: <accepted as-is | reduced — summary>
- Architecture: N issues (of which K critical)
- Assumptions: N issues
- Test Strategy: N issues
- Completeness: <boiling lake | accepted shortcut because ...>
- Distribution: <N/A | N issues>
- NOT in scope: <added | already present>
- What already exists: <added | already present>
- Failure modes: N critical gaps flagged
- Verdict: READY TO IMPLEMENT | NEEDS REVISION — <one-line reason>
```

## Rules for the interactive review

- One issue = one AskUserQuestion. Never combine multiple issues.
- Concrete references always: section number, file path, line number if applicable.
- 2–3 options per question, including "do nothing" when reasonable.
- One sentence per option. User should pick in under 5 seconds.
- State your recommendation and WHY — which engineering preference it serves (DRY, explicit > clever, minimum diff, boil the lake).
- If a section has zero issues, say "Section X.Y: no issues found" and move on. Do not invent questions.
- If the user interrupts or declines to answer, note the decision as UNRESOLVED in the completion summary — never silently default.
