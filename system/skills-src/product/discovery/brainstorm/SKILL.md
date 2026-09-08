---
name: brainstorm
description: Turn an ambiguous idea into a Jobs-to-be-Done brief through Socratic dialogue. Use when the user shares a vague idea, asks "what should I build", wants to explore a concept, or needs requirements discovery.
disable-model-invocation: true
---

# Brainstorm

Last updated: 2026-09-08

Turn an ambiguous idea into a Jobs-to-be-Done brief through natural Socratic conversation.
Ask questions one at a time, understand the context, and build a clear picture before
proposing anything.

This is stage 1 of product ideation — **Demand Discovery**. It establishes what the job is.

## Credit

This skill adapts the Socratic conversation pattern from [Jesse Hattabaugh's superpowers brainstorming skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md), which pioneered the one-question-at-a-time exploration flow and the hard gate before design.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.

```text
Layer:       working
Contributes: personas, problems, outcomes, constraints, assumptions, questions
Writes:      <work-root>/<effort>/discovery.html — shared records, not an exclusive section
Promotes:    persona, job, struggle → product.html, via write-prd
```

Read existing users/problems, demand findings, relevant capabilities, and any selected idea. Enrich the same persona and problem records; keep feature suggestions proposed and link their unresolved questions.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and update `state.md` with record anchors. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Process

Three phases: Explore → Synthesize → Handoff. Keep it conversational and lightweight.

### 1. Explore — Socratic dialogue

Ask questions **one at a time** to understand the idea. Don't rush to solutions.

Core questions to cover (not necessarily in this order):

- **The user** — who exactly? Defined by situation, not title. Where are they, under what pressure?
- **The struggle** — how do they solve this today? Which specific tool, and where does it break?
- **The moment** — what triggers the need? How often?
- **The outcome** — what does success unblock? How should they feel after?
- **The constraints** — platform, connectivity, integrations, latency, budget.

**Prefer multiple choice questions when possible** to keep momentum. Open-ended is fine when exploration needs depth.

**Only one question per message.** If a topic needs more exploration, break it into multiple questions.

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

Enrich the shared records in `discovery.html`: users/problems for the brief, risks/measures for constraints and outcomes, and questions/assumptions for what remains unresolved. Link existing records rather than repeating them in a separate brief. Update `state.md` with the relevant anchors.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections (`overview`, `users-problems`, `capabilities-journeys`, `gaps-opportunities`, `questions-assumptions`, `evidence`, `scope-decisions`, `risks-measures`).
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
