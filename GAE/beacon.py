from google.appengine.ext import ndb


class Beacon(ndb.Model):
    location_name = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
    uuid = ndb.StringProperty(required=True)
    coordinates = ndb.GeoPtProperty()


def add(uuid, location_name, school, coordinates=None):
    Beacon(
        location_name=location_name,
        school=school,
        uuid=uuid,
        coordinates=coordinates
    ).put()


def get_list():
    return Beacon.query().fetch()


def get_uuid(location_name):
    beacon = Beacon.query(Beacon.location_name == location_name).fetch()
    assert beacon is not None
    return beacon[0].uuid


def get_location_name(uuid):
    beacon = Beacon.query(Beacon.uuid == uuid).fetch()
    assert beacon is not None
    return beacon[0].location_name

