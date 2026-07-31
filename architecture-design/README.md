# Architecture Design

<div align="center">
  <a href="../README.md">Home</a> &bull;
  <a href="../product-planning/README.md">Product Planning</a> &bull;
  <strong>Architecture Design</strong> &bull;
  <a href="../feature-delivery/README.md">Feature Delivery</a> &bull;
  <a href="../visualization/README.md">Visualization</a> &bull;
  <a href="../knowledge-management/README.md">Knowledge</a> &bull;
  <a href="../team-collaboration/README.md">Collaboration</a> &bull;
  <a href="../user-setup/README.md">User Setup</a> &bull;
  <a href="../learning-resources/README.md">Learning</a>
</div>
<br>

**Lifecycle stage 2.** Turn a validated plan into a sound technical design — business and technical architecture, module boundaries, interaction contracts, and the review gates that keep the design (and later the code) honest. Builds on the outputs of [Product Planning](../product-planning/) and feeds [Feature Delivery](../feature-delivery/).

## Skills

| Skill | Focus | Description |
| :--- | :--- | :--- |
| [design-agent-architecture](design-agent-architecture/) | Design | Design a layered Agent system following the 6-layer standard (Interaction → Orchestration → Agent/Worker → Tools/MCP/Skills → Local Context & Memory → Data/Knowledge). Outputs a Markdown architecture doc + Mermaid diagram with observability. |
| [code-review](code-review/) | Review suite | A cohesive bundle of five review skills plus shared explorer/reviewer agents (see below). |

### The `code-review/` suite

A single package (5 skills + shared `agents/`) whose skills span the lifecycle — kept whole because several share the same agent pack:

| Skill | Serves stage | Description |
| :--- | :--- | :--- |
| `review-architecture` | Design (2) | TOGAF-style review across business/application/data/technology + deploy + ADR. |
| `review-design-doc` | Design (2) | Pre-implementation review of a design doc — catches scope creep, missing failure modes, overcomplexity. |
| `review-code-quality` | Delivery (4) | Production-readiness review of changes for correctness, reuse, simplification, efficiency. |
| `review-implementation-gaps` | Testing (5) | Compares built code against the design doc — complete / partial / missing / divergent. |
| `analyze-test-gaps` | Testing (5) | Audits test adequacy from business-critical paths (not line coverage). |

The delivery- and testing-stage skills above are also cross-referenced from [`backlog.md`](../backlog.md) under the future testing & deployment stage.

## Workflow Context

Comes after [Product Planning](../product-planning/) (you know *what* and *for whom*) and before [Feature Delivery](../feature-delivery/) (you build it). Engineering setup — context management, project skeleton, roadmap — runs alongside in [Engineering Setup](../engineering-setup/).
