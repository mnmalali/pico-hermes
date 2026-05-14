# pico-hermes

A compact, minimal, OpenAI-compatible agent framework inspired by Hermes Agent, designed to be tiny and hackable.

## Goals
- **Small & fast**: minimal dependencies, short startup, low memory.
- **Core agent loop**: tool calling + prompt assembly + context files.
- **Composable tools**: a tiny registry + toolsets.

## Quickstart

```bash
# install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run (CLI)
pico-hermes -q "Summarize this repo"

# run (TUI)
pico-hermes-tui
```

### Environment
- `OPENAI_API_KEY` (required)
- `PICO_HERMES_BASE_URL` (optional, default: https://api.openai.com/v1)
- `PICO_HERMES_TOOLSET` (optional: basic | net | terminal)
- `PICO_HERMES_ALLOW_SHELL=1` to enable the `terminal` tool

### Config file
`config.toml` (optional). Example:
```toml
model = "gpt-4.1-mini"
base_url = "https://api.openai.com/v1"
toolset = "basic"
allow_shell = false
```

## Tools (pico‑claw philosophy: tiny + essential)
- **File**: read_file, write_file, search_files, list_dir
- **Net**: http_get, http_post_json, rss_fetch, html_to_text
- **Utility**: json_query, sha256
- **Terminal**: terminal (disabled by default)

## Project Layout
```
.
├── src/pico_hermes/
│   ├── main.py               # minimal agent loop
│   ├── tui.py                # minimal TUI
│   ├── config.py             # config loader (env + toml)
│   ├── toolsets.py           # toolset definitions
│   └── tools/
│       ├── registry.py       # tool registry + dispatch
│       ├── file_tools.py     # read/write/search/list
│       ├── terminal_tool.py  # optional shell
│       ├── http_tool.py      # http + rss
│       └── misc_tools.py     # json, hash, html
├── config.toml
└── requirements.txt
```
