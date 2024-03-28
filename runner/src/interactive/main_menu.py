import json

from interactive_menu.src.interactive_menu import InteractiveMenu
from runner.src.interactive.runs_menu import RunsMenu
from runner.src.interactive.routes_menu import RoutesMenu
from runner.src.interactive.shoes_menu import ShoesMenu
from runner.src.interactive.stats_menu import StatsMenu
from runner.src.interactive.graph_menu import GraphMenu
from runner.src.interactive.config_menu import ConfigMenu
from runner.src.interactive.backup_menu import BackupMenu
from runner.src.interactive.about_menu import AboutMenu
from runner.src.interactive.sql_menu import SqlMenu

class MainMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RunsMenu(manager, self.path),
            RoutesMenu(manager, self.path),
            ShoesMenu(manager, self.path),
            StatsMenu(manager, self.path),
            GraphMenu(manager, self.path),
            ConfigMenu(manager, self.path),
            BackupMenu(manager, self.path),
            AboutMenu(manager, self.path)
        ] 
        if manager.config.get('enable_direct_sql'):
            self.sub_menu_modules.append(SqlMenu(manager))

    def title(self):
        return "RunnerReader"
