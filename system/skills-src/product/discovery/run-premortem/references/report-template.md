# Pre-Mortem Report Template

Last updated: 2026-08-02

Use this exact structure. Fill every section; do not skip sections or leave placeholders.

---

```markdown
# [Project Name] — Pre-Mortem Analysis Report

Last updated: [YYYY-MM-DD]

> **Analysis Date:** [Today's date]
> **Failure Date:** [6 months from today]
> **Analyst:** Pre-Mortem Analysis Skill

---

## 1. The Failure Vision

It is [failure date]. The project has officially failed.

- **DAU:** ~0. No meaningful user activity in months.
- **Commit history:** Last commit was [~3 months ago]. The repo looks abandoned.
- **User verdict:** *"[Verbatim user complaint 1]"* and *"[Verbatim user complaint 2]."*
- **Builder state:** [1–2 sentences describing the builder's emotional state — demotivated, avoidant, embarrassed.]
- **The regression:** The builder is back to using [old tool]. [Number] months of effort produced no lasting change in behavior.

---

## 2. The Death List — All Causes of Failure

| # | Cause of Death | Dimension | Prob (1–5) | Sev (1–5) | Score | Priority |
|---|---|---|---|---|---|---|
| 1 | [Specific failure description] | Demand | X | X | XX | ⚠️ Critical / ⚡ High / 🟡 Medium |
| 2 | ... | Tech | | | | |
| 3 | ... | UX | | | | |
| 4 | ... | Habit | | | | |
| 5 | ... | Scenario | | | | |
| 6 | ... | Market | | | | |
| 7 | ... | Personal | | | | |
| 8 | ... | Distribution | | | | |
| 9 | ... | | | | | |
| 10 | ... | | | | | |
| *(add more as needed)* | | | | | | |

**Priority key:** ⚠️ Critical (15–25) · ⚡ High (9–14) · 🟡 Medium (4–8)

---

## 3. Top 3 Red Flags

The three highest-scoring risks that, left unaddressed, guarantee failure:

### 🔴 Red Flag 1: [Risk name] — Score: XX/25

**Root cause:** [1–2 sentences on why this happens for this specific project.]

**Chain of failure:** [Trigger] → [Consequence] → [Terminal outcome]

---

### 🔴 Red Flag 2: [Risk name] — Score: XX/25

**Root cause:** [...]

**Chain of failure:** [...] → [...] → [...]

---

### 🔴 Red Flag 3: [Risk name] — Score: XX/25

**Root cause:** [...]

**Chain of failure:** [...] → [...] → [...]

---

## 4. The Vaccine Plan

Prevention actions for every Critical and High risk. Format: *"To prevent [X], I will [Y] by [milestone]."*

### ⚠️ Critical Risks — Address in Week 1

| Risk | Prevention Action | Deadline |
|---|---|---|
| [Risk name] | To prevent [X], I will [specific action]. | [Week 1 / Before first commit / Before first user / etc.] |
| [Risk name] | To prevent [X], I will [specific action]. | [...] |

### ⚡ High Risks — Monitoring Checkpoints

| Risk | Prevention Action | Checkpoint |
|---|---|---|
| [Risk name] | To prevent [X], I will [specific action]. | [Milestone or date] |
| [Risk name] | To prevent [X], I will [specific action]. | [...] |

---

## 5. The Pivot — Revised Roadmap

Based on the analysis, here are the hard constraints that maximize survival probability:

**Cut from scope:**
- ~~[Feature A]~~ — Removed because [adds X% complexity for Y% gain].
- ~~[Feature B]~~ — Removed because [not validated / not MVP].

**MVP definition (what remains):**
- [Single core function that directly addresses the #1 user pain point]

**Tech hardening:**
- Dropping [risky tech choice] for [proven stable alternative] because [reason].
- *(or: "No tech changes needed; risk is in scope, not stack.")*

**Hard constraints:**
- Dev cycle capped at [N] weeks for v1.0.
- Must find [N] real users to test before any public announcement.
- No new features until [specific milestone or metric].

---

## 6. Monitoring & Early Warnings

If these signals appear, trigger "Plan B" (pivot or stop) immediately — do not push through:

| Warning Signal | Threshold | Action |
|---|---|---|
| [Metric or observable behavior] | If [condition] by [date] | Stop / Pivot to [alternative] |
| [Metric or observable behavior] | If [condition] after [N] users | [Action] |
| Personal motivation check | If you haven't opened the project in [N] days | Force a retrospective; consider stopping |

---

## 7. Final Verdict

> **Soberly Optimistic Assessment:** [2–3 sentences. Acknowledge the real risks honestly. State what specifically makes this idea worth pursuing anyway — not hype, but evidence. End with the single most important action to take in the next 48 hours.]
```
