
from pico_hermes.config import load_config

def test_missing_config(tmp_path):
    cfg = load_config(tmp_path / "missing.toml")
    assert cfg == {}
