import json
import os
from pathlib import Path
from typing import List

from .models import StudySession


def _base_dir() -> Path:
    # Use env var for tests; default to user home
    env = os.getenv("STUDYTRACKER_HOME")
    p = Path(env).expanduser() if env else (Path.home() / ".studytracker")
    p.mkdir(parents=True, exist_ok=True)
    return p


def data_path() -> Path:
    return _base_dir() / "sessions.json"


def load_sessions() -> List[StudySession]:
    p = data_path()
    if not p.exists():
        return []
    raw = p.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    data = json.loads(raw)
    return [StudySession.from_dict(x) for x in data]


def save_sessions(items: List[StudySession]) -> None:
    p = data_path()
    p.write_text(json.dumps([s.to_dict() for s in items], indent=2), encoding="utf-8")
