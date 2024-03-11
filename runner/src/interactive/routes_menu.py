from interactive_menu.src.interactive_menu import InteractiveMenu

class RoutesMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            AddMenu(manager),
            ShowMenu(manager)
        ]

    def title(self):
        return "Routes"

class AddMenu(InteractiveMenu):

    def title(self):
        return "Add"

    def main_loop(self):

        form_results = self.interactive_form(
            [
                {
                    "question": "What is the name of the new route?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "new_route_name",
                    "default": "",
                    "allow_empty": False
                },
                {
                    "question": "How many miles is this route?",
                    "expected_response_type": "INT",
                    "return_as": "num_miles",
                    "default": "",
                    "allow_empty": False
                },
                {
                    "question": "Enter a description for this route",
                    "expected_response_type": "VARCHAR",
                    "return_as": "route_description",
                    "default": "",
                    "allow_empty": False
                }
            ]
        )
        if form_results["user_accept"] != True:
            print("Aborting!")
            return
        form_results.pop("user_accept")
        for answer_key in form_results.keys():
            if not form_results[answer_key]["valid"]:
                print("%s is not a valid value! Aborting" % answer_key)
                return

        new_route_name = form_results["new_route_name"]["value"]
        new_route_distance = form_results["num_miles"]["value"]
        new_route_description = form_results["route_description"]["value"]
        self.manager.add_route(new_route_name, new_route_distance, new_route_description)
        self.manager.reload()

class ShowMenu(InteractiveMenu):

    def title(self):
        return "Show"

    def main_loop(self):
        self.manager.print_all_routes()

