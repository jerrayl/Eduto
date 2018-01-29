import datetime


class SingaporeTZ(datetime.tzinfo):
    def utcoffset(self, date_time):
        return datetime.timedelta(hours=8)

    def tzname(self, date_time):
        return "GMT +8"

    def dst(self, date_time):
        return datetime.timedelta(0)


def get_datetime_now():
    return datetime.datetime.now(SingaporeTZ()).replace(tzinfo=None)
