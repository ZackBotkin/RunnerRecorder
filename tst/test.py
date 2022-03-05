import unittest
import datetime

from src.main import Week, construct_weeks, get_start_of_week

class Tests(unittest.TestCase):

    def test_get_start_of_week(self):
        current_date = datetime.datetime(2022, 1, 1)
        start_of_week = get_start_of_week(current_date)
        self.assertEqual(
            start_of_week,
            datetime.datetime(2021, 12, 26)
        )
    def test_get_start_of_week_with_different_start_date(self):
        current_date = datetime.datetime(2022, 1, 1)
        start_of_week = get_start_of_week(current_date, start_of_week='saturday')
        self.assertEqual(
            start_of_week,
            datetime.datetime(2022, 1, 1)
        )

    def test_weeks(self):
        current_date = datetime.datetime(2022, 3, 5)
        weeks = construct_weeks(current_date)

if __name__ == '__main__':
    unittest.main()
