---
name: design-operational-ontology
description: Design or review domain-specific operational ontology architectures that integrate semantic models, executable Kinetic actions, Dynamic context and evolution, AI agents, data/writeback, decision lineage, security, and governance. Use when a user provides a PRD, product idea, workflow, data model, or existing technical architecture and wants to create or upgrade it with Palantir-inspired ontology principles; build an executable digital twin or system of action; define AI-safe decision loops; or design scenarios such as O2O投放/campaign delivery, B2C commerce, quantitative trading, manufacturing, finance, or operations.
---

# Design Operational Ontology

> Last updated: 2026-08-10

Turn a business decision loop—not a database schema—into a vendor-neutral operational ontology that people and AI can query, act through, audit, and evolve safely.

## Required references

Read these files before producing a design:

1. Read [references/principles.md](references/principles.md) for the architectural doctrine and priority rules.
2. Read [references/architecture-spec.md](references/architecture-spec.md) for the required contracts and deliverable structure.
3. Read [references/scenario-patterns.md](references/scenario-patterns.md) only when its domain patterns match the request or help transfer a pattern to a new domain.

The skill is self-contained. Do not require the source wiki, the Palantir product, or a particular graph database.

## Hard rules

1. Start from a decision and measurable outcome, never from tables or tools.
2. Model business reality. Treat source schemas as evidence to map later, not as the ontology.
3. Separate deterministic logic, statistical/ML logic, and LLM judgment. Never let an LLM impersonate a calculator, policy engine, or source of truth.
4. Do not call a design operational unless at least one controlled action changes state and its result is observed or written back.
5. Do not call a design dynamic unless it covers both live context and governed model evolution.
6. Treat security as part of every data, logic, action, and Agent contract—not as a final section added later.
7. Make facts, assumptions, recommendations, unresolved questions, and deliberate technical debt visibly distinct.
8. Keep designs vendor-neutral by default. Map to Palantir products only when explicitly requested.
9. Do not promise distributed ACID. State the actual transaction boundary; use idempotency, sagas, or compensation across external systems.
10. Never design uncontrolled production self-modification. Learning may propose changes; governed evaluation and release must approve them.

## Route the request

Choose one mode and state it:

- **Greenfield mode**: the user has a PRD (including an effort PRD at `docs/product/<slug>/prd.md`), idea, desired capability, or incomplete workflow.
- **Upgrade mode**: the user has an existing architecture, schema, service design, or implementation.
- **Review mode**: the user wants critique or a gap analysis without a rewritten target design.

If multiple interpretations would materially change the design, ask before choosing. For example, `O2O 投放` may mean ad delivery, coupon allocation, local-store traffic acquisition, or operational dispatch.

## Run the interaction

### Build a working brief

Maintain this compact brief during the conversation:

```yaml
business_outcome: ""
decision_to_improve: ""
decision_maker: "human | system | agent"
triggering_event: ""
action_and_real_world_effect: ""
system_of_record: ""
write_authority: ""
autonomy_and_risk: ""
success_metric: ""
constraints: []
open_questions: []
```

### Ask only blocking questions

Ask one short round of at most three high-leverage questions. Prefer this order:

1. Which recurring decision and measurable outcome should improve?
2. Which system owns the truth, and where must an approved action be written?
3. What may AI do autonomously, and what requires review or approval?

Skip questions already answered by provided artifacts. Continue with explicit assumptions when they are reversible and low risk; stop when an answer changes the decision loop, write authority, safety boundary, or architecture class.

Do not produce a full ontology while the target decision is still unnamed.

## Greenfield workflow

### 1. Frame one use case

Define a single loop:

```text
event -> observe -> decide -> authorize -> act -> write back -> measure -> learn
```

Record the actor, decision cadence, action, consequence, latency target, and success metric. Push back on requests framed only as “build a dashboard,” “add an Agent,” or “create a knowledge graph.”

### 2. Derive competency questions

Write questions the ontology must answer and use later as acceptance tests:

- Fact: What is the current state of the focal object?
- Relationship: Which linked objects affect this decision?
- Judgment: Which rule or model selects an option?
- Action: Which permitted state change should occur, and where is it committed?

Create the event-chain mapping from event to object, links, judgment, action, writeback, and outcome.

### 3. Design the Semantic layer

Define the smallest domain model that can run the loop:

- Object Types with stable identity, business meaning, owner, source authority, state, provenance, and temporal semantics.
- Properties with business names, value types, constraints, freshness, sensitivity, and derivation.
- Link Types with semantic names, direction, cardinality, source, confidence, and validity interval when relationships change over time.
- Interfaces for reusable capabilities or roles. Prefer composition over deep inheritance.

Start with 3–8 core objects. Add a type only if it changes a competency question, decision, permission, lifecycle, or source-of-truth boundary.

### 4. Design Logic and AI boundaries

Classify every decision capability:

- **Deterministic**: policy, validation, arithmetic, constraint solving.
- **Statistical/ML**: scoring, forecasting, optimization under uncertainty.
- **LLM**: intent parsing, explanation, synthesis, plan proposal, long-tail coordination.

Define typed inputs/outputs, version, trigger, SLA, confidence, failure behavior, tests, and owner. Route precise calculations and hard constraints through Functions or dedicated engines. Let the LLM coordinate them through a typed tool surface.

### 5. Design the Kinetic layer

For each Action, specify the complete action contract from `architecture-spec.md`: binding, actor, inputs, preconditions, authorization, risk, idempotency, transaction boundary, state transition, side effects, writeback, emitted events, audit, and compensation.

Add a state–action matrix. An action unavailable in the current state must be structurally blocked, not merely discouraged in a prompt.

### 6. Design the Dynamic layer

Cover both meanings explicitly:

- **Runtime dynamics**: events, observations, current state, event time, relationship validity, freshness, feedback, drift, and changing operational context.
- **Evolution dynamics**: versioned Object/Link/Function/Action/Agent contracts, compatibility, migration, replay tests, canary release, rollback, and ownership.

Model decisions and outcomes so the system learns from consequences, not just from model responses.

### 7. Design the runtime architecture

Separate:

- Systems of record from the system of action.
- Read projection/index from source transactions.
- Ontology metadata from object state.
- Query/Function execution from Action execution.
- Policy enforcement from Agent orchestration.
- Decision/audit history from mutable current state.

Choose materialized/indexed, federated, or hybrid reads deliberately. State freshness, consistency, availability, cost, and lock-in tradeoffs. Preserve existing systems through non-disruptive orchestration unless replacement is required by a named constraint.

### 8. Add security, governance, and evaluation

Define four permission planes:

1. Object/property visibility.
2. Function/model invocation.
3. Action execution.
4. Agent tool access.

Risk-tier every Action. Require human approval and compensation in proportion to external impact and reversibility. Evaluate the whole decision chain: intent, object selection, context, Function choice, Action parameters, policy handling, execution, writeback, and business outcome.

### 9. Scope the Minimum Runnable Ontology

Default first slice:

- 3–8 Object Types.
- 5–15 critical Link Types.
- 1–3 decision Functions.
- 2–5 controlled Actions.
- One complete event-to-outcome loop.
- One baseline permission/audit model.
- One measurable acceptance set.

Reduce scope further when one loop needs fewer constructs. Do not inflate counts to meet the range.

## Upgrade workflow

1. Read the existing design fully and preserve its explicit constraints.
2. Reconstruct the current decision loop, system boundaries, data flows, writes, permissions, SLAs, and failure modes.
3. Map current components to Data / Logic / Action / Security and Semantic / Kinetic / Dynamic responsibilities.
4. Identify gaps: table-shaped domain model, duplicated concepts, read-only analytics, implicit rules, ungoverned AI, missing writeback, missing decision lineage, missing temporal semantics, unsafe actions, or unversioned evolution.
5. Produce a `Keep / Change / Add / Retire` delta matrix. Trace every change to a decision-loop gap or principle.
6. Prefer wrappers, projections, typed contracts, and controlled write paths over gratuitous replatforming.
7. Deliver both the target architecture and an incremental migration path. Do not hide compatibility, data migration, dual-run, or rollback work.

In Review mode, stop after the evidence-backed gap analysis and ranked recommendations unless the user also asks for a target design.

## Deliver and verify

Use the structure in [references/architecture-spec.md](references/architecture-spec.md). Keep prose short; prefer explicit tables, typed contracts, and one useful end-to-end diagram.

Before delivery, verify:

- Every proposed construct traces to a competency question or cross-cutting control.
- One complete decision loop reaches a real Action, writeback/observation, and outcome metric.
- Every Object has identity and a source/provenance strategy.
- Every Function has a type, version, trigger, test, and failure behavior.
- Every Action has authorization, risk, idempotency, audit, and compensation or an explicit reason none is possible.
- Every AI capability has a typed context/tool boundary, least privilege, evaluation, and human-control policy.
- Runtime context and schema evolution are both modeled.
- Security is consistent across human and Agent paths.
- Tradeoffs and unresolved facts are visible.
- The first delivery is a runnable vertical slice, not an enterprise-wide taxonomy.

If verification fails because a fact is missing, ask for that fact. If it fails because the design is weak, revise the design before presenting it. The delivered design feeds `engineering/feature/spec`.

## Example triggers

- “Turn this O2O campaign PRD into an AI + Dynamic/Kinetic Ontology architecture.”
- “Upgrade our B2C customer-data platform design into a decision-centered system of action.”
- “Design a governed ontology and Agent boundary for a quantitative trading workflow.”
- “Review this microservice architecture for semantic, action, writeback, and decision-lineage gaps.”
