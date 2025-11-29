# models.py
# event class which is the data model
from typing import Dict

class Event:
    """Represents a single calendar event."""
    def __init__(self, date: str, title: str, location: str = "", note: str = ""):
        self.date = date   # YYYY-MM-DD
        self.title = title
        self.location = location
        self.note = note

    def to_dict(self) -> Dict[str, str]:
        """Convert event to a dict so it can be saved as JSON."""
        return {
            "date": self.date,
            "title": self.title,
            "location": self.location,
            "note": self.note,
        }

    @staticmethod
    def from_dict(data: dict) -> "Event":
        """Create an Event object from a dict (loaded from JSON)."""
        return Event(
            date=data.get("date", ""),
            title=data.get("title", ""),
            location=data.get("location", ""),
            note=data.get("note", ""),
        )
