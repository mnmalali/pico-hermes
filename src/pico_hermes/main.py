
import argparse
import os
from pathlib import Path
from typing import List, Dict, Any

from openai import OpenAI

from .config import load_config
from .toolsets import resolve_toolset
from .tools.registry import registry, discover_builtin_tools


def load_context_files(cwd: Path) -> str:
    parts = []
    for name in ["PICO_HERMES.md", "AGENTS.md", "CLAUDE.md", ".cursorrules"]:
        p = cwd / name
        if p.exists() and p.is_file():
            parts.append(f"# {name}\n" + p.read_text(encoding="utf-8", errors="ignore"))
    return "\n\n".join(parts)


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
        system = system + "\n\n" + "Project context:\n" + context

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
    parser.add_argument("--config", default="config.toml", help="Path to config.toml")
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--toolset")
    args = parser.parse_args()

    cfg = load_config(args.config)

    model = args.model or cfg.get("model") or os.getenv("PICO_HERMES_MODEL", "gpt-4.1-mini")
    base_url = args.base_url or cfg.get("base_url") or os.getenv("PICO_HERMES_BASE_URL", "https://api.openai.com/v1")
    toolset = args.toolset or cfg.get("toolset") or os.getenv("PICO_HERMES_TOOLSET", "basic")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY")

    out = run_agent(args.query, model, base_url, api_key, toolset)
    print(out)


if __name__ == "__main__":
    main()
