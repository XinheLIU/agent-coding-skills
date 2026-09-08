---
name: validate-demand
description: Grade the evidence behind a product claim and issue a go/no-go verdict. Use when the user asks to validate an idea, critique a concept, check product-market fit, validate an active-product improvement, or decide whether something is worth building.
disable-model-invocation: true
---

# Validate Demand

Last updated: 2026-09-08

Decide whether a product idea has real demand behind it, and say so plainly.

This is the gate at the end of stage 1 — **Demand Discovery**. It owns both halves of the judgment: how
strong the evidence is, and what verdict that evidence supports. Grading precedes scoring,
because a confident zone built on an assumption is the failure mode this skill exists to catch.

Be direct. A clear Red that redirects a month of work is worth more than a hedged Yellow.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.

```text
Layer:       working
Contributes: demand assessments, claim evidence, persona refinements, gaps, assumptions, questions
Writes:      <work-root>/<effort>/discovery.html — shared records, not an exclusive section
Promotes:    scoped demand verdict, evidence grade, persona and job → product.html, via write-prd
```

Read the target problem and actor, existing demand assessments, relevant current behavior, and evidence. Add support or contradictions to existing records; distinguish a code observation from evidence of user demand.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and update `state.md` with record anchors. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

### First promotion point

On Green, route to `write-prd` to preserve the validated claim, persona, job, and supporting evidence before continuing. On Yellow or Red, retain the assessment and the evidence needed to revisit it in working memory. If a new assessment challenges already accepted intent, record a linked review finding for that intent in discovery and state; do not erase or demote it.

## Invocation

```
/validate-demand [idea or path] [--stage pre-product|active-users|paying|internal]
```

Input resolution: positional argument or path → the claim; else shared problem and persona records; else a supplied candidate idea; else ask what should be validated. Infer `--stage` from context when unset.

## Behavioral Flow

Six steps in order. Do not jump to the verdict before the evidence is graded — the ordering is
the method.

### 1. Grade the evidence

Run the six-area diagnostic (demand reality, status quo, specific user, narrowest wedge,
observation, future fit), prioritized by product stage. Ask one question at a time. Push once
when an answer stays generic.

For active products, prefer evidence that reflects real use: support tickets, analytics,
usage funnels, churn or lost-deal notes, stakeholder reports, customer-success notes, observed
sessions, sales/support transcripts, and production behavior recorded in current capability records.
Treat internal stakeholder urgency as evidence of business priority, not proof of user pain,
unless it is tied to observed user behavior or operational cost.

Grade every claim at the strongest level it actually supports: Observed → Committed → Reported
→ Stated interest → Inferred.

**Never promote a weaker level to a stronger one.** Enthusiasm, compliments, surveys, and
signups are level 4 regardless of volume. Behavior, payment, and dependency are what count.

Scale and diagnostic detail: `references/framework.md`.

### 2. Score the Three Soul Questions

Assign 🟢 / 🟡 / 🔴 to each, citing the evidence level supporting it:

- **Q1 Who is the user?** — specific enough to phone and pitch in 10 seconds?
- **Q2 Where is the pain?** — torture or want? Run the 5-Whys until the chain terminates at a noun (a fear, a loss, an identity), not a verb — this is the descent from surface to fundamental need (`references/need-layers.md`); record which layer the terminus reached.
- **Q3 Why choose you?** — a named competitor gap, or the 3× Rule met with real numbers. Red by default; silence here is a finding.

A zone cannot be Green on level 4 or 5 evidence. Cap it at Yellow and say why.

### 3. Classify the demand

Painkiller / Reward / Vitamin, via: *what happens if the user goes without this for 6 months?*
Then compute the Pain Score (Frequency × Severity, max 25).

This skill produces the scoped classification. Other skills cite it and can attach contrary evidence or request reassessment; they never silently reassign it.

### 4. Slice

**Horizontal** — score 3–5 sub-segments and name the highest-Pain-Score beachhead.
**Vertical** — map the day-in-the-life arc from trigger to emotional resolution.

Slicing is often what turns a Yellow into a Green: the same idea aimed at a narrower segment
carries far stronger evidence.

### 5. Issue the verdict

The verdict is the **lowest zone across the three questions**. One Red makes it Red.

The verdict is per-claim: it grades this specific claim, actor, and scenario. It does not
validate the whole-product vision or mission — several Green wedges do not add up to a
validated product. Record the unvalidated mission as a linked open question or assumption,
never as a byproduct of a Green.

| Verdict | Meaning | Route |
| --- | --- | --- |
| 🟢 Green | All three Green, none resting on assumption | Promote the core idea, then design the solution |
| 🟡 Yellow | At least one Yellow, no Red | Stay. All three next steps address the weakest question. |
| 🔴 Red | At least one Red | Stop. Do not recommend downstream work. |

On Yellow or Red, recommend no downstream skill. The next step is evidence, not design.

Promotion is not downstream work — it records what this gate already established, and it is
offered only on Green. On Yellow the idea has not earned a place in the tracked layer yet; the
evidence gap is the work. Do not use the PRD as a way around the gate.

### 6. Enrich shared memory

Create or update the demand assessment for this specific claim, actor, and scenario. Include the verdict and reason, Three Soul Question zones with supporting evidence levels, demand type, Pain Score, beachhead, and day-in-the-life assessment. Link shared personas/problems instead of copying them. Record the layered chain on the problem record — surface ask, deep motivation, fundamental terminus — preserving its identity.

Attach claim-level evidence to existing subjects. Enrich existing gaps with evidence of importance; put unsupported assumptions and the cheapest tests in shared assumption/question records. Answer an existing question when the assessment establishes its answer, with its basis. A gap remains open until its own resolution condition is met.

Record three concrete next validation actions linked to the weakest claims. Each must be executable this week and raise a specific claim's evidence level; "do more research" is not an action. Write HTML records in `discovery.html`, not a separate demand report.

When the effort holds multiple validated claims for the same product, or the user states a
larger mission, synthesize or enrich a candidate `vision` record in `overview` using the
Vision Synthesis method in `references/need-layers.md` (greenfield rules apply when no
implemented stories exist). Mark it inferred, link the claims that imply it, and pair it
with an open question for user confirmation. The vision stays an inference; only the user
confirms it, and it validates no demand.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections (`overview`, `users-problems`, `capabilities-journeys`, `gaps-opportunities`, `questions-assumptions`, `evidence`, `scope-decisions`, `risks-measures`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## What This Skill Does NOT Do

- **Does not frame the problem** — it grades a claim, it does not discover one
- **Does not confirm a vision** — it may synthesize a candidate as inference; only the user confirms it
- **Does not design the solution** — it says whether to proceed, not what to build
- **Does not scope the MVP** — it issues a verdict, not a feature list
- **Does not scope active-product increments** — `scope-product-increment` owns the behavior delta
- **Does not write the PRD** — it promotes the core idea, not the full spec

Adapted from gstack `office-hours` and `plan-ceo-review`; see `system/THIRD_PARTY_NOTICES.md`.
