
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

class InteractiveRunner(object):

    def __init__(self, runner):
        self.runner = runner

    def main_loop(self):
        print("%s Welcome to runner reader\n" % LINE_START)
        self.interactive_loop()
        
    def interactive_loop(self):
        return_result = False
        while not return_result:
            answer = input("%s What do you want to do? %s\n" % (LINE_START, MAIN_MENU))
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
                print("%s Unknown answer type. Please pick again \n" % LINE_START)

            if return_result:
                answer = input("%s Are you all done?\n" % LINE_START)
                if answer in ["Yes", "yes", "y"]:
                    return_result = True
                else:
                    return_result = False
        print("%s Bye bye" % LINE_START)

    def record_run_interactive(self):

        done = False
        print("%s Good for you! Lets record a run!\n" % LINE_START)
        answer = input("%s Which run? Type one of the defaults, type \"new\" to enter a new run, or type \"show\" to show the defaults or \"exit\" to quit\n" % LINE_START)
        if answer in DEFAULT_RUN_OPTIONS:
            print("%s Recording %s run!\n" % (LINE_START, answer))
        elif answer in ['new', 'NEW', 'New']:
            print("%s Ok, lets record a new run!" % LINE_START)
        elif answer in ['show', 'SHOW', 'Show']:
            print('%s %s' % (LINE_START, DEFAULT_RUNS))
        elif answer in EXIT_ANSWERS:
            done = True
        else:
            print('%s Please pick an existing run, or say \"new\"' % LINE_START)

        while not done:
            answer = input("%s Are you done?\n" % LINE_START)
            if answer in ["Yes", "yes", "y"]:
                return True
            elif answer in ["No", "no", "n"]:
                done = self.record_run_interactive()
                return False
            else:
                print("%s Cmon man pick a real answer\n" % LINE_START)

        return True






