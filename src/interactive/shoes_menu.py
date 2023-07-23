
from src.interactive.interactive_menu import InteractiveMenu

class ShoesMenu(InteractiveMenu):

    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            AddShoeMenu(manager),
            ShowShoesMenu(manager),
            RetireShoeMenu(manager)
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

class RetireShoeMenu(InteractiveMenu):
    def title(self):
        return "Retire"
    def main_loop(self):
        print("What is the nickname of the shoe to be retired?")
        nickname = self.fancy_input()
        existing_shoe = self.manager.get_shoe_with_nickname(nickname)
        if existing_shoe is None:
            print("No shoe with name '%s' found")
        else:
            print("What date should the shoe be retired (YYYY-MM-DD)?")
            answer = self.fancy_input()
            self.manager.retire_existing_shoe(nickname, answer)
            print("Retired shoe!")


