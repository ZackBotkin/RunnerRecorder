import unittest
from src.interactive import InteractiveRunner
from src.runner import RunnerReader
from config.config import Configs

class Tests(unittest.TestCase):
    
    def setUp(self):
        configs = Configs("C:\\Users\\zackb\\configs\\tst-runner-reader.json")

        use_db = False
        self.reader = RunnerReader(configs, use_db)
        self.interactive = InteractiveRunner(self.reader)

    def test_one(self):
        self.interactive.main_loop()


if __name__ == '__main__':
    unittest.main()
