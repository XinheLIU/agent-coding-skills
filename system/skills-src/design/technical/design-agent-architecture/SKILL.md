---
name: design-agent-architecture
description: "Design a general layered Agent system architecture following the 6-layer standard: L1 Interaction, L2 Orchestration, L3 Agent/Worker Layer, L4 Tools/MCP/Skills, L5 Local Context & Memory, L6 Data/Knowledge/Semantic Layer. Outputs an English Markdown architecture doc and Mermaid diagram with Agent Observability. Use when the user asks to design, plan, review, or document any Agent system architecture, including English or Chinese-language agent architecture requests, or wants to adapt reusable agentic patterns to a domain, product, workflow, or vertical."
---

# Agent Architecture Designer

Last updated: 2026-08-10

## Workflow

### Phase 1: Discovery

Ask only for missing information. If the effort has a PRD (`docs/product/<slug>/prd.md`), read it first — it usually answers scope, core jobs, and success criteria. If the user's request already answers an item, do not repeat it.

1. **Agent name and scope** - What is this agent called, and what domain or workflow does it serve?
2. **Core jobs** - What are the 1-3 outcomes it must reliably deliver?
3. **Tools and systems** - Which APIs, databases, applications, files, or MCP servers must it use?
4. **Human checkpoints** - Which decisions require approval, review, or escalation?
5. **Memory and data** - Which structured data, unstructured data, semantic models, and local memory should it use?
6. **Success criteria** - How will users know the agent worked: tests, evals, KPIs, review gates, or resolved tasks?

Flag and discuss anything unclear or risky before designing:

- If the task has a fixed, predictable path, recommend a workflow before an autonomous agent.
- If a single LLM call with retrieval is enough, say so instead of over-designing.
- Put routing, state machines, planning policy, and stop conditions in L2, not L3.
- Put executable integrations and tool contracts in L4, not L5 or L6.
- Put local working state, user/project memory, run artifacts, and task snapshots in L5.
- Put structured data, unstructured data, and the semantic layer in L6.
- Split a monolithic agent into L3 agents/workers only when the split maps to real responsibility boundaries.

### Phase 2: Design

Read [layered-architecture.md](references/layered-architecture.md) for layer responsibilities, Anthropic-inspired agentic patterns, context packs, observability, and the Mermaid template.

Map the user's inputs to each layer:

| Layer | What to fill in |
|-------|----------------|
| L6 | Data, knowledge, and semantic layer: structured data, unstructured data, ontology/taxonomy/entity model, semantic retrieval/indexes |
| L5 | Local context and memory: user/project preferences, working memory, task state, local files/assets, run artifacts, episodic memory |
| L4 | Tools/MCP/Skills: tool contracts, APIs, connectors, scripts, skills, SOPs, external system scaffolding |
| L3 | Agent/worker layer: primary agent, specialist workers, evaluator, guardrail, reviewer, or human handoff roles |
| L2 | Orchestration: pattern choice, routing, planner, state machine, context compiler, stop conditions, feedback loop |
| L1 | Interaction and workspace: chat, web/mobile UI, approval queue, task board, notifications, monitoring console |

Select the simplest agentic pattern that fits:

| Pattern | Use when |
|---------|----------|
| Augmented LLM | One model call plus retrieval, tools, or memory is enough |
| Prompt chaining | The task decomposes into fixed sequential steps with gates |
| Routing | Inputs fall into distinct categories with specialized handlers |
| Parallelization | Independent subtasks or multiple judgments improve speed or confidence |
| Orchestrator-workers | The needed subtasks are not known upfront |
| Evaluator-optimizer | Clear evaluation criteria make iterative improvement worthwhile |
| Autonomous agent | The task is open-ended, tool-driven, and cannot be hardcoded safely |

Also design the runtime context packs:

- **Data Pack** - Structured facts from L6 and task snapshots from L5.
- **Knowledge Pack** - Unstructured retrieval results and semantic entities from L6.
- **Instruction Pack** - System rules, domain rules, workflow policy, evaluation criteria, and human constraints.
- **Local Context** - L5 working memory plus L3/L4 execution state and tool results.

### Phase 3: Output

Write all output in English. Produce two artifacts in sequence.

#### 1. Architecture Doc (Markdown)

Structure:
```
# [Agent Name] Architecture Design

## Overview
[One sentence: what this agent does and for whom]

## Design Principles
[Explain the relevant principles: simplicity first, transparent planning, clear tool contracts, measurable feedback]

## Agentic Pattern

[Choose the simplest pattern that fits and explain why]

## Six-Layer Architecture + Observability

### L6 Data, Knowledge, and Semantic Layer
[Structured data, unstructured data, semantic layer, retrieval/indexing]

### L5 Local Context and Memory Layer
[Local workspace, working memory, preferences, task snapshots, artifacts]

### L4 Tools, MCP, and Skills Layer
[Tool/API/MCP/Skill list, SOPs, external system scaffolding, tool contracts]

### L3 Agent and Worker Layer
[Primary agent plus specialist workers/reviewers/evaluators; tools and context each role can access]

### L2 Orchestration Layer
[Pattern, kernel if known, routing/planning/state machine, stop conditions, feedback loop]

### L1 Interaction and Workspace Layer
[UI, chat, task board, approval queue, notifications, monitoring console]

### Agent Observability
[Trace, tool audit, memory audit, evals, cost/latency, replay, anomaly detection]

## Runtime Context Packs
[Data Pack / Knowledge Pack / Instruction Pack / Local Context]

## Human-in-the-loop and Safety
[Approval points, escalation paths, sandboxing, stop conditions]

## Evaluation Plan
[Task success metrics, automated evals/tests, human review, feedback loop]

## Adaptation Guide
[Which layers change when adapting the design to a similar agent]
```

#### 2. Mermaid Diagram

Use the template from [layered-architecture.md](references/layered-architecture.md) as base. Customize:
- Replace placeholder labels with actual component names
- Add domain-specific data/knowledge/semantic nodes inside L6
- Add local memory, workspace, and artifact nodes inside L5
- Add the user's specific tools/SOP inside L4
- Keep L2 orchestration components reusable
- Include the Observability subgraph with dashed arrows to each layer

Wrap in a fenced code block: ` ```mermaid `

## Quality checks before delivering

- The design uses the simplest viable pattern; added autonomy is justified.
- L6 contains structured data, unstructured data, and semantic layer components.
- L5 contains local context, memory, workspace, task state, and artifacts.
- L2 owns routing, planning, state transitions, gates, stop conditions, and feedback loops.
- Every external tool/API the user mentioned appears in L4
- Observability components are present as a vertical column
- Runtime context packs are explicitly mapped
- Human checkpoints and stop conditions are explicit
- Mermaid diagram has no syntax errors (check bracket matching and subgraph nesting)

The architecture doc and diagram feed `engineering/feature/spec`; record hard-to-reverse choices as ADRs via `domain-modeling`.
