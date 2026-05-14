
from pico_hermes.tools.registry import registry, discover_builtin_tools

def test_registry_tools_present():
    discover_builtin_tools()
    assert "read_file" in registry.tools
    assert "write_file" in registry.tools
    assert "search_files" in registry.tools
    assert "list_dir" in registry.tools
