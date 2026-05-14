
# Minimal toolsets for pico-hermes (pico-claw philosophy: tiny + essential)

TOOLSETS = {
    "basic": ["read_file", "write_file", "search_files", "list_dir", "json_query", "sha256"],
    "net": ["read_file", "write_file", "search_files", "list_dir", "http_get", "http_post_json", "rss_fetch", "html_to_text", "json_query", "sha256"],
    "terminal": ["read_file", "write_file", "search_files", "list_dir", "terminal", "json_query", "sha256"],
}


def resolve_toolset(name: str):
    if name == "none":
        return []
    return TOOLSETS.get(name, TOOLSETS["basic"])
