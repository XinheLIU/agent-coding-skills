---
name: prototype
description: Build throwaway code to answer one design question. Use when conversation cannot settle how behavior should work or what an interface should look like. Generates multiple variants (logic harness with state transitions, or radically different UI layouts) for user comparison. Credit to Matt Pocock's engineering workflow.
---

# Prototype

Last updated: 2026-08-10

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Credit

This skill adapts the prototype workflow from [Matt Pocock's engineering skills](../../references/matt-pocock/skills/engineering/prototype/). Core principles: throwaway from day one, generate multiple variants for comparison, capture the decision and archive the code.

## Pick a branch

Identify which question is being answered — from the user's prompt, the surrounding code, or by asking:

- **"Does this logic / state model feel right?"** → Build a tiny interactive terminal app that pushes the state machine through cases hard to reason about on paper. Expose every relevant transition with a simple command interface.
- **"What should this look like?"** → Generate **3-5 radically different UI variations** on a single route, switchable via URL search param (`?variant=A|B|C`) and a floating bottom bar with arrow navigation.

The two branches produce very different artifacts. If the question is ambiguous and the user isn't reachable, default to whichever matches the surrounding code (backend module → logic; page/component → UI) and state the assumption.

## Rules (apply to both)

1. **Throwaway from day one, and clearly marked.** Locate the prototype close to where it will be used (next to the module or page it's prototyping for) so context is obvious — but name it so a casual reader sees it's a prototype, not production.

2. **One command to run.** Use the project's existing task runner — `pnpm <name>`, `python <path>`, `make <target>`. The user must be able to start it without thinking.

3. **No persistence by default.** State lives in memory. Persistence is what the prototype checks, not what it depends on. If the question explicitly involves a database, hit a scratch DB or local file with a clear "PROTOTYPE — wipe me" name.

4. **Skip the polish.** No tests, no error handling beyond what makes it runnable, no abstractions. Learn something fast.

5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user sees what changed.

6. **Multiple variants for key decisions.** For logic: expose all transitions. For UI: generate 3-5 structurally different variants (different layout, information hierarchy, primary affordance — not just color tweaks). Surface the differences so the user can compare and decide.

7. **Capture it when done.** Record the decision in `<work-root>/<effort>/prototypes/<slug>/decision.md` with the question, variants tested, evidence, verdict, and source pointer. Commit the prototype itself to a throwaway branch (not main) as a primary source. Fold only the validated decision into the real code. Update the waiting map/spec issue.

## Logic Prototype Details

Build the smallest interactive harness that exposes every relevant transition. Common pattern:

```python
# prototype_state_machine.py
# Question: Can the reducer handle concurrent edits correctly?

def reducer(state, action):
    # ... the state model being tested

def repl():
    state = initial_state()
    while True:
        print(f"\nCurrent: {state}")
        print("Actions: [a]dd, [e]dit, [d]elete, [u]ndo, [q]uit")
        cmd = input("> ").strip()
        if cmd == 'q': break
        state = reducer(state, parse_action(cmd))
```

Match the project's existing conventions for tooling. Don't add a new package manager or runtime just for the prototype.

## UI Prototype Details

### Two sub-shapes — strongly prefer A

**Sub-shape A — adjustment to an existing page (preferred)**

The route already exists. Variants render on the same route, gated by `?variant=` URL search param. Existing data fetching, params, auth all stay — only rendering swaps. This is the default.

If the prototype is for something that doesn't yet have a page but *would naturally live inside one* (new dashboard section, new settings card, new flow step) — that's still sub-shape A. Mount variants inside the host page.

**Sub-shape B — a new page (last resort)**

Only use when the thing being prototyped genuinely has no existing page to live inside — an entirely new top-level surface or a flow that can't be embedded.

Create a throwaway route following the project's routing convention. Name it obviously (include "prototype" in the path). Same `?variant=` pattern.

### Process

1. **State the question and pick N.** Default to 3 variants. Cap at 5.

2. **Generate radically different variants.** Each variant must differ structurally — different layout, information hierarchy, primary affordance. Three slightly-tweaked card grids isn't a prototype. If two drafts are too similar, redo one with explicit "do not use X" guidance.

3. **Wire them together** with a switcher:
   ```tsx
   const variant = searchParams.get('variant') ?? 'A';
   return (
     <>
       {variant === 'A' && <VariantA {...data} />}
       {variant === 'B' && <VariantB {...data} />}
       {variant === 'C' && <VariantC {...data} />}
       <PrototypeSwitcher variants={['A','B','C']} current={variant} />
     </>
   );
   ```

4. **Build the floating switcher** — fixed bottom-center bar with left/right arrows, variant label, keyboard support (`←` / `→` keys when input not focused), visually distinct, hidden in production builds.

5. **Hand it over** with the URL and variant keys. User flips through and picks (or steals bits from each).

6. **Capture the answer and clean up.** Fold the winner into real code. Move losing variants and the switcher to the throwaway branch, not main.

## Anti-patterns

- **Variants differing only in color/copy.** That's a tweak, not a prototype.
- **Sharing too much code between UI variants.** Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only is fine. Point mutations at stubs.
- **Promoting the prototype directly to production.** Rewrite it properly when folding in.
- **Adding tests to a prototype.** A prototype that needs tests is no longer a prototype.
- **Generalizing.** No "what if we wanted X later." Answer one question.

## Shared Memory Contract

```text
Layer:    working — the code is throwaway and so is the record of testing it
Owns:     <work-root>/<effort>/prototypes/<slug>/decision.md
Promotes: interaction decisions → PRD Part 3, via write-prd
          architectural decisions → an ADR, via domain-modeling
```

Read `docs/agents/memory.md`, the active `state.md`, and the artifact that raised the question (`discovery/solution.md`, `discovery/mvp.md`, a `map.md` decision ticket, or a `design-system/pages/<page>.md` spec). Write only the question, variants tested, evidence from user feedback, verdict, and pointer to the throwaway branch. Never edit upstream artifacts. Update `state.md` to resume the stage that raised the question.

Classify the verdict before handing back — the two kinds promote to different homes. A decision about how the product behaves or looks is product intent and belongs in the PRD. A decision that constrains how the system is built — a data shape, a boundary, a protocol — is an architectural trade-off and belongs in an ADR. State which kind it is in `decision.md` so the promotion is unambiguous later.

The prototype code is deliberately disposable; the decision it bought is not. That is the point of the loop — throw away the code, keep the answer.

If routing is absent, work in conversation only and recommend `manage-context` before persisting.

**Next step:** control returns to the stage that raised the question — `scope-mvp` during scoping, the design skill during design. `state.md` already points there.
