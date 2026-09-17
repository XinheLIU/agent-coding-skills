# Decomposition rules

Last updated: 2026-09-17

How `acs-plan-delivery` turns accepted scope into dependency-ordered tickets. Extracted from `acs-implement`, retaining the former `break-into-tasks` and `bootstrap-project` guidance.

## Slicing rules

1. Identify vertical slices with an independently verifiable outcome. Each execution-ready ticket maps to one or more acceptance criteria and ends on an observable pass/fail check. Early slices link accepted scope and an explicit criteria/design blocker until that check can be defined.
2. A small change stays one ticket. Do not manufacture children for file edits or test/code steps — fine-grained execution steps live in the run checklist, grouped under their ticket, never as tickets themselves.
3. Match existing tickets by parent, scope, and outcome before proposing new ones; keep existing IDs. Rerunning decomposition with unchanged inputs proposes no duplicates.
4. Each ticket references its parent change, available canonical criteria and accepted contracts with consumed revisions, affected surfaces, `depends_on`, verification expectations, and shared-write risks. Design tickets name a concrete question, responsible specialist, and accepted decision artifact that resolves it.
5. Check the dependency graph for cycles and missing IDs before rendering or dispatching.
6. Every accepted outcome maps to a slice or concrete blocker; every available criterion maps to a ticket and check, or an explicit omission with impact. Record readiness separately from progress.
7. For a mechanical refactor spanning many callers, use expand → migrate in verifiable batches → contract; preserve behavior throughout. Keep tests with each slice, including integration checks needed to prove that slice works.

## Parallel safety

The coordinator checks conflicts independently of logical `depends_on` edges. A temporary shared-write conflict serializes dispatch without inventing a permanent prerequisite. Two frontier tickets may run concurrently only when none of these overlap:

- **Shared contracts** — both touch the same API/data/system contract
- **Migrations** — schema or data migrations serialize; ordering is part of correctness
- **Generated artifacts** — one writes what the other reads (codegen, catalogs, lockfiles)
- **Configuration** — shared config files or environment definitions
- **Test surfaces** — the same test module or fixture set

Disjoint filenames alone prove nothing. Worktree isolation removes file-level collisions, not these semantic ones; merge order always follows the dependency graph.

## Verification expectations per ticket

Choose checks from acceptance criteria, regression risk, preservation constraints, and project conventions. Behavioral slices need meaningful tests, with the failing test ordered before its implementation (the `acs-tdd` executor enforces this). Simple reversible documentation edits may use reference/schema checks. Never default all tests off; a new dependency needs authorization.

## Worked example: greenfield bootstrap

Scaffolding and infrastructure are changes proposed by the technical design phase — `design/technical/acs-design-foundation` produces the foundation spec with these five slices and their gates as criteria. Current state: empty repository. Desired state: a working skeleton with zero business logic, from accepted stack and infrastructure-pattern decisions. The natural decomposition:

| Ticket | Outcome | Verify |
| --- | --- | --- |
| 1. Scaffold | Structure, dependency declarations, config skeletons, entry point | Builds and starts cleanly |
| 2. Infrastructure | One encapsulation point each for HTTP/RPC, data access, structured logging with trace IDs, unified errors | Health check returns 200 with dependency status; error produces standardized response |
| 3. Module stubs | Every route/command/page position occupied, nothing implemented | All routes resolve (501 is fine), no 404s |
| 4. Full-link integration | One request through every layer: entry → auth → service → store → response | Trace ID flows end-to-end; this step surfaces proxy, auth, credential, and CORS failures before features exist |
| 5. Startup automation | One idempotent command brings everything up | Fresh clone + one command → app live, URLs printed |

Dependencies: 1 → 2 → 3 → 4; 5 depends on 1. Largely serial — each step's verification gates the next. Infrastructure precedes business code; scattered per-feature HTTP/DB/logging setup is the anti-pattern this ordering prevents.

## Worked example: feature

"Add user profile page with avatar upload" against an existing codebase:

| Ticket | depends_on |
| --- | --- |
| 1. Edit a display name through UI/API/store, with acceptance tests | — |
| 2. Set an avatar through UI/upload/store, with required migration and acceptance tests | —, assuming the storage contract is already accepted |
| 3. Remove an avatar and verify fallback behavior end to end | 2 |

Tickets 1 and 2 are logically independent; the coordinator still checks shared profile code/contracts before concurrent dispatch. If storage/access design is unsettled, add or reuse that design blocker for ticket 2. Ticket 1 can proceed.

## Worked example: bugfix

Reproduce (a test failing for the reported reason) → fix (minimum change turning it green) → regression coverage (edge cases around the fault). Serial by nature; usually one ticket unless the fix spans surfaces.
