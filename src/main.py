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

RECORD_RUN_ANSWERS = [
    'record', 'record_run', 'record run'
]

ALL_RUNS_ANSWERS = [
    'all', 'all_runs', 'list'
]

RUNNING_STAT_ANSWERS = [
    'stats', 'running_stats'
]

DEFAULT_RUNS = [
    'grand', 'roosevelt', 'lake', 'lakeshore', 'sedgewick', 'kingsbury'
]

LINE_START = ">>>" 

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
        #self.grouped_weeks = construct_weeks(datetime.today)
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

    def interactive_mode(self):
        self.main_interactive_loop()

    def main_interactive_loop(self):
        print("%s Welcome to runner reader\n" % LINE_START)
        answer = input("%s What are you doing\n" % LINE_START)
        self.handle_answer_interactive(answer)
        

    def handle_answer_interactive(self, answer):
        if answer in RECORD_RUN_ANSWERS:
            self.record_run_interactive()
        elif answer in ALL_RUNS_ANSWERS:
            self.print_all_runs()
        elif answer in RUNNING_STATS_ANSWERS:
            self.print_stats()
        else:
            print("%s Unknown answer type. Please pick again \n" % LINE_START)

    def record_run_interactive(self):
        print("%s Good for you! Lets record a run!\n" % LINE_START)
        answer = input("%s Which run? Type one of the defaults, or say \"new\" to enter a new one\n" % LINE_START)
        if answer in DEFAULT_RUNS:
            print("%s Recording %s run!\n" % (LINE_START, answer))
        else:
            print("%s Ok, lets record a new run!" % LINE_START)

        done = False
        while not done:
            answer = input("%s Are you done?\n" % LINE_START)
            if answer in ["Yes", "yes", "y"]:
                return True
            elif answer in ["No", "no", "n"]:
                done = self.record_run_interactive()
                return False
            else:
                print("%s Cmon man pick a real answer\n" % LINE_START)

        return True
                


def main():

    parser = argparse.ArgumentParser(description= 'default parser')
    parser.add_argument('--total', help='running totals')
    parser.add_argument('--print_all_runs', help='print the running files')
    parser.add_argument('--graph_all_runs', help='graph the running files')
    parser.add_argument('--line_graph_all_runs', help='graph the running files as a line graph')
    parser.add_argument('--print_stats', help='print the stats')
    parser.add_argument('--interactive', help='interactive mode')
    args = parser.parse_args()

    DEFAULT_DIRECTORY="C:\\Users\\zackb\\Notes\\runs"
    reader = RunnerReader(DEFAULT_DIRECTORY)
    if args.print_all_runs:
        reader.print_all_runs()
    elif args.graph_all_runs:
        reader.graph_all_runs()
    elif args.line_graph_all_runs:
        reader.line_graph_all_runs()
    elif args.print_stats:
        reader.print_stats()
    elif args.interactive:
        reader.interactive_mode()
    else:
        total = reader.get_total()
        print("%f miles run" % total)


if __name__ == '__main__':
    main()
