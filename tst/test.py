import unittest
import datetime
from src.runner import RunnerReader
from src.reader_writer import ReaderWriter
from config.config import Configs

from src.main import Week, construct_weeks, get_start_of_week

class MockConfig(object):

    def __init__(self):
        self.mock_values = {
            "run_goal": 10
        }

    def get(self, parameter):
        return self.mock_values[parameter]

class MockReaderWriter(object):

    def __init__(self, config):
        self.config = config

    def get_runs(self):
        return {
            "2023-03-01": [
                {
                    "date" : "2023-03-01",
                    "route_name": "unit_test",
                    "miles": 4,
                    "comment": "unit_test"
                }
            ]
        }

class Tests(unittest.TestCase):

    def setUp(self):
        config = MockConfig()
        reader_writer = MockReaderWriter(config)
        self.reader = RunnerReader(config, reader_writer)

    def test_stats(self):
        stats = self.reader.get_stats()
        self.assertEquals(stats["total_miles"], 4)
        self.assertEquals(stats["miles_remaining"], 6)
        self.assertEquals(stats["total_runs"], 1)


if __name__ == '__main__':
    unittest.main()
