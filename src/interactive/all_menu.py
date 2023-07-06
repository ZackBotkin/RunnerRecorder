
from src.interactive.interactive_menu import InteractiveMenu

class AllMenu(InteractiveMenu):

    def title(self):
        return "All"

    def main_loop(self):
        self.manager.print_all_runs()
        print("")
