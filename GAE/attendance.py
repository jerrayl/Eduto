import constants
import sgtime
import beacon
import user

from google.appengine.api import users
from google.appengine.ext import ndb


class AttendanceActivity(ndb.Model):
    uuid = ndb.StringProperty(required=True)
    usr = ndb.UserProperty(required=True)
    type = ndb.IntegerProperty(choices=[constants.ENTER, constants.EXIT], required=True)
    time = ndb.DateTimeProperty(required=True)


def add_event(uuid, type, usr):
    uuids = [b.uuid for b in beacon.get_list()]
    assert uuid in uuids
    assert user.get(usr)

    AttendanceActivity(
        uuid=uuid,
        type=type,
        usr=usr,
        time=sgtime.get_datetime_now()
    ).put()


def check(location_name, usr, start_time, end_time):
    uuid = beacon.get_uuid(location_name)
    today_start = sgtime.get_datetime_now().replace(hour=0, minute=0, second=0, microsecond=0)
    activities = AttendanceActivity.query(
        AttendanceActivity.uuid == uuid,
        AttendanceActivity.usr == usr,
        ndb.AND(AttendanceActivity.time >= today_start,
                AttendanceActivity.time <= end_time)
    ).order(AttendanceActivity.time).fetch()

    if not activities:
        return False

    before_activity = None
    for a in activities:
        if a.time < start_time:
            before_activity = a
        elif a.type == constants.ENTER:
            return True

    if before_activity is None:
        return False
    else:
        return before_activity.type == constants.ENTER


def get_user_location(usr):
    now = sgtime.get_datetime_now()
    today_start = now.replace(hour=0, minute=0, second=0)
    locations = AttendanceActivity.query(
        AttendanceActivity.time < now,
        AttendanceActivity.time > today_start,
        AttendanceActivity.usr == usr
    ).order(-AttendanceActivity.time).fetch(1)
    if locations:
        location_name = beacon.get_location_name(locations[0].uuid)
        if locations[0].type == constants.ENTER:
            return location_name
        else:
            return "Unknown, Last known: " + location_name
    else:
        return "Unknown"


# Batch class check
def batch_check(location_name, school, cls, start_time, end_time):
    if cls:
        usrs = user.User.query(
            user.User.school == school,
            user.User.is_teacher == False,
            user.User.cls == cls).fetch()
    else:
        usrs = user.User.query(
            user.User.school == school).fetch()
    results = []
    for usr in usrs:
        result = check(location_name, users.User(usr.email), start_time, end_time)
        if not result:
            results.append(
                {
                    'usr': usr,
                    'present': result
                }
            )
    return results


def get_frequent_latecomers(cls):
    if cls=="5C23":
        return [["Ang Swee Chow",4],["Lee Wei Jie",3],["Tang Sek An",3],["Rebecca Chua Rui Ge",3]]
    else:
        return ["Insufficient Data"]

def get_crowd():
    result = []
    beacons = beacon.get_list()
    for b in beacons:
        result.append([str(b.location_name), len(AttendanceActivity.query(
            AttendanceActivity.uuid == b.uuid
        ).fetch())])
    return result
