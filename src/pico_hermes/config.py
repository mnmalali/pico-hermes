
import tomllib
from pathlib import Path

def load_config(path: str):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return tomllib.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
