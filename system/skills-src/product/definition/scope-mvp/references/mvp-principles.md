# MVP Principles Reference

Last updated: 2026-08-02

## Table of Contents
1. The MVP Mental Model: "Buying Information"
2. The Core Assumption Template
3. The Three Soul Questions Filter (Decision Table)
4. The Not-To-Do List
5. The 4-Week Validation Sprint
6. Avoiding the Self-Deception Trap

---

## 1. The MVP Mental Model: "Buying Information"

Do not think of an MVP as a "cheap version" of the vision. Think of it as **buying the answer to a high-stakes question at the lowest possible price**.

- **Goal:** Maximize Return on Learning (RoL)
- **Formula:** `Information Gained ÷ Effort Expended`

The MVP exists to test a single risky assumption as fast and cheaply as possible. Every feature that doesn't directly test the assumption is waste.

---

## 2. The Core Assumption Template

Before scoping any features, the team must be able to complete this sentence:

> "I assume that **[Target User Group]** has a problem with **[Pain Point]**. They will use **[Our Solution]** to **[Key Action]** because it is **[Specific Advantage: faster / cheaper / simpler]** than their current way of doing things."

If this cannot be filled in clearly, the product is not ready for an MVP. Do not proceed to feature triage. Help the user clarify the assumption first.

---

## 3. The Three Soul Questions Filter

Run every feature or requirement through these three questions in order. Be ruthless.

| Question | If NO | If YES |
|----------|-------|--------|
| **1. Without this, is the product broken?** | It's a P0/P1. Kill it for now. | Move to Question 2. |
| **2. Does this directly verify the Core Assumption?** | It's a "nice-to-have." Kill it. | Move to Question 3. |
| **3. Does a user need this in the first 30 seconds?** | It's a retention feature. Defer to P1. | This is a P0. Keep it. |

**Gold Standard:** If the P0 list has more than 3–5 items, the Core Assumption is still too broad. Narrow the assumption until the P0 list is small enough to build in one week.

### Priority Definitions

| Priority | Definition | Action |
|----------|-----------|--------|
| **P0** | Must-have for the MVP to test the assumption | Build in Week 2 |
| **P1** | Valuable, but not needed to test the assumption | Revisit after Week 4 decision |
| **P2** | Nice-to-have, no direct link to assumption | Backlog or discard |

---

## 4. The Not-To-Do List

The Not-To-Do list is not a trash can. It is a **boundary that protects focus**. Every item on this list is a conscious, strategic decision to defer or permanently exclude.

### Two Categories

**Not Now (P1/P2):** Features worth building if the assumption proves true. Each item should have a named trigger condition, e.g.:
- "Multi-user collaboration → after 10 paying users confirm value"
- "Mobile app → after web conversion rate exceeds 20%"

**Not Ever (for this MVP):** Features that add polish, scaling, or complexity without testing the assumption.

### Common Not-To-Do Items for AI/Tech MVPs

- **Automation:** Don't build a complex agent pipeline if a "Wizard of Oz" approach (manually processing data behind the scenes) can validate whether users like the output.
- **UI Polish:** No dark mode, custom themes, complex onboarding flows, or animations.
- **Scaling Infrastructure:** No multi-tenancy, enterprise SSO, or horizontal scaling.
- **Secondary Personas:** Explicitly list who you are NOT building for. Example: "We are building for individual researchers, NOT enterprise procurement teams."
- **Metrics Dashboards:** No analytics dashboards for the user. Track what you need manually.

---

## 5. The 4-Week Validation Sprint

MVPs that stretch to 3 months stop being MVPs. Use this fixed rhythm:

| Week | Focus | Key Output |
|------|-------|-----------|
| **Week 1** | Scoping | Core Assumption written. P0 list finalized. Not-To-Do list written. |
| **Week 2** | Build | Minimum carrier shipped: landing page, Figma prototype, or single-function script. |
| **Week 3** | Test | 5–10 real target users. Observe, don't sell. Gather behavioral data, not opinions. |
| **Week 4** | Decide | Choose one of three outcomes (see below). |

### Week 4 Decision Framework

| Decision | Condition | Action |
|----------|-----------|--------|
| **Pivot** | Core Assumption was wrong, but a new one emerged from testing. | Rewrite the assumption and restart the sprint. |
| **Persevere** | Core Assumption held. Users demonstrated real behavior. | Promote P1 features to P0. Run another sprint. |
| **Stop** | No signal. No new assumption. | Kill the project. Valuable information was still purchased. |

---

## 6. Avoiding the Self-Deception Trap

Founders are optimists. The MVP is the reality check.

### Kill Vanity Metrics

Vanity metrics make you feel good but don't prove the assumption.

| Vanity Metric | Why It Lies | Real Metric to Use Instead |
|---------------|-------------|---------------------------|
| Sign-ups / registrations | Don't indicate actual use or value | Users who complete the "Key Action" |
| Page views | No intent signal | Return visits or session depth |
| "I'd use this if..." quotes | Polite rejection | Someone using a broken version to solve a real problem |
| Social media followers | Zero correlation to paying | Paying or actively using users |

### Watch for "False Viability"

- **False signal:** "I'd use this if it had X, Y, and Z." → They are being polite. The product does not solve their problem today.
- **Real signal:** Someone uses a buggy, ugly version repeatedly to solve their problem. → You have found a winner.

### The Founder's Bias Checklist

Before finalizing P0s, ask:
- [ ] Am I including this because it tests the assumption, or because I want to build it?
- [ ] Would a stranger with no emotional investment in this product call this P0?
- [ ] Can I validate user desire with a manual process instead of code?
- [ ] Is my success metric tied to the "Key Action" or to a vanity number?
