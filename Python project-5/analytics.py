"""Pandas-based summaries, comparisons, and Matplotlib reports."""

import pandas as pd
import matplotlib.pyplot as plt

from itinerary import FIELDS


def dataframe_from_records(records):
    """Create a DataFrame with known columns, including for an empty itinerary."""
    return pd.DataFrame(records, columns=FIELDS)


def trip_summary(records):
    """Calculate values displayed in the trip summary window using Pandas."""
    frame = dataframe_from_records(records)
    if frame.empty:
        return None

    dates = pd.to_datetime(frame["Date"], format="%d-%m-%Y", errors="coerce")
    valid_dates = dates.dropna()
    start_date = valid_dates.min()
    end_date = valid_dates.max()
    duration = (end_date - start_date).days + 1 if not valid_dates.empty else 0
    categories = frame["Category"].value_counts()
    destinations = frame["Destination"].value_counts()
    return {
        "total_activities": len(frame),
        "total_destinations": frame["Destination"].nunique(),
        "start_date": start_date.strftime("%d-%m-%Y") if pd.notna(start_date) else "Not available",
        "end_date": end_date.strftime("%d-%m-%Y") if pd.notna(end_date) else "Not available",
        "duration": duration,
        "most_common_category": categories.index[0],
        "by_category": categories.to_dict(),
        "by_destination": destinations.to_dict(),
        "by_date": frame.groupby("Date").size().to_dict(),
    }


def compare_categories(records, first_category, second_category):
    """Return a simple planned-activity comparison between two categories."""
    counts = dataframe_from_records(records)["Category"].value_counts()
    return counts.get(first_category, 0), counts.get(second_category, 0)


def show_category_report(records):
    """Display a bar chart of activity counts by category."""
    summary = trip_summary(records)
    if not summary:
        raise ValueError("Add at least one activity before generating a report.")
    values = pd.Series(summary["by_category"])
    axis = values.plot(kind="bar", color="#4C78A8", edgecolor="black")
    axis.set_title("Activities by Category")
    axis.set_xlabel("Category")
    axis.set_ylabel("Number of Activities")
    plt.tight_layout()
    plt.show()


def show_destination_report(records):
    """Display a bar chart of activity counts by destination."""
    summary = trip_summary(records)
    if not summary:
        raise ValueError("Add at least one activity before generating a report.")
    values = pd.Series(summary["by_destination"])
    axis = values.plot(kind="bar", color="#F58518", edgecolor="black")
    axis.set_title("Activities by Destination")
    axis.set_xlabel("Destination")
    axis.set_ylabel("Number of Activities")
    plt.tight_layout()
    plt.show()
