from datetime import date
from typing import List, Optional

from .models import StudySession
from .storage import load_sessions, save_sessions


def add_session(topic: str, minutes: int, when: Optional[str] = None) -> StudySession:
    if when is None:
        when = date.today().isoformat()
    session = StudySession(topic=topic, minutes=int(minutes), date=when)
    items = load_sessions()
    items.append(session)
    save_sessions(items)
    return session


def list_sessions() -> List[StudySession]:
    return load_sessions()


def total_minutes(topic: Optional[str] = None) -> int:
    items = load_sessions()
    if topic:
        items = [x for x in items if x.topic.lower() == topic.lower()]
    return sum(x.minutes for x in items)
