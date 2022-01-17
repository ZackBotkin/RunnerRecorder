import os
import argparse
import json



class RunnerReader(object):

    def __init__(self, runs_directory):
        self.runs_directory = runs_directory
        self.runs_by_date = {}
        self._load_from_disk()

    def _load_from_disk(self):
        for file in os.listdir(self.runs_directory):
            f = open("%s/%s" % (self.runs_directory, file))
            data = json.load(f)
            self.runs_by_date[data["date"]] = data

    def get_total(self):
        total=0
        for date, data in self.runs_by_date.items():
            total+= float(data["miles"])
        return total


def main():

    parser = argparse.ArgumentParser(description= 'default parser')
    parser.add_argument('--total', help='running totals')
    args = parser.parse_args()

    DEFAULT_DIRECTORY="C:\\Users\\zackb\\Notes\\runs"
    reader = RunnerReader(DEFAULT_DIRECTORY)
    total = reader.get_total()
    print("%f miles run" % total)


if __name__ == '__main__':
    main()
