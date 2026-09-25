---
name: acs-validate-prototype
description: Build throwaway code to answer one design question. Use when conversation cannot settle how behavior should work or what an interface should look like.
---

# Validate Prototype

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [design.open_question]
  retrieves: [change.requirements, design.relevant_decisions]
  produces: [design.experiment_evidence, design.decision_proposal]
  updates: [run.prototype]
  invalidates: [design.disproved_assumptions]
  handoff_to: [requesting_domain]
```

Shared semantics: [shared protocol](../../../../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../../../protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../../../protocols/presenter.md); source records retain authority.


A prototype is **throwaway code that answers a question**. The question decides the shape: a hand-driven harness for a state model ([LOGIC.md](references/LOGIC.md)), or competing renderings of one surface ([UI.md](references/UI.md)).

Do not confuse this with `docs/design/prototype.html`, the canonical prototype owned by the pipeline stages ([references/design-memory.md](references/design-memory.md)). Exploration is Working Memory; save the exact candidate and dependencies before formal review. A candidate or screenshot relied on by a decision becomes retained evidence. The stage that raised the question reconciles accepted intent into the canonical prototype.

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

7. **Capture it when done.** Record the decision in `<work-root>/<effort>/prototypes/<slug>/decision.md` with the question, variants tested, evidence, verdict, and source pointer. Preserve the exact reviewed candidate and necessary assets in the resolved persistent evidence home or an already retained revision; commit only with existing explicit Git authorization. Fold only the validated decision into the real code. Update the waiting map/spec issue.

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

6. **Capture the answer and clean up.** Fold the winner into real code. Retain any reviewed variant and necessary assets used as decision evidence; remove remaining working variants only after run reconciliation and within the authorized scope.

## Anti-patterns

- **Variants differing only in color/copy.** That's a tweak, not a prototype.
- **Sharing too much code between UI variants.** Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only is fine. Point mutations at stubs.
- **Promoting the prototype directly to production.** Rewrite it properly when folding in.
- **Adding tests to a prototype.** A prototype that needs tests is no longer a prototype.
- **Generalizing.** No "what if we wanted X later." Answer one question.

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).


Read `docs/agents/memory.md`, the configured run recovery entry, and the artifact that raised the question (a question or journey/scope record in `discovery.html`, a `map.md` decision ticket, or a `design-system/pages/<page>.md` spec). Write only the question, variants tested, evidence from user feedback, verdict, and pointer to the throwaway branch. Return the verdict and evidence to the domain owner/coordinator. Before formal review, save candidate content and evidence as proposed Persistent Memory. Record the actual feedback against its subject, reviewed revision, outcome, scope, basis, and source; retain consequential rationale and alternatives before dependent handoff. Resume the requesting stage through the common handoff envelope.

Classify the verdict before handing back — the two kinds promote to different homes. A decision about how the product behaves or looks is product intent and belongs in the PRD. A decision that constrains how the system is built — a data shape, a boundary, a protocol — is an architectural trade-off and belongs in an ADR. State which kind it is in `decision.md` so the owning stage can reconcile it at acceptance.

Unreviewed exploration is disposable after reconciliation. Preserve the decision and enough exact reviewed code or visual assets to recover its basis; the accepted canonical prototype remains a Persistent artifact.

Use coordinator-resolved existing homes or protocol defaults; ask only when identity or destination remains ambiguous.

## What This Skill Does NOT Do

- **Does not design the system** — it answers one question, not the architecture
- **Does not write production code** — it produces throwaway variants, not shippable features
- **Does not validate demand** — it tests a design hypothesis, not a market hypothesis
- **Does not scope the MVP** — it resolves a design question, not a feature list
