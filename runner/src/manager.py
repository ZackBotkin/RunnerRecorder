from datetime import datetime
from runner.src.util import get_miles_per_week, get_miles_in_date_range_inclusive
from runner.src.io.query_runner import QueryRunner
from runner.src.io.filesystem_reader_writer import FileSystemReaderWriter
from runner.src.graph.grapher import Grapher

#
#   TODO : this should probably now be re-named manager
#

class RunnerReader(object):

    def __init__(self, configs, input_source, output_sources):
        self.config = configs
        self.input_source = input_source
        self.output_sources = output_sources
        self.reload()

    def reload(self):
        self.runs_by_date = self.input_source.get_runs()
        self.legacy_runs_by_date = self.input_source.get_legacy_runs()
        self.routes = self.get_routes()
        self.default_run_options = []
        for route in self.routes:
            self.default_run_options.append(route['route_name'])

    def write_run(self, route_name, comment=None):
        for output_source in self.output_sources:
            output_source.add_run(route_name, comment)

    def add_route(self, route_name, miles, description):
        miles = float(miles)
        for output_source in self.output_sources:
            output_source.add_route(route_name, miles, description)

    def get_routes(self):
        return self.input_source.get_routes()

    def get_runs_on_date(self, run_date):
        runs = self.input_source.get_runs(run_date=run_date)
        return runs

    def edit_run(self, run_date, route_name, distance, comment):
        for output_source in self.output_sources:
            output_source.edit_run(run_date, route_name, distance, comment)

    def get_total(self):
        total=0
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total+= float(data["miles"])
        return total

    def print_all_runs(self):
        total_so_far = 0
        goal = self.config.get("run_goal")
        all_data = [('Date', 'Miles Run', 'Route Name', 'Total So Far', 'Percentage Of Goal', 'Comment')]
        import pandas as pd
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total_so_far += float(data["miles"])
                percentage_of_goal = "{:.2f}".format((total_so_far/goal) * 100)
                comment = ""
                if "comment" in data:
                    comment = data["comment"]
                all_data.append(
                    (
                        date,
                        data['miles'],
                        data['route_name'],
                        total_so_far,
                        "%s %s" % (percentage_of_goal, "%"),
                        comment
                    )
                )
        df = pd.DataFrame(all_data)
        print(df.to_string(index=False))
        return True

    def print_all_routes(self):
        routes = self.get_routes()
        headers = ('Route Name', 'Distance', 'Description', 'Total Miles', 'Total Runs')
        all_data = []
        index = []
        current_index = 1

        by_route_total_miles = {}
        by_route_total_runs = {}

        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                route_name = data["route_name"]
                if route_name not in by_route_total_miles:
                    by_route_total_miles[route_name] = 0
                by_route_total_miles[route_name] += data["miles"]

                if route_name not in by_route_total_runs:
                    by_route_total_runs[route_name] = 0
                by_route_total_runs[route_name] += 1

        import pandas as pd
        for route in routes:
            total_miles = 0
            total_runs = 0
            route_name = route['route_name']
            if route_name in by_route_total_miles:
                total_miles = by_route_total_miles[route_name]
            if route_name in by_route_total_runs:
                total_runs = by_route_total_runs[route_name]
            all_data.append(
                (
                    route_name,
                    "%s miles" % "{:.2f}".format(route['miles']),
                    route['description'],
                    total_miles,
                    total_runs
                )
            )

        def myFunc(val):
            return val[3]

        all_data.sort(reverse=True, key=myFunc)
        df = pd.DataFrame(all_data)
        print(df.to_string(index=False))
        return True

    def get_stats(self):
        total_runs = 0
        total_miles = 0
        goal_number = self.config.get("run_goal")
        day_of_year = datetime.now().timetuple().tm_yday
        days_left = 365 - day_of_year
        for date, data_list in self.runs_by_date.items():
            for data in data_list:
                total_runs += 1
                total_miles += float(data["miles"])
        miles_remaining = goal_number - total_miles
        if total_runs == 0:
            avg_miles_per_run = 0
        else:
            avg_miles_per_run = total_miles/total_runs
        avg_runs_per_day = total_runs/day_of_year
        avg_miles_per_day = total_miles/day_of_year
        needed_avg = miles_remaining/days_left
        miles_per_week = get_miles_per_week(self.runs_by_date, 2023) ## TODO : do not hardcode
        avg_miles_per_week = total_miles/len(miles_per_week)
        this_week = miles_per_week[-1]

        return {
            "day_of_year": day_of_year,
            "days_left": days_left,
            "goal": goal_number,
            "on_pace_for": avg_miles_per_day * 365, ## TODO leap year bug
            "total_runs": total_runs,
            "total_miles": total_miles,
            "miles_remaining": miles_remaining,
            "avg_miles_per_run": avg_miles_per_run,
            "avg_runs_per_day": avg_runs_per_day,
            "avg_miles_per_day": avg_miles_per_day,
            "needed_avg": needed_avg,
            "avg_miles_per_week": avg_miles_per_week,
            "miles_this_week": this_week.total_miles
        }

    def print_stats(self):
        stats = self.get_stats()
        print("\n")
        print("\tDay of year: %d\n" % stats["day_of_year"])
        print("\tDays left: %d\n" % stats["days_left"])
        print("\tGoal: %d\n" % stats["goal"])
        print("\tOn pace for: %f\n" % stats["on_pace_for"])
        print("\tNumber of runs: %d\n" % stats["total_runs"])
        print("\tNumber of miles: %f\n" % stats["total_miles"])
        print("\tNumber of miles remaining until goal: %f\n" % stats["miles_remaining"])
        print("\tMiles per run avg: %f\n" % stats["avg_miles_per_run"])
        print("\tRuns per day avg: %f\n" % stats["avg_runs_per_day"])
        print("\tMiles per day avg: %f\n" % stats["avg_miles_per_day"])
        print("\tMiles per day avg (needed for goal): %f\n" % stats["needed_avg"])
        print("\tMiles per week avg: %f\n" % stats["avg_miles_per_week"])
        print("\tMiles this week: %f\n" % stats["miles_this_week"])
        print("\n")
        return True


    #
    #   sql methods for troubleshooting only
    #
    def run_sql(self):
        raise Exception("Not implemented")

    def read_runs(self):
        results = QueryRunner(self.config).get_all_runs()
        for result in results:
            print(result)

    def read_routes(self):
        results = QueryRunner(self.config).get_routes()
        for result in results:
            print(result)

    def runs_count(self):
        results = QueryRunner(self.config).get_all_runs()
        print("%d rows in 'run' table" % len(results))

    def routes_count(self):
        results = QueryRunner(self.config).get_routes()
        print("%d rows in 'route' table" % len(results))

    def delete_runs(self, run_date=None):
        results = QueryRunner(self.config).get_runs(run_date=run_date)
        runs_count = len(results)
        print("Deleting %d rows from 'runs' table" % runs_count)
        QueryRunner(self.config).delete_data_from_runs_table(run_date=run_date)

    def insert_default_routes(self):
        print("Inserting the default set of routes")
        QueryRunner(self.config).insert_initial_route_data()

    def delete_routes(self):
        results = QueryRunner(self.config).get_routes()
        routes_count = len(results)
        print("Deleting %d rows from 'routes' table" % routes_count)
        QueryRunner(self.config).delete_data_from_routes_table()

    def delete_shoes(self):
        results = QueryRunner(self.config).get_shoes()
        shoes_count = len(results)
        print("Deleting %d rows from 'shoes' table" % shoes_count)
        QueryRunner(self.config).delete_data_from_shoes_table()

    def migrate_data(self):
        legacy_runs = self.legacy_runs_by_date
        print("Saving %d rows" % len(legacy_runs))
        QueryRunner(self.config).migrate_data(legacy_runs)

    def drop_runs(self):
        print("Dropping 'runs' table")
        QueryRunner(self.config).drop_runs_table()

    def drop_routes(self):
        print("Dropping 'routes' table")
        QueryRunner(self.config).drop_routes_table()

    def drop_shoes_table(self):
        print("Dropping 'shoes' table")
        QueryRunner(self.config).drop_shoes_table()

    def migrate_all_data_to_new_db(self):
        print("Migrating all data over to the new Db")
        runs_by_date = self.runs_by_date
        legacy_runs_by_date = FileSystemReaderWriter(self.config, {}).get_legacy_runs()
        QueryRunner(self.config).migrate_all_data_to_new_db(runs_by_date, legacy_runs_by_date)

    def read_data_from_migrated_db(self):
        QueryRunner(self.config).read_migrate_database()

    #
    #   Graph methods
    #
    def graph_all_runs(self):
        Grapher(self.runs_by_date, self.legacy_runs_by_date).graph_all_runs()

    def line_graph_all_runs(self):
        Grapher(self.runs_by_date, self.legacy_runs_by_date).line_graph_all_runs()

    def historical_graph_all_runs(self):
        Grapher(self.runs_by_date, self.legacy_runs_by_date).historical_graph_all_runs()

    def weekly_graph(self):
        Grapher(self.runs_by_date, self.legacy_runs_by_date).weekly_graph()

    def routes_graph(self):
        Grapher(self.runs_by_date, self.legacy_runs_by_date).routes_graph()

    def pie_chart_routes_graph(self):
        Grapher(self.runs_by_date, self.legacy_runs_by_date).pie_chart_routes_graph()

    def miles_per_route_graph(self):
        Grapher(self.runs_by_date, self.legacy_runs_by_date).miles_per_route_graph()


    #
    #   Back up the database
    #
    def back_up_database(self):
        if self.config.get("enable_db_backup"):
            from emailer.src.emailer import EmailerCreds, Emailer
            creds = EmailerCreds(self.config.get('emailer_creds_file'))
            emailer = Emailer(creds)
            database_file_name = "%s\\%s.db" % (
                self.config.get("database_directory"),
                self.config.get("database_name")
            )
            emailer.send_file(
                self.config.get("backups_email"),
                self.config.get("backups_email"),
                database_file_name
            )
            print("Backup of database file sent to %s" % self.config.get("backups_email"))
        else:
            print("DB backup not enabled! enable it in the configs")

    #
    #   Shoes
    #
    def add_shoe(self, nickname, start_date, brand, end_date=None):
        for output_source in self.output_sources:
            output_source.add_shoe(nickname, start_date, brand, end_date=end_date)

    def get_shoe_with_nickname(self, nickname):
        shoe = self.input_source.get_shoe_with_nickname(nickname)
        return shoe

    def retire_existing_shoe(self, nickname, retire_date):
        for output_source in self.output_sources:
            output_source.retire_existing_shoe(nickname, retire_date)
        return None

    def print_all_shoes(self):
        shoes = self.input_source.get_shoes()
        table = [('Nickname', 'Start Date', 'Brand', 'Retire Date', 'Miles Run')]
        for shoe in shoes:
            nickname = shoe[0]
            since_date = shoe[1]
            brand = shoe[2]
            retire_date = shoe[3]
            miles_in_shoe = get_miles_in_date_range_inclusive(self.runs_by_date, since_date)
            table.append(
                (
                    nickname,
                    since_date,
                    brand,
                    retire_date,
                    miles_in_shoe
                )
            )
        import pandas as pd
        df = pd.DataFrame(table)
        print(df.to_string(index=False))

