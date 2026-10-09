"""CSV storage functions for the Travel Itinerary Manager."""

from pathlib import Path
import csv

from itinerary import FIELDS


def ensure_csv(file_path):
    """Create the CSV file and its parent directory when needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=FIELDS).writeheader()


def load_activities(file_path):
    """Load records from CSV. Raises a readable ValueError for corrupt CSV files."""
    ensure_csv(file_path)
    try:
        with Path(file_path).open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != FIELDS:
                raise ValueError("CSV columns are missing or invalid. Restore the required header.")
            return [{field: row.get(field, "") for field in FIELDS} for row in reader]
    except OSError as error:
        raise OSError(f"Could not open itinerary file: {error}") from error


def save_activities(file_path, records):
    """Save all records to the CSV file."""
    ensure_csv(file_path)
    try:
        with Path(file_path).open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(records)
    except OSError as error:
        raise OSError(f"Could not save itinerary file: {error}") from error
