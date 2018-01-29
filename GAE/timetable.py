import json
import user
from google.appengine.ext import ndb


class Event(ndb.Model):
    start = ndb.TimeProperty(required=True)
    end = ndb.TimeProperty(required=True)
    subject = ndb.StringProperty(required=True)
    beacon = ndb.KeyProperty()


class Timetable(ndb.Model):
    school = ndb.StringProperty(required=True)
    cls = ndb.StringProperty(required=True)
    events = ndb.StructuredProperty(Event, repeated=True)

def add_timetable(file, school, cls):
    timetable = Timetable(
        school=school,
        cls=cls,
        events=[]
    )
    data = json.load(file)
    for d in data['events']:
        event = Event(
            start=d['start'],
            end=d['end'],
            subject=d['subject']
        )
        timetable.events.append(event)
    timetable.put()


def add_beacon(school, cls, beacon_key):
    timetable = Timetable.query(
        Timetable.school == school,
        Timetable.cls == cls
    ).fetch()[0]
    timetable.beacon = beacon_key
    timetable.put()


def get(usr, cls=None):
    user_info = user.get(usr)
    if cls is None:
        cls = user_info.cls
    timetable = Timetable.query(
        Timetable.school == user_info.school,
        Timetable.cls == cls.cls,
    ).fetch()[0]
    return timetable.events
