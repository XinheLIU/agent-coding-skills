# Context Protocol Verification

Last updated: 2026-09-25

This records the historical 2026-09-09 context-protocol verification. Skill paths were updated for the ACS namespace migration; historical counts and results below are not a current suite verdict. The migration is complete; this record stands as a historical snapshot only.

Change: suite-context-lifecycle-2026-09-09
Scope: this suite's 45 source skills, shared contracts, workflows, guides, and agent handoffs. Requirements are the user-supplied “Context protocol for your coding suite” implementation plan; this record retains implementation and verification evidence, not a second requirements document.

## Result

The [protocol](../../protocols/skill-declarations.md) now defines four lifecycles, one canonical change/spec, scoped freshness, serialized contributions, and retention. [Coordination](../../workflows/context-coordination.md) owns context assembly and runtime operations. Product/Design authority and source formats remain intact; accepted rationale survives before component documentation. [Delivery](../../workflows/feature-delivery.md) defines direct planning/execution without unavailable skills. Testing, Refactoring, and Operations link criterion/preservation/release evidence to the same change.

## Structural and executable checks

Environment: local macOS, existing Python 3 standard library and system Ruby/Psych; no dependency installation. Changes were uncommitted and not released.

| Check | Result |
| --- | --- |
| `python3 system/evals/validate_suite.py` | PASS: 45 source skills, six-field declarations, loader symlinks, suite-local Markdown links and anchors |
| Ruby/Psych `YAML.safe_load` over all skill frontmatter and context blocks | PASS: 45 valid names/descriptions and six array-valued context fields |
| `python3 -m unittest discover -s system/evals/evals -p 'test_*.py' -v` | PASS: 6 positive/negative fixtures for declarations, identity links, and cleanup retention |
| `python3 -m unittest discover -s system/skills-src/authoring/acs-draw-portfolio-dag/tests -p 'test_*.py' -v` | PASS: existing scan/render test, including status/dependency mapping and read-only generated views |
| Existing `scripts/validate-product-memory.py` against the independent fixture's product HTML | PASS: 0 errors, 0 warnings |
| Edited Markdown dates, JSON parsing, `git diff --check`, scope audit | PASS: dates current; only suite files changed; unrelated pre-existing untracked files preserved |

The system skill creator's Python quick validator needs unavailable PyYAML; existing Ruby/Psych supplied actual YAML parsing without adding dependencies. The local structural validator deliberately accepts only the concise declaration syntax used by this suite; it is not a general YAML parser or runtime Harness.

## Independent forward test

An independent agent executed synthetic EXP-42 delivery/reconciliation in isolated source and receiving directories. It read the actual suite instructions and produced artifacts; it did not edit the suite.

| Behavior | Observed result |
| --- | --- |
| Cold context and Product → Design → Implementation | Reused EXP-42, existing `specs/export.md` req-v3, FR-7/AC-9, and D-4; created two independent children without duplicated requirements |
| Acceptance and cleanup | Retained unique design rationale, historical decision basis, verification commands/results, prior failure, omissions, and release status; 113 final references resolved with receiving scratch unavailable before removal |
| Scoped invalidation | D-4 d-v3 changed CSV premises only; CSV dependents needed review while JSON child, both specs, BILL-2, billing evidence and gap remained byte-identical |
| Concurrent contributions | Stale claim request did not overwrite the current owner; stale assessment retained author and dispute after rereading current records |
| Repeated reconciliation | Zero file changes or duplicate records on unchanged rerun |
| Refactoring | Preserved ADR-3 rationale, blocked until Design reconciled the boundary, then linked accepted ADR-4, updated System State, and before/after preservation evidence |
| Release artifact identity | A rebuilt digest remained not released / needs review; same source revision did not inherit old artifact verification |
| Missing skills and handoff references | Direct planning/execution used workflow contracts; 40 checked suite references resolved; revised analyze accepted canonical inputs without literal three-file requirements |

The forward test caught a remaining literal-file requirement in `analyze`; it was removed and the agent verified the correction. YAML parsing also caught an existing unquoted colon in `acs-refactor-code`'s description; quoting repaired it without changing intent.

These are instruction/artifact tests with synthetic code, verification, and release evidence. Actual Git worktree mechanics, production code behavior, deployments, and atomic concurrent locking were not exercised. No executable Harness or deployment integration was added. The scenario intentionally left changed CSV verification, a disputed assessor conclusion, and new-artifact checks unresolved; it correctly did not label them ready.

## Repeatable scenarios

[context-lifecycle.json](context-lifecycle.json) records ten focused cold-session, identity, retention, invalidation, verification, refactoring, release, concurrency, product-boundary, and missing-capability scenarios. The Product fixture formerly located at `skills-src/product/evals/shared-memory.json` covered enrichment, evidence/commitment, migration, and roadmap cases; that historical fixture is no longer present in this checkout. These scenario files require isolated agent evaluation; passing the structural script does not execute them or prove their behavior.
