import plotly
from datetime import datetime
from src.util import get_miles_per_week

#
#   TODO : in general refactoring idea
#       - interactive --> get user input
#       - runner --> "manager" of the data, deals with classes, not database
#       - reader_writer --> talks to the database, in theory, you could swap this out
#               and the runner would be none the wiser
#

#
#   TODO : this should probably now be re-named manager
#

class RunnerReader(object):

    def __init__(self, configs, input_source, output_sources):

        self.config = configs

        self.input_source = input_source
        self.output_sources = output_sources

        self.runs_by_date = self.input_source.get_runs()
        self.legacy_runs_by_date = self.input_source.get_legacy_runs()

        self.routes = self.get_routes()

        self.default_run_options = []

        for route in self.routes:
            self.default_run_options.append(route['route_name'])

    def reload(self):
        self.runs_by_date = self.input_source.get_runs()

    def write_run(self, route_name, comment=None):
        for output_source in self.output_sources:
            output_source.add_run(route_name, comment)

    def add_route(self, route_name, miles, description):
        miles = float(miles)
        for output_source in self.output_sources:
            output_source.add_route(route_name, miles, description)

    def get_routes(self):
        return self.input_source.get_routes()

    def get_runs_on_date(self, run_date):
        runs = self.input_source.get_runs(run_date=run_date)
        return runs

    def edit_run(self, run_date, route_name, distance, comment):
        for output_source in self.output_sources:
            output_source.edit_run(run_date, route_name, distance, comment)

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
        routes = self.get_routes()
        all_data = [('Route Name', 'Distance', 'Description')]
        import pandas as pd
        for route in routes:
            all_data.append(
                (
                    route['route_name'],
                    "%f miles" % route['miles'],
                    route['description']
                )
            )
        df = pd.DataFrame(all_data)
        print(df.to_string(index=False))
        return True

    ## TODO : this should most likely be refactored into a "Grapher" class
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

    def weekly_graph(self):
        x_vals = []
        y_vals = []
        total_miles = 0

        miles_per_week = get_miles_per_week(self.runs_by_date, 2023) ## TODO do not hardcode
        for week in miles_per_week:
            x_vals.append(week.start_date)
            y_vals.append(week.total_miles)
            total_miles += week.total_miles

        title_string = "%f miles run" % total_miles
        import plotly.express as px
        fig = px.bar(x=x_vals, y=y_vals, title=title_string)
        fig.write_html('first_figure.html', auto_open=True)
        return True

    def routes_graph(self):
        route_count = {}
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                route_name = data["route_name"]
                if route_name not in route_count:
                    route_count[route_name] = 1
                else:
                    route_count[route_name] += 1

        x_vals = []
        y_vals = []
        for route_name, count in route_count.items():
            x_vals.append(route_name)
            y_vals.append(count)

        import plotly.express as px
        fig = px.bar(x=x_vals, y=y_vals, title="Routes")
        fig.write_html('first_figure.html', auto_open=True)
        return True

    def pie_chart_routes_graph(self):
        route_count = {}
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                route_name = data["route_name"]
                if route_name not in route_count:
                    route_count[route_name] = 1
                else:
                    route_count[route_name] += 1
        labels = []
        values = []
        for route_name, count in route_count.items():
            labels.append(route_name)
            values.append(count)

        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.show()
        return True

    def miles_per_route_graph(self):
        miles_per_route = {}
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                route_name = data["route_name"]
                if route_name not in miles_per_route:
                    miles_per_route[route_name] = data["miles"]
                else:
                    miles_per_route[route_name] += data["miles"]

        x_vals = []
        y_vals = []
        for route_name, total in miles_per_route.items():
            x_vals.append(route_name)
            y_vals.append(total)

        import plotly.express as px
        fig = px.bar(x=x_vals, y=y_vals, title="Routes")
        fig.write_html('first_figure.html', auto_open=True)
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
        miles_per_week = get_miles_per_week(self.runs_by_date, 2023) ## TODO : do not hardcode
        avg_miles_per_week = total_miles/len(miles_per_week)
        this_week = miles_per_week[-1]

        return {
            "day_of_year": day_of_year,
            "days_left": days_left,
            "goal": goal_number,
            "on_pace_for": avg_miles_per_day * 365, ## TODO leap year bug
            "total_runs": total_runs,
            "total_miles": total_miles,
            "miles_remaining": miles_remaining,
            "avg_miles_per_run": avg_miles_per_run,
            "avg_runs_per_day": avg_runs_per_day,
            "avg_miles_per_day": avg_miles_per_day,
            "needed_avg": needed_avg,
            "avg_miles_per_week": avg_miles_per_week,
            "miles_this_week": this_week.total_miles
        }

    def print_stats(self):
        stats = self.get_stats()
        print("\n")
        print("\tDay of year: %d\n" % stats["day_of_year"])
        print("\tDays left: %d\n" % stats["days_left"])
        print("\tGoal: %d\n" % stats["goal"])
        print("\tOn pace for: %f\n" % stats["on_pace_for"])
        print("\tNumber of runs: %d\n" % stats["total_runs"])
        print("\tNumber of miles: %f\n" % stats["total_miles"])
        print("\tNumber of miles remaining until goal: %f\n" % stats["miles_remaining"])
        print("\tMiles per run avg: %f\n" % stats["avg_miles_per_run"])
        print("\tRuns per day avg: %f\n" % stats["avg_runs_per_day"])
        print("\tMiles per day avg: %f\n" % stats["avg_miles_per_day"])
        print("\tMiles per day avg (needed for goal): %f\n" % stats["needed_avg"])
        print("\tMiles per week avg: %f\n" % stats["avg_miles_per_week"])
        print("\tMiles this week: %f\n" % stats["miles_this_week"])
        print("\n")
        return True

    ## TODO : eventually get rid of these, they do not belong on the maanger
    def run_sql(self):
        raise Exception("Not implemented")

    def read_data(self):
        raise Exception("Not implemented")

    def delete_data(self):
        raise Exception("Not implemented")

    def delete_routes(self):
        raise Exception("Not implemented")

    def migrate_data(self):
        raise Exception("Not implemented")
