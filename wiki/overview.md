
# pico-hermes Overview

**TL;DR**: pico-hermes is a compact tool-calling agent framework inspired by Hermes Agent, designed to be small, fast, and easily hackable.

## Goals
- Minimal runtime and dependencies
- OpenAI-compatible endpoints
- Tiny tool registry + toolsets
- Optional shell tool (off by default)

## Core Components
- `pico_hermes.py`: agent loop + prompt assembly
- `tools/registry.py`: tool schemas + dispatch
- `toolsets.py`: enable/disable tool groups
- `tools/file_tools.py`: read/write/search

## Related
- Hermes Agent (full-sized reference)
- PicoClaw (compact footprint inspiration)
