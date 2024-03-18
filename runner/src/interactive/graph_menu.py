from runner.src.graph.grapher import Grapher
from interactive_menu.src.interactive_menu import InteractiveMenu

class GraphMenu(InteractiveMenu):

    def title(self):
        return "Graphs"

    def main_loop(self):

        GRAPH_CHOICES = ['bar', 'line', 'historical', 'weeks', 'routes', 'miles_per_route', 'routes_pie']

        form_init = {
                        "question": "Which graph type would you like?\n\t(bar, line, historical, weeks, routes, miles_per_route, routes_pie)",
                        "expected_response_type": "VARCHAR",
                        "return_as": "graph_type",
                        "default": "",
                        "allow_empty": False
                    }

        form_results = self.interactive_form([form_init])

        if form_results["user_accept"] != True:
            print("Aborting!")
            return
        form_results.pop("user_accept")
        for answer_key in form_results.keys():
            if not form_results[answer_key]["valid"]:
                print("%s is not a valid value! Aborting" % answer_key)
                return

        graph_type = form_results["graph_type"]["value"]
        while graph_type not in GRAPH_CHOICES:
            form_results = self.interactive_form([form_init])
            if form_results["user_accept"] != True:
                print("Aborting!")
                return
            form_results.pop("user_accept")
            for answer_key in form_results.keys():
                if not form_results[answer_key]["valid"]:
                    print("%s is not a valid value! Aborting" % answer_key)
                    return
            graph_type = form_results["graph_type"]["value"]

        if graph_type == "bar":
            self.manager.graph_all_runs()
        if graph_type == "line":
            self.manager.line_graph_all_runs()
        if graph_type == "historical":
            self.manager.historical_graph_all_runs()
        if graph_type == "weeks":
            self.manager.weekly_graph()
        if graph_type == "routes":
            self.manager.routes_graph()
        if graph_type == "miles_per_route":
            self.manager.miles_per_route_graph()
        if graph_type == "routes_pie":
            self.manager.pie_chart_routes_graph()

        return True

