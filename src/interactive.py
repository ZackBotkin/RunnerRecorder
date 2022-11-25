import json


## TODO : put some of this stuff inside a config module of sorts
LINE_START = ">>>" 

MAIN_MENU_OPTIONS = ['record', 'all', 'stats', 'exit']
MAIN_MENU = '(' + ', '.join(MAIN_MENU_OPTIONS) + ')'

RECORD_RUN_ANSWERS = [
    'record', 'record_run', 'record run'
]

ALL_RUNS_ANSWERS = [
    'all', 'all_runs', 'list'
]

RUNNING_STAT_ANSWERS = [
    'stats', 'running_stats'
]
GRAPH_ANSWERS = [
    'graph'
]

EXIT_ANSWERS = [
    'exit', 'done'
]

DEFAULT_RUN_OPTIONS = [
    'grand', 'roosevelt', 'lake', 'lakeshore', 'sedgewick', 'kingsbury'
]
DEFAULT_RUNS = '(' + ', '.join(DEFAULT_RUN_OPTIONS) + ')'

def fancy_print(text):
    print("%s %s" % (LINE_START, text))

def fancy_input(text):
    answer = input("%s %s" % (LINE_START, text))
    return answer

class InteractiveRunner(object):

    def __init__(self, runner):
        self.runner = runner

    def main_loop(self):
        fancy_print("Welcome to runner reader\n")
        self.interactive_loop()
        
    def interactive_loop(self):
        return_result = False
        while not return_result:
            answer = fancy_input("What do you want to do? %s\n" % MAIN_MENU)
            if answer in RECORD_RUN_ANSWERS:
                return_result = self.record_run_interactive()
            elif answer in ALL_RUNS_ANSWERS:
                return_result = self.runner.print_all_runs()
            elif answer in RUNNING_STAT_ANSWERS:
                return_result = self.runner.print_stats()
            elif answer in GRAPH_ANSWERS:
                return_result = self.runner.graph_all_runs()
            elif answer in EXIT_ANSWERS:
                return_result = True
            else:
                fancy_print("Unknown answer type. Please pick again\n")

            if return_result:
                answer = fancy_input("Are you all done?\n")
                if answer in ["Yes", "yes", "y"]:
                    return_result = True
                else:
                    self.runner._load_from_disk()
                    return_result = False
        fancy_print("Bye bye")

    def record_run_interactive(self):

        done = False
        fancy_print("Good for you! Lets record a run!\n")
        answer = fancy_input("Which run? Type one of the defaults, type \"new\" to enter a new run, or type \"show\" to show the defaults or \"exit\" to quit\n")
        if answer in DEFAULT_RUN_OPTIONS:
            fancy_print("Recording %s run!\n" % answer)
            self.runner.write_run_to_disk(answer)
        elif answer in ['new', 'NEW', 'New']:
            fancy_print("Ok, lets record a new run!")
            self.record_new_run_interactive()
        elif answer in ['show', 'SHOW', 'Show']:
            fancy_print(DEFAULT_RUNS)
        elif answer in EXIT_ANSWERS:
            done = True
        else:
            fancy_print('Please pick an existing run, or say \"new\"')

        while not done:
            answer = fancy_input("Are you done?\n")
            if answer in ["Yes", "yes", "y"]:
                return True
            elif answer in ["No", "no", "n"]:
                done = self.record_run_interactive()
                return False
            else:
                fancy_print("Cmon man pick a real answer\n")

        return True

    def record_new_run_interactive(self):
        route_name = fancy_input("What is the name of the new route?\n")
        number_of_miles = fancy_input("What is the number of miles on this route?\n")
        ## TODO : some validation of the inputted date
        date_of_run = fancy_input("What is the date of the run? (just type ENTER for today)\n")
        self.runner.write_new_run_to_disk({
            "route_name": route_name,
            "miles": number_of_miles,
            "date": date_of_run
        })



