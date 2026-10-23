---
protocol: acs:questioning
version: 1.0.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/questioning.md
---

# Questioning and Shared Understanding

Last updated: 2026-10-23

How skills question the user and confirm conclusions. The goal is a shared understanding
that the user has actually confirmed. This contract owns question classification, ordering,
and wording; callers own domain evidence grades and persistence. Existing authorization
and user-named gates still govern actions.

## Classify before asking

Classify every candidate question before putting it to the user. Record its classification,
route, and short evidence-based reason in the working decision record; each question in a
round must trace to that decision. Read code, shared memory, supplied artifacts, and earlier
answers first. Never re-ask what those sources already establish.

| Class | Route |
| --- | --- |
| Lookup fact — the environment or supplied records can answer it | Dispatch a sub-agent to look it up when delegation is authorized and available; otherwise inspect it directly. A pending lookup leaves its dependent questions blocked, while independent questions may proceed. |
| Observable fact — running something can establish behavior, timing, layout, output, or performance | Route to [acs-validate-prototype](../resources/skills-src/design/ux/acs-validate-prototype/SKILL.md) (reference procedure; capability not installed) for observation. Record the result or the missing observation; do not ask the user to guess the outcome. |
| Mechanical decision — evidence and existing constraints determine the answer | Decide and record the choice and its basis within the authorized scope. |
| Taste decision — multiple choices remain reasonable within the authorized scope | Decide provisionally, record the recommendation and trade-off, and show it at the next existing review gate so the user can correct it. |
| User challenge — a proposed change to the user's stated direction or a decision reserved to the user | Always ask; never auto-decide. State the original direction, recommended change, evidence, missing context, and cost of being wrong. Keep the user's direction until they accept the change. |

User-held evidence and lived experience that no lookup or observation can supply also belong
to the user-question route: record them as a user challenge to the current assumption, without
inventing an answer. A recommendation may be to leave a claim unverified pending that evidence.
A taste or mechanical label never overrides an explicit user gate or grants new authority.
If the required observation cannot run, retain the unknown and its consequence; absence of a
result is not evidence.

## Frontier rounds

The frontier contains only questions whose prerequisites are already settled. Never ask a
question whose premise is still open in the same round. Select at most five frontier questions
per round, prioritizing the unknowns that most affect the output. A round may contain one
question; do not pad it to meet a minimum. If more than five are ready, defer the remainder.

Wait for answers, reflect them as concrete statements, and recompute the frontier before the
next round. Pending lookups and observations block only their dependents. Follow up where the
answers were thinnest rather than spreading attention evenly. Stop when remaining unknowns
no longer change the output; record them as open questions instead of adding another round.

## Question blocks

Number each question and give it a short bold label, a **recommended answer**, and a one-line
reason grounded in evidence already read. Word each question so "yes" accepts the
recommendation, not its opposite. Offer alternatives when they clarify a real choice.

```text
1. **[Label]** — Do you accept [recommended answer]?
   Recommended: [answer] — [one-line reason from evidence].
```

Recommendations give the user something concrete to correct; they do not count as answers.
Ask through the coordinator's available question interface when coordinated. Preserve the
numbered block and recommendation in either the tool or prose representation.

## Skipped questions are findings

After each block, name every unanswered question. Re-ask it in a later frontier round or
record it explicitly as an assumption with its consequence. Never silently proceed on partial
answers, infer confirmation from silence, or settle a user challenge without an answer.
A blocked user decision stays unresolved; an assumption does not authorize dependent work.

## The close

Before persisting or presenting the artifact as final, state:

1. **Established** — what is now settled, in the user's own terms.
2. **Assumption** — what remains unverified, named as assumption with its consequence.
3. **Disputed** — where the agent and user still read the evidence differently, plus the
   observation that would settle it.

Ask the user to confirm or correct this reading, phrased so yes confirms it; apply corrections
before finalizing. A recorded disagreement is a valid outcome. In a non-interactive run,
record the unconfirmed reading as an open question rather than claiming confirmation.

## Provenance

Promoted from the product-lane shared-understanding protocol. Adapted from Matt Pocock's
[`grilling`](https://github.com/mattpocock/skills/blob/49dd158/skills/productivity/grilling/SKILL.md)
(frontier rounds, recommendations, affirmative wording, environment facts), pstack's
[`poteto-mode`](https://github.com/cursor/plugins/blob/0b8e952/pstack/skills/poteto-mode/SKILL.md)
(observe before asking), and gstack's
[`autoplan`](https://github.com/garrytan/gstack/blob/35dd014/autoplan/SKILL.md)
(mechanical, taste, and user-challenge decisions). The five-question cap, skipped-question
findings, and established/assumption/disputed close preserve the existing ACS contract.
