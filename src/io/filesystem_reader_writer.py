import os
import json
from src.io.reader_writer import ReaderWriter

class FileSystemReaderWriter(ReaderWriter):

    def __init__(self, config, miles_map):
        self.config = config
        self.miles_map = miles_map

    def get_runs(self, date=None):
        runs_by_date = {}
        runs_directory = self.config.get("runs_directory")
        for file in os.listdir(runs_directory):
            f = open("%s/%s" % (runs_directory, file))
            data = json.load(f)
            if data["date"] not in runs_by_date:
                runs_by_date[data["date"]] = []
            runs_by_date[data["date"]].append(data)
        return runs_by_date

    def get_legacy_runs(self):
        runs_by_date = {}
        runs_directory = self.config.get("legacy_runs_directory")
        for file in os.listdir(runs_directory):
            f = open("%s/%s" % (runs_directory, file))
            data = json.load(f)
            if data["date"] not in runs_by_date:
                runs_by_date[data["date"]] = []
            runs_by_date[data["date"]].append(data)
        return runs_by_date

    def add_run(self, route_name, comment=None):

        if route_name not in self.miles_map:
            raise Exception("Unknown route!")

        todays_json_filename = self.todays_file_name()
        already_exists = os.path.exists(todays_json_filename)
        individualizer = 1
        while already_exists:
            todays_json_filename = self.todays_file_name(individualizer=individualizer)
            individualizer += 1
            already_exists = os.path.exists(todays_json_filename)

        with open(todays_json_filename, 'w') as f:
            miles = self.miles_map[route_name]
            if comment is None:
                comment = ''
            json.dump({
                "miles": miles,
                "date": self.todays_date_str(),
                "route_name": route_name,
                "comment": comment
            }, f)

    def edit_run(self, run_date, route_name, distance_in_miles, comment):
        #raise Exception("This is not implemented and probably won't be")
        print("Warning, not updating the file system")

    def get_routes(self):
        raise Exception("This is not implemented and probably won't be")

    def add_route(self, route_name, distance_in_miles, description):
        #raise Exception("This is not implemented and probably won't be")
        print("Warning, not updating the file system")

    ## private methods

    def todays_file_name(self, date_str=None, individualizer=None):
        if individualizer is not None:
            return "%s/%s-%s.json" % (
                self.config.get("runs_directory"),
                date_str or self.todays_date_str(),
                individualizer
            )
        else:
            return "%s/%s.json" % (
                self.config.get("runs_directory"),
                date_str or self.todays_date_str()
            )
