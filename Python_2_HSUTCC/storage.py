# storage.py
# Class which implements Storage and JSON
from abc import ABC, abstractmethod
from typing import List, Iterable
import json

from model import Event   # same folder

class Event_Storage(ABC):
    """Abstract base class for event storage backends."""

    @abstractmethod
    def load(self) -> List[Event]:
        """Load events from storage and return a list of Event objects."""
        pass

    @abstractmethod
    def save(self, events: Iterable[Event]) -> None:
        """Save the given events to storage."""
        pass


class JSON_File_Storage(Event_Storage):
    """Storage implementation that saves events to a JSON file."""

    def __init__(self, filename: str = "events.json"):
        self.filename = filename

    def load(self) -> List[Event]:
        """Load events from a JSON file and return them as Event objects."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Event.from_dict(ev) for ev in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Warning: events file is corrupted. Starting with empty list.")
            return []

    def save(self, events: Iterable[Event]) -> None:
        """Serialize Event objects to JSON and write them to file."""
        data = [ev.to_dict() for ev in events]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
