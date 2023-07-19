
from src.interactive.interactive_menu import InteractiveMenu

class RecordMenu(InteractiveMenu):

    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            DefaultRunsMenu(manager),
            NewRunMenu(manager)
        ]
    def title(self):
        return "Record"

class DefaultRunsMenu(InteractiveMenu):

    def title(self):
        return "Defaults"

    def main_loop(self):
        default_run_options = self.manager.default_run_options
        back_result = False
        while not back_result:
            print("\nPlease pick one of ")
            self.menu_print(default_run_options)
            print("Back, Exit")
            answer = self.fancy_input()
            if answer in default_run_options:
                print("Comment on this run? (Enter for empty comment)")
                comment = self.fancy_input()
                self.manager.write_run(answer, comment)
                print("All done?")
                answer = self.fancy_input()
                if answer in ["yes", "Yes", "y"]:
                    back_result = True
                else:
                    back_result = False
            elif answer in ['Back', 'back']:
                back_result = True
            elif answer in ['exit', 'Exit']:
                exit()
            else:
                back_result = False

        self.manager.reload()

class NewRunMenu(InteractiveMenu):

    def title(self):
        return "New"

