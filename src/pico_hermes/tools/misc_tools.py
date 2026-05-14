
import hashlib
import json
import os
import subprocess
from html.parser import HTMLParser
from typing import Any

from .registry import registry

class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def get_text(self):
        return "".join(self.parts)


def html_to_text(args):
    html = args.get("html", "")
    stripper = _HTMLStripper()
    stripper.feed(html)
    return stripper.get_text()


def sha256(args):
    text = args.get("text")
    path = args.get("path")
    h = hashlib.sha256()
    if text is not None:
        h.update(text.encode("utf-8"))
    elif path:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    else:
        raise ValueError("text or path is required")
    return h.hexdigest()


def _parse_query(query: str):
    # supports a.b[0].c
    parts = []
    buf = ""
    i = 0
    while i < len(query):
        c = query[i]
        if c == '.':
            if buf:
                parts.append(buf)
                buf = ""
            i += 1
            continue
        if c == '[':
            if buf:
                parts.append(buf)
                buf = ""
            j = query.find(']', i)
            if j == -1:
                raise ValueError("unclosed [ in query")
            idx = query[i+1:j]
            parts.append(int(idx))
            i = j + 1
            continue
        buf += c
        i += 1
    if buf:
        parts.append(buf)
    return parts


def json_query(args):
    raw = args.get("json")
    path = args.get("path")
    query = args.get("query")
    if raw is None and path is None:
        raise ValueError("json or path is required")
    if not query:
        raise ValueError("query is required")
    if raw is None:
        raw = open(path, "r", encoding="utf-8").read()
    data = json.loads(raw)
    parts = _parse_query(query)
    cur: Any = data
    for p in parts:
        cur = cur[p]
    return cur


def git_status(args):
    path = args.get("path", ".")
    p = subprocess.run(["git", "-C", path, "status", "-sb"], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "git status failed")
    return p.stdout


def git_diff(args):
    path = args.get("path", ".")
    p = subprocess.run(["git", "-C", path, "diff"], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "git diff failed")
    return p.stdout


registry.register(
    name="html_to_text",
    schema={
        "name": "html_to_text",
        "description": "Strip HTML tags to text.",
        "parameters": {"type": "object", "properties": {"html": {"type": "string"}}, "required": ["html"]},
    },
    handler=html_to_text,
)

registry.register(
    name="sha256",
    schema={
        "name": "sha256",
        "description": "SHA256 of text or file.",
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string"}, "path": {"type": "string"}},
        },
    },
    handler=sha256,
)

registry.register(
    name="json_query",
    schema={
        "name": "json_query",
        "description": "Query JSON with dot/bracket path (e.g., a.b[0].c).",
        "parameters": {
            "type": "object",
            "properties": {"json": {"type": "string"}, "path": {"type": "string"}, "query": {"type": "string"}},
            "required": ["query"],
        },
    },
    handler=json_query,
)

registry.register(
    name="git_status",
    schema={
        "name": "git_status",
        "description": "Git status -sb for a repo.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": []},
    },
    handler=git_status,
)

registry.register(
    name="git_diff",
    schema={
        "name": "git_diff",
        "description": "Git diff for a repo.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": []},
    },
    handler=git_diff,
)
