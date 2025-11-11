# Calendar Event Tracker — Automated Test Report

## Summary

- **Total Tests:** 31
- **Passed:** 31
- **Failed:** 0
- **Pass Rate %:** 100.0

## Detailed Results

- ✅ **Import module** — Module imported successfully.
- ✅ **is_leap_year(2000)**
- ✅ **is_leap_year(1900)**
- ✅ **is_leap_year(2024)**
- ✅ **is_leap_year(2023)**
- ✅ **days_in_months Feb leap**
- ✅ **days_in_months Feb nonleap**
- ✅ **days_in_months April**
- ✅ **days_in_months Jan**
- ✅ **is_valid_date valid pack** — Checked: ['2024-02-29', '2023-12-31', '0001-01-01', '1999-01-05']
- ✅ **is_valid_date invalid pack** — Checked: ['2024-02-30', '2024-13-01', '2024-00-10', '2024-1-01', '24-01-01', '2024/01/01', 'abcd-ef-gh', '2024-11-31']
- ✅ **print_events empty message**
- ✅ **add_event invalid date**
- ✅ **add_event empty title**
- ✅ **add_event success**
- ✅ **list_all_events sorted**
- ✅ **list_events_on_date count**
- ✅ **list_events_on_date invalid**
- ✅ **list_events_in_range inclusive**
- ✅ **list_events_in_range bad start**
- ✅ **list_events_in_range bad end**
- ✅ **list_events_in_range start> end**
- ✅ **delete_event on empty**
- ✅ **delete_event non-digit**
- ✅ **delete_event out of range**
- ✅ **delete_event success**
- ✅ **read_menu_choice non-digit**
- ✅ **read_menu_choice out of range low**
- ✅ **read_menu_choice out of range high**
- ✅ **read_menu_choice valid 7**
- ✅ **print today's date format**

## Notes & Recommendations

- Input validation is robust for dates and menu choices, including leap years.
- Consider persisting `events` to a file (e.g., JSON) so data survives program exit.
- `print_events` prints a leading space in 'No. of events.' message; consider cleaning message text for consistency.
- You might add an 'Edit event' feature and unique IDs to events to handle duplicates more explicitly.
- A lambda function is just a small, unnamed function.
- lambda ev: ev[0] used in the code is similar to using def sort_key(ev): return ev[0]
