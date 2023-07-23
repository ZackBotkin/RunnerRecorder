from datetime import datetime

class ReaderWriter(object):

    def __init__(self, configs):
        self.config = configs

    def todays_date_str(self):
        return datetime.today().strftime("%Y-%m-%d")

    def get_runs(self, run_date=None):
        raise Exception("Not implemented")

    def add_run(self, run_date, route_name, distance_in_miles, comment=None):
        raise Exception("Not implemented")

    def edit_run(self, run_date, route_name, distance_in_miles, comment):
        raise Exception("Not implemented")

    def get_legacy_runs(self):
        raise Exception("Not implemented")

    def get_routes(self):
        raise Exception("Not implemented")

    def add_route(self, route_name, distance_in_miles, description):
        raise Exception("Not implemented")

    def add_shoe(self, nickname, start_date, brand, end_date=None):
        raise Exception("Not implemented")

    def get_shoes(self):
        raise Exception("Not implemented")

    def get_shoe_with_nickname(self, nickname):
        raise Exception("Not implemented")


