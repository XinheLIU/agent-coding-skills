---
name: brainstorm-feature
description: Turn a vague idea into a validated feature brief before any implementation. Use when the user's request is ambiguous, high-impact, or opens a new feature/system area. Runs one-question-at-a-time clarification, produces an Understanding Lock, explores 2–3 approaches with trade-offs, and hands off a concise brief to /spec. Hard gate — no code or specs get written until the user approves the design.
---

# /brainstorm-feature — Turn an idea into a validated brief

Turn a raw, vague, or ambitious idea into a **clear, validated feature brief** through structured dialogue. This is step 0 of the workflow: `/brainstorm-feature` → `/spec` → `/plan` → `/tasks`.

## When to use

Invoke this skill when the user:

- Describes a feature in one vague sentence ("add some kind of reporting thing").
- Opens a new product area, new system, or new architectural direction.
- Asks "what do you think about X?", "how would we approach Y?", or similar exploratory phrasing.
- Explicitly runs `/brainstorm-feature`.

Skip this skill (go straight to `/spec`) only when the user's description is already concrete: multiple paragraphs, named user flows, specific constraints, or a referenced prior design doc.

## Hard gate

While this skill is active:

- **Do NOT write source code.**
- **Do NOT invoke `/spec`, `/plan`, `/tasks`, or any implementation skill.**
- **Do NOT scaffold files, install deps, or modify the working tree** (except writing the design doc at the end, if the user approves).
- You are operating as a **design facilitator**, not a builder.

The only way out of this skill is an approved Understanding Lock + approved design + (optional) written design doc, at which point you hand off to `/spec`.

## Inputs

- The user's initial message (the idea).
- The repo state (files, docs, recent commits) — check it before asking anything.

## Outputs

- A short, validated **Feature Brief** (in-conversation) that `/spec` can take as input.
- Optionally a design doc at `docs/designs/YYYY-MM-DD-<topic>.md` in the current working directory, committed only if the user asks.

---

## Process

### 1. Explore context (no questions yet)

Before asking anything:

- `git log --oneline -n 20` and `git status` to see what's already going on.
- Glob/Read top-level docs: `README*`, `CLAUDE.md`, `AGENTS.md`, `docs/`, `specs/`.
- Identify what already exists vs. what is proposed, and surface any implicit-but-unconfirmed constraints (existing stack, patterns, owners).

Do NOT propose a design yet. Do NOT ask the user questions yet. Just orient.

### 2. Scope check

If the idea spans multiple independent subsystems ("a platform with chat + billing + analytics + file storage"), flag it now:

- Say so explicitly to the user.
- Help them decompose into sub-features.
- Pick one sub-feature to brainstorm-feature first. The others get their own `/brainstorm-feature` passes later.

Don't try to brainstorm-feature a whole platform in one go.

### 3. Clarify — one question at a time

Ask the user one question per message (use `AskUserQuestion`). Prefer multi-choice options with a `(Recommended)` tag on your strongest default. Use open-ended only when options genuinely can't be enumerated.

Cover, in roughly this order — **only the axes that are unclear** from the initial pitch:

1. **Purpose** — what problem does this solve, for whom, and why now?
2. **Target users** — who uses it, and what's their current workaround?
3. **Success criteria** — how will we know this worked? (concrete signal, not "it's good")
4. **Explicit non-goals** — what are we deliberately NOT doing? (forces sharper scope)
5. **Constraints** — existing stack, integrations, regulatory, timeline.
6. **Non-functional expectations** (mandatory to cover at least briefly):
   - Performance / latency / throughput
   - Scale (users, data volume, traffic)
   - Security / privacy / compliance
   - Reliability / availability
   - Maintenance & ownership
   For each NFR axis, if the user is unsure, **propose a reasonable default** and mark it as an assumption.

Stop asking questions as soon as you have enough to write an Understanding Summary. Fewer questions is better; most features need 3–6, not 15.

### 4. Understanding Lock (hard gate)

Before proposing ANY design, pause and present:

**Understanding Summary** — 5–7 bullets covering:
- What we're building
- Why it exists
- Who it's for
- Key constraints
- Explicit non-goals

**Assumptions** — everything you inferred or proposed as a default. Flag each with `(assumption)`.

**Open Questions** — anything unresolved.

Then ask, in plain text (not `AskUserQuestion`, because we want a conversational confirmation, not a forced choice):

> "Does this accurately reflect your intent? Confirm or correct before we move to design."

**Do not proceed until the user explicitly confirms.** Small corrections are normal — update the summary and re-confirm.

### 5. Explore approaches

Propose **2–3 viable approaches**. For each:

- One-line description.
- Trade-offs: complexity, extensibility, risk, maintenance cost.
- Why it fits (or doesn't) the Understanding Summary.

Lead with your recommendation. YAGNI ruthlessly — reject approaches that add scope the user didn't ask for.

Let the user pick or push back. If they want a hybrid, fine — but give the hybrid a name and make it explicit.

### 6. Present the design, in sections

Once an approach is chosen, present the design in small sections (≤300 words each). After each section, ask:

> "Does this look right?"

Cover only the sections that apply:

- Architecture (components and how they relate)
- Data flow / control flow
- Data model (logical, no implementation types)
- External interfaces (APIs, CLIs, events)
- Error handling & edge cases
- Testing strategy (what proves this works)
- Rollout / migration (only if changing existing behavior)

Design for **isolation and clarity**: each component should have one clear purpose, a documented interface, and be understandable without reading its internals.

If the user asks to change something, go back to the relevant step. This is normal.

### 7. Decision Log

Maintain a running decision log in the conversation as you go. For each real decision:

- **What** was decided.
- **Alternatives** considered.
- **Why** this option won.

Include the log in the final design doc.

### 8. Write the design doc

Only after the user has approved the design sections, write to:

```
docs/designs/YYYY-MM-DD-<kebab-topic>.md
```

(Today's date; `<kebab-topic>` derived from the feature.)

If `docs/designs/` doesn't exist, create it. Use this skeleton:

```markdown
# Design: <Feature Title>

**Date**: YYYY-MM-DD
**Status**: Approved — ready for /spec

## Understanding Summary

- <bullet>
- <bullet>

## Assumptions

- <bullet (assumption)>

## Non-Goals

- <bullet>

## Chosen Approach

<one paragraph + why it beat the alternatives>

## Design

### Architecture
<...>

### Data model
<...>

### Interfaces
<...>

### Error handling & edge cases
<...>

### Testing strategy
<...>

## Decision Log

| Decision | Alternatives | Why |
|---|---|---|
| <what> | <alts> | <why> |

## Next step

Hand off to `/spec` with the Feature Brief below.

## Feature Brief (for /spec)

<2–4 sentences capturing: what it is, who it's for, what P1 user story it delivers, the headline constraint. This is what you paste into /spec.>
```

Do NOT `git commit` unless the user explicitly asks.

### 9. Spec self-review

Look at the written doc with fresh eyes and fix inline:

- Any `TBD` / `TODO` / placeholders left? Fill or remove.
- Do any sections contradict each other?
- Is the scope still tight enough for one feature (not a platform)?
- Could any requirement be read two ways? Pick one and make it explicit.

No need for a second review pass — fix and move on.

### 10. User review gate

Tell the user:

> "Design doc written to `<path>`. Review it and let me know if you want to adjust before we run `/spec`."

Wait. If they want changes, make them, re-run step 9, and re-ask.

### 11. Hand off to /spec

Once the user approves:

- Output the **Feature Brief** section of the doc, clearly delimited.
- Say: "Ready for `/spec`. Pass the Feature Brief above as the feature description."
- Do NOT invoke `/spec` yourself (let the user or the calling subagent do it — this keeps the handoff explicit).

---

## Exit criteria (hard stop)

You may exit this skill only when **all** of these hold:

- Understanding Lock was confirmed by the user.
- One design approach is explicitly accepted.
- Major assumptions are documented.
- Key risks are listed (either in the doc or the decision log).
- Decision Log is non-empty (even if short).
- Design doc is written and user-approved OR the user explicitly waived the doc.

If any criterion is unmet, stay in the skill and keep refining.

---

## Key principles

- **One question per message.**
- **Multi-choice > open-ended** when the option space is enumerable.
- **Assumptions must be explicit** and tagged.
- **YAGNI ruthlessly.** Cut anything the user didn't ask for and doesn't need for the P1 use case.
- **Lead with the recommendation**, then give alternatives.
- **Validate incrementally** — approval after each section, not one mega-approval at the end.
- **Be willing to go back.** If a later section reveals an earlier assumption was wrong, loop back.
- **Never implement during brainstorming.** The hard gate is non-negotiable.
