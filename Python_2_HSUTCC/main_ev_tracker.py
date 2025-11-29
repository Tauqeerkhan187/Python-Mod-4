# Author: Tauqeer Khan
# Date: 17-11-2025
# Purpose: This program is a menu-driven Calendar Event Tracker
# lets the user add, view, filter, delete, and view calendar events by date.
# Search events by keyword in the title or note.
# View events in a simple text-based weekly view; and export all events to a
# CSV file for use in Excel or Google sheets. Events are presented as obj, saved via a 
# plugged storage backend (using abstract classes)
# uses decorator (wrappers) to auto-save changes to disk.
from storage import JSON_File_Storage
from tracker import CalendarEventTracker

if __name__ == "__main__":
    storage = JSON_File_Storage("events.json")
    app = CalendarEventTracker(storage)
    app.run()