from interactive_menu.src.interactive_menu import InteractiveMenu

class EditMenu(InteractiveMenu):

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
