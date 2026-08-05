Last updated: 2026-08-06

Every line below is either common sense the agent needs at startup, or an index entry pointing into `docs/`. Anything else, delete.

## Project Overview
[A concise one-sentence definition of the project's nature and core objectives — to enable the agent to establish a holistic understanding of the project.]

## Tech Stack
[Programming languages, frameworks, databases, testing tools, and other technical components — to prevent the agent from recommending mismatched technologies.]

## Project Structure
[Directory layout and corresponding functional responsibilities — to guide the agent on the correct placement of code files. A small table, one sentence of responsibility per module. Detailed dependencies stay in the module graph — link, do not restate.]

## Architecture Decisions
[WHY + WHAT for each non-obvious decision. No implementation detail. One paragraph plus a link to the architecture diagram — never rewrite the diagram as prose.]

## Coding Standards
[Naming conventions, code style guidelines, and prohibited practices — to unify code style across the team. Hard rules, no rationale: "All REST responses are wrapped in `Result`." NOTE: prefer linking to `.claude/rules/*.md` (managed by extract-rules) over inlining. Omit anything generic — standards not specific to this project only dilute.]

## Workflow
[Commit specifications, branching strategy, CI/CD pipeline rules, key commands, run/startup instructions — to align with the team's working process. One sentence plus a link to the runbook.]

## Special Constraints
[Security, performance, and compliance requirements — non-negotiable rules. State each so something could check it: name the frozen contract and the test that covers it, not "be careful".]

## Key Extension Points
[Table: goal → exact file and function to edit.]

## Danger Zones
[Code, interfaces, or configs that will "blow up if touched" — critical for legacy projects. This is where post-incident lessons land: what broke, why, and what to do first instead.]

## Historical Baggage
[Designs that "look weird but have historical reasons" — to prevent AI or newcomers from casually refactoring and causing disasters.]

## Context Files
[Table: file path | read-when trigger condition.]
