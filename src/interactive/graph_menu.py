
from src.graph.grapher import Grapher
from src.interactive.interactive_menu import InteractiveMenu

class GraphMenu(InteractiveMenu):

    def title(self):
        return "Graphs"

    def main_loop(self):

        GRAPH_CHOICES = ['bar', 'line', 'historical', 'weeks', 'routes', 'miles_per_route', 'routes_pie']
        print("Which graph type would you like? (bar, line, historical, weeks, routes, miles_per_route, routes_pie)\n")
        answer = self.fancy_input(" ")
        answer_is_in_choices = answer in GRAPH_CHOICES
        while not answer_is_in_choices:
            print("That isn't a valid choice")
            print("Which graph type would you like? (bar, line, historical, weeks, routes, miles_per_route, routes_pie)\n")
            answer = self.fancy_input(" ")
            answer_is_in_choices = answer in GRAPH_CHOICES

        if answer == "bar":
            self.manager.graph_all_runs()
        if answer == "line":
            self.manager.line_graph_all_runs()
        if answer == "historical":
            self.manager.historical_graph_all_runs()
        if answer == "weeks":
            self.manager.weekly_graph()
        if answer == "routes":
            self.manager.routes_graph()
        if answer == "miles_per_route":
            self.manager.miles_per_route_graph()
        if answer == "routes_pie":
            self.manager.pie_chart_routes_graph()

        return True

