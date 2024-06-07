import sqlite3
from query_runner.src.runner import SqlLiteQueryRunner

class QueryRunner(SqlLiteQueryRunner):

    def create_runs_table(self):
        sql_str = "CREATE TABLE runs(date DATE, miles FLOAT, route_name VARCHAR, comment VARCHAR)"
        self.run_sql(sql_str)

    def create_routes_table(self):
        sql_str = "CREATE TABLE routes(route_name VARCHAR, miles FLOAT, description VARCHAR)"
        self.run_sql(sql_str)

    def create_shoes_table(self):
        sql_str = "CREATE TABLE shoes(shoe_name VARCHAR, start_date DATE, shoe_brand VARCHAR, end_date DATE)"
        self.run_sql(sql_str)

    def delete_data_from_runs_table(self, run_date=None):
        sql_str = 'DELETE FROM runs'
        if run_date is not None:
            sql_str += " WHERE date='%s'" % run_date
        self.run_sql(sql_str)

    def delete_data_from_routes_table(self):
        self.run_sql('DELETE FROM routes')

    def delete_data_from_shoes_table(self, nickname=None):
        sql_str = "DELETE FROM shoes"
        if nickname is not None:
            sql_str += " WHERE nickname = '%s'" % nickname
        self.run_sql(sql_str)

    def drop_runs_table(self):
        self.run_sql('DROP TABLE runs')

    def drop_routes_table(self):
        self.run_sql('DROP TABLE routes')

    def drop_shoes_table(self):
        self.run_sql('DROP TABLE shoes')

    ## TODO : the 2023 is hardcoded
    def get_runs(self, run_date=None):
        if run_date is not None:
            sql_str = "SELECT * FROM runs WHERE date = '%s'" % run_date
            return self.fetch_sql(sql_str)
        else:
            return self.get_runs_for_year(2024)

    def get_all_runs(self):
        return self.fetch_sql("SELECT * FROM runs")

    def get_runs_for_year(self, year):
        next_year = year + 1
        last_year = year - 1
        sql_str = "SELECT * FROM runs WHERE date > '%s-12-31' AND date < '%s-01-01'" % (str(last_year), str(next_year))
        return self.fetch_sql(sql_str)

    def insert_run(self, run_date, route_name, distance_in_miles, comment=None):
        if comment == None:
            sql_str = "INSERT INTO runs ('date', 'miles', 'route_name') VALUES ('%s', %s, '%s')" % (run_date, distance_in_miles, route_name)
            self.run_sql(sql_str)
        else:
            sql_str = "INSERT INTO runs ('date', 'miles', 'route_name', 'comment') VALUES ('%s', %s, '%s', '%s')" % (run_date, distance_in_miles, route_name, comment)
            self.run_sql(sql_str)

    def update_run(self, run_date, route_name, distance_in_miles, comment):
        sql_str = "UPDATE runs SET route_name = '%s', miles = '%s', comment = '%s' WHERE date = '%s'" % (route_name, distance_in_miles, comment, run_date)
        self.run_sql(sql_str)

    def get_routes(self):
        sql_str = 'SELECT * FROM routes'
        return self.fetch_sql(sql_str)

    def insert_route(self, route_name, distance_in_miles, description):
        sql_str = "INSERT INTO routes ('route_name', 'miles', 'description') VALUES ('%s', '%s', '%s')" % (route_name, distance_in_miles, description)
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

    def insert_shoe(self, nickname, start_date, brand, end_date=None):
        if end_date is None:
            sql_str = "INSERT INTO shoes ('shoe_name', 'start_date', 'shoe_brand') VALUES ('%s', '%s', '%s')" % (nickname, start_date, brand)
        else:
            sql_str = "INSERT INTO shoes VALUES ('%s', '%s', '%s', '%s')" % (nickname, start_date, brand, end_date)
        self.run_sql(sql_str)

    def get_shoes(self):
        return self.fetch_sql("SELECT * FROM shoes")

    def get_shoe_with_nickname(self, nickname):
        return self.fetch_sql("SELECT * FROM shoes WHERE shoe_name = '%s'" % nickname)

    def retire_existing_shoe(self, nickname, retire_date):
        sql_str = "UPDATE shoes SET end_date = '%s' WHERE shoe_name = '%s'" % (retire_date, nickname)
        self.run_sql(sql_str)

    def get_runs_in_date_range(self, start_date, end_date):
        sql_str = "SELECT * FROM runs WHERE date >= '%s' AND date <= '%s'" % (start_date, end_date)
        return self.fetch_sql(sql_str)
