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
                DefaultRunChoiceMenu(manager, self.path, route["route_name"].capitalize())
            )

    def title(self):
        return "Defaults"

class DefaultRunChoiceMenu(InteractiveMenu):

    def main_loop(self):
        print("Comment on this run?")
        ## TODO : use interactive form here
        comment = self.fancy_input()
        self.manager.write_run(self.title().lower(), comment)
        self.manager.reload()

class RecordNewRunMenu(InteractiveMenu):

    def title(self):
        return "New"

class EditRunMenu(InteractiveMenu):

    def title(self):
        return "Edit"

    def main_loop(self):

        form_results = self.interactive_form(
            [
                {
                    "question": "Which date do you want to edit?",
                    "expected_response_type": "YYYYMMDD_Date",
                    "return_as": "run_to_edit_date",
                    "default": "",
                    "allow_empty": False
                }
            ]
        )

        if form_results["user_accept"] != True:
            print("Aborting!")
            return
        form_results.pop("user_accept")
        for answer_key in form_results.keys():
            if not form_results[answer_key]["valid"]:
                print("%s is not a valid value! Aborting" % answer_key)
                return

        run_to_edit_date = form_results["run_to_edit_date"]["value"]
        runs_on_date = self.manager.get_runs_on_date(run_date=run_to_edit_date)
        if len(runs_on_date) == 0:
            print("No runs on date %s found" % run_to_edit_date)
        elif len(runs_on_date) > 1:
            print("More than one run on date %s currently found" % run_to_edit_date)
        else:
            form_results = self.interactive_form(
                [
                    {
                        "question": "What is the new route name?",
                        "expected_response_type": "VARCHAR",
                        "return_as": "new_route_name",
                        "default": "",
                        "allow_empty": False
                    },
                    {
                        "question": "What is the new route distance in miles?",
                        "expected_response_type": "FLOAT",
                        "return_as": "new_route_distance",
                        "default": "",
                        "allow_empty": False
                    },
                    {
                        "question": "What comment do you want to give the run?",
                        "expected_response_type": "VARCHAR",
                        "return_as": "new_route_comment",
                        "default": "",
                        "allow_empty": True
                    }
                ]
            )
            if form_results["user_accept"] != True:
                print("Aborting!")
                return
            form_results.pop("user_accept")
            for answer_key in form_results.keys():
                if not form_results[answer_key]["valid"]:
                    print("%s is not a valid value! Aborting" % answer_key)
                    return

            new_route_name = form_results["new_route_name"]["value"]
            new_route_distance = form_results["new_route_distance"]["value"]
            new_route_comment = form_results["new_route_comment"]["value"]

            self.manager.edit_run(run_to_edit_date, new_route_name, new_route_distance, new_route_comment)
            self.manager.reload()

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

    def main_loop(self):
        return self.manager.print_all_runs()

class ShowRunRange(InteractiveMenu):

    def title(self):
        return "Range"
