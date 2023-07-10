import plotly
from datetime import datetime
from src.util import get_miles_per_week

class Grapher(object):

    def __init__(self, runs_by_date, legacy_runs_by_date):
        self.runs_by_date = runs_by_date
        self.legacy_runs_by_date = legacy_runs_by_date

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
