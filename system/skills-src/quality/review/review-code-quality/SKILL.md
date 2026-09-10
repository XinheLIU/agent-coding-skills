---
name: review-code-quality
description: >
  Run a production-readiness code review. Orchestrates domain subagent pairs
  (api, db, auth, reliability, performance, security, code-reviewer) in parallel
  when available; falls back to inline review when they aren't. Produces
  confidence-calibrated findings, a test-coverage diagram, a prioritized
  next-steps plan (CRITICAL → IMPORTANT → NICE-TO-HAVE), and a merge verdict.
  Findings are tagged on two axes — Standards (code vs this repo's conventions
  and quality bar) and Spec (code vs what the plan/issue asked for) — reported
  separately, never reranked against each other. Supports three modes: (A)
  recent-changes via git diff [default], (B) whole codebase vs spec/rules,
  (C) drill-down after an architecture review. Triggers: "review my code",
  "code review", "review this PR", "review recent changes", "review against
  spec", "verify my changes", "review before commit/merge", "drill into arch
  review", "what should I work on next", "ready for PR?". Consumes a matching change/revision gap-analysis artifact from review-implementation-gaps when
  present.
---

# Code Quality Review

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [source.review_scope]
  retrieves: [change.requirements, design.contracts, repository.standards, verification.latest_evidence]
  produces: [verification.standards_findings, verification.spec_findings]
  updates: [change.review_evidence]
  invalidates: [verification.unsupported_readiness]
  handoff_to: [implementation, testing, operations]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


You are a staff engineer running a production-readiness review. Two jobs:
1. Surface real issues with confidence-calibrated findings.
2. Produce a prioritized next-steps plan and a merge verdict the user can act on.

## Two axes: Standards and Spec

Every finding is tagged with the axis it fails:

- **Standards** — does the code follow this repo's documented conventions and quality bar? Fed by the domain subagents (Step 1) and the inline pass (Steps 2.1–2.5, 3, 4).
- **Spec** — does the code do what the plan/issue asked for? Fed by the spec-fidelity pass (Step 2.6).

A change can pass one axis and fail the other: code that follows every standard but implements the wrong thing fails Spec; code that does exactly what was asked but breaks the repo's conventions fails Standards. Report the axes separately — never merge or rerank findings across them, so one axis cannot mask the other.

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

**Mode A** — use the coordinator-resolved explicit path/range or active branch diff, including relevant uncommitted changes. Reuse a gap-analysis artifact only when its canonical change identity and consumed source/design revisions match the review scope; otherwise mark it for reassessment. For COMPLETE/PARTIAL items review existing code, for DIVERGENT items carry the accepted design deviation, and retain MISSING items as Spec-axis omissions. Do not let a prior report narrow away accepted criteria.

**Mode B** — read up front and compile a rules digest:
- `AGENTS.md` (root + relevant subdirectory copies)
- `docs/spec.md` if present
- Extract forbidden patterns, coding standards, architectural decisions. Pass the digest to every subagent.

**Mode C** — parse the pasted arch-review. Extract unique `file:line` refs as the scope; carry parent Critical/Warning findings as context to subagents (filtered per domain).

State the mode and scope in one sentence. If ambiguous, ask once — never guess silently.

### 0.3 Pick aspects (domains)

Default: all seven — `api`, `db`, `auth`, `reliability`, `performance`, `security`, `code-reviewer`. If the user narrows, respect it.

### 0.4 Identify the spec source (Spec axis)

Use the coordinator-resolved canonical change/spec and acceptance criteria, then relevant accepted design/contracts and matching gap evidence. Record consumed revisions. Explicit user references take precedence; never use an unrelated newest report as authority. If criteria are absent, report the Spec axis as unassessed; Standards review can continue.

## Step 1 — Request relevant domain analysis

Propose the relevant `api`, `db`, `auth`, `reliability`, `performance`, `security`, and `code-reviewer` lenses. The coordinator handles available/authorized delegation, explorer-before-reviewer dependencies, accessible context, claims, and runtime calls. When delegation is absent, apply the same lenses inline. A failed or omitted lens is visible as unassessed scope, not a passing review.

Each domain receives the shared handoff envelope plus review mode/scope, relevant diff or rules, and domain-filtered parent findings. Return evidence with criterion/contract IDs, source revision/diff identity, environment assumptions, and omissions. Role prompts are suite-local under `system/agents/` (resolve from the suite, not a hardcoded runtime mirror).

## Step 2 — Inline review (always runs; also the fallback)

Domain contributions cover their assigned concerns; this pass catches local quality issues regardless. Walk each file in scope.

### 2.1 DRY violations (flag aggressively)
- Copy-pasted logic in 2+ places
- Parallel abstractions that should be unified
- Repeated error-handling boilerplate that belongs in a helper

Beyond duplication, scan against the Fowler smell baseline: Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. Two rules bind it: a documented repo standard overrides the baseline (where the repo endorses something the baseline would flag, suppress the smell), and every smell is a labelled judgment call ("possible Feature Envy"), never a hard violation. Skip anything tooling already enforces.

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

### 2.6 Spec fidelity (Spec axis)

Compare the behavior in scope against the spec source from Step 0.4:

- Required behavior that is missing or partial.
- Behavior the spec did not ask for (scope creep).
- Requirements that look implemented but whose implementation is wrong.

Cite the spec line for each finding. If a gap-analysis artifact from `review-implementation-gaps` exists, reuse its PARTIAL/MISSING/DIVERGENT statuses as the starting point instead of re-deriving them. This pass runs inline — no dedicated subagent; the axes are a reporting split, not a third reviewer.

**Interactive flow.** Stop after each file. For every finding with confidence ≥ 7, follow *Rules for the interactive review* below — one issue, one `the coordinator’s question interface`.

## Evidence identity

Use [engineering context](../../../craft/context/init-context/references/engineering-memory.md). Retain change/task ID, criteria and contract revisions, reviewed code/diff revision, environment assumptions, failures, skipped checks, omissions, and separate Standards/Spec readiness. A static code review cannot stand in for executed acceptance evidence. Changed relevant inputs mark affected conclusions for review.

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

## Step 4.5 — Static security greps

Run deterministic scans over the added lines of the review diff. Any match feeds the security findings (Standards axis) — cheap, no subagent needed:

```bash
DIFF="git diff <range>"   # the scope's diff command from Step 0
$DIFF | grep "^+" | grep -iE "(api_key|secret|password|token|passwd)\s*=\s*['\"][^'\"]{6,}['\"]"   # hardcoded secrets
$DIFF | grep "^+" | grep -E "os\.system\(|subprocess.*shell=True"                                  # shell injection
$DIFF | grep "^+" | grep -E "\beval\(|\bexec\("                                                    # dangerous eval/exec
$DIFF | grep "^+" | grep -E "pickle\.loads?\("                                                     # unsafe deserialization
$DIFF | grep "^+" | grep -E "execute\(f\"|\.format\(.*SELECT|\.format\(.*INSERT"                   # SQL via string formatting
```

A match is a candidate, not an automatic Critical — read the surrounding code, then score confidence like any other finding.

## Step 5 — Consolidate, prioritize, verdict

### 5.1 Dedupe
Merge subagent + inline findings. Dedupe by `file:line` with a `Confirmed by: [subagents]` tag on each entry. Keep the axis tag on every finding; Standards and Spec findings stay in separate subsections and are never reranked against each other.

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

- Any unresolved Critical (HIGH or MEDIUM confidence) on **either axis** → **NOT-READY** (FIX CRITICAL FIRST) — name the axis in the reasoning
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
Spec source: {path | "none — Standards-only review"}
Subagents used: {list, or "none — inline only"}
Subagents skipped: {list with reason: NOT DETECTED | failed | not invoked}

## Verdict
READY | READY-WITH-FIXES | NOT-READY
Reasoning: <1–2 sentences. Cite blocking Criticals and their axis if NOT-READY.>

## Summary
- Findings: N total (P0: a, P1: b, P2: c — Standards: s, Spec: p)
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
[P0|P1|P2] [Standards|Spec] (confidence: N/10) file:line — short description
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

- One issue = one `the coordinator’s question interface`. Never batch.
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
Findings: N (P0: a / P1: b / P2: c — Standards: s / Spec: p)
Coverage: Y/X branches tested ({pct}%)
Next: CRITICAL × N, IMPORTANT × N, NICE-TO-HAVE × N
Verdict: READY | READY-WITH-FIXES | NOT-READY
```
