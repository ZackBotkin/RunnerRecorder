import json
from src.interactive.all_menu import AllMenu
from src.interactive.edit_menu import EditMenu
from src.interactive.graph_menu import GraphMenu
from src.interactive.interactive_menu import InteractiveMenu
from src.interactive.record_menu import RecordMenu
from src.interactive.routes_menu import RoutesMenu
from src.interactive.sql_menu import SqlMenu
from src.interactive.stats_menu import StatsMenu
from src.interactive.shoes_menu import ShoesMenu

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
