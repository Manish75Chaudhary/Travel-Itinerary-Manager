"""Tkinter interface for the Travel Itinerary Manager."""

import tkinter as tk
from tkinter import ttk, messagebox

import analytics
from file_manager import load_activities, save_activities
from itinerary import CATEGORIES, create_activity, delete_activity, filter_activities, search_activities, sort_activities, update_activity


class TravelItineraryApp:
    """A small GUI class that connects form controls with itinerary functions."""

    def __init__(self, root, csv_path):
        self.root = root
        self.csv_path = csv_path
        self.selected_id = None
        try:
            self.records = load_activities(csv_path)
        except (OSError, ValueError) as error:
            messagebox.showerror("File Error", str(error))
            self.records = []

        self.root.title("Travel Itinerary Manager")
        self.root.geometry("1120x650")
        self.root.minsize(900, 560)
        self._build_interface()
        self.show_records(self.records)

    def _build_interface(self):
        title = ttk.Label(self.root, text="Travel Itinerary Manager", font=("Arial", 18, "bold"))
        title.pack(pady=(12, 4))

        form = ttk.LabelFrame(self.root, text="Activity Details", padding=10)
        form.pack(fill="x", padx=12, pady=6)
        self.entries = {}
        labels = [("Date", 0, 0), ("Destination", 0, 2), ("Activity", 0, 4), ("Time", 1, 0), ("Category", 1, 2), ("Notes", 1, 4)]
        for label, row, column in labels:
            ttk.Label(form, text=label + ":").grid(row=row, column=column, sticky="w", padx=(0, 5), pady=5)
            if label == "Category":
                widget = ttk.Combobox(form, values=CATEGORIES, state="readonly", width=23)
            else:
                widget = ttk.Entry(form, width=27)
            widget.grid(row=row, column=column + 1, sticky="ew", padx=(0, 12), pady=5)
            self.entries[label] = widget

        actions = ttk.Frame(self.root, padding=(12, 3))
        actions.pack(fill="x")
        for text, command in [("Add", self.add_record), ("Update", self.update_record), ("Delete", self.delete_record), ("Clear", self.clear_form), ("Trip Summary", self.show_summary), ("Reports", self.open_reports)]:
            ttk.Button(actions, text=text, command=command).pack(side="left", padx=3)

        search_frame = ttk.LabelFrame(self.root, text="Search and Filter", padding=8)
        search_frame.pack(fill="x", padx=12, pady=6)
        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame, width=18)
        self.search_entry.pack(side="left", padx=4)
        ttk.Button(search_frame, text="Search", command=self.search_records).pack(side="left", padx=2)
        ttk.Label(search_frame, text="  Filter Date:").pack(side="left")
        self.filter_date = ttk.Entry(search_frame, width=13)
        self.filter_date.pack(side="left", padx=3)
        ttk.Label(search_frame, text="Destination:").pack(side="left")
        self.filter_destination = ttk.Entry(search_frame, width=14)
        self.filter_destination.pack(side="left", padx=3)
        ttk.Label(search_frame, text="Category:").pack(side="left")
        self.filter_category = ttk.Combobox(search_frame, values=[""] + CATEGORIES, state="readonly", width=13)
        self.filter_category.pack(side="left", padx=3)
        ttk.Button(search_frame, text="Filter", command=self.filter_records).pack(side="left", padx=2)
        ttk.Button(search_frame, text="Show All", command=lambda: self.show_records(self.records)).pack(side="left", padx=2)

        table_frame = ttk.Frame(self.root, padding=(12, 4))
        table_frame.pack(fill="both", expand=True)
        columns = ("ID", "Date", "Destination", "Activity", "Time", "Category", "Notes")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        widths = {"ID": 80, "Date": 95, "Destination": 120, "Activity": 180, "Time": 75, "Category": 110, "Notes": 290}
        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=widths[column], anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.table.bind("<<TreeviewSelect>>", self.select_record)

    def values(self):
        return [self.entries[name].get() for name in ("Date", "Destination", "Activity", "Time", "Category", "Notes")]

    def save_and_refresh(self, message):
        try:
            save_activities(self.csv_path, self.records)
            self.show_records(self.records)
            self.clear_form()
            messagebox.showinfo("Success", message)
        except OSError as error:
            messagebox.showerror("Save Error", str(error))

    def add_record(self):
        try:
            self.records.append(create_activity(*self.values()))
            self.save_and_refresh("Activity added successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))

    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning("Select Record", "Select a record to update.")
            return
        try:
            if update_activity(self.records, self.selected_id, *self.values()):
                self.save_and_refresh("Activity updated successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))

    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning("Select Record", "Select a record to delete.")
        elif messagebox.askyesno("Confirm Delete", "Delete the selected activity?"):
            delete_activity(self.records, self.selected_id)
            self.save_and_refresh("Activity deleted successfully.")

    def clear_form(self):
        for widget in self.entries.values():
            widget.set("") if isinstance(widget, ttk.Combobox) else widget.delete(0, tk.END)
        self.selected_id = None
        for item in self.table.selection():
            self.table.selection_remove(item)

    def select_record(self, _event):
        selected = self.table.selection()
        if not selected:
            return
        values = self.table.item(selected[0], "values")
        self.selected_id = values[0]
        for name, value in zip(("Date", "Destination", "Activity", "Time", "Category", "Notes"), values[1:]):
            widget = self.entries[name]
            widget.set(value) if isinstance(widget, ttk.Combobox) else (widget.delete(0, tk.END), widget.insert(0, value))

    def show_records(self, records):
        for item in self.table.get_children():
            self.table.delete(item)
        for record in sort_activities(records):
            self.table.insert("", "end", values=[record[field] for field in ("ID", "Date", "Destination", "Activity", "Time", "Category", "Notes")])

    def search_records(self):
        self.show_records(search_activities(self.records, self.search_entry.get()))

    def filter_records(self):
        self.show_records(filter_activities(self.records, self.filter_date.get(), self.filter_destination.get(), self.filter_category.get()))

    def show_summary(self):
        summary = analytics.trip_summary(self.records)
        if not summary:
            messagebox.showinfo("Trip Summary", "No activities have been added yet.")
            return
        categories = "\n".join(f"{key}: {value}" for key, value in summary["by_category"].items())
        destinations = "\n".join(f"{key}: {value}" for key, value in summary["by_destination"].items())
        text = (f"TRIP SUMMARY\n\nTotal Activities: {summary['total_activities']}\n"
                f"Total Destinations: {summary['total_destinations']}\n"
                f"Trip Start Date: {summary['start_date']}\nTrip End Date: {summary['end_date']}\n"
                f"Trip Duration: {summary['duration']} Days\nMost Common Category: {summary['most_common_category']}\n\n"
                f"Activities by Category:\n{categories}\n\nActivities by Destination:\n{destinations}")
        window = tk.Toplevel(self.root)
        window.title("Trip Summary")
        tk.Text(window, width=55, height=25, padx=12, pady=12, wrap="word").pack()
        widget = window.winfo_children()[0]
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def open_reports(self):
        window = tk.Toplevel(self.root)
        window.title("Visual Reports")
        ttk.Label(window, text="Choose a report", padding=12).pack()
        ttk.Button(window, text="Activities by Category", command=lambda: self.run_report(analytics.show_category_report)).pack(fill="x", padx=12, pady=4)
        ttk.Button(window, text="Activities by Destination", command=lambda: self.run_report(analytics.show_destination_report)).pack(fill="x", padx=12, pady=(0, 12))
        comparison = ttk.LabelFrame(window, text="Compare Planned Activities", padding=8)
        comparison.pack(fill="x", padx=12, pady=(0, 12))
        first_category = ttk.Combobox(comparison, values=CATEGORIES, state="readonly", width=15)
        second_category = ttk.Combobox(comparison, values=CATEGORIES, state="readonly", width=15)
        first_category.grid(row=0, column=0, padx=3)
        ttk.Label(comparison, text="vs").grid(row=0, column=1, padx=3)
        second_category.grid(row=0, column=2, padx=3)
        ttk.Button(comparison, text="Compare", command=lambda: self.compare_categories(first_category.get(), second_category.get())).grid(row=0, column=3, padx=5)

    def compare_categories(self, first_category, second_category):
        if not first_category or not second_category:
            messagebox.showwarning("Choose Categories", "Select two categories to compare.")
            return
        first_count, second_count = analytics.compare_categories(self.records, first_category, second_category)
        messagebox.showinfo("Activity Comparison", f"{first_category}: {first_count} planned activities\n{second_category}: {second_count} planned activities")

    def run_report(self, report_function):
        try:
            report_function(self.records)
        except (ValueError, ImportError) as error:
            messagebox.showerror("Report Error", str(error))
