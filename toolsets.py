
# Minimal toolsets for pico-hermes

TOOLSETS = {
    "basic": ["read_file", "write_file", "search_files"],
    "terminal": ["read_file", "write_file", "search_files", "terminal"],
}


def resolve_toolset(name: str):
    return TOOLSETS.get(name, TOOLSETS["basic"])
