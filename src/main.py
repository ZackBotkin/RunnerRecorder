import argparse
from datetime import datetime, timedelta
from src.runner import RunnerReader
from src.interactive.main_menu import MainMenu
from src.reader_writer import ReaderWriter
from config.config import Configs


def main():

    parser = argparse.ArgumentParser(description= 'default parser')
    parser.add_argument('--total', action= "store_true", help='running totals')
    parser.add_argument('--print_all_runs', action= "store_true", help='print the running files')
    parser.add_argument('--graph_all_runs', action= "store_true", help='graph the running files')
    parser.add_argument('--line_graph_all_runs', action= "store_true", help='graph the running files as a line graph')
    parser.add_argument('--print_stats', action= "store_true", help='print the stats')
    parser.add_argument('--interactive', action= "store_true", help='interactive mode')
    parser.add_argument('--config_file', help='the configuration file')
    args = parser.parse_args()

    configs = Configs(args.config_file)
    reader_writer = ReaderWriter(configs)
    reader = RunnerReader(configs, reader_writer)

    if args.print_all_runs:
        reader.print_all_runs()
    elif args.graph_all_runs:
        reader.graph_all_runs()
    elif args.line_graph_all_runs:
        reader.line_graph_all_runs()
    elif args.print_stats:
        reader.print_stats()
    elif args.interactive:
        interactive = MainMenu(reader)
        interactive.main_loop()
    else:
        total = reader.get_total()
        print("%f miles run" % total)


if __name__ == '__main__':
    main()
