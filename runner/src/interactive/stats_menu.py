from interactive_menu.src.interactive_menu import InteractiveMenu

class StatsMenu(InteractiveMenu):

    def title(self):
        return "Stats"

    def main_loop(self):
        self.manager.print_stats()
