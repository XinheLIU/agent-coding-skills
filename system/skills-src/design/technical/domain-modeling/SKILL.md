---
name: domain-modeling
description: Maintain shared domain language and durable architectural decisions. Use when terms are vague or conflicting, the code and stated model disagree, or a hard-to-reverse trade-off needs an ADR.
---

# Domain Modeling

Last updated: 2026-08-10

Read the configured `CONTEXT.md` or `CONTEXT-MAP.md`, relevant ADRs, and — when the effort has one — the PRD (`docs/product/<slug>/prd.md`) for candidate terms. Challenge overloaded terms with concrete scenarios and compare claims against code.

Update the glossary as soon as a term is resolved. Keep it implementation-free:

```markdown
## <Canonical term>
<Precise domain meaning and invariants.>
Not: <explicitly rejected synonyms or meanings>.
```

Offer an ADR only when the decision is hard to reverse, surprising without context, and selected through a real trade-off. Record context, decision, alternatives, consequences, and status. Create memory lazily and update its date; do not use the glossary as a spec or scratchpad. Resolved vocabulary and ADRs feed `spec` and `plan.md`; hand control back to the stage that raised the term.
