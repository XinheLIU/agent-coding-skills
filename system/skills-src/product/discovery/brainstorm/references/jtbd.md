# Jobs-to-be-Done Framework — Reference

Last updated: 2026-08-06

The framework behind the JTBD brief that `brainstorm` produces. Read this when the Specify phase needs the full pillar detail, the interview probes, or the output template.

## Table of Contents

- [Why JTBD](#why-jtbd)
- [The 5 Pillars](#the-5-pillars)
- [Interview Probes](#interview-probes)
- [The Struggle Audit](#the-struggle-audit)
- [Output Template](#output-template)
- [The 3 Beginner Sins](#the-3-beginner-sins)

---

## Why JTBD

A feature list describes what a product does. A job describes what a person is trying to accomplish and why the current way fails them. The distinction matters because features can be added indefinitely without ever making the job easier — that is what feature creep is.

The job is defined by three things the product team does not control: the user's situation, the moment the need becomes urgent, and the outcome they are reaching for. Get those wrong and every downstream decision inherits the error.

---

## The 5 Pillars

### Pillar 1 — The Specific User & Micro-Moment

Define the user by **situation, not title**. "Product manager" is a title; "a PM who has fifteen minutes before a stakeholder review and cannot find last quarter's numbers" is a situation. Only the second one tells you what to build.

```markdown
**User Context**
- Situation: [Where they are, what pressure they face]
- Moment: [The specific trigger for the need]
- Frequency: [How often this moment occurs]
```

Frequency is not decoration. A job that occurs daily and a job that occurs twice a year support completely different products.

### Pillar 2 — The Task Trilogy

Every job has three layers. Products that only serve the functional layer get adopted and abandoned.

| Job Type | Question it answers |
| --- | --- |
| Functional | What must it DO? The core utility. |
| Emotional | How should the user FEEL after? Confident, relieved, in control. |
| Social | How do they want to be PERCEIVED? Data-driven, prepared, competent. |

The social layer is the one most often skipped and most often decisive. People adopt tools that make them look good to someone whose opinion they care about.

### Pillar 3 — The Struggle

The current solution is the real competition, not the named competitor product.

```markdown
**Current Solution Analysis**
- Tool(s) used: [Excel, WeChat, memory, a manual process]
- Pain points: [Specific frustrations, not "it's inefficient"]
- Cost of pain: [Time, money, or stress — quantified]
- Why it fails: [The root cause of inadequacy, not the symptom]
```

"Why it fails" must bottom out at something structural. "It's slow" is a symptom; "every update requires manually reconciling three spreadsheets that different teams own" is a cause.

### Pillar 4 — Feature Scoping (deliberately deferred)

Not this stage. Feature scoping — P0 / P1 / Not-To-Do — belongs to `scope-mvp`, after `validate-demand` has issued a verdict and `shape-solution` has made the journey concrete.

Naming features here is the most common way a JTBD brief quietly becomes a spec. Resist it. If the user pushes for features, record the ideas in Open Questions and move on.

### Pillar 5 — Technical Constraints

Boundaries that are true regardless of what gets built.

```markdown
**Implementation Boundaries**
- Platform: [Mobile-first / desktop / both]
- Connectivity: [Online / offline-first / hybrid]
- Performance: [What must be fast, and what may be slow]
- Integrations: [Required systems or data sources]
- Latency limits: [If applicable — LLM, API, batch window]
```

These constrain form without choosing it. The form decision itself belongs to `scope-mvp`.

---

## Interview Probes

Ask only what the input has not already answered. One question at a time, and push once when an answer stays generic.

| Area | Opening question | Push when the answer is vague |
| --- | --- | --- |
| The user | Who exactly will use this? Describe their situation, not their title. | Where are they physically? What pressure are they under? |
| The struggle | How do they solve this today? | Which specific tool? Where exactly does it break? |
| The moment | When does this need become urgent? | What event triggers it? How often does that happen? |
| The outcome | What does success look like? | What decision does it unblock? How should they feel after? |
| The constraints | What are the technical realities? | Device, connectivity, integrations, latency ceiling? |

Good answers are concrete and slightly uncomfortable. If every answer is comfortable, the interview has not reached the struggle yet.

---

## The Struggle Audit

**Stop condition.** If the user cannot describe a current clunky solution, do not proceed to the brief. Flag it:

```markdown
**Warning: The Struggle Audit failed**

No existing workaround detected. This usually means one of:
- The problem does not cause enough pain for anyone to have worked around it
- The target user is defined too broadly to have a shared workaround
- The moment of need is not yet identified

**Recommendation**: Sharpen the user context before proceeding.
```

The absence of a workaround is strong evidence, not a gap to paper over. People route around pain they actually feel. When nobody has bothered, that is information.

Record it and stop. `validate-demand` will grade this as Inferred-level evidence and the verdict will reflect it.

---

## Output Template

```markdown
# JTBD Brief: [Name]

Last updated: [YYYY-MM-DD]

## Project Job
"Help a [specific user in a specific situation] [achieve a specific outcome] during [a specific micro-moment]."

## 1. Context & Challenge
[2–3 sentences: the situation, the time pressure, the core challenge]

## 2. The Task Trilogy
| Job Type | Description |
| --- | --- |
| Functional | [What it must DO] |
| Emotional | [How the user should FEEL] |
| Social | [How they want to be PERCEIVED] |

## 3. Current Pain
[The clunky current solution, its cost, and why it structurally fails]

## 4. Implementation Rules
- [Platform constraint]
- [Performance priority]
- [Key technical boundary]

## 5. Assumptions & Open Questions
| Assumption | Confidence | Cheapest test |
| --- | --- | --- |

## Summary
When [a type of user] is in [a situation],
they want to [accomplish a task],
so they can [achieve a result or feeling].

Today their solution is [current solution],
but it fails because [pain point].

## Anti-Patterns to Avoid
- Do NOT add [likely feature-creep item]
- Do NOT over-engineer [specific area]
- Do NOT assume [likely false assumption]
```

The Assumptions table is what `validate-demand` grades. Every claim in the brief that came from the team rather than from a user belongs in it.

---

## The 3 Beginner Sins

Check the brief against all three before persisting. Any failure sends you back to the interview.

| Sin | Antibody check |
| --- | --- |
| Feature creep | Does the brief define the job without prescribing features? |
| Solving the void | Is a current clunky solution documented? |
| Broad personas | Is the user defined by situation rather than title? |

These are the three failures that survive review most often, because each one produces a document that reads well. A brief can be articulate, well-structured, and still describe a job nobody has.
