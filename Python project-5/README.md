# Travel Itinerary Manager

## Problem Statement

Travel details are often spread across notes. This application stores activities, destinations, and schedules in one structured itinerary and provides useful trip summaries.

## Objective

To develop a simple desktop application that manages itinerary information and summarizes how a trip is organized.

## Features

- Add, update, delete, search, and filter itinerary activities.
- Display records chronologically by date and time, and organize them by destination and category.
- Validate DD-MM-YYYY dates, HH:MM times, and required fields.
- Save data permanently in a CSV file.
- Display a Pandas-based trip summary and category comparison-ready counts.
- Generate bar charts for activities by category and destination.

## Technologies Used

Python, Tkinter, Pandas, Matplotlib, CSV, and the Python standard library.

## Project Structure

```
travel_itinerary_manager/
├── main.py              # Starts the application
├── gui.py               # Tkinter interface
├── itinerary.py         # CRUD operations and validation
├── file_manager.py      # CSV loading and saving
├── analytics.py         # Pandas summaries and Matplotlib charts
├── data/itinerary.csv   # Persistent sample itinerary data
├── test_itinerary.py    # Small automated core tests
├── TESTING.md           # Manual testing checklist
└── README.md
```

## How the Application Works

Enter an activity in the form and click **Add**. Select a table row to load it into the form for updating or deleting. Use Search for keyword matching and Filter for date, destination, or category. Trip Summary uses Pandas to calculate totals and grouped counts. Reports opens either Matplotlib chart.

The modules have deliberately simple roles: `itinerary.py` manages records and validation; `file_manager.py` handles CSV persistence; `analytics.py` calculates summaries; `gui.py` displays the interface; and `main.py` starts it.

## How to Run

1. Install dependencies: `pip install pandas matplotlib`
2. In the project folder, run: `python main.py`
3. Use the sample data in `data/itinerary.csv`, or add your own records.

## Sample Data

The CSV includes ten Indian travel activities across Jaipur, Jodhpur, and Udaipur, in Travel, Hotel, Food, Sightseeing, and Shopping categories.

## Testing

Follow [TESTING.md](TESTING.md) for the manual checklist. Run the core automated tests with:

```
python -m unittest test_itinerary.py
```

## Future Scope

- Export the itinerary as a PDF.
- Add a per-date line chart.
- Add a simple budget field and expense summary.
