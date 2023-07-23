import unittest
from runner.src.interactive import InteractiveRunner
from runner.src.runner import RunnerReader
from runner.src.reader_writer import ReaderWriter
from config.config import Configs

class Tests(unittest.TestCase):
    
    def setUp(self):
        configs = Configs("C:\\Users\\zackb\\configs\\tst-runner-reader.json")

        reader_writer = ReaderWriter(configs)
        self.reader = RunnerReader(configs, reader_writer)
        self.interactive = InteractiveRunner(self.reader)

    def test_one(self):
        self.interactive.main_loop()


if __name__ == '__main__':
    unittest.main()
