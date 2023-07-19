
from src.interactive.interactive_menu import InteractiveMenu

class RoutesMenu(InteractiveMenu):

    def __init__(self, manager):
        self.manager = manager
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
        print("What is the name of the new route?")
        new_route_name = self.fancy_input()
        print("How many miles is this route?")
        new_route_distance = self.fancy_input()
        print("Enter a description for this route")
        new_route_description = self.fancy_input()
        print("%s %s miles %s ... correct?" % (new_route_name, new_route_distance, new_route_description))
        answer = self.fancy_input()
        if answer in ["yes", "Yes", "correct"]:
            self.manager.add_route(new_route_name, new_route_distance, new_route_description)
            self.manager.reload()
        else:
            print("Aborting!")

class ShowMenu(InteractiveMenu):

    def title(self):
        return "Show"

    def main_loop(self):
        self.manager.print_all_routes()

