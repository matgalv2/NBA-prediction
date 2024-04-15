import datetime


class NBADate(object):
    __create_key = object()
    __months = {
        'JAN': 1,
        'FEB': 2,
        'MAR': 3,
        'APR': 4,
        'MAY': 5,
        'JUN': 6,
        'JUL': 7,
        'AUG': 8,
        'SEP': 9,
        'OCT': 10,
        'NOV': 11,
        'DEC': 12
    }

    @classmethod
    def create(cls, date_string: str):
        date = cls.__parseDate(date_string)
        return NBADate(cls.__create_key, date)

    def __init__(self, create_key, value: datetime.date):
        assert (create_key == NBADate.__create_key), \
            "NBADate objects must be created using NBADate.create"
        self.value = value

    @classmethod
    def __parseDate(cls, date_string: str) -> datetime.date:
        month, day, year = date_string.replace(',','').split()
        return datetime.date(int(year), cls.__months[month], int(day))
