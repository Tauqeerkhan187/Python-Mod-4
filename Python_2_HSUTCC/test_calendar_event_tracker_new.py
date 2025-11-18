import os
import io
import json
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout

from calendar_event_tracker import (
    Event,
    JSON_File_Storage,
    Event_Storage,
    CalendarEventTracker,
)


class FakeStorage(Event_Storage):
    """
    In-memory storage backend for testing.
    Keeps track of how many times save() is called.
    """

    def __init__(self, initial_events=None):
        self._events = list(initial_events) if initial_events else []
        self.save_call_count = 0

    def load(self):
        # Return a copy so tests don't mutate internal list by accident
        return list(self._events)

    def save(self, events):
        self.save_call_count += 1
        self._events = list(events)


class TestEventModel(unittest.TestCase):
    def test_to_dict_and_from_dict_roundtrip(self):
        ev = Event(
            date="2025-11-17",
            title="Meeting",
            location="Office",
            note="Bring laptop",
        )
        data = ev.to_dict()
        self.assertEqual(
            data,
            {
                "date": "2025-11-17",
                "title": "Meeting",
                "location": "Office",
                "note": "Bring laptop",
            },
        )

        ev2 = Event.from_dict(data)
        self.assertEqual(ev2.date, ev.date)
        self.assertEqual(ev2.title, ev.title)
        self.assertEqual(ev2.location, ev.location)
        self.assertEqual(ev2.note, ev.note)


class TestJSONFileStorage(unittest.TestCase):
    def test_save_and_load(self):
        # Use a temporary file so we don't touch real events.json
        fd, path = tempfile.mkstemp()
        os.close(fd)

        try:
            storage = JSON_File_Storage(path)
            events = [
                Event("2025-11-17", "Test 1", "Home", "Note 1"),
                Event("2025-11-18", "Test 2", "Work", "Note 2"),
            ]

            storage.save(events)
            loaded = storage.load()

            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0].title, "Test 1")
            self.assertEqual(loaded[1].location, "Work")
        finally:
            os.remove(path)

    def test_load_corrupt_file_returns_empty_list(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("{this is not valid json")

            storage = JSON_File_Storage(path)
            # Should not raise; should return []
            loaded = storage.load()
            self.assertEqual(loaded, [])
        finally:
            os.remove(path)


class TestDateValidation(unittest.TestCase):
    def test_is_leap_year(self):
        self.assertTrue(CalendarEventTracker.is_leap_year(2000))
        self.assertFalse(CalendarEventTracker.is_leap_year(1900))
        self.assertTrue(CalendarEventTracker.is_leap_year(2024))
        self.assertFalse(CalendarEventTracker.is_leap_year(2023))

    def test_days_in_month(self):
        self.assertEqual(CalendarEventTracker.days_in_month(2024, 2), 29)
        self.assertEqual(CalendarEventTracker.days_in_month(2023, 2), 28)
        self.assertEqual(CalendarEventTracker.days_in_month(2025, 1), 31)
        self.assertEqual(CalendarEventTracker.days_in_month(2025, 4), 30)

    def test_is_valid_date(self):
        valid_dates = [
            "2024-02-29",  # leap-year Feb 29
            "2025-01-01",
            "0001-01-01",
        ]
        invalid_dates = [
            "2023-02-29",  # non-leap Feb 29
            "2025-13-01",  # month 13
            "2025-00-10",  # month 0
            "2025-11-00",  # day 0
            "2025-11-32",  # day 32
            "abcd-ef-gh",  # nonsense
            "2025/11/17",  # wrong separators
            "2025-1-1",    # wrong length
        ]

        for d in valid_dates:
            with self.subTest(date=d):
                self.assertTrue(CalendarEventTracker.is_valid_date(d))

        for d in invalid_dates:
            with self.subTest(date=d):
                self.assertFalse(CalendarEventTracker.is_valid_date(d))


class TestCalendarEventTrackerCore(unittest.TestCase):
    def setUp(self):
        self.storage = FakeStorage()
        self.app = CalendarEventTracker(self.storage)

    def test_add_event_success_triggers_save(self):
        with patch("builtins.input", side_effect=[
            "2025-11-17",  # date
            "My Event",    # title
            "Home",        # location
            "Some note",   # note
        ]):
            self.app.add_event()

        self.assertEqual(len(self.app.events), 1)
        self.assertEqual(self.app.events[0].title, "My Event")
        self.assertEqual(self.storage.save_call_count, 1)

    def test_add_event_invalid_date_does_not_save(self):
        with patch("builtins.input", side_effect=[
            "2025-02-30",  # invalid date
            "My Event",
            "Home",
            "Note",
        ]):
            result = self.app.add_event()

        self.assertIs(result, False)
        self.assertEqual(len(self.app.events), 0)
        self.assertEqual(self.storage.save_call_count, 0)

    def test_add_event_empty_title_does_not_save(self):
        with patch("builtins.input", side_effect=[
            "2025-11-17",  # valid date
            "",            # empty title
            "Home",
            "Note",
        ]):
            result = self.app.add_event()

        self.assertIs(result, False)
        self.assertEqual(len(self.app.events), 0)
        self.assertEqual(self.storage.save_call_count, 0)

    def test_list_all_events_sorted(self):
        self.app.events = [
            Event("2025-11-20", "C"),
            Event("2025-11-18", "A"),
            Event("2025-11-19", "B"),
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = self.app.list_all_events()

        self.assertEqual([ev.title for ev in result], ["A", "B", "C"])
        output = buf.getvalue()
        # Rough sanity check that header is printed
        self.assertIn("Idx | Date", output)

    def test_delete_event_by_index(self):
        e1 = Event("2025-11-18", "Event 1")
        e2 = Event("2025-11-19", "Event 2")
        self.app.events = [e1, e2]

        # Sorted by date: [e1, e2], so index 0 deletes e1
        with patch("builtins.input", return_value="0"):
            self.app.delete_event()

        self.assertEqual(len(self.app.events), 1)
        self.assertEqual(self.app.events[0].title, "Event 2")
        self.assertEqual(self.storage.save_call_count, 1)

    def test_delete_event_invalid_index_does_not_save(self):
        e1 = Event("2025-11-18", "Event 1")
        self.app.events = [e1]

        with patch("builtins.input", return_value="5"):
            result = self.app.delete_event()

        self.assertIs(result, False)
        self.assertEqual(len(self.app.events), 1)
        self.assertEqual(self.storage.save_call_count, 0)

    def test_edit_event_updates_fields(self):
        e1 = Event("2025-11-18", "Old Title", "Old Loc", "Old Note")
        self.app.events = [e1]

        # Sorted list has e1 at index 0.
        # New location left blank -> should remain "Old Loc".
        with patch("builtins.input", side_effect=[
            "0",             # index
            "New Title",     # new title
            "",              # new location (blank => keep old)
            "New Note",      # new note
        ]):
            self.app.edit_event()

        self.assertEqual(self.app.events[0].title, "New Title")
        self.assertEqual(self.app.events[0].location, "Old Loc")
        self.assertEqual(self.app.events[0].note, "New Note")
        self.assertEqual(self.storage.save_call_count, 1)

    def test_search_events_by_keyword(self):
        self.app.events = [
            Event("2025-11-18", "Project Meeting", "Office", "Discuss timeline"),
            Event("2025-11-19", "Gym", "Club", "Leg day"),
            Event("2025-11-20", "Family Meeting", "Home", "Dinner"),
        ]

        with patch("builtins.input", return_value="meeting"):
            buf = io.StringIO()
            with redirect_stdout(buf):
                results = self.app.search_events()

        titles = [ev.title for ev in results]
        self.assertEqual(set(titles), {"Project Meeting", "Family Meeting"})
        self.assertIn("Project Meeting", buf.getvalue())


class TestExportAndWeeklyView(unittest.TestCase):
    def setUp(self):
        self.storage = FakeStorage()
        self.app = CalendarEventTracker(self.storage)

    def test_export_to_csv_creates_file(self):
        self.app.events = [
            Event("2025-11-18", "Event 1", "Place 1", "Note 1"),
            Event("2025-11-19", "Event 2", "Place 2", "Note 2"),
        ]

        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            # Capture stdout just to avoid cluttering test output
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.app.export_to_csv(path)

            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Event 1", content)
            self.assertIn("Event 2", content)
        finally:
            os.remove(path)

    def test_weekly_view_does_not_crash(self):
        # Two events inside the week, one outside
        self.app.events = [
            Event("2025-11-18", "In Week 1", "Loc", ""),
            Event("2025-11-20", "In Week 2", "Loc", ""),
            Event("2025-12-31", "Outside", "Loc", ""),
        ]

        with patch("builtins.input", return_value="2025-11-17"):
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.app.weekly_view()

        out = buf.getvalue()
        self.assertIn("Weekly view from 2025-11-17", out)
        self.assertIn("In Week 1", out)
        self.assertIn("In Week 2", out)
        self.assertNotIn("Outside", out)


if __name__ == "__main__":
    unittest.main()
