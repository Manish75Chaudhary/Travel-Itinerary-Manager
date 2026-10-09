"""Entry point for the Travel Itinerary Manager application."""

from pathlib import Path
import tkinter as tk

from gui import TravelItineraryApp


def main():
    root = tk.Tk()
    csv_path = Path(__file__).parent / "data" / "itinerary.csv"
    TravelItineraryApp(root, csv_path)
    root.mainloop()


if __name__ == "__main__":
    main()
