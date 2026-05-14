
import json
from typing import Dict, Callable, Any, List

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, schema: Dict[str, Any], handler: Callable[[Dict[str, Any]], Any]):
        self.tools[name] = {"schema": schema, "handler": handler}

    def get_tool_schemas(self, enabled: List[str]):
        return [self.tools[n]["schema"] for n in enabled if n in self.tools]

    def dispatch(self, name: str, args_json: str):
        if name not in self.tools:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            args = json.loads(args_json) if args_json else {}
        except Exception as e:
            return json.dumps({"error": f"Invalid tool args: {e}"})
        try:
            res = self.tools[name]["handler"](args)
            return json.dumps({"ok": True, "result": res})
        except Exception as e:
            return json.dumps({"ok": False, "error": str(e)})

registry = ToolRegistry()


def discover_builtin_tools():
    # importing registers tools
    from . import file_tools, terminal_tool, http_tool, misc_tools  # noqa: F401
