
from pico_hermes.toolsets import resolve_toolset

def test_toolsets():
    assert "read_file" in resolve_toolset("basic")
    assert "terminal" in resolve_toolset("terminal")
    assert "http_get" in resolve_toolset("net")
