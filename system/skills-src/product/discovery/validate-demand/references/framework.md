# Demand Validation Framework

Last updated: 2026-08-06

Two instruments, used in sequence. The **evidence scale** grades how strongly each claim is
supported. The **Three Soul Questions** convert those graded claims into zones and a verdict.

Grading first is what keeps the verdict honest: a Green zone built on Inferred evidence is a
guess wearing a color.

## Table of Contents

- [The Evidence Scale](#the-evidence-scale)
- [The Diagnostic](#the-diagnostic)
- [Q1: Who Is the User?](#q1-who-is-the-user)
- [Q2: Where Is the Pain?](#q2-where-is-the-pain)
- [Q3: Why Choose You?](#q3-why-choose-you)
- [Demand Classification](#demand-classification)
- [Slicing Techniques](#slicing-techniques)
- [Traffic Light Rubric](#traffic-light-rubric)

---

## The Evidence Scale

Grade every claim at the strongest level it actually supports.

| Level | Name | What it means |
| --- | --- | --- |
| 1 | **Observed** | Direct observation of the workflow or product use |
| 2 | **Committed** | Money, time, data, access, migration, or reputation put at risk |
| 3 | **Reported** | A specific account of current behavior or cost |
| 4 | **Stated interest** | Compliments, surveys, signups, hypothetical intent |
| 5 | **Inferred** | The team's assumption, with no user evidence yet |

**Never silently promote a weaker level to a stronger one.** This is the single rule that
matters most here. "Five people said they'd use it" is level 4 and stays level 4 no matter how
enthusiastic they were. Interest is not demand. Behavior, commitment, cost, and dependency are.

Level 4 and 5 claims cannot produce a Green zone. They can produce Yellow at best, and the
next validation action must be the experiment that moves them up the scale.

---

## The Diagnostic

Six forcing questions. Ask only what the upstream brief has not already answered; one at a
time, pushing once when an answer stays generic.

| Area | Forcing question | Strong evidence looks like |
| --- | --- | --- |
| Demand reality | Who would be materially disrupted if this disappeared tomorrow? | Payment, repeated use, escalation, workflow dependency |
| Status quo | What do users do now, and what does it cost? | Named steps, tools, time, money, risk, headcount |
| Specific user | Who experiences the highest-cost version of this problem? | A reachable person, role, context, and consequence |
| Narrowest wedge | What is the smallest result they would pay for or adopt this week? | One outcome or deliverable, in days |
| Observation | What did users do that contradicted the team's assumptions? | Unguided observation — not a demo, not a survey |
| Future fit | What change makes this more essential in three years? | A specific causal thesis, not market-growth boilerplate |

### Adapt to product stage

| Stage | Prioritize |
| --- | --- |
| Pre-product | Demand reality, status quo, specific user |
| Active users | Status quo, wedge, observation |
| Paying customers | Wedge, observation, future fit |
| Internal product | Replace payment with sponsor commitment, workflow adoption, and resilience to reorganization |

The internal-product substitution matters. An internal tool has no price signal, so commitment
shows up as a sponsor spending political capital and a team restructuring work around the tool.

---

## Q1: Who Is the User?

### The specificity test

A persona is specific enough when you could call that person right now, pitch in 10 seconds,
and they would immediately recognize the problem. A demographic category ("young
professionals", "AI users") fails. A role plus a situation plus a fear passes.

### Zone criteria

| Zone | Criteria | Example |
| --- | --- | --- |
| 🟢 Green | Named role, industry, tech comfort, and a specific situational constraint | "A 45-year-old operations manager at a small trading firm, afraid of missing price shifts, comfortable with messaging apps but not spreadsheets" |
| 🟡 Yellow | A role or domain, but no situational texture or emotional context | "Supply chain managers in manufacturing" |
| 🔴 Red | A demographic label, a behavior type, or "everyone" | "Young professionals", "people who want to be productive" |

### Sharpening questions

- "Can you give this person a specific fear — not a goal?"
- "What does their Tuesday afternoon look like, before your product exists?"
- "If you called them right now to pitch this, what would you say in the first 10 seconds?"

---

## Q2: Where Is the Pain?

### Want vs. Torture

| Type | Definition | Example | Commercial signal |
| --- | --- | --- | --- |
| **Torture** (real pain) | Daily friction with emotional or financial consequences | "I missed my kid's dinner copy-pasting Excel until 8pm. I'm angry at myself." | High willingness to pay |
| **Want** (fake pain) | A vague aspiration with no emotional stakes | "I want to be more efficient" | Low — they will use a free tool |

### The 5-Whys probe

Ask "why?" from the stated pain until the chain reaches an emotion or a dollar amount.

1. "I want to summarize news faster." → Why?
2. "Too many articles to read." → Why does that matter?
3. "I fall behind on industry trends." → Why does that hurt?
4. "I look uninformed in leadership meetings." → Why does that matter?
5. **"I'm afraid my boss thinks I'm not across the market. I'm afraid of losing my job."**

The real pain is #5. Features resolve #5, not #1.

**Diagnostic:** if the chain terminates at a verb (saves time, reduces clicks, automates X), it
has not bottomed out. Keep going until it terminates at a noun — a fear, a loss, an identity.

### Zone criteria

| Zone | Criteria |
| --- | --- |
| 🟢 Green | Specific trigger event AND an emotional or financial consequence |
| 🟡 Yellow | A real inconvenience, but vague consequences ("wastes time", "inefficient") |
| 🔴 Red | A stated preference or aspiration, not a friction ("would be nice to") |

---

## Q3: Why Choose You?

### The two tests

**For products:** name the one thing competitors do poorly. More focused? Simpler? Specific to
a vertical?

**For tools, scripts, and automations:** apply the 3× Rule.

```
Saved Time > Development Time × 3
```

5 hours to build, saves 10 min/month → breaks even in 18 months → Red.
2 hours to build, saves 90 min/week → breaks even in week 2 → Green.

### Zone criteria

| Zone | Criteria |
| --- | --- |
| 🟢 Green | Explicit competitor gap named; OR the 3× Rule met with specific numbers |
| 🟡 Yellow | Vague differentiation ("more user-friendly", "we use the latest AI") |
| 🔴 Red | No differentiation stated; or a free tool already does 80% of the job |

**Q3 is Red by default.** Silence on this question is a finding, not permission to skip it.

### Common red flags

- "There's nothing else like this" — almost never true; it means competitors were not researched.
- "We use GPT-4 / Claude" — infrastructure, not differentiation.
- "It's faster" — only valid at 10×+ AND when that speed resolves the Q2 fear.

---

## Demand Classification

Owned here. Downstream skills reference this classification; they never reassign it.

| Type | Metaphor | Definition | WTP signal | Example |
| --- | --- | --- | --- | --- |
| **Painkiller** | Emergency medicine | Solves a survival, security, or financial risk | High; budget already exists | Compliance tool preventing a regulatory fine |
| **Reward** | Dessert | Delight, significant time saved, status | Medium; discretionary budget | Report generator producing polished client decks in one click |
| **Vitamin** | Daily supplement | Marginal improvement; life continues without it | Low to none | A daily habit tracker |

### Classification rule

Ask: *what happens if the user does not have this for the next 6 months?*

- **Painkiller** — they lose money, lose a job, miss a deadline, damage a relationship.
- **Reward** — work is slower or uglier, but nothing catastrophic.
- **Vitamin** — they barely notice.

### Commercial implication

- **Painkiller** — B2B sales cycles work; users pay without a free tier.
- **Reward** — freemium works; convert when ROI becomes visible.
- **Vitamin** — very hard to monetize; expect churn once novelty fades.

### Pain Score

| Dimension | Score 1–5 |
| --- | --- |
| **Frequency** | 1 = yearly, 5 = daily |
| **Severity** | 1 = minor inconvenience, 5 = business-threatening |

**Pain Score = Frequency × Severity** (max 25)

- 16–25 — build immediately; this is the core market.
- 9–15 — proceed with caution; validate willingness to pay first.
- 1–8 — vitamin territory; do not build a business around this.

---

## Slicing Techniques

### Horizontal — who to target first

1. List 3–5 sub-segments of the stated audience.
2. Score each on Frequency × Severity.
3. Recommend the highest scorer as the beachhead.

Stated target: "fitness app for everyone"

| Segment | Frequency | Severity | Score |
| --- | --- | --- | --- |
| Post-partum moms | 5 | 5 | 25 |
| Diabetic patients | 5 | 4 | 20 |
| Busy office workers | 3 | 2 | 6 |

→ Build for post-partum moms first. Highest pain, highest willingness to pay.

### Vertical — day in the life

```
[T-60 Trigger] → [T-30 Friction builds] → [T-0 Moment of need]
→ [T+5 First interaction] → [T+30 Outcome / emotional resolution]
```

- **Trigger** — what specific event created awareness of the need? Not "they want to save time" — what *happened*?
- **Friction builds** — what do they try first, and where does it fail?
- **Moment of need** — the emotional state right before reaching for a solution. Frustration? Panic? Shame?
- **First interaction** — what do they actually do? What is the first click?
- **Outcome** — which emotion resolves the pain? Relief, confidence, competence?

---

## Traffic Light Rubric

### Verdict rules

The verdict is the **lowest zone across the three questions**. One Red makes the verdict Red
regardless of the other two.

| Verdict | Condition | Prescribed action |
| --- | --- | --- |
| 🟢 Green | All three Green | Promote the core idea with `write-prd`, then proceed to `shape-solution`. |
| 🟡 Yellow | At least one Yellow, none Red | Return to the Yellow question. Run 5 customer interviews first. |
| 🔴 Red | At least one Red | Stop. Do not invest further until the Red is resolved. |

### Green criteria — all must hold

- A specific person: job title, situational context, named fear.
- Pain Score ≥ 16, terminating at an emotion or financial loss.
- Concrete differentiation OR a 3× ROI calculation with real numbers.
- No Green zone rests on level 4 or 5 evidence.

### Common failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| **Product OCD** | Solving a personal annoyance assumed to be universal | Observe 5 people who aren't you hitting this pain |
| **Feature envy** | "Competitor X does this, so we should" | Ask whether users are actually switching *because of* that feature |
| **Efficiency theater** | Optimizing something that isn't broken | Run the Pain Score; below 9, stop |
| **Demo-driven development** | Building what looks impressive over what resolves pain | Ask: would someone pay for this at 3 AM when stressed? |
| **Evidence inflation** | Survey enthusiasm reported as demand | Re-grade on the evidence scale; level 4 stays level 4 |
