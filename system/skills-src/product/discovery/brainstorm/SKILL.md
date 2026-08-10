---
name: brainstorm
description: >
  Transforms an ambiguous idea into a Jobs-to-be-Done brief through Socratic dialogue.
  Explores who the user is, what job they hire the product for, how they solve it today,
  and what constrains any solution. Use when the user shares a vague idea, asks "what should
  I build", wants to explore a concept, or needs requirements discovery. Stops before feature
  scoping. Credit to Jesse Hattabaugh's superpowers brainstorming skill for the Socratic
  conversation pattern.
---

# Brainstorm

Last updated: 2026-08-10

Turn an ambiguous idea into a Jobs-to-be-Done brief through natural Socratic conversation.
Ask questions one at a time, understand the context, and build a clear picture before
proposing anything.

This is stage 1 of product ideation — **发现需求**. It establishes what the job is.
`validate-demand` then decides whether the evidence supports pursuing it.

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
constraints, assumptions, and open questions once. Update `state.md` with the artifact pointer
and `validate-demand` as the next transition.

The brief is disposable; the understanding in it is not. The job statement, the persona, and the
struggle become project truth when `write-prd` promotes them into the tracked product docs —
which happens as soon as `validate-demand` returns Green, not at the end of the pipeline. Write
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

**No feature scoping here.** P0/P1/Not-To-Do belongs to `scope-mvp`. Feature ideas raised during conversation go into Open Questions.

Ask the user if the brief looks right. Revise if needed.

### 3. Handoff

Before persisting, check against the 3 Beginner Sins:

1. **Feature creep** — are you listing features instead of describing a problem?
2. **Solving the void** — is there no current workaround? (that's a red flag)
3. **Broad personas** — "developers", "businesses", "users" aren't specific enough

Any failure returns to Phase 1 to sharpen the focus.

Once the brief passes, produce a short summary: what is confirmed, what still needs validation, and the next step.

Persist to `<work-root>/<effort>/discovery/brainstorm.md` and update `state.md` to point at `validate-demand` as the next transition.

## Pipeline Integration

- No candidate idea yet → `/generate-product-ideas` first
- External uncertainty → `/research`, then return here
- A question needing runnable evidence → `/prototype`, then return here
- Unsure where you are in the workflow → `/ideate-product` routes for you

Do not duplicate work another skill has already done when its output is present.

## Anti-Pattern: "This Is Too Simple To Need Discovery"

Every product idea goes through this, even "simple" ones. A todo list, a single utility, a config change — all of them. "Simple" ideas are where unexamined assumptions cause the most wasted work. The brief can be short (a few paragraphs for truly simple projects), but you MUST produce it.

## What This Skill Does NOT Do

- **Does not generate ideas** — use `generate-product-ideas` for that
- **Does not validate demand** — use `validate-demand` for go/no-go decisions
- **Does not scope features** — use `scope-mvp` for P0/P1 triage
- **Does not design the solution** — use `shape-solution` for that
- **Does not build prototypes** — use `prototype` when a design question needs throwaway code

This skill answers one question: **What is the job?** Everything else comes after.
