import os
import json
import plotly
from datetime import datetime

MILE_MAP = {
    "grand": 7.45,
    "lake": 8.25,
    "lakeshore": 6.1,
    "sedgewick": 4.75,
    "kingsbury": 3.5
}

class RunnerReader(object):

    def __init__(self, runs_directory):
        self.runs_directory = runs_directory
        self.runs_by_date = {}
        #self.grouped_weeks = construct_weeks(datetime.today)
        self._load_from_disk()

    def _load_from_disk(self):
        self.runs_by_date = {}
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
        total_so_far = 0
        goal = 1000
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
        goal_number = 1000
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
        print("Day of year: %d\n" % day_of_year)
        print("Days left: %d\n" % days_left)
        print("Number of runs: %d\n" % total_runs)
        print("Number of miles: %f\n" % total_miles)
        print("Number of miles remaining until goal: %f\n" % miles_remaining)
        print("Miles per run avg: %f\n" % avg_miles_per_run)
        print("Runs per day avg: %f\n" % avg_runs_per_day)
        print("Miles per day avg: %f\n" % avg_miles_per_day)
        print("Miles per day avg (needed for goal): %f\n" % needed_avg)
        return True

    def todays_date_str(self):
        todays_date = datetime.today()
        date_str = "%s-%s-%s" % (
            todays_date.year,
            todays_date.month,
            todays_date.day
        )
        return date_str

    def todays_file_name(self, date_str=None):
        return "%s/%s.json" % (
            self.runs_directory,
            date_str or self.todays_date_str()
        )

    ## TODO : need to add some code here so that
    ## it doesn't overwrite stuff that is already there
    def write_run_to_disk(self, route_name):
        with open(self.todays_file_name(), 'w') as f:
            if route_name not in MILE_MAP:
                raise Exception("Unknown route!")
            else:
                miles = MILE_MAP[route_name]
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
