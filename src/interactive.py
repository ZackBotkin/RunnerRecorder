import json

class InteractiveRunner(object):

    def __init__(self, runner):
        self.runner = runner
        self.main_menu = '(' + ', '.join(runner.config.get("main_menu_options")) + ')'
        self.default_runs = '(' + ', '.join(runner.config.get("default_run_options")) + ')'

    def fancy_print(self, text):
        print("%s %s" % (self.runner.config.get("line_start"), text))

    def fancy_input(self, text):
        answer = input("%s %s" % (self.runner.config.get("line_start"), text))
        answer = answer.strip()
        return answer

    def main_loop(self):
        self.fancy_print("Welcome to runner reader\n")
        self.interactive_loop()
        
    def interactive_loop(self):
        return_result = False
        exit_result = False
        while not exit_result:
            answer = self.fancy_input("What do you want to do? %s\n" % self.main_menu)
            if answer in self.runner.config.get("record_run_answers"):
                return_result = self.record_run_interactive()
                self.runner.reload()
                exit_result = False
            elif answer in self.runner.config.get("all_run_answers"):
                return_result = self.runner.print_all_runs()
                exit_result = False
            elif answer in self.runner.config.get("running_stat_answers"):
                return_result = self.runner.print_stats()
                exit_result = False
            elif answer in self.runner.config.get("graph_answers"):
                return_result = self.graph_run_interactive()
                exit_result = False
            elif answer in self.runner.config.get("route_answers"):
                return_result = self.routes_interactive()
                exit_result = False
            ## Temporary methods while I am migrating data around
            elif answer in ["migrate", "migrate_data"]:
                self.runner.migrate_data()
                exit_result = False
                self.runner.reload()
            elif answer == "create_table":
                #self.runner.create_table()
                exit_result = False
            elif answer in ["read_data", "table_data", "db_data"]:
                self.runner.read_data()
                exit_result = False
            elif answer == "delete_data":
                #self.runner.delete_data()
                exit_result = False
                self.runner.reload()
            elif answer == "drop_table":
                #self.runner.reader_writer.drop_routes_table()
                exit_result = False

            ## NOTE : this is highly suspect to abuse, and should
            ## eventually get rid of this
            elif answer == "sql":
                self.runner.run_sql()
                self.runner.reload()
                exit_result = False
            elif answer in self.runner.config.get("exit_answers"):
                exit_result = True
            else:
                self.fancy_print("Unknown answer type. Please pick again\n")


        self.fancy_print("Bye bye")

    def record_run_interactive(self):

        done = False
        self.fancy_print("Good for you! Lets record a run!\n")
        answer = self.fancy_input("Which run? Type one of the defaults, type \"new\" to enter a new run, or type \"show\" to show the defaults or \"exit\" to quit\n")


        if answer in self.runner.default_run_options:
            comment = self.get_comment_interactive()
            self.fancy_print("Recording %s run!\n" % answer)
            self.runner.write_run(answer, comment)
        elif answer in ['new', 'NEW', 'New']:
            self.fancy_print("Ok, lets record a new run!")
            self.record_new_run_interactive()
        elif answer in ['show', 'SHOW', 'Show']:
            self.fancy_print(self.default_runs)
        elif answer in self.runner.config.get("exit_answers"):
            done = True
        else:
            self.fancy_print('Please pick an existing run, or say \"new\"')

        while not done:
            answer = self.fancy_input("Are you done recording runs?\n")

            if answer in ["Yes", "yes", "y"]:
                return True
            elif answer in ["No", "no", "n"]:
                done = self.record_run_interactive()
                return False
            else:
                self.fancy_print("Cmon man pick a real answer\n")

        return True

    ## TODO : have some sort of support to save the route if doing it this way... honestly sort of low priority though since I dont use this use case a whole lot
    def record_new_run_interactive(self):
        route_name = self.fancy_input("What is the name of the new route?\n")
        number_of_miles = self.fancy_input("What is the number of miles on this route?\n")
        ## TODO : some validation of the inputted date
        date_of_run = self.fancy_input("What is the date of the run? (just type ENTER for today)\n")
        self.runner.write_new_run({
            "route_name": route_name,
            "miles": number_of_miles,
            "date": date_of_run
        })
        return True

    def get_comment_interactive(self):
        answer = self.fancy_input("Comment on this run? Just hit enter to proceed without a comment\n")
        if answer == "":
            return None
        else:
            return answer

    ## TODO : this is starting to become cumbersome, and should probably be refactored into a "grapher" class or something
    def graph_run_interactive(self):
        GRAPH_CHOICES = ['bar', 'line', 'historical', 'weeks', 'routes', 'miles_per_route', 'routes_pie']
        answer = self.fancy_input("Which graph type would you like? (bar, line, historical, weeks, routes, miles_per_route, routes_pie)\n")
        answer_is_in_choices = answer in GRAPH_CHOICES
        while not answer_is_in_choices:
            self.fancy_print("That isn't a valid choice")
            answer = self.fancy_input("Which graph type would you like? (bar, line, historical, weeks, routes, miles_per_route, routes_pie)\n")
            answer_is_in_choices = answer in GRAPH_CHOICES

        if answer == "bar":
            self.runner.graph_all_runs()
        if answer == "line":
            self.runner.line_graph_all_runs()
        if answer == "historical":
            self.runner.historical_graph_all_runs()
        if answer == "weeks":
            self.runner.weekly_graph()
        if answer == "routes":
            self.runner.routes_graph()
        if answer == "miles_per_route":
            self.runner.miles_per_route_graph()
        if answer == "routes_pie":
            self.runner.pie_chart_routes_graph()

        return True

    ## right now this just prints, but this will be the entry
    ## point for adding routes and stuff like that
    def routes_interactive(self):

        ROUTE_CHOICES = ['add', 'show', 'delete', 'quit']

        answer = self.fancy_input('What would you like to do? (add, show, delete, quit)\n')
        answer_in_choices = answer in ROUTE_CHOICES
        while not answer_in_choices:
            self.fancy_print("That isn't a valid choice\n")
            answer = self.fancy_input('What would you like to do? (add, show, delete, quit)\n')
            answer_is_in_choices = answer in ROUTE_CHOICES

        if answer == "add":
            self.add_new_route_interactive()
        if answer == "show":
            self.runner.print_all_routes()
            print("\n")
        if answer == "delete":
            self.delete_route_interactive()

        return True

    def add_new_route_interactive(self):

        route_name = self.fancy_input('What is the name of the new route?\n')

        ## TODO enforce that this is a number
        miles = self.fancy_input('How many miles is this route?\n')
        description = self.fancy_input('Enter a description for this route.\n')

        answer = self.fancy_input('route_name: %s, miles: %s, description: %s\n correct?\n' %(route_name, miles, description))

        ## TODO - this should go in the config as "affirmative answers' or w/e
        if answer in ['yes', 'Yes', 'y', 'correct']:

            ## TODO -- implement this
            self.runner.add_route(route_name, miles, description)
        else:
            self.fancy_print("aborting\n")

        return True

    def delete_route_interactive(self):
        return True
