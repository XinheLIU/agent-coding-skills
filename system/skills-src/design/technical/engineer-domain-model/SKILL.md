---
name: engineer-domain-model
description: Maintain shared domain language and durable architectural decisions. Use when terms are vague or conflicting, the code and stated model disagree, or a hard-to-reverse trade-off needs an ADR.
---

# Engineer Domain Model

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [design.domain_question]
  retrieves: [system.terminology, design.relevant_decisions, change.requirements]
  produces: [design.domain_model, design.decision_records]
  updates: [system.terminology, design.applicable_decisions]
  invalidates: [context.term_dependents, design.contract_dependents]
  handoff_to: [design, implementation]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Read the configured `CONTEXT.md` or `CONTEXT-MAP.md`, relevant ADRs, and the product document resolved through memory/state pointers (`product.html#prd`, or a canonical legacy PRD) for candidate terms. Challenge overloaded terms with concrete scenarios and compare claims against code.

Update the glossary as soon as a term is resolved. Keep it implementation-free:

```markdown
## <Canonical term>
<Precise domain meaning and invariants.>
Not: <explicitly rejected synonyms or meanings>.
```

Offer an ADR only when the decision is hard to reverse, surprising without context, and selected through a real trade-off. Record context, decision, alternatives, consequences, and status. Create memory lazily and update its date; do not use the glossary as a spec or scratchpad. Resolved vocabulary and ADRs feed `build/implement` and its ticket decomposition; hand control back to the stage that raised the term.
