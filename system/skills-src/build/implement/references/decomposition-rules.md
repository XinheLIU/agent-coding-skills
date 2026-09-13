# Decomposition rules

Last updated: 2026-09-13

How `implement` turns one verifiable change into dependency-ordered tickets. Absorbed from the retired `break-into-tasks` and `bootstrap-project` skills.

## Slicing rules

1. Identify vertical slices with an independently verifiable outcome. Each ticket maps to one or more acceptance criteria and ends on an observable pass/fail check.
2. A small change stays one ticket. Do not manufacture children for file edits or test/code steps — fine-grained execution steps live in the run checklist, grouped under their ticket, never as tickets themselves.
3. Match existing tickets by parent, scope, and outcome before proposing new ones; keep existing IDs. Rerunning decomposition with unchanged inputs proposes no duplicates.
4. Each ticket references its parent change, canonical criterion IDs with consumed revision, accepted contracts, affected surfaces, `depends_on`, verification expectations, and shared-write risks.
5. Check the dependency graph for cycles and missing IDs before rendering or dispatching.
6. Every accepted criterion maps to a ticket and check, or to an explicit omission with its impact stated.

## Parallel safety

Two frontier tickets may run concurrently only when none of these overlap:

- **Shared contracts** — both touch the same API/data/system contract
- **Migrations** — schema or data migrations serialize; ordering is part of correctness
- **Generated artifacts** — one writes what the other reads (codegen, catalogs, lockfiles)
- **Configuration** — shared config files or environment definitions
- **Test surfaces** — the same test module or fixture set

Disjoint filenames alone prove nothing. Worktree isolation removes file-level collisions, not these semantic ones; merge order always follows the dependency graph.

## Verification expectations per ticket

Choose checks from acceptance criteria, regression risk, preservation constraints, and project conventions. Behavioral slices need meaningful tests, with the failing test ordered before its implementation (the `tdd` executor enforces this). Simple reversible documentation edits may use reference/schema checks. Never default all tests off; a new dependency needs authorization.

## Worked example: greenfield bootstrap

Scaffolding and infrastructure are changes proposed by the technical design phase — `design/technical/design-foundation` produces the foundation spec with these five slices and their gates as criteria. Current state: empty repository. Desired state: a working skeleton with zero business logic, from accepted stack and infrastructure-pattern decisions. The natural decomposition:

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
| 1. Migration: `avatar_url` on users | — |
| 2. Upload API endpoint | 1 |
| 3. Profile UI component | 1 |
| 4. End-to-end integration test | 2, 3 |

Tickets 2 and 3 run in parallel after 1 — different surfaces, no shared contract, no shared tests.

## Worked example: bugfix

Reproduce (a test failing for the reported reason) → fix (minimum change turning it green) → regression coverage (edge cases around the fault). Serial by nature; usually one ticket unless the fix spans surfaces.
