
import os
import readline
from pathlib import Path

from .config import load_config
from .main import run_agent

HISTORY_FILE = ".pico_hermes_history"


def _load_history():
    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass


def _save_history():
    try:
        readline.write_history_file(HISTORY_FILE)
    except Exception:
        pass


def main():
    cfg = load_config("config.toml")

    model = os.getenv("PICO_HERMES_MODEL", cfg.get("model", "gpt-4.1-mini"))
    base_url = os.getenv("PICO_HERMES_BASE_URL", cfg.get("base_url", "https://api.openai.com/v1"))
    toolset = os.getenv("PICO_HERMES_TOOLSET", cfg.get("toolset", "basic"))

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY")

    _load_history()
    print("pico-hermes TUI. Commands: /exit /clear /help")

    try:
        while True:
            try:
                prompt = input("pico-hermes> ").strip()
            except EOFError:
                break

            if not prompt:
                continue
            if prompt in ("/exit", "/quit"):
                break
            if prompt == "/help":
                print("Commands: /exit /clear /help")
                continue
            if prompt == "/clear":
                os.system("clear" if os.name != "nt" else "cls")
                continue

            print("\n---")
            out = run_agent(prompt, model, base_url, api_key, toolset)
            print(out)
            print("---\n")
    finally:
        _save_history()
