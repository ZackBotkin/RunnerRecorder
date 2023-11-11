from interactive_menu.src.interactive_menu import InteractiveMenu

class StatsMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            MainStatsMenu(manager, self.path),
            HistoricalStatsMenu(manager, self.path)
        ]

    def title(self):
        return "Stats"

class MainStatsMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            YearStatsMenu(manager, self.path),
            MonthStatsMenu(manager, self.path),
            WeekStatsMenu(manager, self.path)
        ]

    def title(self):
        return "Main"

class YearStatsMenu(InteractiveMenu):

    def title(self):
        return "Year"

    def main_loop(self):
        self.manager.print_stats()

class MonthStatsMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = []
        for month in ["January", "February", "March", "April", "May", "June"]:
            self.sub_menu_modules.append(
                IndividualMonthStatsMenu(manager, self.path, month)
            )

    def title(self):
        return "Month"

class IndividualMonthStatsMenu(InteractiveMenu):
    def main_loop(self):
        print("Recording a run for %s" % self.title_text)

class WeekStatsMenu(InteractiveMenu):

    def title(self):
        return "Week"

class HistoricalStatsMenu(InteractiveMenu):

    def title(self):
        return "Historical"
