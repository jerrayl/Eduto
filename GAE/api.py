# -*- coding: utf-8 -*-
import endpoints
import msg
import constants
import attendance
import task
import beacon
import datetime
import suggestions
import user

from protorpc import message_types
from protorpc import remote

CLIENT_IDS = [endpoints.API_EXPLORER_CLIENT_ID,
              '282977843977-7jr6mbjgpngkneg3mppqavvu8fbeap60.apps.googleusercontent.com',
              '282977843977-5u88g6cj44n6ktj7ibgtrei7o1d23kg6.apps.googleusercontent.com',
              '282977843977-orukbr3f1q49i8npjks4ib8fc2ths0jq.apps.googleusercontent.com',
              '282977843977-kusbrei0o9na0vk6u6nmg75rf02efvqb.apps.googleusercontent.com']

AUDIENCES = ['282977843977-5u88g6cj44n6ktj7ibgtrei7o1d23kg6.apps.googleusercontent.com',
             '282977843977-orukbr3f1q49i8npjks4ib8fc2ths0jq.apps.googleusercontent.com']


@endpoints.api(name='eduapi', version='v1',
               allowed_client_ids=CLIENT_IDS,
               audiences=AUDIENCES,
               scopes=[endpoints.EMAIL_SCOPE])
class EduAPI(remote.Service):
    # ATTENDANCE
    @endpoints.method(msg.AttendanceActivityMessage, message_types.VoidMessage,
                      path='submit_attendance', http_method='POST',
                      name='submit_attendance')
    def submit_attendance(self, request):
        attendance.add_event(
            uuid=request.uuid,
            type=request.type,
            usr=endpoints.get_current_user()
        )
        return message_types.VoidMessage()

    @endpoints.method(msg.AttendanceRequestMessage, msg.AttendanceResultsMessage,
                      path='get_attendance', http_method='POST',
                      name='get_attendance')
    def get_attendance(self, request):
        result = attendance.batch_check(
            location_name=request.location_name,
            school=request.school,
            cls=request.cls,
            start_time=request.start_time,
            end_time=request.end_time
        )
        message = []
        for r in result:
            m = msg.AttendanceResultMessage(
                usr=r['usr'].email,
                present=r['present']
            )
            message.append(m)
        return msg.AttendanceResultsMessage(results=message)

    @endpoints.method(message_types.VoidMessage, msg.LocationMessage,
                      path='get_location', http_method='GET',
                      name='get_location')
    def get_location(self, _):
        message = attendance.get_user_location(
            usr=endpoints.get_current_user()
        )
        return msg.LocationMessage(location=message)

    # TASK
    @endpoints.method(msg.TaskMessage, message_types.VoidMessage,
                      path='add_task', http_method='POST',
                      name='add_task')
    def add_task(self, request):
        task.add(
            subject=request.subject,
            cls=request.cls,
            title=request.title,
            due_date=request.due_date,
            usr=endpoints.get_current_user()
        )
        return message_types.VoidMessage()

    @endpoints.method(msg.TaskMessage, message_types.VoidMessage,
                      path='edit_task', http_method='POST',
                      name='edit_task')
    def edit_task(self, request):
        task.edit(
            url_id=request.url_id,
            subject=request.subject,
            cls=request.cls,
            title=request.title,
            due_date=request.due_date,
            usr=endpoints.get_current_user(),
        )
        return message_types.VoidMessage()

    @endpoints.method(msg.TaskIDMessage, message_types.VoidMessage,
                      path='remove_task', http_method='GET',
                      name='remove_task')
    def remove_task(self, request):
        task.remove(
            url_id=request.url_id,
            usr=endpoints.get_current_user()
        )
        return message_types.VoidMessage()

    @endpoints.method(msg.TaskIDMessage, msg.TaskMessage,
                      path='get_task', http_method='GET',
                      name='get_task')
    def get_task(self, request):
        t = task.get(
            url_id=request.url_id,
            usr=endpoints.get_current_user()
        )
        return msg.TaskMessage(
            title=t.title,
            time_added=t.time_added,
            usr=t.usr.email(),
            subject=t.subject,
            due_date=datetime.datetime.combine(t.due_date, datetime.datetime.min.time()),
            cls=t.cls,
            description=t.description,
            school=t.school,
        )

    @endpoints.method(message_types.VoidMessage, msg.TasksMessage,
                      path='get_task_list', http_method='GET',
                      name='get_task_list')
    def get_task_list(self, _):
        usr = endpoints.get_current_user()
        tasks = task.get_list(
            usr=usr
        )
        message = []
        for t in tasks:
            message.append(
                msg.TaskMessage(
                    title=t.title,
                    time_added=t.time_added,
                    usr=user.get(t.usr).name,
                    subject=t.subject,
                    due_date=datetime.datetime.combine(t.due_date, datetime.datetime.min.time()),
                    url_id=t.key.urlsafe(),
                    cls=t.cls,
                    description=t.description,
                    school=t.school,
                    done=t.done,
                    is_owner=t.usr==usr
                )
            )
        return msg.TasksMessage(tasks=message)

    @endpoints.method(msg.TaskIDMessage, message_types.VoidMessage,
                      path='toggle_task_done', http_method='GET',
                      name='toggle_task_done')
    def toggle_task_done(self, request):
        task.toggle_done(request.url_id, endpoints.get_current_user())
        return message_types.VoidMessage()

    # Beacon
    @endpoints.method(msg.BeaconMessage, message_types.VoidMessage,
                      path='add_beacon', http_method='GET',
                      name='add_beacon')
    def add_beacon(self, request):
        beacon.add(
            uuid=request.uuid,
            school=request.school,
            location_name=request.location_name
        )
        return message_types.VoidMessage()

    @endpoints.method(message_types.VoidMessage, msg.BeaconsMessage,
                      path='get_beacon_list', http_method='GET',
                      name='get_beacon_list')
    def get_beacon_list(self, _):
        beacons = beacon.get_list()
        message = []
        for b in beacons:
            message.append(
                msg.BeaconMessage(
                    location_name=b.location_name,
                    uuid=b.uuid
                )
            )
        return msg.BeaconsMessage(beacons=message)

    # # Timetable
    # @endpoints.method(msg.TimetableRequestMessage, msg.TimetableMessage,
    #                   path='get_timetable', http_method='GET',
    #                   name='get_timetable')
    # def get_timetable(self, request):
    #     timetable = timetable

    # Suggestions
    @endpoints.method(msg.SuggestionMessage, message_types.VoidMessage,
                      path='add_suggestion', http_method='POST',
                      name='add_suggestion')
    def add_suggestion(self, request):
        suggestions.add(
            text=request.text,
            date=request.date,
            subject=request.subject,
            location=request.location,
            usr=endpoints.get_current_user()
        )
        return message_types.VoidMessage()

    @endpoints.method(message_types.VoidMessage, msg.SuggestionsMessage,
                      path='get_suggestions', http_method='GET',
                      name='get_suggestions')
    def get_suggestions(self, _):
        suggestion_list = suggestions.get(endpoints.get_current_user())
        suggestions_msg = []
        for s in suggestion_list:
            message = msg.SuggestionMessage(text=s.text, type=s.type, subject=s.subject)
            suggestions_msg.append(message)
        return msg.SuggestionsMessage(suggestions=suggestions_msg)

    # User
    @endpoints.method(message_types.VoidMessage, msg.UserMessage,
                      path='get_user_info', http_method='GET',
                      name='get_user_info')
    def get_user_info(self, _):
        usr = user.get(endpoints.get_current_user())
        fixedSubjects = []
        for s in usr.subjects:
            if s == 'MA':
                fixedSubjects.append('MATH')
            else:
                fixedSubjects.append(s)

        return msg.UserMessage(
            name=usr.name,
            subjects=fixedSubjects,
            points=usr.points,
            rank=usr.rank,
            cls=usr.cls
        )

    @endpoints.method(message_types.VoidMessage, msg.UsersMessage,
                      path='get_scoreboard', http_method='GET',
                      name='get_scoreboard')
    def get_scoreboard(self, _):
        users = user.get_scoreboard(endpoints.get_current_user())
        message = []
        for u in users:
            message.append(
                msg.UserMessage(
                    name=u.name,
                    points=u.points,
                    rank=u.rank
                )
            )
        return msg.UsersMessage(users=message)


API = endpoints.api_server([EduAPI])
