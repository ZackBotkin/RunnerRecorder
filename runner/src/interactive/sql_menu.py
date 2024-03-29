from interactive_menu.src.interactive_menu import InteractiveMenu

class SqlMenu(InteractiveMenu):
    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            ReadData(manager, self.path),
            InsertRoutes(manager, self.path),
            Count(manager, self.path),
            MigrateData(manager, self.path),
            MigrateToNewDb(manager, self.path),
            ReadFromNewDb(manager, self.path),
            DeleteSql(manager, self.path),
            DropSql(manager, self.path)
        ]
    def title(self):
        return "Sql"

class MigrateData(InteractiveMenu):
    def title(self):
        return "Migrate"
    def main_loop(self):
        self.manager.migrate_data()
        self.manager.reload()
class MigrateToNewDb(InteractiveMenu):
    def title(self):
        return "Test"
    def main_loop(self):
        self.manager.migrate_all_data_to_new_db()
class ReadFromNewDb(InteractiveMenu):
    def title(self):
        return "Test2"
    def main_loop(self):
        self.manager.read_data_from_migrated_db()

class InsertRoutes(InteractiveMenu):
    def title(self):
        return "Insert"
    def main_loop(self):
        self.manager.insert_default_routes()

class ReadData(InteractiveMenu):
    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            ReadRuns(manager, self.path),
            ReadRoutes(manager, self.path)
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
    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RunsCount(manager, self.path),
            RoutesCount(manager, self.path)
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
    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            DeleteRuns(manager, self.path),
            DeleteRoutes(manager, self.path),
            DeleteShoes(manager, self.path)
        ]
    def title(self):
        return "Delete"

class DeleteRuns(InteractiveMenu):
    def title(self):
        return "Runs"
    def main_loop(self):
        print("For which date? (YYYY-MM-DD) (hit enter to delete everything)")
        run_date = self.fancy_input()
        if run_date == '':
            self.manager.delete_runs()
        else:
            self.manager.delete_runs(run_date=run_date)
        self.manager.reload()

class DeleteRoutes(InteractiveMenu):
    def title(self):
        return "Routes"
    def main_loop(self):
        self.manager.delete_routes()
        self.manager.reload()

class DeleteShoes(InteractiveMenu):
    def title(self):
        return "Shoes"
    def main_loop(self):
        self.manager.delete_shoes()
        self.manager.reload()

class DropSql(InteractiveMenu):
    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            DropShoes(manager, self.path)
        ]
    def title(self):
        return "Drop"

class DropShoes(InteractiveMenu):
    def title(self):
        return "Shoes"
    def main_loop(self):
        self.manager.drop_shoes_table()

