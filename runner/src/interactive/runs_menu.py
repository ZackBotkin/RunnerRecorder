from interactive_menu.src.interactive_menu import InteractiveMenu

class RunsMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordRunMenu(manager, self.path),
            EditRunMenu(manager, self.path),
            ShowRunsMenu(manager, self.path)
        ]

    def title(self):
        return "Runs"

class RecordRunMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordDefaultRunMenu(manager, self.path),
            RecordNewRunMenu(manager, self.path)
        ]

    def title(self):
        return "Record"

class RecordDefaultRunMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        routes = manager.get_routes()
        self.sub_menu_modules = []
        for route in routes:
            self.sub_menu_modules.append(
                DefaultRunChoiceMenu(manager, self.path, route["route_name"])
            )

    def title(self):
        return "Defaults"

class DefaultRunChoiceMenu(InteractiveMenu):

    def main_loop(self):
        print("Recording a run for %s" % self.title_text)

class RecordNewRunMenu(InteractiveMenu):

    def title(self):
        return "New"

class EditRunMenu(InteractiveMenu):

    def title(self):
        return "Edit"

class ShowRunsMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            ShowAllRunsMenu(manager, self.path),
            ShowRunRange(manager, self.path)
        ]

    def title(self):
        return "Show"

class ShowAllRunsMenu(InteractiveMenu):

    def title(self):
        return "All"

class ShowRunRange(InteractiveMenu):

    def title(self):
        return "Range"
