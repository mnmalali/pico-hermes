
# pico-hermes Wiki Schema

This schema defines how the LLM Wiki works for pico-hermes.

## Layers
- **raw/**: immutable sources (papers, docs, repos, notes). Never edited by the LLM.
- **wiki/**: generated markdown pages (summaries, concepts, entities).
- **schema.md**: this file (how to maintain the wiki).

## Page Types
- **overview.md**: high-level summary of pico-hermes.
- **entities/*.md**: people, repos, frameworks.
- **concepts/*.md**: core ideas (toolsets, tool registry, agent loop).
- **decisions/*.md**: architecture decisions & tradeoffs.
- **comparisons/*.md**: comparisons against similar projects.

## Conventions
- Use `#` title as filename stem.
- Include a short **TL;DR** at the top.
- Add `Related:` links at bottom.
- Cite sources with links or paths (e.g., `raw/hermes/README.md`).

## Index & Log
- **wiki/index.md**: content index with one-line summaries.
- **wiki/log.md**: append-only record of ingests/queries.

## Ingest Workflow
1) Add source to `raw/`.
2) Summarize into `wiki/` pages.
3) Update `wiki/index.md` with entries.
4) Append to `wiki/log.md` with date + source.
5) Update related pages (concepts, entities, comparisons).

## Query Workflow
1) Read `wiki/index.md` to find relevant pages.
2) Read those pages and answer.
3) If new synthesis emerges, store it as a new page.

## Lint Workflow (periodic)
- Find contradictions, stale claims, missing pages, or orphan pages.
- Propose new sources to ingest.
