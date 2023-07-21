import unittest
import datetime

from src.util import (
    get_weeks,
    get_miles_per_week,
    get_miles_since_date_inclusive,
    get_miles_in_date_range_inclusive
)

class Tests(unittest.TestCase):

    def test_get_weeks(self):
        weeks = get_weeks(2023)

        # first week of 2023, sunday starts the week by default
        self.assertEqual(weeks[0].dates[0], datetime.datetime(2023, 1, 1, 0, 0))
        self.assertEqual(weeks[0].dates[1], datetime.datetime(2023, 1, 2, 0, 0))
        self.assertEqual(weeks[0].dates[2], datetime.datetime(2023, 1, 3, 0, 0))
        self.assertEqual(weeks[0].dates[3], datetime.datetime(2023, 1, 4, 0, 0))
        self.assertEqual(weeks[0].dates[4], datetime.datetime(2023, 1, 5, 0, 0))
        self.assertEqual(weeks[0].dates[5], datetime.datetime(2023, 1, 6, 0, 0))
        self.assertEqual(weeks[0].dates[6], datetime.datetime(2023, 1, 7, 0, 0))

        ## last run of 2023 .. only one day :(
        self.assertEqual(weeks[-1].dates[0], datetime.datetime(2023, 12, 31, 0, 0))
        self.assertEqual(weeks[-1].dates[1], datetime.datetime(2024, 1, 1, 0, 0))
        self.assertEqual(weeks[-1].dates[2], datetime.datetime(2024, 1, 2, 0, 0))
        self.assertEqual(weeks[-1].dates[3], datetime.datetime(2024, 1, 3, 0, 0))
        self.assertEqual(weeks[-1].dates[4], datetime.datetime(2024, 1, 4, 0, 0))
        self.assertEqual(weeks[-1].dates[5], datetime.datetime(2024, 1, 5, 0, 0))
        self.assertEqual(weeks[-1].dates[6], datetime.datetime(2024, 1, 6, 0, 0))

        ## now let's say a week "starts" on monday
        weeks = get_weeks(2023, start_of_week_index=0)

        ## by making the week "start" on monday, this goes back into 2022 a bit
        self.assertEqual(weeks[0].dates[0], datetime.datetime(2022, 12, 26, 0, 0))
        self.assertEqual(weeks[0].dates[1], datetime.datetime(2022, 12, 27, 0, 0))
        self.assertEqual(weeks[0].dates[2], datetime.datetime(2022, 12, 28, 0, 0))
        self.assertEqual(weeks[0].dates[3], datetime.datetime(2022, 12, 29, 0, 0))
        self.assertEqual(weeks[0].dates[4], datetime.datetime(2022, 12, 30, 0, 0))
        self.assertEqual(weeks[0].dates[5], datetime.datetime(2022, 12, 31, 0, 0))
        self.assertEqual(weeks[0].dates[6], datetime.datetime(2023, 1, 1, 0, 0))


    def test_get_miles_per_week(self):

        runs_by_date = {
            "2023-01-01": [{"miles": 10}],
            "2023-01-02": [{"miles": 5}],
            "2023-01-07": [{"miles": 3}, {"miles": 2}],
            "2023-01-08": [{"miles": 10}]
        }
        miles_per_week = get_miles_per_week(runs_by_date, 2023)

        first_week = miles_per_week[0]
        self.assertEqual(first_week.start_date, datetime.datetime(2023, 1, 1, 0, 0))
        self.assertEqual(first_week.total_miles, 20)

        second_week = miles_per_week[1]
        self.assertEqual(second_week.start_date, datetime.datetime(2023, 1, 8, 0, 0))
        self.assertEqual(second_week.total_miles, 10)

        third_week = miles_per_week[2]
        self.assertEqual(third_week.start_date, datetime.datetime(2023, 1, 15, 0, 0))
        self.assertEqual(third_week.total_miles, 0)


    def test_get_miles_since(self):

        runs_by_date = {
            "2023-01-01" : [{"miles": 10}],
            "2023-01-02" : [{"miles": 10}],
            "2023-01-03" : [{"miles": 10}, {"miles": 10}],
            "2023-01-05" : [{"miles": 10}]
        }

        jan5 = get_miles_since_date_inclusive(runs_by_date, "2023-01-05")
        self.assertEqual(jan5, 10)

        jan4 = get_miles_since_date_inclusive(runs_by_date, "2023-01-04")
        self.assertEqual(jan4, 10)

        jan3 = get_miles_since_date_inclusive(runs_by_date, "2023-01-03")
        self.assertEqual(jan3, 30)

        jan2 = get_miles_since_date_inclusive(runs_by_date, "2023-01-02")
        self.assertEqual(jan2, 40)

        jan1 = get_miles_since_date_inclusive(runs_by_date, "2023-01-01")
        self.assertEqual(jan1, 50)


    def test_get_miles_in_date_range(self):

        runs_by_date = {
            "2023-01-01" : [{"miles": 10}],
            "2023-01-02" : [{"miles": 10}],
            "2023-01-03" : [{"miles": 10}, {"miles": 10}],
            "2023-01-05" : [{"miles": 10}]
        }

        whole_range = get_miles_in_date_range_inclusive(runs_by_date, "2023-01-01")
        self.assertEqual(whole_range, 50)

        whole_range = get_miles_in_date_range_inclusive(runs_by_date, "2023-01-01", "2023-01-10")
        self.assertEqual(whole_range, 50)

        partial_range = get_miles_in_date_range_inclusive(runs_by_date, "2023-01-01", "2023-01-03")
        self.assertEqual(partial_range, 40)

        partial_range = get_miles_in_date_range_inclusive(runs_by_date, "2023-01-03", "2023-01-05")
        self.assertEqual(partial_range, 30)

        bad_range = get_miles_in_date_range_inclusive(runs_by_date, "2023-01-05", "2023-01-01")
        self.assertEqual(bad_range, 0)

if __name__ == '__main__':
    unittest.main()
