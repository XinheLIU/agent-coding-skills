# Domain Lenses

Last updated: 2026-09-29

Step 1 applies these seven lenses to the files in scope. For each lens, first **map** what exists in scope (endpoints, queries, auth flows, external calls, and so on), then **judge** it against the checks. Every finding needs a `file:line` anchor and evidence.

A lens can run inline or as a delegated task. A delegated task gets this file's section for its lens as its whole instruction, plus the scope, the rules digest and the parent findings filtered to its domain. It returns findings and never edits files.

**Confidence.** `HIGH` = both the defect and a caller or consumer have been read. `MEDIUM` = one side has been read. `LOW` = inferred from a pattern alone.

**Out of scope for every lens.** Design-level issues (module seams, schema ownership, topology, missing decisions) go to *Cross-references to design cards* (Step 5.1), not into findings. Each lens leaves its neighbours' checks alone; the lens named in brackets owns that check.

## api

- Route/handler mismatch, wrong HTTP semantics or status codes, response shape drift across similar endpoints, a breaking change with no versioning.
- Missing validation on path/query/body, weak constraints (range, enum, format, length), reflected unsanitized input, no request size limit.
- Unhandled exceptions surfacing as 500s, an inconsistent error envelope, no machine-readable error codes, leaked internals (stack, SQL, paths).
- No rate limit on abuse-prone endpoints, CORS or security-header misconfiguration, sensitive data returned without need.
- No pagination on list endpoints, docs that disagree with the handler, retryable writes with no idempotency.

## db

- Missing PK/FK/UNIQUE/CHECK constraints, columns that should be non-null, wrong types (money, date, uuid), unconstrained status text.
- Join fanout, multi-step writes with no transaction, update/delete with unsafe predicates, **SQL built by string concatenation**.
- A missing index on a hot filter/join/order path, full scans on large tables, `SELECT *`, N+1 query emission in repositories. [App caching and pool sizing: performance]
- Non-idempotent migrations, unsafe DDL order, backfills with no rollback, breaking schema changes with no compatibility path, no online-index plan.

## auth

- Missing identity verification in login or callbacks, weak password hashing, no lockout or throttle, reset flows that leak whether an account exists, implicit allow.
- JWT checks missing issuer/audience/signature/expiry/algorithm, long-lived tokens with no rotation or revocation, cookies without `HttpOnly`/`Secure`/`SameSite`.
- No server-side authorization, IDOR/BOLA, bypassable role logic, trusting client-supplied roles.
- Unsafe logout or session invalidation, auth errors that leak internals, hardcoded auth secrets.
- No logging of auth events (login, reset, privilege change), PII in auth logs.

## reliability

- External calls with no timeout, no circuit breaker on a flaky dependency, no bulkhead between workloads that share a pool, unbounded fan-out.
- Retries on non-idempotent operations with no key, no backoff with jitter, no max attempts, retries on permanent errors (4xx, auth, validation).
- Hard failures where a stale or default answer would be safe, no kill switch on high-blast-radius paths.
- Critical paths with no structured logs, no request ID propagation, no error/latency metrics on hot paths.
- Readiness and liveness probes mixed up, no graceful shutdown on SIGTERM, accepting traffic before dependencies are ready.

## performance

- A cache in the wrong place, missing or wrong invalidation, no TTL on mutable data, stampede risk, no negative caching.
- Unbounded or mis-sized pools, no acquisition timeout, connections/handles leaked on error paths, timeouts not propagated.
- Blocking calls inside an event loop, pool sizes decoupled from the workload, a hot mutex, races on shared mutable state.
- In-process state that prevents horizontal scaling, hot partitions, fan-out without backpressure, no cursoring over large result sets.
- Buffering where streaming would bound memory, accidental retention, unbounded caches or queues.

## security

- Hardcoded or committed secrets, env secrets with insecure fallbacks, secrets in logs or errors, no rotation story.
- Weak primitives (MD5, SHA1, DES, RC4), ECB, static IVs or predictable nonces, home-grown crypto, missing TLS across a trust boundary, PII stored unencrypted, keys kept in env or on disk.
- Security events not logged, PII in logs, unrestricted log access.
- Command injection through subprocess, path traversal, templates rendered with untrusted input, unsafe deserialization (`pickle`, `yaml.load`, `eval`), XXE and zip bombs.
- Unpinned dependencies, lockfile missing or uncommitted, known-vulnerable packages (flag them for a CVE check), install scripts that reach the network.

## code

This lens judges quality and tests on the changed lines.

- **Complexity.** More than 21 branches in one function is `P0` (critical); 11–21 is `P1`.
- **Missing and weak tests.** Changed logic with no test is `P0`. Tests with no assertion, truthiness-only asserts, or snapshot-only tests of logic are `P1`.
- **Test shape.** An ice-cream-cone shape (heavy e2e, thin unit) on a non-trivial change is `P0`. Pure logic covered only by e2e, or cross-module flow covered only by mocks, is `P1`.
- **FIRST and AAA.** Real I/O or sleeps in unit tests, order-dependent tests, unfrozen time or randomness, mixed arrange/act/assert, several acts in one test. Tests of framework or library internals are waste.
- **Smells.** Functions over 50 lines or nested 4+ levels, magic values, duplicated blocks (cite both places), more than 4 positional parameters, god classes, dead code, TODOs with no owner.
- **Maintainability.** No error handling on I/O or parsing, vague names, `any` escape hatches, SRP/DIP violations in new abstractions.

Judge the diff. Flag an existing issue only when the change makes it materially worse.
