import argparse
from datetime import datetime, timedelta
from src.runner import RunnerReader
from src.interactive import InteractiveRunner


class Week(object):

    def __init__(self):
        pass


weekday_mappings = {
    0 : 'monday',
    1 : 'tuesday',
    2 : 'wednesday',
    3 : 'thursday',
    4 : 'friday',
    5 : 'saturday',
    6 : 'sunday'
}


def get_start_of_week(from_date, start_of_week='sunday'):
    weekday = weekday_mappings[from_date.weekday()]
    while weekday != start_of_week:
        from_date = from_date - timedelta(days=1)
        weekday = weekday_mappings[from_date.weekday()]
    return from_date


def construct_weeks(from_date, start_of_week='sunday'):

    by_weeks = {}

    year = from_date.year
    start_of_year = datetime(year, 1, 1)

    current_date = get_start_of_week(start_of_year)
    by_weeks[str(current_date)] = Week()

    current_date = current_date + timedelta(days=1)
    while current_date < from_date:
        weekday = weekday_mappings[current_date.weekday()]
        if weekday == start_of_week:
            by_weeks[str(current_date)] = Week()
        current_date = current_date + timedelta(days=1)

    return by_weeks



def main():

    parser = argparse.ArgumentParser(description= 'default parser')
    parser.add_argument('--total', help='running totals')
    parser.add_argument('--print_all_runs', help='print the running files')
    parser.add_argument('--graph_all_runs', help='graph the running files')
    parser.add_argument('--line_graph_all_runs', help='graph the running files as a line graph')
    parser.add_argument('--print_stats', help='print the stats')
    parser.add_argument('--interactive', help='interactive mode')
    args = parser.parse_args()

    DEFAULT_DIRECTORY="C:\\Users\\zackb\\Notes\\runs"
    reader = RunnerReader(DEFAULT_DIRECTORY)

    if args.print_all_runs:
        reader.print_all_runs()
    elif args.graph_all_runs:
        reader.graph_all_runs()
    elif args.line_graph_all_runs:
        reader.line_graph_all_runs()
    elif args.print_stats:
        reader.print_stats()
    elif args.interactive:
        interactive = InteractiveRunner(reader)
        interactive.main_loop()
    else:
        total = reader.get_total()
        print("%f miles run" % total)


if __name__ == '__main__':
    main()
