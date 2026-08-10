---
name: validate-demand
description: >
  Stage 1 demand gate. Grades the evidence behind a product claim on a five-level scale, scores
  the Three Soul Questions (who is the user, where is the pain, why choose you), classifies the
  demand as painkiller / reward / vitamin, slices to a beachhead segment, and issues a
  traffic-light verdict with three concrete next steps. Use when the user asks to validate an
  idea or demand, asks whether anyone actually wants this, asks for a critique or reality check
  or stress test of a product idea, asks "is this a real problem", asks for a go/no-go on a
  concept, asks to check product-market fit or willingness to pay, or has a JTBD brief needing a
  verdict before design work. Triggers include "validate", "critique this idea", "is this worth
  building", "will anyone pay for this", "reality check", "poke holes in this", "demand
  validation", or "should I build this".
---

# Validate Demand

Last updated: 2026-08-10

Decide whether a product idea has real demand behind it, and say so plainly.

This is the gate at the end of stage 1 — **发现需求**. It owns both halves of the judgment: how
strong the evidence is, and what verdict that evidence supports. Grading precedes scoring,
because a confident zone built on an assumption is the failure mode this skill exists to catch.

Be direct. A clear Red that redirects a month of work is worth more than a hedged Yellow.

## Shared Memory Contract

```text
Layer:    working — the evidence trail behind the verdict
Owns:     <work-root>/<effort>/discovery/demand.md
Promotes: demand type, evidence grade, verdict → PRD Part 1, via write-prd
```

Read `docs/agents/memory.md`, the active `state.md`, and `discovery/brainstorm.md` when present.
Write the graded evidence, zones, demand type, slicing, verdict, unsupported assumptions, and
next validation action once. Update `state.md` with the artifact pointer and the next transition
implied by the verdict.

Reference the upstream brief rather than restating it. Do not edit `brainstorm.md`; when the brief is
wrong, name the conflict and recommend re-running `brainstorm`.

### This gate is the first promotion point

A Green verdict is the moment the core idea stops being speculation. Recommend `/write-prd` now,
before `shape-solution`, so the persona, job, and demand verdict land in the tracked product
docs while they are fresh. It runs in early mode: Part 1 filled, later parts marked pending.

The reason is durability, not ceremony. Up to this point everything lives under a git-ignored
work root — deleting it costs nothing. After this point the project has a validated reason to
exist, and that reason should not be one directory removal away from gone.

On Yellow or Red, promote nothing. Record the verdict and what would have to be true to revisit
it, and leave it in working memory. A killed or parked idea's value is the record of why, which
the next `ideate-product` run reads from here.

If routing is absent, work in conversation only and recommend `manage-context` before persisting.

## Invocation

```
/validate-demand [idea or path] [--stage pre-product|active-users|paying|internal]
```

Input resolution: positional argument or path → the claim; else `discovery/brainstorm.md`; else
`discovery/ideas.md`; else ask what should be validated. Infer `--stage` from context when unset.

## Behavioral Flow

Six steps in order. Do not jump to the verdict before the evidence is graded — the ordering is
the method.

### 1. Grade the evidence

Run the six-area diagnostic (demand reality, status quo, specific user, narrowest wedge,
observation, future fit), prioritized by product stage. Ask one question at a time. Push once
when an answer stays generic.

Grade every claim at the strongest level it actually supports: Observed → Committed → Reported
→ Stated interest → Inferred.

**Never promote a weaker level to a stronger one.** Enthusiasm, compliments, surveys, and
signups are level 4 regardless of volume. Behavior, payment, and dependency are what count.

Scale and diagnostic detail: `references/framework.md`.

### 2. Score the Three Soul Questions

Assign 🟢 / 🟡 / 🔴 to each, citing the evidence level supporting it:

- **Q1 Who is the user?** — specific enough to phone and pitch in 10 seconds?
- **Q2 Where is the pain?** — torture or want? Run the 5-Whys until the chain terminates at a noun (a fear, a loss, an identity), not a verb.
- **Q3 Why choose you?** — a named competitor gap, or the 3× Rule met with real numbers. Red by default; silence here is a finding.

A zone cannot be Green on level 4 or 5 evidence. Cap it at Yellow and say why.

### 3. Classify the demand

Painkiller / Reward / Vitamin, via: *what happens if the user goes without this for 6 months?*
Then compute the Pain Score (Frequency × Severity, max 25).

This skill owns the classification. Downstream skills cite it and never reassign it.

### 4. Slice

**Horizontal** — score 3–5 sub-segments and name the highest-Pain-Score beachhead.
**Vertical** — map the day-in-the-life arc from trigger to emotional resolution.

Slicing is often what turns a Yellow into a Green: the same idea aimed at a narrower segment
carries far stronger evidence.

### 5. Issue the verdict

The verdict is the **lowest zone across the three questions**. One Red makes it Red.

| Verdict | Meaning | Route |
| --- | --- | --- |
| 🟢 Green | All three Green, none resting on assumption | `write-prd` to promote the core idea, then `shape-solution` |
| 🟡 Yellow | At least one Yellow, no Red | Stay. All three next steps address the weakest question. |
| 🔴 Red | At least one Red | Stop. Do not recommend downstream work. |

On Yellow or Red, recommend no downstream skill. The next step is evidence, not design.

Promotion is not downstream work — it records what this gate already established, and it is
offered only on Green. On Yellow the idea has not earned a place in the tracked layer yet; the
evidence gap is the work. Do not use the PRD as a way around the gate.

### 6. Write the artifact

Persist to `<work-root>/<effort>/discovery/demand.md`:

```markdown
# Demand Validation: [Name]

Last updated: [YYYY-MM-DD]

## Verdict
[🟢 / 🟡 / 🔴] — [one sentence]

## Evidence Summary
| Claim | Level | Basis |
| --- | --- | --- |

## Three Soul Questions
| Question | Zone | Finding | Evidence level |
| --- | --- | --- | --- |

## Demand Type
[Painkiller / Reward / Vitamin] · Pain Score [F × S = N] · [commercial implication]

## Slicing
**Beachhead**: [segment, and why]
**Day in the life**: [trigger → friction → moment → first interaction → outcome]

## Unsupported Assumptions
| Assumption | Current level | Cheapest test to raise it |
| --- | --- | --- |

## Next Validation Action
1. [Concrete, this week, names who to talk to or what to observe]
2. …
3. …
```

Every next step must be executable this week and must raise a specific claim's evidence level.
"Do more research" is not a next step.

## Pipeline Integration

- No JTBD brief yet → `/brainstorm` first; this skill grades a claim, it does not discover one
- Green verdict → `/shape-solution`
- A gap needing external evidence → `/research`
- A gap needing runnable evidence → `/prototype`, then return here
- Unsure where you are → `/ideate-product`

Adapted from gstack `office-hours` and `plan-ceo-review`; see `system/THIRD_PARTY_NOTICES.md`.
