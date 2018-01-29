from protorpc import messages
from protorpc import message_types


class AttendanceActivityMessage(messages.Message):
    uuid = messages.StringField(1)
    type = messages.IntegerField(2)
    time = message_types.DateTimeField(3)
    email = messages.StringField(4)


class AttendanceActivitiesMessage(messages.Message):
    beacon_activities = messages.MessageField(AttendanceActivityMessage, 1, repeated=True)


class BeaconMessage(messages.Message):
    location_name = messages.StringField(1)
    school = messages.StringField(2)
    uuid = messages.StringField(3)


class BeaconsMessage(messages.Message):
    beacons = messages.MessageField(BeaconMessage, 1, repeated=True)


class AttendanceRequestMessage(messages.Message):
    school = messages.StringField(1)
    cls = messages.StringField(2)
    location_name = messages.StringField(3)
    start_time = message_types.DateTimeField(4)
    end_time = message_types.DateTimeField(5)


class AttendanceResultMessage(messages.Message):
    usr = messages.StringField(1)
    present = messages.BooleanField(2)


class AttendanceResultsMessage(messages.Message):
    results = messages.MessageField(AttendanceResultMessage, 1, repeated=True)


class TaskMessage(messages.Message):
    title = messages.StringField(1)
    time_added = message_types.DateTimeField(2)
    usr = messages.StringField(3)
    subject = messages.StringField(4)
    due_date = message_types.DateTimeField(5)
    url_id = messages.StringField(6)
    cls = messages.StringField(7)
    description = messages.StringField(8)
    school = messages.StringField(9)
    done = messages.BooleanField(10)
    is_owner = messages.BooleanField(11)


class TaskIDMessage(messages.Message):
    url_id = messages.StringField(1)


class TasksMessage(messages.Message):
    tasks = messages.MessageField(TaskMessage, 1, repeated=True)


class UserMessage(messages.Message):
    email = messages.StringField(1)
    school = messages.StringField(2)
    name = messages.StringField(3)
    cls = messages.StringField(4)
    subjects = messages.StringField(5, repeated=True)
    is_teacher = messages.BooleanField(6)
    points = messages.IntegerField(7)
    rank = messages.IntegerField(8)


class UsersMessage(messages.Message):
    users = messages.MessageField(UserMessage, 1, repeated=True)


class EventMessage(messages.Message):
    subject = messages.StringField(1)
    start_time = message_types.DateTimeField(2)
    end_time = message_types.DateTimeField(3)
    beacon_location_name = messages.StringField(4)


class TimetableMessage(messages.Message):
    events = messages.MessageField(EventMessage, 1)


class TimetableRequestMessage(messages.Message):
    cls = messages.StringField(1)


class SuggestionMessage(messages.Message):
    text = messages.StringField(1)
    date = message_types.DateTimeField(2)
    type=messages.StringField(3)
    subject = messages.StringField(4)
    location = messages.StringField(5)


class SuggestionsMessage(messages.Message):
    suggestions = messages.MessageField(SuggestionMessage, 1, repeated=True)


class LocationMessage(messages.Message):
    location = messages.StringField(1)
