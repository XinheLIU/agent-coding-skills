# External Indexers for the Wiki Layer

Last updated: 2026-08-03

The Wiki layer is machine-generated. These four tools build it. They solve the same problem — give the agent a queryable map of the code instead of repeated greps — and trade speed against depth. Pick one; running several produces redundant indexes that drift apart.

`index-codebase` owns the choice. This file is the evidence behind it.

## Choosing

| Tool | Language | Speed | Index | Best when |
| --- | --- | --- | --- | --- |
| **codemap** | Go | Fastest | `.codemap/`, layered prefix/delta hashes | Default. Structure, dependency flow, blast radius, cross-agent handoff. |
| **codegraph** | Rust kernel + TS CLI | Medium | SQLite at `.codegraph/codegraph.db` (FTS5, WAL) | Persistent symbol graph with call chains; auto-syncs on edit. |
| **graphify** | Python + Tree-sitter | Slowest | `graphify-out/graph.json` + HTML | Mixed corpora — code plus PDFs, images, prose. Semantic relationships. |
| **GitNexus** | TS + Tree-sitter native | Medium | `.gitnexus/` + `~/.gitnexus/registry.json` | Multi-repo groups, Cypher queries, browser exploration of the graph. |

Rules of thumb:

- **Start with codemap.** It is the fastest, has no runtime to install, and covers the questions agents ask most (where does this live, what imports it, what breaks if I change it).
- **Switch to codegraph** when the repo is large enough that a stale index is the real problem — it watches the filesystem and reconciles at connect time, so there is nothing to re-run.
- **Reach for graphify** only when the corpus is not just code. It is the one that parses PDFs and images, and it is markedly slower.
- **Reach for GitNexus** when the unit of work spans several repositories, or when a human wants to explore the graph visually.

## codemap

Go, [JordanCoin/codemap](https://github.com/JordanCoin/codemap). Fastest, incremental.

```bash
brew tap JordanCoin/tap && brew install codemap    # macOS/Linux
# Windows: scoop bucket add codemap https://github.com/JordanCoin/scoop-codemap && scoop install codemap
```

Dependency mode needs `ast-grep` separately (`python3 -m pip install --no-cache-dir ast-grep-cli`); the `codemap-full` release artifact bundles both for CI.

```bash
codemap .                          # structure / context view
codemap --diff --ref main .        # changed files vs a ref
codemap --deps .                   # dependency edges (needs ast-grep)
codemap --importers path/to/file . # blast radius before editing
codemap blast-radius --json .      # review bundle
codemap handoff --json .           # cross-agent continuation payload
codemap mcp                        # MCP server over stdio
```

Flags precede the path. `codemap setup` wires the project: it writes `.codemap/config.json`, merges hooks into agent settings, and registers MCP in `.mcp.json`. Run it only when the user asks — it edits files outside the index.

Persistence is project-local in `.codemap/`. Handoff splits a stable `prefix` layer (hub summaries, counts) from a `delta` layer (changed-file stubs, risk files), each content-hashed, so repeat calls reuse unchanged bytes. The CLI saves by default (`--no-save` opts out); MCP does not save unless `save=true`.

`codemap serve --port 9471` exposes an HTTP API on loopback. It has no authentication — never pass `--host 0.0.0.0` on a shared network.

## codegraph

Rust parsing kernel with a TypeScript CLI, [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph). 20 languages, ships its own Node runtime.

```bash
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh   # macOS/Linux
npm i -g @colbymchenry/codegraph                                                          # via npm
```

Piping a remote script to a shell executes whatever that URL returns. Prefer the npm install, or download and read the script first.

```bash
codegraph init            # create .codegraph/ and build the graph
codegraph query <search>  # search symbols
codegraph callers|callees <symbol>
codegraph impact          # change impact
codegraph affected --stdin --json
codegraph status
codegraph serve --mcp     # MCP server over stdio
```

Index is SQLite at `.codegraph/codegraph.db` with FTS5; `CODEGRAPH_DIR` relocates it. Embedding the library in your own process needs Node 22.5+ for built-in `node:sqlite`.

Auto-sync is on by default via a native OS watcher (~2000ms debounce, `CODEGRAPH_WATCH_DEBOUNCE_MS`), plus reconciliation at MCP connect time that catches out-of-session changes like `git pull`. Manual `codegraph sync` is only needed when the daemon is off.

Registration: `codegraph install` auto-detects and configures Claude Code and other agents. Manual entry in `~/.claude.json`:

```json
{ "mcpServers": { "codegraph": { "type": "stdio",
  "command": "codegraph", "args": ["serve", "--mcp"] } } }
```

Only `codegraph_explore` is exposed by default; widen with `CODEGRAPH_MCP_TOOLS=explore,node,search,callers`.

## graphify

Python + Tree-sitter. Slowest, and the only one that handles multimodal sources (PDFs, images) alongside code.

```bash
uv tool install graphifyy      # note: package is graphifyy, command is graphify
graphify --help                # verify
```

```bash
graphify extract <src> --out . --code-only    # code only, no LLM backend
graphify extract <src> --out . --backend deepseek
graphify update                               # refresh a compatible layout
```

Do not run `graphify install` — it creates an unmanaged copy.

Outputs `graph.json`, `GRAPH_REPORT.md`, and `graph.html`. Relationships are labeled `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`; preserve those confidence labels when reporting findings, and cite the source file rather than the inference. Split corpora above roughly 200 files or 500k words into subgraphs. Stage prepared input outside any excluded directory — graphify honors `.git/info/exclude`, so a corpus staged inside an ignored output dir scans as empty.

No MCP server.

## GitNexus

TypeScript with native Tree-sitter bindings, [abhigyanpatwari/GitNexus](https://github.com/abhigyanpatwari/GitNexus). Graph plus a browser UI.

```bash
npm install -g gitnexus     # global; fastest MCP startup
npx gitnexus analyze        # zero-install, from repo root
```

```bash
gitnexus analyze [path]     # index or refresh (--force, --embeddings, --pdg)
gitnexus query|context|impact|trace|cypher
gitnexus group ...          # multi-repo groups
gitnexus mcp                # MCP server over stdio
gitnexus serve              # local HTTP server for the web UI
```

Registration: `gitnexus setup` writes config for detected editors, or `claude mcp add gitnexus -- npx -y gitnexus@latest mcp`. Exposes 17 MCP tools.

Index lives in `.gitnexus/` per repo, with a pointer in `~/.gitnexus/registry.json` so the MCP server can serve any indexed repo.

Two hardening switches are worth setting in shared environments: `GITNEXUS_MCP_READ_ONLY=1` drops raw Cypher, rename, and group tools; `GITNEXUS_MCP_ALLOWED_REPOS` is a startup-validated allowlist. `gitnexus eval-server` binds loopback without auth and requires `GITNEXUS_AUTH_TOKEN` for any non-loopback bind.

The hosted browser UI runs the full pipeline client-side in WebAssembly with no server, practically capped near 5k files. `gitnexus serve` lifts that ceiling by letting the page read CLI-built indexes.

## Prose knowledge bases

None of the above build a curated prose wiki. When the user wants distilled reading notes rather than a code index, use `wiki-init`, `wiki-ingest`, and `wiki-lint` instead: immutable hashed sources under `raw/`, curated pages under `wiki/` with frontmatter and `[[wikilinks]]`, a `SCHEMA.md` recording conventions, and an append-only `log.md`. That lineage is written by the agent following a procedure, not generated by a CLI, and needs no installation.

## Operating notes

- **Never install without asking.** Each tool adds a dependency and, for the MCP variants, edits agent configuration. Confirm first.
- **Record the choice.** `AGENTS.md` must say which indexer this repo uses, where the index lives, and how to query it. An index the agent does not know about is dead weight.
- **Git policy.** Track the index by default so every session shares one map. When it is large or churns on every commit, exclude it via `.git/info/exclude` rather than the tracked `.gitignore`, which keeps the choice local to the developer who made it.
- **Treat the index as a lead, not proof.** Confidence labels, staleness windows, and inferred edges are all fallible. Confirm against the source file before acting on it.
