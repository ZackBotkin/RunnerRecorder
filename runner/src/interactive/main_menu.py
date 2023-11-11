import json

from interactive_menu.src.interactive_menu import InteractiveMenu
from runner.src.interactive.all_menu import AllMenu
from runner.src.interactive.edit_menu import EditMenu
from runner.src.interactive.graph_menu import GraphMenu
from runner.src.interactive.record_menu import RecordMenu
from runner.src.interactive.routes_menu import RoutesMenu
from runner.src.interactive.sql_menu import SqlMenu
from runner.src.interactive.stats_menu import StatsMenu
from runner.src.interactive.shoes_menu import ShoesMenu
from runner.src.interactive.runs_menu import RunsMenu

class MainMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordMenu(manager, self.path),
            EditMenu(manager, self.path),
            AllMenu(manager, self.path),
            StatsMenu(manager, self.path),
            GraphMenu(manager, self.path),
            RoutesMenu(manager, self.path),
            ShoesMenu(manager, self.path),
            RunsMenu(manager, self.path)
        ] 
        if manager.config.get('enable_direct_sql'):
            self.sub_menu_modules.append(SqlMenu(manager))

    def title(self):
        return "RunnerReader"
