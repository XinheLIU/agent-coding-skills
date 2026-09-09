# Logic Prototype

Last updated: 2026-09-08

A hand-driven harness for a state model. Use it when the question is about behavior — transitions, legality, data shape — the kind that reads fine on paper and only fails once real cases run through it.

Wrong branch if the question is "what should this look like". See [UI.md](UI.md).

## Signals this is the right shape

- A transition sequence is suspect: "does it survive X then Y?"
- The data model may not be able to represent a case that matters.
- The method surface needs to be felt before it is committed to.
- The user wants to press keys and watch state move.

## Process

### 1. Write the question down

One paragraph at the top of the file: what state model, what question. A harness that answers the wrong question costs more than no harness, and the question is what makes the answer checkable later — including by whoever reads it after the session ends.

### 2. Separate the logic from the shell

The logic goes behind a pure interface that could be lifted into the real codebase unchanged. The shell around it is disposable; the logic is not. This split is the whole value of the exercise — it is what lets a validated answer move without a rewrite.

Choose the shape from the question, not from what is easiest to wire up:

| Shape | Fits when |
|---|---|
| Pure reducer `(state, action) -> state` | Actions are discrete events over a single value |
| Explicit state machine | "Which actions are legal right now" is part of the question |
| Pure functions over a data type | No implicit current state, just transformations |
| Module with a method surface | The logic genuinely owns ongoing internal state |

Keep it pure: no I/O, no terminal code, no printing for control flow. The shell imports the logic; nothing flows back.

### 3. Build the thinnest shell that shows state

Redraw the whole frame each tick — clear the screen and reprint. One stable view, never growing scrollback.

Two parts per frame, in order:

1. **Current state**, one field per line or formatted JSON, so consecutive frames diff by eye.
2. **Available keys** at the bottom: `[a] add  [d] delete  [t] tick  [q] quit`.

Bold field names, dim derived values and IDs. Raw ANSI codes are fine (`\x1b[1m`, `\x1b[2m`, `\x1b[0m`) — do not add a styling dependency the project does not already have.

The loop: initialize state in memory, render, read one keystroke, dispatch to a handler, re-render the full frame, repeat until quit. The frame fits one screen.

### 4. One command to run it

Register a script in whatever task runner the project already has. The user types `pnpm <name>` or `make <target>`, never a path. No new package manager or runtime for a throwaway.

### 5. Hand it over

Give the run command and stop. The valuable moments are "wait, that shouldn't be possible" and "I assumed X would differ" — those are defects in the idea, which is what the harness exists to find. Add transitions on request; a harness is allowed to grow while it is still answering.

### 6. Capture and split

Capture the answer as [SKILL.md](../SKILL.md) describes. The logic-specific split: the validated reducer, machine, or function set lifts into the real module; the shell rides to the throwaway branch with the rest.

## Anti-patterns

- **Tests.** A harness that needs tests has stopped being one.
- **The real database.** In-memory, unless persistence is the question.
- **Generalizing.** No "what if we later wanted X." One question.
- **Fusing logic and shell.** If the reducer prints or prompts, it is no longer portable, and the exercise bought nothing.
- **Shipping the shell.** It was built to be driven by hand from a terminal. Only the module behind it is worth keeping.
