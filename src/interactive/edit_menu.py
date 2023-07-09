
from src.interactive.interactive_menu import InteractiveMenu

class EditMenu(InteractiveMenu):

    def title(self):
        return "Edit"

    def main_loop(self):
        print("Which date (YYYY-MM-DD) do you want to edit?\n")
        print("(currently cannot do this for dates with more than one run)\n")
        print("Back, Exit\n")
        run_date = self.fancy_input(" ")
        if run_date in ['Back', 'back']:
            return
        if run_date in ['Exit', 'exit']:
            exit()
        runs_on_date = self.manager.get_runs_on_date(run_date=run_date)
        if len(runs_on_date) == 0:
            print("No runs on date %s found" % run_date)
        elif len(runs_on_date) > 1:
            print("More than one run on date %s currently found" % run_date)
        else:
            print("New route name?")
            new_route_name = self.fancy_input(" ")
            print("New route distance?")
            new_route_distance = self.fancy_input(" ")
            print("New route comment?")
            new_route_comment = self.fancy_input(" ")
            print("%s %s %s .... correct?" % (new_route_name, new_route_distance, new_route_comment))
            answer = self.fancy_input(" ")
            if answer in ["yes", "Yes", "correct"]:
                self.manager.edit_run(run_date, new_route_name, new_route_distance, new_route_comment)
                self.manager.reload()
            else:
                print("Aborting!")
