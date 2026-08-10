# Story Thinking Framework — Reference

Last updated: 2026-08-02

## Table of Contents
1. [The 3D Persona](#the-3d-persona)
2. [The 4-Act Narrative](#the-4-act-narrative)
3. [The 4-Stage User Journey](#the-4-stage-user-journey)
4. [Fear Archetypes](#fear-archetypes)
5. [Common Failure Modes](#common-failure-modes)
6. [Example: Full Output](#example-full-output)

---

## The 3D Persona

Generic personas produce generic stories. The persona must be specific enough to visualize — if you can see the person sitting at their desk at a particular time of day, you're there.

### Dimension 1: Who (Surface)

Demographics and situational context. The goal isn't a demographic profile — it's a vivid snapshot of their work reality.

**Questions to surface:**
- What is their exact job title? ("Manager" isn't enough — "Regional Sales Operations Manager" is.)
- Are they tech-savvy or tech-fearful? Do they use keyboard shortcuts or hunt through menus?
- What device are they on, and when does this pain typically hit?
- What does their worst workday morning look like?

**Example (too vague):** "A busy professional who uses Excel."

**Example (specific enough):** "Xiao Wang, 34, Regional Sales Operations Manager at a mid-size manufacturing firm. Uses Excel daily but avoids the IT ticketing system — calls it 'a black hole.' Always on laptop. The pain hits every Monday at 9 AM."

### Dimension 2: What (Behavior)

The current "hack" — how they're failing to solve the problem before your product exists. This is the most important behavioral context and the most commonly skipped.

**Questions to surface:**
- What do they do *today* to solve this? (Excel, sticky notes, email threads, hiring an intern, manual Google searches)
- Where does that hack break down? (Version conflicts? It takes too long? It produces errors?)
- How often does the failure happen, and what does the failure look like?

**Example (too vague):** "They struggle to manage information."

**Example (specific enough):** "Every Monday morning, Xiao manually scans 50+ industry newsletters, copy-pastes excerpts into a Word doc, and tries to synthesize a summary. By 11 AM he's still not done. The hack breaks down whenever a board meeting is approaching — he never has time to finish."

### Dimension 3: Fear (Motivation)

The emotional engine. This is the most important and most commonly missing dimension.

People don't adopt tools because they're efficient. They adopt them to avoid a specific fear or achieve a specific identity. "Wants to save time" is a desire, not a fear. A fear has a witness — someone who will find out when things go wrong.

**Questions to surface:**
- What happens if this problem isn't solved? Who finds out?
- Are they afraid of looking incompetent? Missing a critical signal? Being held responsible for a mistake?
- What would it feel like to "win"? More confidence? Respect from their boss? Peace of mind at 5 PM?

**The "So what happens then?" test:** If you can't name a specific fear, keep asking "So what happens then?" until you hit something uncomfortable.

> "They want to save time."
> → So what happens if they don't? "They might miss something important."
> → So what happens then? "Their boss would ask why they didn't catch it."
> → So what happens then? "They'd look uninformed in front of the CFO."
> → **Fear: Looking uninformed in front of the CFO.**

---

## The 4-Act Narrative

The story arc gives the product team the emotional "why" behind every "what." Don't summarize — show it happening.

### Act 1 — Status Quo (The Ordinary World)

Describe the mundane routine before your product exists. The workaround in action. No drama yet.

**Purpose:** Establish the time, place, rhythm of their day. Make the workaround feel normal — because it is, for them. This sets the emotional baseline.

**Example:** "Every Monday at 8:55 AM, Xiao opens his inbox to find 50+ industry newsletters. He starts a new Word doc titled 'Weekly Intel — DRAFT' and begins copy-pasting. He's been doing this for two years."

### Act 2 — Breaking Point (The Conflict)

The specific moment the status quo fails catastrophically. This is the emotional wound the product heals.

**Purpose:** Create the need. Without this moment, there's no reason to change behavior.

**What makes a good Act 2:**
- A specific triggering event (a meeting, a deadline, a public failure)
- The emotional consequence, not just the logistical one (embarrassment, fear, loss of standing)

**Example:** "It's 10:45 AM. The board meeting starts at 11. He's only summarized 15 of the 50 alerts. He skims the rest and goes in. The CFO mentions a supplier news item Xiao missed. He says nothing. He feels his credibility drain."

### Act 3 — Intervention (The Resolution)

The "Aha!" moment — first encounter with your product. Be ruthlessly specific.

**Purpose:** Show the product solving the exact problem from Act 2. The contrast between old and new must be visceral.

**What makes a good Act 3:**
- One named action (what they click, type, or say)
- A visible time contrast (50 minutes → 11 seconds; 3 hours → one click)
- The emotional reaction in that moment ("Wait — that's it?")

**Example:** "A colleague shares a link. Xiao pastes in the 50 newsletter URLs, clicks 'Generate.' In 11 seconds, a 3-bullet executive summary appears with the top market shifts flagged. He reads it in 90 seconds and walks into the meeting prepared."

### Act 4 — New Reality (The Payoff)

What does their life feel like after the product becomes a habit? Focus on identity, not features.

**Purpose:** Show the team what they're actually building toward — not a product metric, but a changed human.

**What makes a good Act 4:**
- An identity shift ("I'm now the person who...")
- A specific moment where the shift becomes visible (a meeting, a conversation, a daily routine)
- NOT: "They saved 120 hours this quarter"

**Example:** "Xiao walks into next Monday's meeting with a printed summary in his folder. When the CFO asks about the supplier news, Xiao answers before anyone else. He's booked a coffee break for 10:30. He no longer dreads Mondays."

---

## The 4-Stage User Journey

Where UX decisions live. Each stage has a job to do — don't blend them.

### Stage 1 — Discovery

How and where does the user first encounter the product?

- **Trigger:** The specific channel or event that surfaces it (colleague recommendation, LinkedIn ad, desperate Google search at 10 PM)
- **Core skepticism to overcome:** Every user arrives with a default objection — "Is this accurate?" / "Will I actually use this?" / "Is this just another tool I'll abandon?"
- **Design implication:** Social proof, a credible first impression, and immediate trust signals matter more than feature lists here.

### Stage 2 — First Use

The moment they try it for the first time.

- **Goal:** Zero friction. Immediate value within 30 seconds. No 12-step onboarding.
- **The "Aha!" moment:** Must be a single, concrete visible result. Not "they explored the features" — they clicked one thing and got one specific result that proved the product worked.
- **Design implication:** The first output must be so obviously good that sharing it feels natural. What does "good" mean for this persona's specific fear?

### Stage 3 — Core Process

The repeated interaction that becomes part of their routine.

- **Trigger:** What causes them to open the app each time? (Monday mornings, before each client meeting, end-of-day)
- **Anti-fatigue goal:** Make the 10th use as satisfying as the 1st. Preventing output fatigue is harder than getting the first use right.
- **Design implication:** Personalization, memory of past interactions, and progressive disclosure — what does the product learn about them over time?

### Stage 4 — Long-Term Value

The moment they realize the product has changed who they are.

- **Identity moment:** A review, a performance conversation, a public moment where their new capability becomes visible
- **Retention hook:** Why do they stay? Not "because it saves time" but because the product is woven into their professional identity
- **Design implication:** History, analytics, and "look how far you've come" moments. Show the user their own growth.

---

## Fear Archetypes

Use these when the user can't name a specific fear — pick the closest match and confirm:

| Archetype | Example |
|-----------|---------|
| **Incompetence fear** | "I'll look uninformed in the meeting" |
| **Accountability fear** | "If we miss this price shift, it's on me" |
| **Speed fear** | "My competitor will know before I do" |
| **Status fear** | "The team will stop trusting my judgment" |
| **Peace-of-mind fear** | "I just want to leave work feeling caught up" |
| **Reliability fear** | "If I forget something important, I look undependable" |

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| **Generic Who** | "A busy professional" | Name their job title and one specific daily constraint |
| **No current hack** | Story starts with the product already in place | Ask "What do they do today, before your tool exists?" |
| **Vague fear** | "They want to save time" | Ask "If they fail, who finds out? What do they lose?" |
| **Feature Aha!** | "They discovered all the analytics features" | The Aha! must be one specific interaction — one click, one visible result |
| **Metric payoff** | "They saved 120 hours this quarter" | Act 4 must be an identity statement — "I'm the person who always knows what's happening" |
| **Smooth onboarding** | "The onboarding experience was seamless" | Name the one action they take and the one result they see |

---

## Example: Full Output

**Input**: "I'm building an AI tool that monitors industry news and summarizes it for sales leaders."

---

### Persona: Xiao Wang

**Who:** Regional Sales Operations Manager, mid-size manufacturing firm. Uses Excel fluently, avoids new software unless forced. Laptop only. Pain hits every Monday at 9 AM.

**Current Hack:** Manually scans 50+ industry newsletter emails, copy-pastes into a Word doc, tries to write a synthesis. By 11 AM, still not finished. The hack breaks down every time a board meeting approaches.

**Fear:** Looking uninformed in front of the CFO. Two years ago he missed a competitor move that came up in the quarterly review. He hasn't forgotten.

---

### The Story

**Act 1 — Status Quo:** Every Monday at 8:55 AM, Xiao opens his inbox to 50+ newsletters. He starts a new Word doc: "Weekly Intel — DRAFT." He's been doing this for two years. Some weeks it's fine. Most weeks he runs out of time.

**Act 2 — Breaking Point:** It's 10:45 AM. Board meeting at 11:00. He's only finished 15 of the 50 alerts. He skims the rest in 10 minutes and walks in. The CFO mentions a supplier news item. Xiao says nothing. He can feel the credibility drain from his face.

**Act 3 — Intervention:** A colleague sends him a link. "Try this — it took me 30 seconds." Xiao pastes in the 50 newsletter URLs. Clicks "Generate." In 11 seconds: a 3-bullet executive summary, top signals flagged, source links included. He reads it in 90 seconds. He thinks: *Wait. That's it?*

**Act 4 — New Reality:** Next Monday morning, Xiao reads his summary with his coffee. He prints it and puts it in his folder. In the board meeting, the CFO asks about the supplier news. Xiao answers before anyone else. He's booked a standing coffee break for 10:30 AM. He no longer dreads Mondays.

---

### User Journey

**Discovery:** Colleague Slack message: "This thing is wild, took me 30 seconds." Core skepticism: "Will the summaries actually be accurate enough to trust in front of my boss?" Overcomes it by: seeing a sample output that names a real recent signal he recognizes.

**First Use:** Pastes newsletter URLs, clicks one button, sees a 3-bullet summary in 11 seconds. Aha!: The second bullet names an industry development he just read about — he knows the output is real, not hallucinated. He shares it in Slack immediately.

**Core Process:** Every Monday morning before coffee. Trigger: first thing when he opens his laptop. Anti-fatigue: the summaries update based on what he's flagged as important — the tool learns which signals matter to him over time.

**Long-Term Value:** At his 6-month performance review, Xiao's manager mentions that he's "always the most informed person in the room." Xiao has 24 weeks of Monday summaries saved. He pulls up the one from the week the CFO asked that question. He's become the person his team comes to for industry context.

---

### Story Prompt

> "I'm building an AI news monitoring tool for a Regional Sales Operations Manager who currently spends 2+ hours every Monday manually copy-pasting 50 newsletters into a Word doc — and still walks into board meetings unprepared. He is terrified of looking uninformed in front of his CFO (it happened once; he hasn't forgotten). The first use should be: paste URLs, click one button, read a 3-bullet summary in under 90 seconds. The core process: a standing Monday-morning habit that takes less time than making coffee. The goal: he becomes the person in every meeting who already knows what's happening."
