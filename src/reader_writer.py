import sqlite3
import os
import json
from datetime import datetime

class ReaderWriter(object):

    def __init__(self, configs):

        self.config = configs

        if self.config.get("read_from_db") and self.config.get("read_from_disk"):
            raise Exception("Cannot read from both datasources, update the config file to set either \"read_from_db\" or \"read_from_disk\" to false")
        elif not self.config.get("read_from_db") and not self.config.get("read_from_disk"):
            raise Exception("Need to select a datasource to read from, update the config file to set either \"read_from_db\" or \"read_from_disk\" to true")
        else:
            self.use_db = self.config.get("read_from_db")

        self.database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("database_name")
        )

        ## attempt to create the table
        if self.config.get("create_table_upon_start"):
            try:
                self.create_runs_table()
            ## ignore if the table already exists
            except sqlite3.OperationalError:
                pass
            try:
                self.create_routes_table()
            ## ignore if the table already exists
            except sqlite3.OperationalError:
                pass

    def todays_date_str(self):
        return datetime.today().strftime("%Y-%m-%d")

    def todays_file_name(self, date_str=None, individualizer=None):

        if individualizer is not None:
            return "%s/%s-%s.json" % (
                self.config.get("runs_directory"),
                date_str or self.todays_date_str(),
                individualizer
            )
        else:
            return "%s/%s.json" % (
                self.config.get("runs_directory"),
                date_str or self.todays_date_str()
            )

    ## TODO : maybe this should return a class/object rather than
    ## a json struct
    def get_runs(self):
        if self.use_db:
            return self.get_runs_from_db()
        else:
            return self.get_runs_from_disk()

    def get_legacy_runs(self):
        runs_by_date = {}
        runs_directory = self.config.get("legacy_runs_directory")
        for file in os.listdir(runs_directory):
            f = open("%s/%s" % (runs_directory, file))
            data = json.load(f)
            if data["date"] not in runs_by_date:
                runs_by_date[data["date"]] = []
            runs_by_date[data["date"]].append(data)
        return runs_by_date

    ## TODO : maybe this should return a list of "Route" classes
    def get_routes(self):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute('SELECT * FROM routes')
        results = query.fetchall()
        routes = []
        for route in results:
            routes.append({
                'route_name': route[0],
                'miles': float(route[1]),  ## TODO: kinda janky, should enforce that we are saving as a float or w/e
                'description': route[2]
            })
        return routes

    def miles_map(self):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute('SELECT * FROM routes')
        results = query.fetchall()
        miles_map = {}
        for route in results:
            miles_map[route[0]] = float(route[1]) ## TODO -- again a little janky
        return miles_map

    def get_runs_from_db(self):
        runs_by_date = {}
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute('SELECT * FROM runs')
        results = query.fetchall()
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

    def get_runs_from_disk(self):
        runs_by_date = {}
        runs_directory = self.config.get("runs_directory")
        for file in os.listdir(runs_directory):
            f = open("%s/%s" % (runs_directory, file))
            data = json.load(f)
            if data["date"] not in runs_by_date:
                runs_by_date[data["date"]] = []
            runs_by_date[data["date"]].append(data)
        return runs_by_date

    def write_run(self, route_name, comment=None):
        if self.config.get("write_to_disk"):
            self.write_run_to_disk(route_name, comment)
        if self.config.get("write_to_db"):
            self.write_run_to_db(route_name, comment)

    def write_new_run(self, args, comment=None):
        if self.config.get("write_to_disk"):
            self.write_new_run_to_disk(args)
        if self.config.get("write_to_db"):
            self.write_new_run_to_db(args, comment)

    def write_run_to_disk(self, route_name, comment=None):

        mile_map = self.miles_map()
        if route_name not in mile_map:
            raise Exception("Unknown route!")

        todays_json_filename = self.todays_file_name()
        already_exists = os.path.exists(todays_json_filename)
        individualizer = 1
        while already_exists:
            todays_json_filename = self.todays_file_name(individualizer=individualizer)
            individualizer += 1
            already_exists = os.path.exists(todays_json_filename)

        with open(todays_json_filename, 'w') as f:
            miles = mile_map[route_name]
            if comment is None:
                comment = ''
            json.dump({
                "miles": miles,
                "date": self.todays_date_str(),
                "route_name": route_name,
                "comment": comment
            }, f)
            return

    def write_new_run_to_disk(self, args):
        if "miles" not in args:
            raise Exception("Need \'miles\' as an arg")
        if "route_name" not in args:
            raise Exception("Need \'route_name\' as an arg")
        with open(self.todays_file_name(date_str=args["date"]), "w") as f:
            comment = ''
            if 'comment' in args:
                comment = args['comment']

            json.dump({
                "miles": args["miles"],
                "date": args["date"] or self.todays_date_str(),
                "route_name": args["route_name"],
                "comment": comment
            }, f)
            return

    ## TODO : standardize these method names man
    def add_route(self, route_name, miles, description):
        query_str = "INSERT INTO routes VALUES ('%s', '%s', '%s')" % (route_name, miles, description)
        conn = sqlite3.connect(self.database_file_name)
        conn.execute(query_str)
        conn.commit()

    def get_runs_on_date(self, run_date):
        query_str = "SELECT * FROM runs WHERE date = '%s'" % run_date
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute(query_str)
        results = query.fetchall()
        return results

    ## TODO : comment editable?
    def edit_run(self, run_date, route_name, distance, comment):
        query_str = "UPDATE runs SET route_name = '%s', miles = '%s', comment = '%s' WHERE date = '%s'" % (route_name, distance, comment, run_date)
        conn = sqlite3.connect(self.database_file_name)
        conn.execute(query_str)
        conn.commit()

    def write_run_to_db(self, route_name, comment=None):
        mile_map = self.miles_map()
        if route_name not in mile_map:
            raise Exception("Unknown route!")
        else:

            miles = mile_map[route_name]
            _date = self.todays_date_str()
            conn = sqlite3.connect(self.database_file_name)
            query_str = "INSERT INTO runs VALUES "

            if comment == None:
                query_str += "('%s', %s, '%s', '')" % (
                    _date,
                    miles,
                    route_name,
                )
            else:
                query_str += "('%s', %s, '%s', '%s')" % (
                    _date,
                    miles,
                    route_name,
                    comment
                )

            conn.execute(query_str)
            conn.commit()

    def write_new_run_to_db(self, args):
        raise Exception("Not implemented yet")


    def create_runs_table(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute("CREATE TABLE runs(date, miles, route_name, comment)")
        conn.commit()

    def create_routes_table(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute("CREATE TABLE routes(route_name, miles, description)")
        conn.commit()


    ## TODO : maybe deprecate this or otherwise rename once everything is inside the
    ## database, it's only purpose is to migrate from json files to database
    def migrate_data(self, runs_by_date):
        conn = sqlite3.connect(self.database_file_name)
        query_str = "INSERT INTO runs VALUES "
        for date, runs in runs_by_date.items():
            for run in runs:

                if 'comment' in run:
                    query_str += "('%s', %s, '%s'), " % (
                        run['date'],
                        run['miles'],
                        run['route_name'],
                        run['comment']
                    )
                else:
                    query_str += "('%s', %s, '%s', ''), " % (
                        run['date'],
                        run['miles'],
                        run['route_name']
                    )
        query_str = query_str.strip().rstrip(',')
        conn.execute(query_str)
        conn.commit()

    def read_data(self):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute("SELECT * FROM runs")
        results = query.fetchall()
        for result in results:
            print(result)

    def delete_data(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute('DELETE FROM runs')
        conn.commit()

    def delete_routes(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute('DELETE FROM routes')
        conn.commit()

    def drop_table(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute('DROP TABLE runs')
        conn.commit()

    def drop_routes_table(self):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute('DROP TABLE routes')
        conn.commit()

    def run_sql(self):
        conn = sqlite3.connect(self.database_file_name)

        #sql_str = """
        #INSERT INTO runs (date, miles, route_name, comment)
        #VALUES ('2023-05-04', 3.5, 'kingsbury', 'beautiful day, still recovering from vacation') 
        #"""
        #sql_str = """
        #DELETE FROM runs
        #WHERE date = '2023-06-04'
        #"""

        #sql_str = """
        #UPDATE runs
        #SET route_name = 'kingsbury'
        #WHERE date = '2023-03-16'
        #"""

        sql_str = """
        INSERT INTO routes
        (route_name, miles, description)
        VALUES
        ('grand', 7.45, 'to the lake, turn back at grand'),
        ('lake', 8.25, 'to the lake, turn back at lake'),
        ('lakeshore', 6.1, 'to the lake, turn back at division'),
        ('sedgewick', 4.75, 'turn back at sedgewick'),
        ('kingsbury', 3.5, 'turn back at kingsbury'),
        ('roosevelt', 10.73, 'to the lake, turn back at roosevelt'),
        ('madison', 8.8, 'to the lake, turn back at madison'),
        ('farmers market', 2.45, 'out to damen, turn back at milwaukee'),
        ('van buren', 9.45, 'out to the lake, turn back at van buren')
        """

        conn.execute(sql_str)
        conn.commit()

