---
name: analyze-nfrs
description: Analyze non-functional requirements for frameworks and libraries — usability, performance, scalability, fault tolerance, generality. Produces measurable targets and implementation constraints.
---

# Analyze Non-Functional Requirements

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [change.requirements]
  retrieves: [system.current_state, design.capability_map, design.relevant_decisions]
  produces: [design.nfr_targets, verification.nfr_strategy]
  updates: [design.accepted_constraints]
  invalidates: [design.affected_contracts, verification.nfr_coverage]
  handoff_to: [design_architecture, design_foundation, design_modules]
```

## What this skill does

Analyzes and specifies non-functional requirements (NFRs) for frameworks, libraries, SDKs, and reusable platform components. Produces measurable targets for usability, performance, scalability, fault tolerance, generality, observability, and testability with trade-off analysis.

## When to use

- Building a framework, library, SDK, or shared platform component
- User says: "design a reusable X", "build an extensible Y", "performance-critical Z"
- Requirements phase for non-business generic infrastructure
- Before designing system architecture for framework work
- When a component will be used by multiple teams or external developers

**Entry requirement:** The component being designed is reusable infrastructure, not a single-use feature.

## What you'll produce

- `NFR-SPEC.md` — measurable NFR targets with rationale and acceptance criteria
- Trade-off analysis (generality vs. simplicity, performance vs. maintainability)
- Constraint documentation for downstream design and implementation
- Test strategy for validating NFRs

## How it works

### 1. Identify the NFR dimensions

For the component being designed, determine which NFRs matter:

**Usability** — How easy is it for developers to use correctly?
- API learnability (can devs understand it from examples?)
- Error messages (actionable guidance when things fail)
- Defaults (safe and sensible without configuration)
- Discoverability (can devs find the right API for their need?)
- Documentation burden (how much reading before productive use?)

**Performance** — How fast and lightweight is it?
- Latency budgets (p50, p95, p99 response times)
- Throughput (requests/operations per second)
- Memory footprint (heap, stack, allocations)
- Cold start time (initialization cost)
- Resource efficiency (CPU, I/O, network)

**Scalability** — How well does it handle growth?
- Vertical scaling (larger inputs, more data)
- Horizontal scaling (more instances, sharding)
- Resource usage growth (linear, logarithmic, quadratic?)
- Bottlenecks (what limits scale?)

**Fault tolerance** — How does it handle failures?
- Failure modes (what can go wrong?)
- Error propagation (fail fast vs. degrade gracefully)
- Retry policies (idempotency, backoff, limits)
- Degradation paths (what works when dependencies fail?)
- Recovery mechanisms (automatic vs. manual)

**Generality** — How flexible and extensible is it?
- Extension points (where can users customize?)
- Plugin architecture (how to add new capabilities?)
- Configurability (what's tunable without code changes?)
- Abstraction level (too specific vs. too abstract?)
- Composability (works with other components?)

**Observability** — How visible is its behavior?
- Logging (what gets logged, at what levels?)
- Metrics (what's measured, at what granularity?)
- Tracing hooks (distributed tracing integration?)
- Debug mode (verbose diagnostics when troubleshooting?)
- Health checks (how to know if it's working?)

**Testability** — How easy is it to test?
- Test seams (where can tests inject behavior?)
- Mock points (what dependencies can be faked?)
- Fixture requirements (what setup is needed?)
- Determinism (reproducible behavior in tests?)
- Isolation (tests don't interfere with each other?)

Not every dimension applies to every component. Focus on the ones that matter for the use case.

### 2. Specify measurable targets

For each relevant NFR, set concrete targets with acceptance criteria:

**Example - Usability:**
- Target: "Developer can make first successful API call within 5 minutes of reading quickstart"
- Acceptance: Quickstart example runs without errors for 90% of users (measured via telemetry)
- Rationale: Adoption depends on fast initial success

**Example - Performance:**
- Target: "p95 request latency < 10ms at 1000 qps throughput"
- Acceptance: Load test shows p95 ≤ 10ms across 5-minute window at 1000 qps
- Rationale: Backend SLA requires < 50ms end-to-end, leaving 40ms for other hops

**Example - Fault tolerance:**
- Target: "Circuit breaker opens after 5 consecutive failures, half-open after 30s"
- Acceptance: Integration test verifies circuit opens, requests fast-fail while open, half-open attempt after 30s
- Rationale: Prevent cascade failures in distributed system

Write targets as:
- **Target:** [measurable statement]
- **Acceptance:** [how to verify]
- **Rationale:** [why this number]

### 3. Analyze trade-offs

NFRs often conflict. Document the trade-offs explicitly:

**Generality vs. Simplicity:**
- More extension points = more complexity = higher learning curve
- Where did you choose simplicity over flexibility? Why?
- What use cases were ruled out by that choice?

**Performance vs. Maintainability:**
- Aggressive optimization = harder to understand/modify
- Where did you choose readability over speed? Why?
- What performance optimizations were deferred?

**Fault tolerance vs. Performance:**
- Retries, circuit breakers, timeouts add latency
- Where did you choose reliability over speed? Why?

**Usability vs. Power:**
- Simple API may hide advanced features
- Where did you choose ease-of-use over flexibility? Why?

For each trade-off, document:
- The tension (which two NFRs conflict)
- The choice made (which one wins in this case)
- The rationale (why that choice for this use case)
- The consequence (what's limited by that choice)

### 4. Document constraints for implementation

Extract design constraints from the NFR targets:

**From performance targets:**
- "Must use async I/O to meet latency budget"
- "Must cache parsed config to meet cold start requirement"

**From usability targets:**
- "Default config must work for 80% of use cases"
- "Error messages must include resolution steps"

**From fault tolerance targets:**
- "All network calls must have timeout and retry logic"
- "Must handle partial failures without crashing"

**From generality targets:**
- "Must expose plugin interface for custom validators"
- "Core logic must not depend on specific transport"

These constraints feed directly into `design/technical/harden-architecture`.

### 5. Define NFR test strategy

Specify how each NFR will be validated:

**Usability:**
- Manual quickstart walkthrough by fresh developer
- API documentation coverage check
- Error message audit (do they explain what happened and what to do?)

**Performance:**
- Load test at target qps with latency measurement
- Memory profiling under sustained load
- Cold start timing in test harness

**Scalability:**
- Benchmark with varying input sizes (10x, 100x, 1000x)
- Horizontal scaling test (2x, 5x, 10x instances)

**Fault tolerance:**
- Chaos testing (kill dependencies, inject errors)
- Circuit breaker integration test
- Retry behavior verification

**Generality:**
- Build example plugins using extension points
- Test with multiple backend implementations

**Observability:**
- Verify metrics emitted under load
- Check logs contain expected context
- Integration with tracing framework

**Testability:**
- Unit test coverage with mocked dependencies
- Integration tests with real dependencies
- Verify test isolation (parallel test runs don't interfere)

## Example: NFR analysis for an API client library

### NFR dimensions (selected)

**Usability, Performance, Fault tolerance** are critical.
**Generality, Observability, Testability** matter but are secondary.
**Scalability** is not a primary concern (caller scales, not the library).

### Targets

**Usability:**
- Target: Developer makes first successful API call within 5 minutes of reading quickstart
- Acceptance: Quickstart runs without errors, measured via test harness
- Rationale: Adoption blocked by high initial friction

**Performance:**
- Target: p95 request latency overhead < 5ms (on top of network round trip)
- Acceptance: Benchmark shows < 5ms for serialization + deserialization + client logic
- Rationale: Client should not be bottleneck; network dominates latency

**Fault tolerance:**
- Target: Automatic retry with exponential backoff for transient failures (500, 502, 503, 504, timeouts)
- Acceptance: Integration test verifies 3 retries with 100ms, 200ms, 400ms delays
- Rationale: Network blips should not surface to caller as errors

### Trade-offs

**Generality vs. Simplicity:**
- Choice: Simple synchronous API by default, advanced async API for power users
- Rationale: 80% of use cases are synchronous request/response; async adds complexity
- Consequence: High-throughput use cases need async API

**Performance vs. Maintainability:**
- Choice: JSON serialization using standard library, not hand-rolled parser
- Rationale: 5ms overhead is acceptable; correctness and maintainability matter more
- Consequence: Cannot optimize serialization below library limits

**Fault tolerance vs. Performance:**
- Choice: Retries enabled by default, can be disabled for idempotency concerns
- Rationale: Most APIs are idempotent; retry-by-default improves reliability
- Consequence: Non-idempotent calls need explicit retry disabling

### Implementation constraints

- Must use connection pooling to reuse TCP connections (performance)
- Must include timeout on every network call (fault tolerance)
- Default config must specify retry policy (usability)
- Error types must distinguish client errors (4xx) from server errors (5xx) (fault tolerance)
- Must expose hooks for logging requests/responses (observability)

### NFR test strategy

- Usability: Manual quickstart test by 3 developers unfamiliar with library
- Performance: Benchmark suite measuring serialization, connection overhead, request latency
- Fault tolerance: Integration tests with fault injection (network errors, timeouts, 500 errors)

## Exit criteria

- `NFR-SPEC.md` complete with measurable targets for each relevant NFR
- Trade-offs documented with choices and rationales
- Implementation constraints extracted and ready for architecture design
- NFR test strategy specified with acceptance criteria
- All targets have clear "how to verify" steps

## What this skill does NOT do

- Design the system architecture (that's `harden-architecture`)
- Implement the component (that's `build/`)
- Define functional requirements (that's `plan/define-outcomes` and `plan/specs/`)
- Test the implementation (that's `quality/`)

## Cross-references

- Upstream: `plan/define-outcomes` defines what the component does
- Downstream: `engineer-domain-model` for API naming and domain clarity
- Downstream: `harden-architecture` uses constraints to design structure
- Downstream: `quality/test-specs` uses NFR test strategy

---

## Instructions for the agent

You are analyzing non-functional requirements for a reusable framework or library.

### Step 1: Identify NFR dimensions

Determine which NFRs matter for this component:
- Usability (developer experience)
- Performance (speed, memory, resources)
- Scalability (growth handling)
- Fault tolerance (failure handling)
- Generality (extensibility, flexibility)
- Observability (visibility into behavior)
- Testability (ease of testing)

Not every dimension applies. Focus on the critical ones for the use case.

### Step 2: Specify measurable targets

For each relevant NFR, write:
- **Target:** [measurable statement]
- **Acceptance:** [how to verify it]
- **Rationale:** [why this number matters]

Make targets concrete and verifiable, not vague aspirations.

### Step 3: Analyze trade-offs

Identify conflicts between NFRs:
- Generality vs. Simplicity
- Performance vs. Maintainability
- Fault tolerance vs. Performance
- Usability vs. Power

For each conflict, document:
- The tension
- The choice made
- The rationale
- The consequence (what's limited)

### Step 4: Extract implementation constraints

Turn NFR targets into design constraints:
- "Must use X to meet Y requirement"
- "Cannot do A because of B constraint"

These constraints guide architecture decisions.

### Step 5: Define NFR test strategy

Specify how to validate each NFR:
- What to test
- How to measure
- Acceptance thresholds

### Output format

Write `NFR-SPEC.md`:

```markdown
# Non-Functional Requirements: [Component Name]

## Context
[What the component is, who uses it, why NFRs matter]

## NFR Dimensions
[Which NFRs apply: usability, performance, scalability, fault tolerance, generality, observability, testability]

## Targets

### Usability
- **Target:** [measurable statement]
- **Acceptance:** [verification method]
- **Rationale:** [why]

### Performance
- **Target:** [measurable statement]
- **Acceptance:** [verification method]
- **Rationale:** [why]

[Continue for each dimension]

## Trade-off Analysis

### Generality vs. Simplicity
- **Tension:** [describe conflict]
- **Choice:** [which wins]
- **Rationale:** [why]
- **Consequence:** [what's limited]

[Continue for each trade-off]

## Implementation Constraints

Derived from NFR targets:
- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## NFR Test Strategy

### Usability
- Test: [what to test]
- Method: [how to measure]
- Acceptance: [threshold]

### Performance
- Test: [what to test]
- Method: [how to measure]
- Acceptance: [threshold]

[Continue for each dimension]
```

### Quality checklist

Before finishing:
- [ ] Every NFR target is measurable (not "fast" but "< 10ms p95")
- [ ] Every target has acceptance criteria (how to verify)
- [ ] Trade-offs are explicit (not hidden assumptions)
- [ ] Constraints are concrete (guide architecture design)
- [ ] Test strategy covers all critical NFRs
- [ ] Rationales explain why these numbers matter

### Boundaries

This skill analyzes requirements; it does not design the system. Use `harden-architecture` to turn constraints into structure.

If functional requirements are unclear, run `plan/define-outcomes` first.
