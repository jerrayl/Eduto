# -*- coding: utf-8 -*-
import user
import attendance
import sgtime
import task

from google.appengine.ext import ndb


SUGGESTION_TYPES = ['lessoninfo', 'quote', 'homeworkdue', 'nextlesson']


class Suggestion(ndb.Model):
    text = ndb.TextProperty(required=True)
    date = ndb.DateProperty(required=True)
    type=ndb.StringProperty(required=True, choices=SUGGESTION_TYPES)
    location = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    usr = ndb.UserProperty(required=True)


def add(text, date, type, subject, location, usr):
    Suggestion(
        text=text,
        date=date,
        type=type,
        subject=subject,
        location=location,
        usr=usr
    ).put()


def remove(url_id, usr):
    key = ndb.Key(urlsafe=url_id)
    if key.get().usr == usr:
        key.delete()
    else:
        raise Exception('Unauthorised to delete')


def get(usr):
    usr_details = user.get(usr)
    usr_location = attendance.get_user_location(usr)
    today = sgtime.get_datetime_now().replace(hour=0, minute=0, second=0, microsecond=0)

    suggestions = Suggestion.query(
        Suggestion.date == today,
        Suggestion.subject.IN(usr_details.subjects),
        Suggestion.location == usr_location
    ).fetch()

    if attendance.get_user_location(usr) == 'Comp Lab S2':
        for t in task.get_due_homework(usr, 'COMP'):
            suggestions.append(Suggestion(
                text=t.title + ' due this lesson',
                type='homeworkdue',
                subject=t.subject
            ))
    string = unicode("\n大学之道，在明明德， 在亲民，在止于至善。", "utf-8" )
    suggestions.append(Suggestion(
        text='Quote of the day: '+ string,
        type='quote',
        subject='GP'
    ))
    return suggestions


def get_all():
    today = sgtime.get_datetime_now().date()
    suggestions = Suggestion.query(
        Suggestion.date >= today
    ).fetch()
    return suggestions
