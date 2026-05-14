
import argparse
import os
from pathlib import Path
from typing import List, Dict, Any

from openai import OpenAI

from toolsets import resolve_toolset
from tools.registry import registry, discover_builtin_tools


def load_context_files(cwd: Path) -> str:
    parts = []
    for name in ["PICO_HERMES.md", "AGENTS.md", "CLAUDE.md", ".cursorrules"]:
        p = cwd / name
        if p.exists() and p.is_file():
            parts.append(f"# {name}
" + p.read_text(encoding="utf-8", errors="ignore"))
    return "

".join(parts)


def build_system_prompt() -> str:
    return (
        "You are pico-hermes, a compact tool-calling agent. "
        "Use tools when needed and keep responses concise."
    )


def run_agent(prompt: str, model: str, base_url: str, api_key: str, toolset: str):
    discover_builtin_tools()
    enabled_tools = resolve_toolset(toolset)
    tool_schemas = registry.get_tool_schemas(enabled_tools)

    cwd = Path.cwd()
    context = load_context_files(cwd)

    system = build_system_prompt()
    if context:
        system = system + "

" + "Project context:
" + context

    client = OpenAI(api_key=api_key, base_url=base_url)

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    while True:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tool_schemas if tool_schemas else None,
        )
        msg = resp.choices[0].message

        if msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
            for call in msg.tool_calls:
                result = registry.dispatch(call.function.name, call.function.arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                })
            continue

        return msg.content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", required=True, help="User prompt")
    parser.add_argument("--model", default=os.getenv("PICO_HERMES_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--base-url", default=os.getenv("PICO_HERMES_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--api-key", default=os.getenv("OPENAI_API_KEY"))
    parser.add_argument("--toolset", default=os.getenv("PICO_HERMES_TOOLSET", "basic"))
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Missing OPENAI_API_KEY")

    out = run_agent(args.query, args.model, args.base_url, args.api_key, args.toolset)
    print(out)


if __name__ == "__main__":
    main()
