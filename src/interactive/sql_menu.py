
from src.interactive.interactive_menu import InteractiveMenu

class SqlMenu(InteractiveMenu):

    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = [
            ReadData(manager),
            MigrateData(manager),
            RunSql(manager),
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

class ReadData(InteractiveMenu):

    def title(self):
        return "Read"

    def main_loop(self):
        self.manager.read_data()

class RunSql(InteractiveMenu):

    def title(self):
        return "Run"

    def main_loop(self):
        self.manager.run_sql()
        self.manager.reload()

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
        self.manager.delete_data()
        self.manager.reload()

class DeleteRoutes(InteractiveMenu):

    def title(self):
        return "Routes"

    def main_loop(self):
        self.manager.delete_routes()
        self.manager.reload()



