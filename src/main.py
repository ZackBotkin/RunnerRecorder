import os
import argparse
import json
import plotly
from datetime import datetime, timedelta


class Week(object):

    def __init__(self):
        pass


weekday_mappings = {
    0 : 'monday',
    1 : 'tuesday',
    2 : 'wednesday',
    3 : 'thursday',
    4 : 'friday',
    5 : 'saturday',
    6 : 'sunday'
}

def get_start_of_week(from_date, start_of_week='sunday'):
    weekday = weekday_mappings[from_date.weekday()]
    while weekday != start_of_week:
        from_date = from_date - timedelta(days=1)
        weekday = weekday_mappings[from_date.weekday()]
    return from_date


def construct_weeks(from_date, start_of_week='sunday'):

    by_weeks = {}

    year = from_date.year
    start_of_year = datetime(year, 1, 1)

    current_date = get_start_of_week(start_of_year)
    by_weeks[str(current_date)] = Week()

    current_date = current_date + timedelta(days=1)
    while current_date < from_date:
        weekday = weekday_mappings[current_date.weekday()]
        if weekday == start_of_week:
            by_weeks[str(current_date)] = Week()
        current_date = current_date + timedelta(days=1)

    return by_weeks


class RunnerReader(object):

    def __init__(self, runs_directory):
        self.runs_directory = runs_directory
        self.runs_by_date = {}
        self.grouped_weeks = construct_weeks(datetime.today) 
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

    def graph_all_runs(self):

        x_vals = []
        y_vals = []
        for date, data_list in self.runs_by_date.items():
            total = 0
            for data in data_list:
                total += float(data["miles"])
            x_vals.append(date)
            y_vals.append(total)
        import plotly.express as px
        fig = px.bar(x=x_vals, y=y_vals)
        fig.write_html('first_figure.html', auto_open=True)

    def print_stats(self):
        total_runs = 0
        total_miles = 0
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total_runs += 1
                total_miles += float(data["miles"])
        print("Number of runs: %d\n" % total_runs)
        print("Number of miles: %f\n" % total_miles)
        avg_miles_per_run = total_miles/total_runs
        print("Miles per run avg: %f\n" % avg_miles_per_run)


def main():

    parser = argparse.ArgumentParser(description= 'default parser')
    parser.add_argument('--total', help='running totals')
    parser.add_argument('--print_all_runs', help='print the running files')
    parser.add_argument('--graph_all_runs', help='graph the running files')
    parser.add_argument('--print_stats', help='print the stats')
    args = parser.parse_args()

    DEFAULT_DIRECTORY="C:\\Users\\zackb\\Notes\\runs"
    reader = RunnerReader(DEFAULT_DIRECTORY)
    if args.print_all_runs:
        reader.print_all_runs()
    elif args.graph_all_runs:
        reader.graph_all_runs()
    elif args.print_stats:
        reader.print_stats()
    else:
        total = reader.get_total()
        print("%f miles run" % total)


if __name__ == '__main__':
    main()
