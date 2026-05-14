
import os
import re
import fnmatch

from tools.registry import registry


def read_file(args):
    path = args.get("path")
    if not path:
        raise ValueError("path is required")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write_file(args):
    path = args.get("path")
    content = args.get("content", "")
    if not path:
        raise ValueError("path is required")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"path": path, "bytes": len(content)}


def search_files(args):
    pattern = args.get("pattern")
    target = args.get("target", "content")
    root = args.get("path", ".")
    limit = int(args.get("limit", 50))

    results = []
    if target == "files":
        for dirpath, _, filenames in os.walk(root):
            for name in filenames:
                if fnmatch.fnmatch(name, pattern):
                    results.append(os.path.join(dirpath, name))
                    if len(results) >= limit:
                        return results
        return results

    regex = re.compile(pattern)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            p = os.path.join(dirpath, name)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if regex.search(line):
                            results.append({"path": p, "line": i, "text": line.strip()})
                            if len(results) >= limit:
                                return results
            except Exception:
                continue
    return results


registry.register(
    name="read_file",
    schema={
        "name": "read_file",
        "description": "Read a UTF-8 text file.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    },
    handler=read_file,
)

registry.register(
    name="write_file",
    schema={
        "name": "write_file",
        "description": "Write a UTF-8 text file.",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"],
        },
    },
    handler=write_file,
)

registry.register(
    name="search_files",
    schema={
        "name": "search_files",
        "description": "Search files by regex (content) or glob (files).",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "target": {"type": "string", "enum": ["content", "files"]},
                "path": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["pattern"],
        },
    },
    handler=search_files,
)
