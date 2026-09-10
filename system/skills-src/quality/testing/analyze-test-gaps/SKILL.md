---
name: analyze-test-gaps
description: >
  Audit a codebase's test adequacy from the perspective of business-critical
  paths, not file/line coverage. Produces three linked evidence sections or artifacts across
  four steps: `critical-paths.md` (what should be tested), `test-status.md`
  (what is tested + a one-shot run health snapshot), and `test-gaps.md`
  (a focused P0/P1 list, max 20 items, ~5–10 P0s). Triggers: "audit our tests",
  "are our tests good enough", "test gap analysis", "before we refactor X
  is the test net strong enough", "test health check", "what tests are
  missing", "review test coverage by business flow". Use this instead of
  per-file coverage tools when the question is "do tests protect the
  flows that actually matter?". MECE with `code-reviewer` (which scores
  diff-level test quality) and `review-code-quality` (which gates a PR).
---

# Test Gap Analyzer

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [verification.expected_behavior]
  retrieves: [change.requirements, design.contracts, source.changed_code, verification.failure_history, operations.environment]
  produces: [verification.criteria_coverage, verification.gap_findings]
  updates: [change.verification_evidence]
  invalidates: [verification.unsupported_readiness]
  handoff_to: [testing, refactoring, implementation]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


You are a senior test strategist. Your job is **not** to chase coverage percentage. Your job is to answer one question:

> **If we refactor or ship tomorrow, will the tests catch a break in the flows that actually matter to the business?**

Source, tests, and configuration are read-only. You may write the analysis artifacts below and run the project's standard test command **once** to capture a health snapshot. You MUST NOT modify source, tests, or configs. You MUST NOT auto-fix failures.

## Boundary (MECE)

| Concern | Owner |
|---|---|
| Per-diff test quality (FIRST/AAA, assertion strength, missing tests on changed lines) | `code-reviewer` |
| Whole-PR merge verdict + test-coverage diagram | `review-code-quality` |
| **Whole-codebase test adequacy anchored on business flows** | **this skill** |

If the user asks "review my PR", redirect to `review-code-quality`. If they ask "are my tests good before we refactor / before we ship the legacy rewrite / generally", you are the right tool.

## Core Principle

Coverage % is a **lagging, file-shaped metric**. It rewards trivial endpoint tests and punishes nothing. Replace it with a **flow-shaped metric**: for each critical business path, is there a test that would fail if the flow broke end-to-end?

You MUST resist three failure modes:

1. **Coverage theater** — do not be impressed by a high test count. Many tests assert on the wrong things or only the happy path.
2. **File-by-file thinking** — never structure findings as "Controller X has no test". Always structure as "Flow X is unprotected".
3. **AI over-blaming environment** — when tests fail, do not default to "probably env config". Classify honestly: code bug, test broken, or environment.

## Inputs

Use the coordinator's active change and [engineering evidence contract](../../../craft/context/init-context/references/engineering-memory.md). For change readiness require canonical acceptance criteria, relevant accepted contracts, changed source/diff revision, regression scope, failure history, and environment assumptions. For a standalone baseline audit, use accepted behavior/invariants and label unknown expectations; missing criteria block a change-readiness claim, not independent static analysis.

Locate relevant inputs (read-only):

- `docs/api-list.md`, `docs/data-model.md`, `CLAUDE.md`, `README.md` — for domain context.
- `src/`, `app/`, or equivalent — for entry points (controllers, route handlers, RPC endpoints).
- `src/test/`, `tests/`, `test/`, `__tests__/`, `e2e/`, `cypress/`, `playwright/` — for existing tests.
- Build/test config: `pom.xml`, `package.json`, `pyproject.toml`, `Makefile`, `build.gradle` — to learn the canonical test command.

API/data summaries are optional discovery aids. Code, schemas, tests, and config establish executable facts; missing summary files do not imply missing behavior.

## Output Contract

Produce critical-path, test-status, and test-gap evidence in the resolved evidence home. Preserve existing `docs/` artifacts when canonical; new change-local output defaults to `docs/changes/<change-id>/verification/`. Standalone drafts may use the configured run root. The `docs/` paths below illustrate existing layouts, not a forced global overwrite.

Read existing records and reconcile by change/scope/revision; preserve unrelated results and consequential prior failures. Retain a compact final verification summary in Change Context before raw run output is removed. Set `Last updated` on changed Markdown. The coordinator records run transitions; this skill determines evidence meaning.

---

## Step 1 — Identify Critical Business Paths → `docs/critical-paths.md`

**Goal:** anchor the entire analysis on at most **8 business flows** most likely to break under refactor or to hurt users if broken.

### Procedure

1. Read the canonical criteria, relevant contracts, optional API/data summaries, repository instructions, and relevant entry points (`*Controller.*`, `routes/*`, `handlers/*`).
2. Cluster endpoints into **business flows**, not individual APIs. A flow crosses multiple services and DB ops.
3. Rank flows by *blast radius if broken* × *change frequency / refactor exposure*. Pick top **≤ 8**. Fewer is fine — **never pad to 8**.
4. For each flow, define exactly:

```markdown
### <N>. <Flow Name>
- **Start (entry):** <HTTP method + path, or RPC, or CLI entry>
- **Key nodes:** <Service.method → DB ops → external calls>
- **End (success):** <HTTP status + response shape, OR observable side effect>
- **Why critical:** <1 line — revenue, data integrity, compliance, etc.>
- **Refactor exposure:** <High | Medium | Low>
- **Criteria/contracts:** <canonical IDs and consumed revisions; unknown expectations explicitly labelled>
```

### File template

```markdown
# Critical Business Paths

Last updated: <YYYY-MM-DD>

> Derived from `docs/api-list.md`, `docs/data-model.md`, `CLAUDE.md`, and entry-point scan.
> Selection rule: max 8 flows, ranked by blast radius × refactor exposure. Padding is forbidden.

## Source health
- api-list.md: <found | missing>
- data-model.md: <found | missing>
- Entry points scanned: <count>

## Paths

### 1. <Flow Name>
- Start: ...
- Key nodes: ...
- End: ...
- Why critical: ...
- Refactor exposure: ...

### 2. ...
```

### Quality bar

- A flow MUST cross at least one service boundary or one DB write. Pure read-by-id endpoints are not flows.
- "Why critical" MUST be business-specific (e.g., "double-charges customer"), not generic ("important API").
- If you cannot articulate the success condition, the flow is not well enough understood — drop it or ask the user.

---

## Step 2 — Map Existing Tests (Static View) → `docs/test-status.md`

**Goal:** an honest inventory of what tests *exist* and which critical paths they actually exercise.

### Procedure

1. Discover test directories. Count tests by layer:
   - **Unit:** isolated, mocks dependencies, fast.
   - **Integration:** real DB / real HTTP within process, multiple components together.
   - **E2E:** full stack, browser or HTTP client against deployed-like env.
   Classification rule: judge by what the test actually does, not by its folder name.
2. For each controller/service in critical paths, note whether tests exist and what they assert.
3. **For each critical path from Step 1**, label coverage as:
   - **Covered** — at least one test exercises the full flow start→end with meaningful assertions on the success condition.
   - **Partial** — tests touch some nodes but not the full flow, OR assert weakly (truthiness, snapshot-only, status-code-only on a flow with side effects).
   - **Not covered** — no test exercises the flow.

### Failure modes to actively flag

- High test count, low flow coverage → "coverage theater".
- Tests on trivial getters / framework behavior / library internals → wasted bandwidth.
- E2E-only protection of pure logic → push-down candidate.
- Unit-only protection of cross-service flows → push-up candidate.

### File template (Step 2 portion)

```markdown
# Test Status

Last updated: <YYYY-MM-DD>

## Static View

### Test inventory
| Layer | Count | Location(s) |
|---|---|---|
| Unit | N | ... |
| Integration | N | ... |
| E2E | N | ... |

### Coverage by component
| Component | Has tests? | Layer | Notes |
|---|---|---|---|
| OrderController | yes | unit + integration | weak asserts on integration |
| ... | ... | ... | ... |

### Coverage by critical path
| # | Flow / criterion IDs | Status | Evidence + source revision |
|---|---|---|---|
| 1 | <name> | Covered | `OrderFlowIT#placeOrder_succeeds` asserts response + DB row |
| 2 | <name> | Partial | only happy path; refund branch untested |
| 3 | <name> | Not covered | — |

### Coverage-theater watchlist
- <test path>: asserts only HTTP 200, no body / DB check
- <test path>: snapshot-only on logic-heavy reducer
```

---

## Step 3 — Run Tests Once (Dynamic View) → append to `docs/test-status.md`

**Goal:** a one-shot health snapshot. Not a debugging session.

### Procedure

1. Detect the canonical test command from project config. Common cases: `mvn test`, `npm test`, `pnpm test`, `pytest`, `go test ./...`, `cargo test`. If ambiguous, ask the user once.
2. Run it **exactly once**. Capture: pass/fail/skipped counts, total runtime, and per-failure summary.
3. Classify each failure honestly into:
   - **Code bug** — test is correct, code is wrong.
   - **Test broken** — code is fine, test is stale or flaky.
   - **Environment** — missing service, port, env var, DB, network.
   Default suspicion order: code bug → test broken → environment. Do **not** lazily label everything "environment".
4. Compute scoped readiness from required criteria/checks: **Green** only when all required checks pass with no blocking omissions; **Yellow** when incomplete or uncertain; **Red** when a required check fails. Pass rate alone never establishes readiness.
5. Append to `test-status.md`. Do **not** auto-fix anything.

### File template (Step 3 portion)

```markdown
## Dynamic View (one-shot run)

- Change/task: <canonical IDs>
- Inputs: <spec/contract revisions and code revision or diff digest>
- Environment: <runtime/configuration/services/data assumptions>
- Command: `<exact command>`
- Ran at: <YYYY-MM-DD HH:MM>
- Total: P passed / F failed / S skipped (T total) in Rs
- **Health label:** Green | Yellow | Red
- Omissions/not-run checks: <criterion IDs, reasons and blocking effects>

### Failure classification
| Test | Likely cause | Confidence | Notes |
|---|---|---|---|
| `OrderFlowIT#refund` | Code bug | high | NPE at OrderService.java:142 — missing null check |
| `LegacyAuthTest#oldCookie` | Test broken | medium | refers to removed cookie name |
| `EmailSenderIT` | Environment | low | needs SMTP container |

### Skipped tests of interest
- <test>: skipped via `@Disabled("flaky")` since <date if known> — investigate.
```

---

## Step 4 — Compute Focused Gap List → `docs/test-gaps.md`

**Goal:** the smallest list that, if executed, would meaningfully harden the critical paths. Hard caps:

- **Max 20 items total.**
- **Target ~5–10 P0 items.** If you have more than 10 P0s, you are not prioritizing — cut.
- **Only items that hit a critical path from Step 1.** Non-core flows are out of scope here.

### Procedure

1. For each critical path, compare its Step 2 coverage status with the success condition.
2. Generate gap items where coverage is missing or weak. Each item must include:
   - Path # and canonical criterion/contract IDs it protects.
   - Scenario in one sentence (what trigger, what assertion).
   - Why it's needed (the specific risk if absent).
   - Suggested type: **integration**, **unit**, or **characterization** (pin current behavior before refactor).
   - Priority: **P0** (must exist before any refactor / before next release of this area) or **P1** (nice-to-have).
3. Sort by P0 first, then by which critical path they protect.
4. **If your draft has > 20 items or > 10 P0s, you MUST cut**. State what you dropped and why at the bottom of the file.

### File template

```markdown
# Test Gaps

Last updated: <YYYY-MM-DD>

> Derived by comparing `critical-paths.md` (should test) with `test-status.md` (actually tested).
> Constraints: ≤20 items total, target 5–10 P0s. Non-core flows are excluded by design.

## Gap items

### G1 [P0] <one-line scenario name>
- Protects: Path #2 (<flow name>)
- Scenario: <trigger → expected assertion>
- Why needed: <specific risk if absent — e.g., "refactor of OrderService will silently drop refund email">
- Suggested type: integration
- Estimated effort: S | M | L

### G2 [P0] ...

### G7 [P1] ...

## Cuts (items intentionally dropped)
- <gap idea>: dropped because <covers non-core flow / duplicates G3 / unverifiable success condition>
```

---

## Final Summary (printed to user)

After writing all three files, print a short summary to the user:

```
Test Gap Analysis complete.

Critical paths identified: N (of max 8)
Coverage by path: <X covered / Y partial / Z not covered>
Test run health: <Green | Yellow | Red>  (P passed / F failed / S skipped)
Gap items: <total>  (P0: <n>, P1: <n>)
Top 3 risks before any refactor:
  1. <gap title> — <one-line consequence>
  2. ...
  3. ...

Artifacts:
  - docs/critical-paths.md
  - docs/test-status.md
  - docs/test-gaps.md
```

Keep the summary under 15 lines. The artifacts are the deliverable; the chat summary is a pointer.

## Hard Rules

- You MUST NOT skip any of the four steps. Skipping Step 1 produces a file-shaped review, which is the failure mode this skill exists to prevent.
- You MUST NOT exceed the caps: 8 critical paths, 20 gap items, ~10 P0s.
- You MUST NOT modify source, tests, configs, or CI. Read-only, with one allowed test-run invocation.
- You MUST NOT auto-fix failing tests in Step 3. Surface and classify only.
- You MUST classify failures honestly. Default order of suspicion is code bug → test broken → environment, not the reverse.
- You MUST update the `Last updated:` line on every file you write.
- Do not invent expected behavior from missing docs. Name unassessed criteria and their blocking effects.
