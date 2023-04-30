import plotly
from datetime import datetime

class RunnerReader(object):

    def __init__(self, configs, reader_writer):
        self.config = configs
        self.reader_writer = reader_writer
        self.runs_by_date = self.reader_writer.get_runs()
        self.legacy_runs_by_date = self.reader_writer.get_legacy_runs()

    def reload(self):
        self.runs_by_date = self.reader_writer.get_runs()

    def write_run(self, route_name, comment=None):
        self.reader_writer.write_run(route_name, comment)

    def write_new_run(self, args, comment=None):
        self.reader_writer.write_new_run(args, comment)

    def create_table(self):
        self.reader_writer.create_table()

    def migrate_data(self):
        self.reader_writer.migrate_data(self.runs_by_date)

    def read_data(self):
        self.reader_writer.read_data()

    def delete_data(self):
        self.reader_writer.delete_data()

    def drop_table(self):
        self.reader_writer.drop_table()

    def get_total(self):
        total=0
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total+= float(data["miles"])
        return total

    def print_all_runs(self):
        total_so_far = 0
        goal = self.config.get("run_goal")
        all_data = [('Date', 'Miles Run', 'Route Name', 'Total So Far', 'Percentage Of Goal', 'Comment')]
        import pandas as pd
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total_so_far += float(data["miles"])
                percentage_of_goal = (total_so_far/goal) * 100
                comment = ""
                if "comment" in data:
                    comment = data["comment"]
                all_data.append(
                    (
                        date,
                        data['miles'],
                        data['route_name'],
                        total_so_far,
                        percentage_of_goal,
                        comment
                    )
                )
        df = pd.DataFrame(all_data)
        print(df.to_string(index=False))
        return True

    def print_all_routes(self):

        ## TODO : get this from the database
        routes = self.config.get('mile_map')
        all_data = [('Route Name', 'Distance')]
        import pandas as pd
        for route_name, miles in routes.items():
            all_data.append((route_name, "%f miles" % miles))
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

    def historical_graph_all_runs(self):
        x_vals = []
        y_vals = []
        total_miles = 0
        max_date = None
        for date, data_list in self.runs_by_date.items():
            total = 0
            for data in data_list:
                total += float(data["miles"])
            x_vals.append(date)
            y_vals.append(total)
            total_miles += total
            max_date = date
        title_string = "%f miles run" % total_miles
        import plotly.express as px
        fig = px.bar(x=x_vals, y=y_vals, title=title_string)
        fig.write_html('first_figure.html', auto_open=True)

        max_date = datetime.fromisoformat(max_date)
        max_month = max_date.month
        max_day = max_date.day

        x_vals = []
        y_vals = []
        total_miles = 0
        current_date = None
        for date, data_list in self.legacy_runs_by_date.items():

            current_date = datetime.fromisoformat(date)
            current_month = current_date.month
            current_day = current_date.day
            if current_month > max_month and current_day > max_day:
                break

            total = 0
            for data in data_list:
                total += float(data["miles"])
            x_vals.append(date)
            y_vals.append(total)
            total_miles += total
        title_string = "%f miles run" % total_miles
        import plotly.express as px
        fig = px.bar(x=x_vals, y=y_vals, title=title_string)
        fig.write_html('second_figure.html', auto_open=True)
        return True

    def get_stats(self):
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
        if total_runs == 0:
            avg_miles_per_run = 0
        else:
            avg_miles_per_run = total_miles/total_runs
        avg_runs_per_day = total_runs/day_of_year
        avg_miles_per_day = total_miles/day_of_year
        needed_avg = miles_remaining/days_left
        return {
            "day_of_year": day_of_year,
            "days_left": days_left,
            "total_runs": total_runs,
            "total_miles": total_miles,
            "miles_remaining": miles_remaining,
            "avg_miles_per_run": avg_miles_per_run,
            "avg_runs_per_day": avg_runs_per_day,
            "avg_miles_per_day": avg_miles_per_day,
            "needed_avg": needed_avg
        }

    def print_stats(self):
        stats = self.get_stats()
        print("\n")
        print("\tDay of year: %d\n" % stats["day_of_year"])
        print("\tDays left: %d\n" % stats["days_left"])
        print("\tNumber of runs: %d\n" % stats["total_runs"])
        print("\tNumber of miles: %f\n" % stats["total_miles"])
        print("\tNumber of miles remaining until goal: %f\n" % stats["miles_remaining"])
        print("\tMiles per run avg: %f\n" % stats["avg_miles_per_run"])
        print("\tRuns per day avg: %f\n" % stats["avg_runs_per_day"])
        print("\tMiles per day avg: %f\n" % stats["avg_miles_per_day"])
        print("\tMiles per day avg (needed for goal): %f\n" % stats["needed_avg"])
        print("\n")
        return True
