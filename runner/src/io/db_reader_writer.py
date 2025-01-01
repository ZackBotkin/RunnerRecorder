import sqlite3
from runner.src.io.reader_writer import ReaderWriter
from runner.src.io.query_runner import QueryRunner

class DbReaderWriter(ReaderWriter):

    def __init__(self, config):

        self.config = config
        self.query_runner = QueryRunner(config)

        if self.config.get("create_table_upon_start"):
            try:
                self.query_runner.create_runs_table()
            ## ignore if the table already exists
            except sqlite3.OperationalError:
                pass
            try:
                self.query_runner.create_routes_table()
            ## ignore if the table already exists
            except sqlite3.OperationalError:
                pass
            try:
                self.query_runner.create_shoes_table()
            except sqlite3.OperationalError:
                pass

    ## TODO : have this return a class/classes
    def get_runs(self, run_date=None):
        runs_by_date = {}
        results = self.query_runner.get_runs(run_date=run_date)
        for result in results:
            _date = result[0]
            _miles = result[1]
            _route_name = result[2]
            _comment = result[3]
            if _comment is None:
                _comment = ""
            if _date not in runs_by_date:
                runs_by_date[_date] = []
            runs_by_date[_date].append({
                'date': _date,
                'miles': _miles,
                'route_name': _route_name,
                'comment': _comment
            })
        return runs_by_date

    def add_run(self, route_name, comment=None):

        miles_map = self.miles_map()

        if route_name not in miles_map:
            raise Exception("Cannot find route name %s" % route_name)

        distance_in_miles = miles_map[route_name]

        run_date = self.todays_date_str()

        self.query_runner.insert_run(run_date, route_name, distance_in_miles, comment=comment)

    def edit_run(self, run_date, route_name, distance_in_miles, comment):
        self.query_runner.update_run(run_date, route_name, distance_in_miles, comment)

    def get_legacy_runs(self):
        runs_by_date = {}
        results = self.query_runner.get_runs_for_year(2024) ## TODO do not hardcode
        for result in results:
            _date = result[0]
            _miles = result[1]
            _route_name = result[2]
            _comment = result[3]
            if _comment is None:
                _comment = ""
            if _date not in runs_by_date:
                runs_by_date[_date] = []
            runs_by_date[_date].append({
                'date': _date,
                'miles': _miles,
                'route_name': _route_name,
                'comment': _comment
            })
        return runs_by_date

    def get_routes(self):
        results = self.query_runner.get_routes()
        routes = []
        for route in results:
            routes.append({
                'route_name': route[0],
                'miles': float(route[1]),  ## TODO: kinda janky, should enforce that we are saving as a float or w/e
                'description': route[2]
            })
        return routes

    def add_route(self, route_name, distance_in_miles, description):
        self.query_runner.insert_route(route_name, distance_in_miles, description)

    def miles_map(self):
        return self.query_runner.miles_map()

    def add_shoe(self, nickname, start_date, brand, end_date=None):
        self.query_runner.insert_shoe(nickname, start_date, brand, end_date=end_date)

    def get_shoes(self):
        shoes = self.query_runner.get_shoes()
        return shoes

    def get_shoe_with_nickname(self, nickname):
        shoe = self.query_runner.get_shoe_with_nickname(nickname)
        return shoe

    def retire_existing_shoe(self, nickname, retire_date):
        self.query_runner.retire_existing_shoe(nickname, retire_date)

    def get_runs_in_date_range(self, start_date, end_date):
        return self.query_runner.get_runs_in_date_range(start_date, end_date)

