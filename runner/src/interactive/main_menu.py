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

class MainMenu(InteractiveMenu):

    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            RecordMenu(manager),
            EditMenu(manager),
            AllMenu(manager),
            StatsMenu(manager),
            GraphMenu(manager),
            RoutesMenu(manager),
            ShoesMenu(manager)
        ] 
        if manager.config.get('enable_direct_sql'):
            self.sub_menu_modules.append(SqlMenu(manager))
