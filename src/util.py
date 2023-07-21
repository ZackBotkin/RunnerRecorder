import datetime


SUNDAY_INDEX = 6
START_OF_WEEK_INDEX = SUNDAY_INDEX

class Week(object):

    def __init__(self, dates):
        self.dates = dates
        self.start_date = dates[0] ## TODO sort the dates
        self.total_miles = 0

    def add_miles(self, miles):
        self.total_miles += float(miles)


def get_miles_per_week(runs_by_date, year):
    
    weeks = get_weeks(year)
    miles_per_week = []
    for week in weeks:
        if week.start_date <= datetime.datetime.today():
            miles_per_week.append(week)
        for current_date in week.dates:
            if current_date > datetime.datetime.today():
                return miles_per_week
            date_str = current_date.strftime("%Y-%m-%d")
            runs = runs_by_date[date_str] if date_str in runs_by_date else []
            for run in runs:
                week.add_miles(run["miles"])

    return miles_per_week

def get_weeks(year, start_of_week_index=START_OF_WEEK_INDEX):

    if start_of_week_index < 0 or start_of_week_index > 6:
        raise Exception("Index for the start of the week needs to be (0, 6)")

    weeks = []
    first_day = datetime.datetime(year, 1, 1)
    day_of_week = first_day.weekday()

    while day_of_week != start_of_week_index:
        first_day = first_day - datetime.timedelta(days=1)
        day_of_week = first_day.weekday()

    current_day = first_day
    while current_day.year <= year:

        dates_in_week = []
        for day_index in range(7):
            dates_in_week.append(current_day)
            current_day = current_day + datetime.timedelta(days=1)

        week = Week(dates_in_week)
        weeks.append(week)

    return weeks


def get_miles_since_date_inclusive(runs_by_date, since_date_str):
    all_dates = []
    total_miles = 0
    for date_str in runs_by_date.keys():
        as_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        all_dates.append(as_date)
    all_dates.sort()
    all_dates.reverse()
    since_date = datetime.datetime.strptime(since_date_str, "%Y-%m-%d")
    for date in all_dates:
        if date >= since_date:
            runs = runs_by_date[date.strftime("%Y-%m-%d")]
            for run in runs:
                total_miles += run["miles"]
        else:
            break
    return total_miles
