
import os
import subprocess

from tools.registry import registry


def terminal(args):
    if os.getenv("PICO_HERMES_ALLOW_SHELL") != "1":
        raise RuntimeError("terminal tool disabled; set PICO_HERMES_ALLOW_SHELL=1")
    cmd = args.get("command")
    if not cmd:
        raise ValueError("command is required")
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"stdout": p.stdout, "stderr": p.stderr, "exit_code": p.returncode}


registry.register(
    name="terminal",
    schema={
        "name": "terminal",
        "description": "Run a shell command (disabled by default).",
        "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]},
    },
    handler=terminal,
)
