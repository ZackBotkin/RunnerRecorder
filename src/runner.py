import os
import json
import plotly
import sqlite3
from datetime import datetime

class RunnerReader(object):

    def __init__(self, configs):
        self.config = configs


        if self.config.get("read_from_db") and self.config.get("read_from_disk"):
            raise Exception("Cannot read from both datasources, update the config file to set either \"read_from_db\" or \"read_from_disk\" to false")
        elif not self.config.get("read_from_db") and not self.config.get("read_from_disk"):
            raise Exception("Need to select a datasource to read from, update the config file to set either \"read_from_db\" or \"read_from_disk\" to true")
        else:
            self.use_db = self.config.get("read_from_db")

        self.runs_by_date = {}
        self.database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("database_name")
        )
        self._load_runs()

    def _load_runs(self):
        if self.use_db:
            self._load_runs_from_db()
        else:
            self._load_runs_from_disk()

    def _load_runs_from_disk(self):
        self.runs_by_date = {}
        runs_directory = self.config.get("runs_directory")
        for file in os.listdir(runs_directory):
            f = open("%s/%s" % (runs_directory, file))
            data = json.load(f)
            if data["date"] not in self.runs_by_date:
                self.runs_by_date[data["date"]] = []
            self.runs_by_date[data["date"]].append(data)

    def _load_runs_from_db(self):
        self.runs_by_date = {}
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute('SELECT * FROM runs')
        results = query.fetchall()
        for result in results:
            _date = result[0]
            _miles = result[1]
            _route_name = result[2]
            if _date not in self.runs_by_date:
                self.runs_by_date[_date] = []
            self.runs_by_date[_date].append({
                'date': _date,
                'miles': _miles,
                'route_name': _route_name
            })

    def get_total(self):
        total=0
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total+= float(data["miles"])
        return total

    def print_all_runs(self):
        total_so_far = 0
        goal = self.config.get("run_goal")
        all_data = [('Date', 'Miles Run', 'Route Name', 'Total So Far', 'Percentage Of Goal')]
        import pandas as pd
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total_so_far += float(data["miles"])
                percentage_of_goal = (total_so_far/goal) * 100
                all_data.append((date, data['miles'], data['route_name'], total_so_far, percentage_of_goal))
        df = pd.DataFrame(all_data)
        print(df.to_string(index=False))
        return True

    def graph_all_runs(self):

        x_vals = []
        y_vals = []
        total_miles = 0
        for date, data_list in self.runs_by_date.items():
            total = 0
            for data in data_list:
                total += float(data["miles"])
            x_vals.append(date)
            y_vals.append(total)
            total_miles += total
        title_string = "%f miles run" % total_miles
        import plotly.express as px
        fig = px.bar(x=x_vals, y=y_vals, title=title_string)
        fig.write_html('first_figure.html', auto_open=True)
        return True

    def line_graph_all_runs(self):
        x_vals = []
        y_vals = []
        total_miles = 0
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total_miles += float(data["miles"])
            x_vals.append(date)
            y_vals.append(total_miles)
        title_string = "%f miles run" % total_miles
        import plotly.express as px
        fig = px.line(x=x_vals, y=y_vals, title=title_string)
        fig.write_html('first_figure.html', auto_open=True)
        return True

    def print_stats(self):
        total_runs = 0
        total_miles = 0
        goal_number = self.config.get("run_goal")
        day_of_year = datetime.now().timetuple().tm_yday
        days_left = 365 - day_of_year
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total_runs += 1
                total_miles += float(data["miles"])
        miles_remaining = goal_number - total_miles
        avg_miles_per_run = total_miles/total_runs
        avg_runs_per_day = total_runs/day_of_year
        avg_miles_per_day = total_miles/day_of_year
        needed_avg = miles_remaining/days_left
        print("\n")
        print("\tDay of year: %d\n" % day_of_year)
        print("\tDays left: %d\n" % days_left)
        print("\tNumber of runs: %d\n" % total_runs)
        print("\tNumber of miles: %f\n" % total_miles)
        print("\tNumber of miles remaining until goal: %f\n" % miles_remaining)
        print("\tMiles per run avg: %f\n" % avg_miles_per_run)
        print("\tRuns per day avg: %f\n" % avg_runs_per_day)
        print("\tMiles per day avg: %f\n" % avg_miles_per_day)
        print("\tMiles per day avg (needed for goal): %f\n" % needed_avg)
        print("\n")
        return True


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

    def todays_date_str(self):
        return datetime.today().strftime("%Y-%m-%d")

    def todays_file_name(self, date_str=None):
        return "%s/%s.json" % (
            self.config.get("runs_directory"),
            date_str or self.todays_date_str()
        )

    ## TODO : need to add some code here so that
    ## it doesn't overwrite stuff that is already there
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

    def migrate_data(self):
        conn = sqlite3.connect(self.database_file_name)
        query_str = "INSERT INTO runs VALUES "
        for date, runs in self.runs_by_date.items():
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
