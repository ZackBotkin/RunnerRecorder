import sqlite3
import os
import json
from datetime import datetime

class ReaderWriter(object):

    def __init__(self, configs):

        self.config = configs

        if self.config.get("read_from_db") and self.config.get("read_from_disk"):
            raise Exception("Cannot read from both datasources, update the config file to set either \"read_from_db\" or \"read_from_disk\" to false")
        elif not self.config.get("read_from_db") and not self.config.get("read_from_disk"):
            raise Exception("Need to select a datasource to read from, update the config file to set either \"read_from_db\" or \"read_from_disk\" to true")
        else:
            self.use_db = self.config.get("read_from_db")

        self.database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("database_name")
        )

    def todays_date_str(self):
        return datetime.today().strftime("%Y-%m-%d")

    def todays_file_name(self, date_str=None):
        return "%s/%s.json" % (
            self.config.get("runs_directory"),
            date_str or self.todays_date_str()
        )

    def get_runs(self):
        if self.use_db:
            return self.get_runs_from_db()
        else:
            return self.get_runs_from_disk()

    def get_runs_from_db(self):
        runs_by_date = {}
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute('SELECT * FROM runs')
        results = query.fetchall()
        for result in results:
            _date = result[0]
            _miles = result[1]
            _route_name = result[2]
            if _date not in runs_by_date:
                runs_by_date[_date] = []
            runs_by_date[_date].append({
                'date': _date,
                'miles': _miles,
                'route_name': _route_name
            })
        return runs_by_date

    def get_runs_from_disk(self):
        runs_by_date = {}
        runs_directory = self.config.get("runs_directory")
        for file in os.listdir(runs_directory):
            f = open("%s/%s" % (runs_directory, file))
            data = json.load(f)
            if data["date"] not in runs_by_date:
                runs_by_date[data["date"]] = []
            runs_by_date[data["date"]].append(data)
        return runs_by_date

    def write_run(self, route_name):
        if self.config.get("write_to_disk"):
            self.write_run_to_disk(route_name)
        if self.config.get("write_to_db"):
            self.write_run_to_db(route_name)

    def write_new_run(self, args):
        if self.config.get("write_to_disk"):
            self.write_new_run_to_disk(args)
        if self.config.get("write_to_db"):
            self.write_new_run_to_db(args)

    def write_run_to_disk(self, route_name):
        with open(self.todays_file_name(), 'w') as f:
            mile_map = self.config.get("mile_map")
            if route_name not in mile_map:
                raise Exception("Unknown route!")
            else:
                miles = mile_map[route_name]
                json.dump({
                    "miles": miles,
                    "date": self.todays_date_str(),
                    "route_name": route_name
                }, f)
                return

    def write_new_run_to_disk(self, args):
        if "miles" not in args:
            raise Exception("Need \'miles\' as an arg")
        if "route_name" not in args:
            raise Exception("Need \'route_name\' as an arg")
        with open(self.todays_file_name(date_str=args["date"]), "w") as f:
            json.dump({
                "miles": args["miles"],
                "date": args["date"] or self.todays_date_str(),
                "route_name": args["route_name"]
            }, f)
            return

    def write_run_to_db(self, route_name):
        mile_map = self.config.get("mile_map")
        if route_name not in mile_map:
            raise Exception("Unknown route!")
        else:
            miles = mile_map[route_name]
            _date = self.todays_date_str()
            conn = sqlite3.connect(self.database_file_name)
            query_str = "INSERT INTO runs VALUES "
            query_str += "('%s', %s, '%s')" % (
                _date,
                miles,
                route_name
            )
            conn.execute(query_str)
            conn.commit()

    def write_new_run_to_db(self, args):
        raise Exception("Not implemented yet")


    def create_table(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute("CREATE TABLE runs(date, miles, route_name)")
        conn.commit()

    def migrate_data(self, runs_by_date):
        conn = sqlite3.connect(self.database_file_name)
        query_str = "INSERT INTO runs VALUES "
        for date, runs in runs_by_date.items():
            for run in runs:
                query_str += "('%s', %s, '%s'), " % (
                    run['date'],
                    run['miles'],
                    run['route_name']
                )
        query_str = query_str.strip().rstrip(',')
        conn.execute(query_str)
        conn.commit()

    def read_data(self):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute("SELECT * FROM runs")
        results = query.fetchall()
        for result in results:
            print(result)

    def delete_data(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute('DELETE FROM runs')
        conn.commit()

    def drop_table(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute('DROP TABLE runs')
        conn.commit()

