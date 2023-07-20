
from src.interactive.interactive_menu import InteractiveMenu

class ShoesMenu(InteractiveMenu):

    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            AddShoeMenu(manager),
            ShowShoesMenu(manager)
        ]

    def title(self):
        return "Shoes"


class AddShoeMenu(InteractiveMenu):

    def title(self):
        return "Add"

    def main_loop(self):
        print("What is the nickname for the shoe")
        new_shoe_nickname = self.fancy_input()
        print("What is the start date for this shoe? (YYYY-MM-DD)")
        new_shoe_start_date = self.fancy_input()
        print("What is the brand of shoe?")
        new_shoe_brand = self.fancy_input()
        print("%s -- %s -- %s... correct?" % (new_shoe_nickname, new_shoe_start_date, new_shoe_brand) )
        answer = self.fancy_input()
        if answer in ["yes", "Yes", "ok"]:
            self.manager.add_shoe(new_shoe_nickname, new_shoe_start_date, new_shoe_brand)
        else:
            print("Aborting")

class ShowShoesMenu(InteractiveMenu):

    def title(self):
        return "Show"

    def main_loop(self):
        self.manager.print_all_shoes()
