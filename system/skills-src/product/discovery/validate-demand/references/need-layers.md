# Need Layering Framework

Last updated: 2026-09-08

Shared vocabulary for digging beneath a stated ask to the need that drives it, synthesizing a
product vision from a set of stories, and judging whether modules serve real needs. Product
skills reference these definitions instead of redefining depth locally.

## Table of Contents

- [The Three Layers](#the-three-layers)
- [Descending the Layers](#descending-the-layers)
- [Category Splits Are Not Depth](#category-splits-are-not-depth)
- [Recording Rules](#recording-rules)
- [Vision Synthesis](#vision-synthesis)
- [Module-Need Fit](#module-need-fit)

---

## The Three Layers

| Layer | What it is | Where it shows up |
| --- | --- | --- |
| **Surface need** | What the user literally asks for — usually a solution in disguise | Feature requests, tickets, implemented behavior, marketing copy |
| **Deep need** | The motivation the ask serves — why the ask arises at all | Interviews, workflow context, the job the surface ask is hired for |
| **Fundamental need** | The human-instinct layer: safety, comfort, status, control, belonging, fear of loss | The terminus of a "why" chain — a noun (a fear, a loss, an identity), never a verb |

The classic example:

- **Surface**: "I want a faster horse carriage."
- **Deep**: "I want to reach my destination sooner." The deep need survives replacing the
  surface solution — a car serves it and makes the carriage irrelevant.
- **Fundamental**: comfort, safety, and control over one's own time.

A product that optimizes the surface ask competes on the carriage. A product that serves the
deep need is allowed to replace it.

---

## Descending the Layers

Two existing instruments perform the same move — a descent from surface toward fundamental:

- **The 5-Whys probe** (`validate-demand`, `references/framework.md`): ask "why?" from the
  stated pain until the chain reaches an emotion or a dollar amount.
- **The "So what happens then?" test** (`shape-solution`, `references/framework.md`): keep
  asking until you hit something uncomfortable.

Label the steps of a worked chain by layer. Using the validate-demand chain:

1. "I want to summarize news faster." — **surface**
2. "Too many articles to read." — **deep**
3. "I fall behind on industry trends." — **deep**
4. "I look uninformed in leadership meetings." — **deep**
5. "I'm afraid my boss thinks I'm not across the market. I'm afraid of losing my job." — **fundamental**

The existing terminus rule is the fundamental-layer test: if the chain ends at a verb ("saves
time", "reduces clicks", "automates X"), it has not bottomed out. Keep going until it
terminates at a noun — a fear, a loss, an identity.

---

## Category Splits Are Not Depth

Two existing instruments slice needs by type, orthogonally to depth:

- **The Task Trilogy** (`brainstorm`, `references/jtbd.md`) splits a job into Functional /
  Emotional / Social. Functional jobs usually state surface or deep needs; Emotional and
  Social jobs are expressions of fundamental needs — how the user wants to feel, and how they
  want to be perceived.
- **Fear Archetypes** (`shape-solution`, `references/framework.md`) are a catalog of
  fundamental-layer needs phrased as fears: incompetence and status fears express status and
  belonging; accountability fear expresses safety and control; peace-of-mind fear expresses
  comfort.

Use a category split to make sure no need type is skipped, and the layer split to make sure no
need stays at the surface.

---

## Recording Rules

- **Never stop at a verb.** "Saves time" is an unfinished descent, not a deep need.
- **Every layer entry marks its layer and its status**: inferred / user-confirmed / evidenced.
  Evidence levels follow the validate-demand scale. A deep or fundamental claim inferred from
  code, copy, or data models stays inferred until the user or user evidence confirms it.
- **Cluster before concluding.** One surface ask can serve several deep needs; several surface
  asks often share one deep need.
- **Layering enriches, it never re-identifies.** Adding surface/deep/fundamental entries to an
  existing `problem` record preserves its ID and other contributions.
- **Absence is a question, not a blank to fill.** When evidence supports no fundamental-layer
  claim, record the open question instead of inventing an instinct.

---

## Vision Synthesis

Stories are not single points. A set of stories, each individually modest, can implicate a
larger intent than any one of them states. The vision is the coherent story the deep and
fundamental needs tell together.

Method:

1. Cluster the stories by shared deep need — not by module or feature area.
2. Ask what larger intent would make the clusters coherent as one product.
3. Record at most one or two candidate visions, each linking the stories that imply it.

Worked example: a "project management system" whose stories cover capturing and sharing work
context, posting and claiming tickets through a chat platform, and per-person effort analysis
is not three features. The clusters — shared context anyone can act on, and work flowing to
whoever can do it — may imply an **AI-native organization** vision: a context subsystem plus a
collaborative ticket market. That is a candidate vision, recorded as inference and put to the
user as a question.

Rules:

- A candidate vision needs at least two independent clusters behind it. A single story
  is a need, not a vision.
  - **Existing product**: the clusters are implemented story clusters. Doc-stated larger
    intent without two implemented story clusters is recorded as an open question, not a
    vision record — docs are evidence of stated intent, not of behavior.
  - **Greenfield**: no stories exist yet, so a candidate vision may rest on at least two
    independently validated demand claims, or one validated claim plus a user-stated
    mission (the user's own statement in this effort, not doc-stated intent). Record the
    correspondingly weaker evidence status on the vision record.
- A candidate vision is an inference about the intent behind existing behavior or
  validated claims — never a roadmap. It authorizes no scope and validates no demand.
- It stays inferred until the user confirms, corrects, or rejects it. Competing candidates are
  separate records linked by an open question.

---

## Module-Need Fit

Judge each module against the **deep** needs of the stories it implements — not the surface
asks. Structural verdicts (cohesion, coupling) say whether a module is well built; fit
verdicts say whether it serves anything real.

| Verdict | Meaning |
| --- | --- |
| **Serves** | The module's behavior is what the deep need requires |
| **Over-serves** | Machinery beyond any evidenced need — configurability, generality, or polish nothing depends on |
| **Under-serves** | A real deep need is met partially; users compensate with workarounds |
| **Serves no real need** | No story's deep need depends on this module's behavior |

Add a **change-resilience note** per module: would this boundary survive the candidate or
confirmed vision, or does the vision imply the boundary moves? If the vision is an AI-native
organization, is the ticket module extensible toward agents posting and claiming work, or is
it hard-wired to human-only flows? The note names the strain; it is not a refactoring plan.

A fit shortfall — under-serves, serves-no-real-need, or poor vision resilience — becomes a gap
or opportunity naming the layer it fails, so `scope-product-increment` can act on it: an
under-serving module is a candidate for MODIFIED behavior; a serves-no-real-need module is a
candidate for REMOVED.
