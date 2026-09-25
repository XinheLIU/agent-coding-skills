# Shared-Understanding Protocol

Last updated: 2026-09-09

How product skills question the user and confirm conclusions. The goal is a shared
understanding the user has actually confirmed — not an answer the model believes is true.

## Question blocks

Ask 4–5 questions per message, never one at a time and never more than five. Number them.
Each question carries a short bold label and the agent's **recommended answer** with a
one-line reason, grounded in the evidence already read. A recommendation gives the user
something concrete to correct; an open question with no stance makes them do all the work.

```text
1. **[Label]** — the question?
   Recommended: [answer] — [one-line reason from evidence].
```

## Facts vs. decisions

Before asking anything, look up what the environment can answer: code, shared memory
records, supplied artifacts, prior assessments. Only decisions, lived experience, and
evidence the user holds belong in a block. Never re-ask what shared memory already answers —
re-asking signals you did not read.

## Skipped questions are findings

After each block, reflect the answers back as concrete statements. Name every question that
went unanswered and either re-ask it in the next block or record it explicitly as an
assumption with its consequence. Never silently proceed on partial answers.

## Rounds

A follow-up block goes where the previous answers were thinnest — do not spread attention
evenly. Stop when the remaining unknowns no longer change the output; record them as open
questions instead of asking another round.

## The close

Before persisting or presenting the artifact as final, state:

1. **Established** — what is now settled, in the user's own terms.
2. **Assumption** — what remains unverified, named as assumption with its consequence.
3. **Disputed** — where the agent and the user still read the evidence differently, plus
   the observation that would settle it.

Ask the user to confirm or correct this statement; apply corrections before finalizing.
A recorded disagreement is a valid outcome — yielding to end the conversation is not.
In a non-interactive run, record the unconfirmed reading as an open question rather than
claiming confirmation.
