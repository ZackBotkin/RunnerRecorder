import sqlite3

class QueryRunner(object):

    def __init__(self, config):
        self.config = config
        self.database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("database_name")
        )

    def run_sql(self, sql_str):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute(sql_str)
        conn.commit()

    def fetch_sql(self, sql_str):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute(sql_str)
        results = query.fetchall()
        return results

    def migrate_data(self, runs_by_date):
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
        sql_str = query_str.strip().rstrip(',')
        self.run_sql(sql_str)

    def create_runs_table(self):
        sql_str = "CREATE TABLE runs(date DATE, miles FLOAT, route_name VARCHAR, comment VARCHAR)"
        self.run_sql(sql_str)

    def create_routes_table(self):
        sql_str = "CREATE TABLE routes(route_name, miles, description)"
        self.run_sql(sql_str)

    def delete_data_from_runs_table(self, run_date=None):
        sql_str = 'DELETE FROM runs'
        if run_date is not None:
            sql_str += " WHERE date='%s'" % run_date
        self.run_sql(sql_str)

    def delete_data_from_routes_table(self):
        self.run_sql('DELETE FROM routes')

    def drop_runs_table(self):
        self.run_sql('DROP TABLE runs')

    def drop_routes_table(self):
        self.run_sql('DROP TABLE routes')

    def insert_initial_route_data(self):
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
        self.run_sql(sql_str)


    ## TODO : the 2023 is hardcoded
    def get_runs(self, run_date=None):
        sql_str = "SELECT * FROM runs"
        if run_date is not None:
            sql_str += " WHERE date = '%s'" % run_date
        else:
            return self.get_runs_for_year(2023)

    def get_runs_for_year(self, year):
        next_year = year + 1
        last_year = year - 1
        sql_str = "SELECT * FROM runs WHERE date > '%s-12-31' AND date < '%s-01-01'" % (str(last_year), str(next_year))
        return self.fetch_sql(sql_str)

    def insert_run(self, run_date, route_name, distance_in_miles, comment=None):
        sql_str = "INSERT INTO runs VALUES "
        if comment == None:
            sql_str += "('%s', %s, '%s', '')" % (
                run_date,
                distance_in_miles,
                route_name,
            )
        else:
            sql_str += "('%s', %s, '%s', '%s')" % (
                run_date,
                distance_in_miles,
                route_name,
                comment
            )
        self.run_sql(sql_str)

    def update_run(self, run_date, route_name, distance_in_miles, comment):
        sql_str = "UPDATE runs SET route_name = '%s', miles = '%s', comment = '%s' WHERE date = '%s'" % (route_name, distance_in_miles, comment, run_date)
        self.run_sql(sql_str)

    def get_routes(self):
        sql_str = 'SELECT * FROM routes'
        return self.fetch_sql(sql_str)

    def insert_route(self, route_name, distance_in_miles, description):
        sql_str = "INSERT INTO routes VALUES ('%s', '%s', '%s')" % (route_name, distance_in_miles, description)
        self.run_sql(sql_str)

    ## TODO : might not need this anymore
    def miles_map(self):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute('SELECT * FROM routes')
        results = query.fetchall()
        miles_map = {}
        for route in results:
            miles_map[route[0]] = float(route[1]) ## TODO -- again a little janky
        return miles_map


    def migrate_all_data_to_new_db(self, runs_by_date, legacy_runs_by_date):
        migrate_database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("migrate_database_name")
        )
        sql_str = "CREATE TABLE runs(date DATE, miles FLOAT, route_name VARCHAR, comment VARCHAR)"
        conn = sqlite3.connect(migrate_database_file_name)
        conn.execute(sql_str)
        conn.commit()

        runs = self.get_runs()

        query_str = "INSERT INTO runs VALUES "
        for date, runs in runs_by_date.items():
            for run in runs:
                if 'comment' in run:
                    query_str += "('%s', %s, '%s', '%s'), " % (
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
        for date, runs in legacy_runs_by_date.items():
            for run in runs:
                if 'comment' in run:
                    query_str += "('%s', %s, '%s', '%s'), " % (
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
        sql_str = query_str.strip().rstrip(',')
        conn.execute(sql_str)
        conn.commit()

    def read_migrate_database(self):
        migrate_database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("migrate_database_name")
        )
        conn = sqlite3.connect(migrate_database_file_name)
        query = conn.execute("SELECT * FROM runs")
        results = query.fetchall()
        for result in results:
            print(result)


