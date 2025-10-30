# Calendar Event Tracker
# Author: Tauqeer Khan
# Date: 15-06-2024
# Purpose: creates a simple calendar event tracker which allows
# Users to add, view, and delete events stored in memory
# Each events contains a date, title, location, and note.
# The program uses the datetime lib to validate dates and display
# the current date.

from datetime import datetime

# Global list which stores events, (date, title, location, note)
events = [] 

def main():
    while True:
        print("-" * 60)
        print("Calendar Event Tracker ".center(60, "-"))
        print("-" * 60)
        print("1. Add event")
        print("2. List all events")
        print("3. List events on a certain date")
        print("4. List events in a date range")
        print("5. Delete an event")
        print("6. Show today's date")
        print("7. Exit menu")
        print("-" * 60)

        choice_selected = input("Choose (1-7): ").strip()

        if choice_selected == "1":
            add_event()
        elif choice_selected == "2":
            list_all_events()
        elif choice_selected == "3":
            list_events_on_date()
        elif choice_selected == "4":
            list_events_in_range()
        elif choice_selected == "5":
            delete_event()
        elif choice_selected == "6":
            today = datetime.today().strdtime("%d-%m-%Y")
            print(f"\nToday's date is: {today}\n")
        elif choice_selected == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.\n")

# Validation for leap year

def is_leap_year(year: int) -> bool:
    
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

# Returns the number of days in given month for given year

def days_in_months(year: int, month: int) -> int

    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    # Feb depends on leap year
    if month == 2:
        return 29 if is_leap_year(year) else 28
    if month in(4,6,9,11):
        return 30

    return 0 
# is_valid_date checks if the date format is valid (DD-MM-YYYY)

def is_valid_date(date_text: str) -> bool:
    #expects exact format DD-MM-YYYY with digits only
    if len(date_text) != 10:
        return False
    if date_text[4] != "-" or date_text[7] != "-":
        return False

    # - split into components as string 
    year, month, day = date_text[4], date_text[5:7], date_text[8:]

    # All components must be digits only
    if not(year.isdigit() and month.isdigit() and day.isdigit()):
        return false

    # Convert to integer to check range
    year = int(year)
    month = int(month)
    day = int(day)

    if year < 1 or month < 1 or month < 12:
        return False

    # Day must be within the max days for that month/year.
    max_day = days_in_month(year, month)
    if max_day == 0 or day < 1 or day > max_day:
        return False

    return True

# menu_banner function to show the menu after executing a option
def menu_banner() -> None:
    print(



