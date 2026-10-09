"""Small automated tests for the core itinerary functions."""

import unittest

from itinerary import create_activity, delete_activity, filter_activities, search_activities, sort_activities, update_activity


class ItineraryTests(unittest.TestCase):
    def setUp(self):
        self.record = create_activity("10-11-2026", "Jaipur", "Amber Fort", "09:00", "Sightseeing", "Morning")
        self.records = [self.record]

    def test_add_creates_id(self):
        self.assertEqual(self.record["Destination"], "Jaipur")
        self.assertEqual(len(self.record["ID"]), 8)

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            create_activity("2026-11-10", "Jaipur", "Amber Fort", "09:00", "Sightseeing")
        with self.assertRaises(ValueError):
            create_activity("10-11-2026", "Jaipur", "Amber Fort", "9 AM", "Sightseeing")

    def test_search_filter_update_and_delete(self):
        self.assertEqual(len(search_activities(self.records, "amber")), 1)
        self.assertEqual(len(filter_activities(self.records, category="Sightseeing")), 1)
        self.assertTrue(update_activity(self.records, self.record["ID"], "10-11-2026", "Jaipur", "City Palace", "10:00", "Sightseeing"))
        self.assertEqual(self.records[0]["Activity"], "City Palace")
        self.assertTrue(delete_activity(self.records, self.record["ID"]))
        self.assertEqual(self.records, [])

    def test_records_sort_by_date_then_time(self):
        later = create_activity("11-11-2026", "Jodhpur", "Fort", "08:00", "Sightseeing")
        earlier_time = create_activity("10-11-2026", "Jaipur", "Breakfast", "08:00", "Food")
        sorted_records = sort_activities([later, self.record, earlier_time])
        self.assertEqual([record["Activity"] for record in sorted_records], ["Breakfast", "Amber Fort", "Fort"])


if __name__ == "__main__":
    unittest.main()
