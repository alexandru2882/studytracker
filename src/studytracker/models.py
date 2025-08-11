from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class StudySession:
    topic: str
    minutes: int
    date: str  # YYYY-MM-DD

    def __post_init__(self) -> None:
        if not isinstance(self.topic, str) or not self.topic.strip():
            raise ValueError("topic must be a non-empty string")
        if not isinstance(self.minutes, int) or self.minutes <= 0:
            raise ValueError("minutes must be a positive integer")
        # Very light date format check
        parts = self.date.split("-")
        if len(parts) != 3:
            raise ValueError("date must be YYYY-MM-DD")

    def to_dict(self) -> Dict[str, Any]:
        return {"topic": self.topic, "minutes": self.minutes, "date": self.date}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StudySession":
        return StudySession(topic=str(d["topic"]), minutes=int(d["minutes"]), date=str(d["date"]))
