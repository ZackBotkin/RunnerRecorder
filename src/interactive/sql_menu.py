
from src.interactive.interactive_menu import InteractiveMenu

class SqlMenu(InteractiveMenu):
    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            ReadData(manager),
            InsertRoutes(manager),
            Count(manager),
            MigrateData(manager),
            DeleteSql(manager)
        ]
    def title(self):
        return "Sql"

class MigrateData(InteractiveMenu):
    def title(self):
        return "Migrate"
    def main_loop(self):
        self.manager.migrate_data()
        self.manager.reload()

class InsertRoutes(InteractiveMenu):
    def title(self):
        return "Insert"
    def main_loop(self):
        self.manager.insert_default_routes()

class ReadData(InteractiveMenu):
    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            ReadRuns(manager),
            ReadRoutes(manager)
        ]
    def title(self):
        return "Read"
class ReadRuns(InteractiveMenu):
    def title(self):
        return "Runs"
    def main_loop(self):
        self.manager.read_runs()
class ReadRoutes(InteractiveMenu):
    def title(self):
        return "Routes"
    def main_loop(self):
        self.manager.read_routes()

class Count(InteractiveMenu):
    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            RunsCount(manager),
            RoutesCount(manager)
        ]
    def title(self):
        return "Count"

class RunsCount(InteractiveMenu):
    def title(self):
        return "Runs"
    def main_loop(self):
        self.manager.runs_count()
class RoutesCount(InteractiveMenu):
    def title(self):
        return "Routes"
    def main_loop(self):
        self.manager.routes_count()

class DeleteSql(InteractiveMenu):
    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            DeleteRuns(manager),
            DeleteRoutes(manager)
        ]
    def title(self):
        return "Delete"

class DeleteRuns(InteractiveMenu):
    def title(self):
        return "Runs"
    def main_loop(self):
        self.manager.delete_runs()
        self.manager.reload()

class DeleteRoutes(InteractiveMenu):
    def title(self):
        return "Routes"
    def main_loop(self):
        self.manager.delete_routes()
        self.manager.reload()



