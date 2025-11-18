# Author: Tauqeer Khan
# Date: 17-11-2025
# Purpose: This program is a menu-driven Calendar Event Tracker
# lets the user add, view, filter, delete, and view calendar events by date.
# Search events by keyword in the title or note.
# View events in a simple text-based weekly view; and export all events to a
# CSV file for use in Excel or Google sheets. Events are presented as obj, saved via a 
# plugged storage backend (using abstract classes)
# uses decorator (wrappers) to auto-save changes to disk.

from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import functools
import json
import csv
from typing import List, Iterable

LINE = "_" * 60
MENU_MIN = 1
MENU_MAX = 11

# Decorators method
def autosave(method):
    """Decorator for methods that modify the events list.
        After the wrapped method runs, the current calendar is saved
        via self._save()."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        # Only saves if the method didn't signal false
        if result is not False:
            self.save()
        return result
    return wrapper

# Data model
class Event:
    """Represents a single calendar event."""
    def __init__(self, date:str, title: str, location: str = "", note: str = ""):
        self.date = date # YYYY-MM-DD 
        self.title = title
        self.location = location
        self.note = note
        
    def to_dict(self) -> dict:
        """Convert event to a dict so it can be saved as JSON."""
        return{
            "date": self.date,
            "title": self.title,
            "location": self.location,
            "note": self.note }
    
    @staticmethod
    def from_dict(data: dict) -> "Event":
        """Create an Event object from a dict (loaded from JSON)."""
        return Event(
                date = data.get("date", ""),
                title = data.get("title", ""),
                location = data.get("location", ""),
                note = data.get("note", ""),
            )

# Abstract Storage
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
    
# Json file storage
class JSON_File_Storage(Event_Storage):
    """Storage implementation that saves events to a JSON file."""
    
    def __init__(self, filename: str = "events.json"):
        # File path where events will be loaded from / saved to
        self.filename = filename
    
    def load(self) -> List[Event]:
        """Load events from a JSON file and return them as Event obj"""
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
        with open(self.filename, "w", encoding = "utf-8") as f:
            json.dump(data, f, indent=4)
    
# Main App class
class CalendarEventTracker:
    """Main application class for managing events."""
    
    def __init__(self, storage: Event_Storage):
        # Insert storage backend (inject dependency)
        self._storage = storage
        self.events: List[Event] = self._storage.load()
    
    # internal method helper used by decorator
    def Save(self) -> None:
        self._storage.save(self.events)
    
    # Date Validation
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Return True if a given year is a leap year."""
        return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
    
    @classmethod
    def days_in_month(cls, year: int, month: int) -> int:
        """Return the number of days in a given month of a given year."""
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        if month == 2:
            return 29 if cls.is_leap_year(year) else 28
        if month in (4, 6, 9, 11):
            return 30
        return 0
    
    @classmethod
    def is_valid_date(cls, date_text: str) -> bool:
        """Validate date in YYYY-MM-DD format."""
        if len(date_text) != 10:
            return False
        if date_text[4] != "-" or date_text[7] != "-":
            return False
        
        year_str, month_str, day_str = date_text[:4], date_text[5:7], date_text[8:]
        
        # All three must be numeric
        
        if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
            return False
        
        year = int(year_str)
        month = int(month_str)
        day = int(day_str)
        
        # Basic checks
        if year < 1 or month < 1 or month > 12:
            return False
        
        # Check day against max days in that month or year.
        max_day = cls.days_in_month(year, month)
        if day < 1 or day > max_day:
            return False
        
        return True
    
    # UI and Menu
    def run(self) -> None:
        """Main loop"""
        while True:
            self.menu_banner()
            choice = self.read_menu_choice()
            if choice == 0:
                continue
            
            if choice == 1:
                self.add_event()
            elif choice == 2:
                self.list_all_events()
            elif choice == 3:
                self.list_events_on_date()
            elif choice == 4:
                self.list_events_in_range()
            elif choice == 5:
                self.delete_event()
            elif choice == 6:
                today = datetime.today().strftime("%Y-%m-%d")
                print(f"\nToday's date is: {today}\n")
            elif choice == 7:
                self.edit_event()
            elif choice == 8:
                self.search_events()
            elif choice == 9:
                self.export_to_csv()
            elif choice == 10:
                self.weekly_view()
            elif choice == 11:
                print("Goodbye!")
                break
    @staticmethod
    def menu_banner() -> None:
        """Print the main menu."""
        print(LINE)
        print("Calendar Event Tracker".center(60, "-"))
        print(LINE)
        print("1. Add event")
        print("2. List all events")
        print("3. List events on a certain date")
        print("4. List events in a date range")
        print("5. Delete an event")
        print("6. Show today's date")
        print("7. Edit an event (title/location/note)")
        print("8. Search events by keyword")
        print("9. Export all events to CSV")
        print("10. Weekly view (7- day range)")
        print(LINE)
    
    @staticmethod
    def read_menu_choice() -> int:
        choice = input(f"Choose ({MENU_MIN}-{MENU_MAX}): ").strip()
        if not choice.isdigit():
            print("Invalid choice: not a number.\n")
            return 0
        
        num = int(choice)
        if num < MENU_MIN or num > MENU_MAX:
            print("Invalid choice: out of range.\n")
            return 0
        return num
    
    # Presentation to make the program look good.
    
    @staticmethod
    def print_events(view: List[Event]) -> None:
        if len(view) == 0:
            print("\nNo events.\n")
            return
        
        print("\nIdx | Date       | Title                   | Location           | Note")
        print("-" * 100)
        
        for index, ev in enumerate(view):
            date = ev.date or ""
            title = (ev.title or "")[:23]
            location = (ev.location or "")[:18]
            note = (ev.note or "")[:40]

            print(
                f"{index:>3} | "
                f"{date} | "
                f"{title:<23} | "
                f"{location:<18} | "
                f"{note:<40}"
            )
    
    @autosave
    def add_event(self) -> None:
        print("\n --- Add Event ---")
        date = input("Date (YYYY-MM-DD): ").strip()
        if not self.is_valid_date(date):
            print("Invalid date. Use YYYY-MM-DD format.\n")
            return False
        
        title = input("Title: ").strip()
        if title == "":
            print("Title cannot be empty.\n")
            return False
        
        location = input("Location (opt): ").strip()
        note = input("Note (opt): ").strip()
        
        self.events.append(Event(date, title, location, note))
        print("Event added.\n")
        
    def list_all_events(self) -> List[Event]:
        sorted_display = sorted(self.events, key=lambda ev: ev.date)
        self.print_events(sorted_display)
        return sorted_display
    
    def list_events_on_date(self) -> List[Event]:
        date = input("\nShow events on (YYYY-MM-DD): ").strip()
        if not self.is_valid_date(date):
            print("Invalid date. Please enter a valid date.\n")
            return []
        
        display = sorted(
            [ev for ev in self.events if ev.date == date],
            key=lambda ev: ev.date,
        )
        self.print_events(display)
        return display
    
    def list_events_in_range(self) -> List[Event]:
        start_date = input("\nStart date (YYYY-MM-DD): ").strip()
        if not self.is_valid_date(start_date):
            print("Invalid start date.\n")
            return []
        
        end_date = input("End date (YYYY-MM-DD): ").strip()
        if not self.is_valid_date(end_date):
            print("Invalid end date.\n")
            return []
        
        if start_date > end_date:
            print("Start date must be <= end date.\n")
            return []
        
        display = sorted(
            [ev for ev in self.events if start_date <= ev.date <= end_date],
            key=lambda ev: ev.date,
        )
        self.print_events(display)
        return display
    
    @autosave
    def delete_event(self) -> None:
        """Delete a single event selected by index from a sorted view."""
        if len(self.events) == 0:
            print("\nNo events available to delete.\n")
            return False
        
        sorted_display = sorted(self.events, key=lambda ev: ev.date)
        self.print_events(sorted_display)
        
        idx_text = input("Enter the index to delete: ").strip()
        if not idx_text.isdigit():
            print("Invalid index (must be a number).\n")
            return False
        
        idx = int(idx_text)
        if idx < 0 or idx >= len(sorted_display):
            print("Index out of range.\n")
            return False
        
        target = sorted_display[idx]
        
        # Rebuild event list without the chosen target (first match)
        removed = False
        new_list: List[Event] = []
        for ev in self.events:
            if (not removed) and ev is target:
                removed = True
                continue
            new_list.append(ev)
            
        self.events = new_list
        print("Event delete.\n")
    
    # Extra features
    
    @ autosave
    def edit_event(self) -> None:
        """Edit an existing event's title, location, or note."""
        if len(self.events) == 0:
            print("\nNo events to edit.\n")
            return False
        
        sorted_display = sorted(self.events, key=lambda ev: ev.date)
        self.print_events(sorted_display)
        
        idx_text = input("Enter the index of the event to edit: ").strip()
        if not idx_text.isdigit():
            return False
        
        idx = int(idx_text)
        if idx < 0 or idx >= len(sorted_display):
            print("Index out of range.\n")
            return False
        
        target = sorted_display[idx]
        
        print("\nLeave a field blank to keep the current value.")
        new_title = input(f"New Title [{target.title}]: ").strip()
        new_location = input(f"New location [{target.location}]: ").strip()
        new_note = input(f"New note [{target.note}]: ").strip()
        
        if new_title != "":
            target.title = new_title
        if new_location != "":
            target.location = new_location
        if new_note != "":
            target.note = new_note
            
        print("Event update.\n")
                
    def search_events(self) -> List[Event]:
        """Search events by keyword in title or note"""
        keyword = input("\nEnter keyword to search in title/note: ").strip()
        if keyword == "":
            print("Keyword cannot be empty.\n")
            return []
        
        needle = keyword.lower()
        matches = [
            ev for ev in self.events
            if needle in ev.title.lower() or needle in ev.note.lower()
        ]
        
        matches_sorted = sorted(matches, key=lambda ev: ev.date)
        self.print_events(matches_sorted)
        return matches_sorted
    
    def export_to_csv(self, csv_filename: str = "events_export.csv") -> None:
        """Exports all events to a csv file"""
        if len(self.events) == 0:
            print("\nNo events in calendar to export.\n")
            return
        
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Title", "Location", "note"])
            for ev in sorted(self.events, key=lambda e: e.date):
                writer.writerow([ev.date, ev.title, ev.location, ev.note])
        
        print(f"\nEvents exported to '{csv_filename}'.\n")
        
    def weekly_view(self) -> None:
        """Show a weekly view.
           User provides a week start date (YYYY-MM-DD).
           Display events for that day and the next 6 days."""
        start_date_str = input("\nEnter week start date (YYYY-MM-DD): ").strip()
        
        if not self.is_valid_date(start_date_str):
            print("Invalid date.\n")
            return

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format.\n")
            return
        
        end_date = start_date + timedelta(days=6)
        print(f"\nWeekly view from {start_date} to {end_date}:\n")
        
        # Build mapping date -> list of events on that day
        date_to_events = {}
        for ev in self.events:
            try:
                ev_date = datetime.strptime(ev.date, "%Y-%m-%d").date()
            except ValueError:
                # Skip wrong dates
                continue
            if start_date <= ev_date <= end_date:
                date_to_events.setdefault(ev_date, []).append(ev)
        # Iterate each day in the week and print events
        for i in range(7):
            current_day = start_date + timedelta(days = i)
            day_name = current_day.strftime("%A")
            print(LINE)
            print(f"{current_day} ({day_name})")
            print(LINE)
            
            day_events = date_to_events.get(current_day, [])
            if not day_events:
                print("No events available.")
            else:
                for ev in sorted(day_events, key = lambda x: x.title.lower()):
                    print(f" - {ev.title} @ {ev.location or 'N/A'} ")
                    if ev.note:
                        print(f"    Note: {ev.note}")
            print("")

if __name__ == "__main__":
    storage = JSON_File_Storage("events.json")
    app = CalendarEventTracker(storage)
    app.run()