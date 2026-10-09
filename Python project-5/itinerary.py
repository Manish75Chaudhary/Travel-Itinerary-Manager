"""Basic itinerary operations and input validation."""

from datetime import datetime
import uuid


CATEGORIES = ["Travel", "Sightseeing", "Food", "Shopping", "Hotel", "Other"]
FIELDS = ["ID", "Date", "Destination", "Activity", "Time", "Category", "Notes"]


def validate_activity(date, destination, activity, time, category, notes=""):
    """Validate form values and return cleaned record data.

    A ValueError with a clear message is raised when a value is invalid.
    """
    date = date.strip()
    destination = destination.strip()
    activity = activity.strip()
    time = time.strip()
    category = category.strip()

    if not destination:
        raise ValueError("Destination cannot be empty.")
    if not activity:
        raise ValueError("Activity cannot be empty.")
    if category not in CATEGORIES:
        raise ValueError("Please select a valid category.")
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError as error:
        raise ValueError("Date must be in DD-MM-YYYY format.") from error
    try:
        datetime.strptime(time, "%H:%M")
    except ValueError as error:
        raise ValueError("Time must be in HH:MM (24-hour) format.") from error

    return {
        "Date": date,
        "Destination": destination,
        "Activity": activity,
        "Time": time,
        "Category": category,
        "Notes": notes.strip(),
    }


def create_activity(date, destination, activity, time, category, notes=""):
    """Create a validated record with a short unique ID."""
    record = validate_activity(date, destination, activity, time, category, notes)
    record["ID"] = uuid.uuid4().hex[:8].upper()
    return {field: record[field] for field in FIELDS}


def update_activity(records, record_id, date, destination, activity, time, category, notes=""):
    """Update one record in a list of dictionaries."""
    cleaned = validate_activity(date, destination, activity, time, category, notes)
    for record in records:
        if str(record["ID"]) == str(record_id):
            record.update(cleaned)
            return True
    return False


def delete_activity(records, record_id):
    """Delete a record by ID and return True if it was found."""
    for index, record in enumerate(records):
        if str(record["ID"]) == str(record_id):
            records.pop(index)
            return True
    return False


def search_activities(records, keyword):
    """Search destination, activity, and category text without case sensitivity."""
    keyword = keyword.strip().lower()
    if not keyword:
        return records[:]
    searchable = ("Destination", "Activity", "Category")
    return [record for record in records if any(keyword in str(record[field]).lower() for field in searchable)]


def filter_activities(records, date="", destination="", category=""):
    """Filter records using any combination of date, destination, and category."""
    return [
        record for record in records
        if (not date.strip() or record["Date"] == date.strip())
        and (not destination.strip() or destination.strip().lower() in record["Destination"].lower())
        and (not category.strip() or record["Category"] == category.strip())
    ]


def sort_activities(records):
    """Return records ordered by date and time without changing the saved list."""
    return sorted(
        records,
        key=lambda record: datetime.strptime(
            f"{record['Date']} {record['Time']}", "%d-%m-%Y %H:%M"
        ),
    )
