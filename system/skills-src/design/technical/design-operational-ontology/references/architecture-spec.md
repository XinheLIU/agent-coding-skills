# Operational Ontology Architecture Spec

> Last updated: 2026-08-02

## Contents

1. [Default deliverable](#default-deliverable)
2. [Design brief](#1-design-brief)
3. [Decision loop and competency questions](#2-decision-loop-and-competency-questions)
4. [Upgrade delta](#3-upgrade-delta)
5. [Semantic contracts](#4-semantic-contracts)
6. [Logic and AI contracts](#5-logic-and-ai-contracts)
7. [Kinetic contracts](#6-kinetic-contracts)
8. [Dynamic contracts](#7-dynamic-contracts)
9. [Runtime architecture](#8-runtime-architecture)
10. [Security and governance](#9-security-and-governance)
11. [Delivery and verification](#10-delivery-and-verification)

## Default deliverable

Produce sections 1–10 unless the user asks for a narrower review. Omit empty sections; do not fill them with generic prose. Use business language from the user’s domain.

Mark each important statement as one of:

- **Fact**: present in a source artifact or confirmed by the user.
- **Assumption**: necessary but unconfirmed.
- **Recommendation**: a design choice.
- **Open question**: materially unresolved.
- **Debt**: deliberate temporary compromise with an exit condition.

## 1. Design brief

| Field | Content |
|---|---|
| Business outcome | Measurable operational change |
| Decision | Repeated choice the design improves |
| Decision owner | Human or accountable service |
| Trigger and cadence | Event, schedule, or request |
| Action | Real-world or system state change |
| Consequence/risk | Financial, safety, compliance, customer, or operational effect |
| System of record | Owner of committed truth |
| System of action | Where cross-system decisioning/orchestration happens |
| AI role | None, explain, recommend, draft, or execute |
| Success metrics | Business, decision-quality, technical, and safety metrics |
| Constraints | Current stack, latency, scale, regulation, budget, team |

State scope and non-goals. For a greenfield idea, show the assumptions the user must confirm. For an upgrade, cite the current components being preserved.

## 2. Decision loop and competency questions

### Decision loop

| Stage | Event/input | Object context | Logic | Actor | Action/output | State/writeback | Metric |
|---|---|---|---|---|---|---|---|
| Observe |  |  |  |  |  |  |  |
| Decide |  |  |  |  |  |  |  |
| Authorize |  |  |  |  |  |  |  |
| Act |  |  |  |  |  |  |  |
| Learn |  |  |  |  |  |  |  |

### Competency questions

Provide a compact, testable set:

| ID | Type | Question | Required constructs | Acceptance evidence |
|---|---|---|---|---|
| CQ-F1 | Fact |  | Object/Property |  |
| CQ-R1 | Relationship |  | Link |  |
| CQ-J1 | Judgment |  | Function/model/policy |  |
| CQ-A1 | Action |  | Action/writeback |  |

### Event-chain mapping

```text
triggering event
  -> locate subject Object
  -> traverse decision-relevant Links
  -> compute deterministic/ML judgments
  -> propose and authorize Action
  -> commit/write back
  -> observe result and business outcome
  -> append decision lineage
```

Replace generic labels with domain names in the final diagram.

## 3. Upgrade delta

Include only in Upgrade or Review mode.

| Current element | Evidence/current role | Keep / Change / Add / Retire | Target role | Principle or gap | Migration impact |
|---|---|---|---|---|---|

Also map the baseline:

| Current component | Data | Logic | Action | Security | Semantic | Kinetic | Dynamic |
|---|---|---|---|---|---|---|---|

Rank gaps by decision-loop impact, not theoretical purity.

## 4. Semantic contracts

### Object Types

| Object Type | Business meaning | Stable ID | Key properties/state | System of record | Freshness | Owner | Sensitivity |
|---|---|---|---|---|---|---|---|

For each Object, state the identity-resolution and attribute-provenance strategy when more than one source contributes.

### Properties

List only decision-critical or governance-critical properties.

| Property | Object | Value type/unit | Base or derived | Source/Function | Constraints | Freshness | Sensitivity |
|---|---|---|---|---|---|---|---|

### Link Types

| Link Type | From -> To | Business semantics | Cardinality | Source | Valid time/confidence | Traversal use |
|---|---|---|---|---|---|---|

Use a relationship Object instead of a plain Link when the relationship carries identity, properties, history, permissions, or actions.

### Interfaces/value types

| Contract | Kind | Shared fields/capabilities | Implemented by | Why it is stable/reused |
|---|---|---|---|---|

Do not add an interface without at least two credible implementations or a clear cross-team stability need.

### Typed pseudo-spec

Use a compact implementation-neutral form when precision helps:

```yaml
object_types:
  Order:
    id: OrderId
    state: [pending, approved, rejected]
    source_of_record: order_service

link_types:
  placed_by:
    from: Order
    to: Customer
    cardinality: many_to_one
```

This is an architectural contract, not deployable configuration unless the user supplies a target platform schema.

## 5. Logic and AI contracts

### Functions/models

| Capability | Type: deterministic / ML / optimizer / LLM | Typed input -> output | Trigger | Version | SLA | Failure behavior | Tests/owner |
|---|---|---|---|---|---|---|---|

Make rules and constraints explicit. Separate a model score from the policy that decides what the score permits.

### Agent contract

| Field | Required content |
|---|---|
| Agent goal | One bounded decision-support or execution responsibility |
| Context view | Allowed Object Types, properties, Links, time window |
| Functions/tools | Typed allowlist |
| Actions | Typed allowlist and risk tier |
| Forbidden operations | Explicit deny list |
| Authorization | Delegation source and runtime re-check |
| Human control | Review/approval/escalation conditions |
| Memory | What may persist; retention and provenance |
| Evaluation | Intent, context, tool, argument, policy, outcome tests |
| Fallback | Refuse, ask, queue, or hand off |

### AI boundary diagram

Show the LLM coordinating typed retrieval, Functions, policies, and Actions. Keep the policy check immediately before Action execution; do not draw the LLM as directly writing a system of record.

## 6. Kinetic contracts

### State–action matrix

| Object state | Allowed Action | Actor | Preconditions | Approval | Next state | Prohibited alternatives |
|---|---|---|---|---|---|---|

### Action catalog

| Action | Bound Object/interface | Intent | Inputs | Preconditions/invariants | Authorization | Risk tier | Idempotency key | Transaction boundary | Side effects/writeback | Compensation | Emitted event | Audit/success |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Risk tiers:

| Tier | Typical effect | Minimum control |
|---|---|---|
| Low | Internal reversible state with no external effect | Runtime authorization and log |
| Medium | External write, reversible | Authorization, idempotency, log, rollback |
| High | External or broad effect, difficult to reverse | Approval, bounded batch, compensation, full lineage |
| Critical | Safety, regulated, contractual, or major financial effect | Multi-party approval, explicit human confirmation, hard limits, full audit |

For distributed effects, specify retries, timeout, duplicate handling, partial completion, reconciliation, and escalation.

## 7. Dynamic contracts

### Events and observations

| Event/Observation | Subject | Producer | Event time | Processing SLA | Ordering/dedup | Retention | Consumer/effect |
|---|---|---|---|---|---|---|---|

### Decision and outcome records

| Record | Required fields | Retention | Query/replay use |
|---|---|---|---|
| Decision | Context ref, data time, logic/model/policy versions, options, actor, selected Action |  | Audit and replay |
| Execution | Action version, arguments, approvals, idempotency, effects, errors |  | Reconciliation |
| Outcome | Delayed business result, attribution window, metric |  | Learning and evaluation |

### Evolution plan

| Asset | Version strategy | Compatibility rule | Replay test | Release | Rollback | Owner |
|---|---|---|---|---|---|---|
| Object/Link schema |  |  |  |  |  |  |
| Function/model |  |  |  |  |  |  |
| Action/policy |  |  |  |  |  |  |
| Agent/prompt/toolset |  |  |  |  |  |  |

Describe feedback as a governed pipeline:

```text
outcomes -> evaluation/drift -> change proposal -> replay -> review
         -> canary -> observation -> promote or rollback
```

## 8. Runtime architecture

### Required responsibility map

Assign each responsibility to an existing or proposed component:

| Responsibility | Component | Build/reuse | State owned | API/event boundary | Scale/SLA | Failure mode |
|---|---|---|---|---|---|---|
| Source adapters/CDC |  |  |  |  |  |  |
| Mapping/entity resolution |  |  |  |  |  |  |
| Ontology metadata/schema registry |  |  |  |  |  |  |
| Object/Link projection and query |  |  |  |  |  |  |
| Function/model runtime |  |  |  |  |  |  |
| Policy/identity engine |  |  |  |  |  |  |
| Action/workflow engine |  |  |  |  |  |  |
| Agent context/tool gateway |  |  |  |  |  |  |
| Decision/audit ledger |  |  |  |  |  |  |
| Writeback/reconciliation |  |  |  |  |  |  |
| Evaluation/monitoring |  |  |  |  |  |  |

Do not invent a new service for each row if the existing stack can own several responsibilities coherently.

### Data path choices

For each critical Object/property, state:

| Data path | Materialized / federated / hybrid | Freshness | Consistency | Source outage behavior | Reconciliation | Cost/lock-in |
|---|---|---|---|---|---|---|

### Diagrams

Prefer two small diagrams over one unreadable mega-diagram:

1. System context: sources, ontology operational layer, AI/human consumers, writeback targets.
2. One end-to-end sequence: event to decision, authorization, Action, writeback, and outcome.

## 9. Security and governance

### Permission matrix

| Principal/role | Object/property view | Function/model invoke | Action propose | Action approve/execute | Agent tools | Audit scope |
|---|---|---|---|---|---|---|

### Governance matrix

| Change | Risk | Required review | Replay/evaluation | Release mode | Rollback |
|---|---|---|---|---|---|

Include data classification, retention, geographic/regulatory constraints, separation of duties, break-glass behavior, and incident response only when relevant to the scene.

## 10. Delivery and verification

### Minimum Runnable Ontology plan

| Slice | Included constructs | User value | Acceptance test | Dependency | Exit/expansion condition |
|---|---|---|---|---|---|

The first slice must execute one controlled loop on representative data. A diagram or taxonomy alone is not runnable.

### Acceptance tests

Cover:

- Identity resolution and source conflict.
- Relationship traversal and temporal validity.
- Function/model correctness and version reproducibility.
- State transition and Action preconditions.
- Authorization parity for human and Agent paths.
- Idempotency, retry, partial failure, compensation, and reconciliation.
- Decision and execution replay.
- Late/stale data and drift.
- Business outcome measurement.

### Ranked tradeoffs and open questions

Finish with:

1. Recommended architecture and why.
2. Highest-risk assumption.
3. Most expensive irreversible choice.
4. A simpler fallback.
5. The next user decision required.
