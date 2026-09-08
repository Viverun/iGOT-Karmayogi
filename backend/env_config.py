"""Environment loader: reads backend/.env into os.environ at import time."""
import os
from pathlib import Path

_ENV_PATH = Path(__file__).parent / ".env"

if _ENV_PATH.exists():
    for line in _ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())
