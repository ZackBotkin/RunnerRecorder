import argparse
from datetime import datetime, timedelta
from runner.src.manager import RunnerReader
from runner.src.interactive.main_menu import MainMenu
from runner.src.io.reader_writer import ReaderWriter
from runner.src.io.db_reader_writer import DbReaderWriter
from runner.src.io.filesystem_reader_writer import FileSystemReaderWriter
from runner.src.io.query_runner import QueryRunner
from runner.config.config import Configs


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

    use_db = True
    if configs.get("read_from_db") and configs.get("read_from_disk"):
        raise Exception("Cannot read from both datasources, update the config file to set either \"read_from_db\" or \"read_from_disk\" to false")
    elif not configs.get("read_from_db") and not configs.get("read_from_disk"):
        raise Exception("Need to select a datasource to read from, update the config file to set either \"read_from_db\" or \"read_from_disk\" to true")
    else:
        use_db = configs.get("read_from_db")

    if use_db:
        input_source = DbReaderWriter(configs)
    else:
        miles_map = QueryRunner(configs).miles_map()
        input_source = FileSystemReaderWriter(configs, miles_map)

    output_sources = []
    if not configs.get("write_to_db") and not configs.get("write_to_disk"):
        raise Exception("Need to select a datasource to read from, update the config file to set either \"read_from_db\" or \"read_from_disk\" to true")
    if configs.get("write_to_db"):
        output_sources.append(DbReaderWriter(configs))
    if configs.get("write_to_disk"):
        miles_map = QueryRunner(configs).miles_map()
        output_sources.append(FileSystemReaderWriter(configs, miles_map))

    reader = RunnerReader(configs, input_source, output_sources)

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
        if configs.get("never_back_up_database") == True:
            answer = "no"
        elif configs.get("always_back_up_database") == True:
            answer = "yes"
        else:
            print("Back up the database?\n")
            answer = interactive.fancy_input()

        if answer in ["yes", "Yes", "ok"]:
            reader.back_up_database()
    else:
        total = reader.get_total()
        print("%f miles run" % total)


if __name__ == '__main__':
    main()
