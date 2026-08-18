---
name: brainstorm
description: Turn an ambiguous idea into a Jobs-to-be-Done brief through Socratic dialogue. Use when the user shares a vague idea, asks "what should I build", wants to explore a concept, or needs requirements discovery.
---

# Brainstorm

Last updated: 2026-08-17

Turn an ambiguous idea into a Jobs-to-be-Done brief through natural Socratic conversation.
Ask questions one at a time, understand the context, and build a clear picture before
proposing anything.

This is stage 1 of product ideation — **Demand Discovery**. It establishes what the job is.

## Credit

This skill adapts the Socratic conversation pattern from [Jesse Hattabaugh's superpowers brainstorming skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md), which pioneered the one-question-at-a-time exploration flow and the hard gate before design.

## Shared Memory Contract

```text
Layer:    working — a draft of the problem, not yet project truth
Owns:     <work-root>/<effort>/discovery/brainstorm.md
Promotes: persona, job, struggle → PRD Part 1, via write-prd
```

Read `docs/agents/memory.md`, the active `state.md`, relevant core and human memory, and
`discovery/ideas.md` when present. Write the resolved job, struggle, moment, outcomes,
constraints, assumptions, and open questions once. Update `state.md` with the artifact pointer.

The brief is disposable; the understanding in it is not. The job statement, the persona, and the
struggle become project truth when promoted into the tracked product docs. Write
here as the drafting surface, and do not treat this file as the permanent home of the core idea.

If routing is absent, work in conversation only and recommend `manage-context` before persisting.

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
- **Job to Be Done** — what they're trying to accomplish (functional / emotional / social dimensions)
- **Current Struggle** — how they solve it today and where it breaks
- **Success Outcome** — what changes when this works
- **Constraints** — technical, organizational, or environmental limits
- **Assumptions** — what we're assuming that needs validation
- **Open Questions** — what's still unclear

Keep sections short. A few sentences if straightforward, a paragraph if nuanced. Scale to complexity.

**No feature scoping here.** Feature ideas raised during conversation go into Open Questions.

Ask the user if the brief looks right. Revise if needed.

### 3. Handoff

Before persisting, check against the 3 Beginner Sins:

1. **Feature creep** — are you listing features instead of describing a problem?
2. **Solving the void** — is there no current workaround? (that's a red flag)
3. **Broad personas** — "developers", "businesses", "users" aren't specific enough

Any failure returns to Phase 1 to sharpen the focus.

Once the brief passes, produce a short summary: what is confirmed, what still needs validation, and the next step.

Persist to `<work-root>/<effort>/discovery/brainstorm.md` and update `state.md` with the artifact pointer.

## What This Skill Does NOT Do

- **Does not generate ideas** — it clarifies an existing one
- **Does not validate demand** — it frames the problem, not the evidence
- **Does not scope features** — it stops before P0/P1 triage
- **Does not design the solution** — it answers "what is the job", not "what is the product"
- **Does not build prototypes** — it produces a brief, not code

This skill answers one question: **What is the job?** Everything else comes after.
