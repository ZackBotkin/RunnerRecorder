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
            if data["date"] not in self.runs_by_date:
                self.runs_by_date[data["date"]] = []
            self.runs_by_date[data["date"]].append(data)

    def get_total(self):
        total=0
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total+= float(data["miles"])
        return total

    def print_all_runs(self):
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                print("%s -- %s miles" % (date, data["miles"]))


def main():

    parser = argparse.ArgumentParser(description= 'default parser')
    parser.add_argument('--total', help='running totals')
    parser.add_argument('--print_all_runs', help='print the running files')
    args = parser.parse_args()

    DEFAULT_DIRECTORY="C:\\Users\\zackb\\Notes\\runs"
    reader = RunnerReader(DEFAULT_DIRECTORY)
    if args.print_all_runs:
        reader.print_all_runs()
    else:
        total = reader.get_total()
        print("%f miles run" % total)


if __name__ == '__main__':
    main()
