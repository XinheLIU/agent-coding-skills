# Report Templates

Last updated: 2026-10-23

Use the resolved evidence home and [skill procedure](../SKILL.md); legacy docs paths are illustrative. Replace sample claims with inspected evidence, preserving prior failures and unrelated records.

## Template 1

```markdown
### <N>. <Flow Name>
- **Start (entry):** <HTTP method + path, or RPC, or CLI entry>
- **Key nodes:** <Service.method → DB ops → external calls>
- **End (success):** <HTTP status + response shape, OR observable side effect>
- **Why critical:** <1 line — revenue, data integrity, compliance, etc.>
- **Refactor exposure:** <High | Medium | Low>
- **Criteria/contracts:** <canonical IDs and consumed revisions; unknown expectations explicitly labelled>
```

## Template 2

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

## Template 3

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

## Template 4

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

## Template 5

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
