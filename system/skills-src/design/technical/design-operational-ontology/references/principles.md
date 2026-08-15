# Operational Ontology Design Principles

> Last updated: 2026-08-02

## Contents

1. [Core mental model](#core-mental-model)
2. [Priority-ordered modeling principles](#priority-ordered-modeling-principles)
3. [Semantic, Kinetic, and Dynamic layers](#semantic-kinetic-and-dynamic-layers)
4. [AI operating principles](#ai-operating-principles)
5. [Data, action, security, and governance](#data-action-security-and-governance)
6. [Architecture tradeoffs](#architecture-tradeoffs)
7. [Anti-patterns](#anti-patterns)
8. [Decision rules](#decision-rules)

## Core mental model

An operational ontology is a shared, typed representation of business reality and the permitted ways to change it. It is useful when it closes a controlled decision loop:

```text
observe state -> evaluate options -> authorize decision -> execute action
      ^                                                 |
      +--------- capture result and consequence <-------+
```

Its target is a **decision**, not a data catalog. Data describes the world; Logic calculates or judges; Action changes the world; Security constrains all three.

| Dimension | Required question |
|---|---|
| Data | Which typed objects, properties, links, events, and observations describe the decision context? |
| Logic | Which deterministic rules, models, and optimizers evaluate options? |
| Action | Which state changes and external effects are permitted? |
| Security | Who or what may see, calculate, propose, approve, execute, and audit? |

The ontology becomes a decision-learning system only when it captures:

- The context and versions used for a decision.
- The options considered and chosen action.
- The human, service, or Agent responsible.
- The actual execution result.
- The later business outcome.

## Priority-ordered modeling principles

Apply these in order when they conflict.

### 1. Domain-driven design

Model real business entities and relationships before looking at source schemas. Use `Customer`, `Campaign`, `OrderIntent`, or `Equipment`, not `crm_account_v2`, `tbl_1047`, or an API response envelope.

Separate identity from observations. A `Machine` is not its telemetry row; an `Instrument` is not a market tick; a `Customer` is not a CRM account record.

### 2. DRY, with the rule of three

Keep one authoritative representation for one business concept or capability. Tolerate one duplicate, investigate the second, refactor the third. Extract repeated shapes or capabilities into interfaces, shared value types, or Functions only after repetition is real.

### 3. Open for extension, stable against modification

Protect proven core contracts. Add a new linked type, interface implementation, Function version, or Action version instead of repeatedly breaking a shared type. A breaking change requires impact analysis, migration, replay tests, staged release, and rollback.

### 4. Composition over deep inheritance

Compose focused interfaces such as `Schedulable`, `RiskAssessable`, or `Approvable`. Avoid deep taxonomies and hybrid types created only to inherit unrelated abilities.

### 5. Pragmatism

Ontology is production software, not a quest for taxonomic perfection. Deliver the smallest valuable loop, record deliberate debt, and name the migration path. Business value may justify temporary denormalization or adapters, but the compromise must remain explicit.

## Semantic, Kinetic, and Dynamic layers

### Semantic: what exists

The Semantic layer supplies a stable business language:

- **Object Type**: a business entity, decision, event, observation, or durable record with stable identity.
- **Property**: a typed fact, derived value, status, or measurement with provenance and freshness.
- **Link Type**: a semantic relationship with direction, cardinality, source, and optional temporal validity/confidence.
- **Interface**: a reusable role or capability contract implemented by multiple Object Types.
- **Value Type**: a primitive plus business meaning and validation, such as `CurrencyAmount` or `InstrumentId`.

Logical graph semantics do not require a graph database. Implement Object and Link projections in the existing stack when it meets traversal, latency, consistency, and governance requirements.

### Kinetic: what may be done

The Kinetic layer pairs semantics with controlled behavior:

- **Function** calculates or judges without directly changing external state.
- **Action** performs a permitted state transition or external side effect.
- **Trigger** decides when a Function or Action is considered, not whether it is authorized.
- **Policy** validates actor, context, state, risk, and approvals before execution.
- **Writeback** commits or communicates the result to the authoritative system.
- **Compensation** reverses or counteracts an effect when distributed rollback is impossible.

An Action is a contract, not a generic tool call. Across external systems, define the local transaction boundary, idempotency key, retry policy, partial-failure behavior, and compensation. Never claim one global ACID transaction without evidence.

### Dynamic: what is changing and how the model evolves

Dynamic has two distinct responsibilities.

**Runtime dynamics** represent the changing world:

- Current object state and allowed transitions.
- Business events and observations.
- Event time versus ingestion/processing time.
- Relationship validity intervals and confidence.
- Freshness, drift, late data, and reconciliation.
- Decision results and downstream consequences.

**Evolution dynamics** govern changes to the representation and behavior:

- Version Object, Link, Function, Action, policy, prompt, Agent, and model contracts.
- Test historical decisions through replay.
- Maintain compatibility or supply explicit migration.
- Release through review, canary/gray rollout, observation, and rollback.
- Allow learning systems to propose changes; require governed promotion to production.

Do not use “Dynamic Ontology” as a synonym for a frequently updated table.

## AI operating principles

### Make the ontology authoritative

Treat the LLM as a replaceable coordinator. Supply typed objects, relationships, policies, and tool contracts as context. Do not let free-form text override source records, constraints, or permissions.

### Use the right engine

| Capability | Preferred engine |
|---|---|
| Arithmetic, validation, eligibility, limits | Deterministic Function or rules engine |
| Forecasting, ranking, anomaly/risk scoring | Versioned statistical or ML model |
| Optimization | Dedicated solver with explicit objective and constraints |
| Intent parsing, explanation, synthesis, plan proposal | LLM |
| State change | Authorized Action service |

An LLM may select or parameterize a tool within policy. It must not silently replace that tool.

### Expose typed, least-privilege tools

Derive the Agent tool surface from approved Functions and Actions. Validate arguments structurally, re-check authorization at execution time, restrict accessible Object/property views, and record every invocation.

Agent permissions never exceed the delegated human/service scope. Prompt instructions are not an authorization mechanism.

### Increase autonomy gradually

Use a staged ladder:

1. Read-only analysis.
2. Recommendation.
3. Pre-filled Action draft.
4. Human-confirmed low-risk execution.
5. Approved medium/high-risk execution.
6. Autonomous execution for a narrow, evaluated, reversible scope.

Promotion requires decision-chain evaluation and business outcome evidence. Autonomy may be reduced when drift, incident rate, data quality, or operating context changes.

### Evaluate the decision chain

Measure intent interpretation, object selection, relationship traversal, Function/model choice, Action parameters, policy response, execution result, writeback, and business outcome. Answer quality alone is insufficient.

## Data, action, security, and governance

### Separate system of record from system of action

Keep transactional truth in its authoritative system unless replacement is a deliberate goal. Place cross-system decision context and orchestration above existing systems. Write through governed APIs or commands, then reconcile the observed result.

### Govern identity and provenance

Every core Object needs:

- Stable identifier and resolution rules across sources.
- Attribute-level source authority or survivor rules.
- Observed time, source time, and ingestion time when relevant.
- Data quality/confidence for uncertain identity or relationships.
- Owner and sensitivity classification.

### Use four permission planes

1. Object/property visibility.
2. Function/model invocation.
3. Action execution and approval.
4. Agent tool availability and delegation.

Enforce policies at runtime for humans and Agents. Record policy version and decision in the audit trail.

### Capture decision lineage

A reproducible decision record should include:

```yaml
decision_id: "stable-id"
subject_refs: []
context_snapshot_ref: "versioned-or-time-bound-reference"
logic_versions: []
options_considered: []
selected_action: ""
actor: "human | service | agent"
policy_decision_ref: ""
execution_ref: ""
outcome_ref: ""
```

### Treat ontology changes as governed software changes

Classify change risk. A display label needs light review; a primary-key change, high-risk Action, or expanded Agent autonomy needs impact analysis, replay, security review, migration, staged release, observation, and rollback.

## Architecture tradeoffs

### Materialized/indexed versus federated reads

| Choice | Strength | Cost |
|---|---|---|
| Materialized/indexed | Predictable low-latency reads, source outage isolation, unified query policy | Freshness lag, duplicate storage, pipelines, reconciliation, lock-in risk |
| Federated | Fresh source data, less duplication, easier incremental adoption | Source latency/availability, query planning, uneven policy enforcement |
| Hybrid | Match each workload to its needs | More explicit consistency and ownership rules |

Do not simultaneously claim “zero-copy real time” and “pre-indexed independent reads” for the same path. State the path used by each Object/property.

### Normalization versus read performance

Prefer semantic clarity. Use Functions, projections, caches, or read models for hot access paths before corrupting the domain model. If denormalization is necessary, identify the canonical source, refresh/reconciliation rule, and consumers.

### Integrated platform versus semantic sovereignty

Deep integration improves policy consistency, typed Actions, and decision capture but may bind semantics and workflows to one vendor. Keep an implementation-neutral ontology contract, exportable identifiers, event schemas, policy definitions, and decision records when portability matters.

## Anti-patterns

| Anti-pattern | Why it fails | Replacement |
|---|---|---|
| Kitchen-sink Object mirrors one wide source table | Encodes storage accidents as business meaning | Model entities first; map sources later |
| Knowledge graph plus scripts | Actions, permissions, and feedback remain implicit | Typed Functions, Actions, policies, and lineage |
| Dashboard as the goal | Stops at insight and preserves the execution gap | Name the decision and controlled Action |
| LLM as policy/calculator | Probabilistic, non-reproducible, hard to audit | Deterministic Function or model with versioned contract |
| Prompt-only guardrail | Cannot enforce authorization or state invariants | Runtime policy and Action preconditions |
| Generic `execute(command)` Action | No semantic intent, risk boundary, or audit shape | Domain Action such as `ReserveInventory` |
| “Real-time” without timestamps | Hides staleness and ordering errors | Define event/source/processing time and SLA |
| Self-learning production rules | Converts feedback noise into uncontrolled behavior | Proposal, replay, review, canary, rollback |
| Deep inheritance taxonomy | Brittle and hard to extend | Focused interfaces and composition |
| Big-bang enterprise ontology | Slow, political, and untestable | Minimum Runnable Ontology around one loop |

## Decision rules

- Create an Object Type when it has identity, independent lifecycle, distinct permissions, a source-of-truth boundary, or participates materially in decisions.
- Create an Event/Observation Type when history, event-time ordering, provenance, or replay matters. Do not overwrite history into a current-state property.
- Create a Link Type when the relationship has business meaning. Add a relationship Object when the link has its own properties, lifecycle, permissions, or actions.
- Create a Function when logic is reusable, testable, versioned, or required for authorization/decisioning.
- Create an Action only for a named business state change or effect. Keep read-only operations as queries or Functions.
- Create an Interface after multiple types share a stable role/capability; do not invent one for a single use.
- Use AI only where ambiguity or long-tail language justifies probabilistic reasoning. Keep hard limits, precise math, and final authorization deterministic.
