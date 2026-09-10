---
name: brainstorm
description: Turn an ambiguous idea into a Jobs-to-be-Done brief through Socratic dialogue. Use when the user shares a vague idea, asks "what should I build", wants to explore a concept, or needs requirements discovery.
disable-model-invocation: true
---

# Brainstorm

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [product.idea]
  retrieves: [product.relevant_context]
  produces: [product.problem_hypotheses]
  updates: [product.discovery_records]
  invalidates: [product.premise_dependents]
  handoff_to: [product]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Turn an ambiguous idea into a Jobs-to-be-Done brief through natural Socratic conversation.
Ask questions in small blocks, understand the context, and build a clear picture before
proposing anything.

This is stage 1 of product ideation — **Demand Discovery**. It establishes what the job is.

## Credit

This skill adapts the Socratic conversation pattern from [Jesse Hattabaugh's superpowers brainstorming skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md), which pioneered the one-question-at-a-time exploration flow and the hard gate before design. The local adaptation deliberately replaces one-at-a-time with question blocks (`references/shared-understanding.md`) while keeping the Socratic intent and the hard gate.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.


Read existing users/problems, demand findings, relevant capabilities, and any selected idea. Enrich the same persona and problem records; keep feature suggestions proposed and link their unresolved questions.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and return record anchors to the coordinator. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Process

Three phases: Explore → Synthesize → Handoff. Keep it conversational and lightweight.

### 1. Explore — Socratic dialogue in blocks

Open with **one question block** covering the five core dimensions (format and rules:
`references/shared-understanding.md`). Don't rush to solutions.

The five dimensions:

- **The user** — who exactly? Defined by situation, not title. Where are they, under what pressure?
- **The struggle** — how do they solve this today? Which specific tool, and where does it break?
- **The moment** — what triggers the need? How often?
- **The outcome** — what does success unblock? How should they feel after?
- **The constraints** — platform, connectivity, integrations, latency, budget.

**Prefer multiple choice questions when possible** to keep momentum. Open-ended is fine when exploration needs depth.

Follow up serially only where an answer stayed thin — one focused block or question aimed at
the weakest dimension, not a fresh interview.

**The Struggle Audit:** If the user cannot describe a current clunky solution or workaround, stop and flag it rather than proceeding. The absence of a workaround is evidence about the problem (maybe it's not painful enough), not a gap to fill in with assumptions.

Push once when an answer stays generic, but don't interrogate. This is collaborative, not an interview.

### 2. Synthesize — the brief

Once you understand the idea, present the JTBD brief conversationally:

- **User & Context** — who they are, what situation triggers the need
- **Job to Be Done** — what they're trying to accomplish (functional / emotional / social dimensions). Mark each stated need's layer and inferred/confirmed status per `references/need-layers.md`.
- **Current Struggle** — how they solve it today and where it breaks
- **Success Outcome** — what changes when this works
- **Constraints** — technical, organizational, or environmental limits
- **Assumptions** — what we're assuming that needs validation
- **Open Questions** — what's still unclear

Keep sections short. A few sentences if straightforward, a paragraph if nuanced. Scale to complexity.

**No feature scoping here.** Keep feature ideas as proposed capability records linked to the problem and a decision question; an idea is not itself an unanswered question.

Ask the user if the brief looks right. Revise if needed.

### 3. Handoff

Before persisting, check against the 3 Beginner Sins:

1. **Feature creep** — are you listing features instead of describing a problem?
2. **Solving the void** — is there no current workaround? (that's a red flag)
3. **Broad personas** — "developers", "businesses", "users" aren't specific enough

Any failure returns to Phase 1 to sharpen the focus.

Once the brief passes, produce a short summary: what is confirmed, what still needs validation, and the next step.

Enrich the shared records in `discovery.html`: users/problems for the brief, risks/measures for constraints and outcomes, and questions/assumptions for what remains unresolved. Link existing records rather than repeating them in a separate brief. Return the relevant anchors to the coordinator.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections listed in the contract's section table (including `research` in `discovery.html` and `roadmap` in `product.html`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## What This Skill Does NOT Do

- **Does not generate ideas** — it clarifies an existing one
- **Does not validate demand** — it frames the problem, not the evidence
- **Does not scope features** — it stops before P0/P1 triage
- **Does not design the solution** — it answers "what is the job", not "what is the product"
- **Does not build prototypes** — it produces a brief, not code

This skill answers one question: **What is the job?** Everything else comes after.
