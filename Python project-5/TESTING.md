# Testing Checklist

Use this checklist while demonstrating the project.

| Test | Expected result |
|---|---|
| Add valid activity | Record appears in the table and remains after restart. |
| Add invalid activity | Clear validation message is shown. |
| Update activity | Selected record changes in table and CSV. |
| Delete activity | Confirmation is requested and record is removed. |
| Search activity | Matching destination, activity, or category is displayed. |
| Filter activity | Matching date, destination, and/or category is displayed. |
| Load saved data | Existing CSV records appear on startup. |
| Save data | Add, update, and delete changes are written to CSV. |
| Generate trip summary | Totals, dates, categories, and destinations are shown. |
| Generate both charts | Category and destination bar charts open. |
| Invalid date | A date other than DD-MM-YYYY is rejected. |
| Invalid time | A time other than HH:MM is rejected. |
| Empty required fields | Empty destination/activity/category is rejected. |

Automated core-function tests are included in `test_itinerary.py` and can be run with `python -m unittest test_itinerary.py`.
