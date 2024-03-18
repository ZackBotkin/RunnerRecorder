from datetime import datetime
from interactive_menu.src.interactive_menu import InteractiveMenu

class ShoesMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
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

        form_results = self.interactive_form(
            [
                {
                    "question": "What is the nickname for the shoe?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "new_shoe_nickname",
                    "default": "",
                    "allow_empty": False
                },
                {
                    "question": "What is the start date (YYYY-MM-DD) for this shoe? Hit enter for today",
                    "expected_response_type": "YYYYMMDD_Date",
                    "return_as": "new_shoe_start_date",
                    "default": datetime.now().strftime("%Y-%m-%d"),
                    "allow_empty": False
                },
                {
                    "question": "What is the brand of shoe?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "new_shoe_brand",
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

        new_shoe_nickname = form_results["new_shoe_nickname"]["value"]
        new_shoe_start_date = form_results["new_shoe_start_date"]["value"]
        new_shoe_brand = form_results["new_shoe_brand"]["value"]
        self.manager.add_shoe(new_shoe_nickname, new_shoe_start_date, new_shoe_brand)

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


