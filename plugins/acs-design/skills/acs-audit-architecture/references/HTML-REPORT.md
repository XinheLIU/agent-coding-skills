# HTML Report Format

Last updated: 2026-09-14

Use the local `visual-report.md` contract. `AUDIT.html` is a concise visual index of `AUDIT.md`, not a roadmap.

Each ranked finding is an `<article>` with a stable anchor, priority badge, affected files, one-sentence problem, one-sentence fix direction, up to four wins, collapsed evidence, and a 320–360px current/target visual. Use inline SVG for seams, mass diagrams, cross-sections, and call-graph collapse. Use Mermaid only for graph-shaped relationships and retain ordinary HTML fallback labels. End with one anchored top recommendation.
