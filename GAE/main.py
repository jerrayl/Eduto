#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from google.appengine.api import users, mail
import jinja2
import webapp2
import user
import suggestions
import datetime
import constants
import beacon
import time
import attendance
import task
import random
today = datetime.date.today().strftime("%Y-%m-%d")

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class AddUsers(webapp2.RequestHandler):
    def get(self):
        user.add()
        self.response.write('Nothing here')


class Home(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            log = ""
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            log = "(Not logged in)"
        template_values = {
            'log': log,
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('html/index.html')
        self.response.write(template.render(template_values))


class Suggestions(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        if not usr:
            self.redirect("/")
        suggestion_list = [[i.location, i.date, constants.SUBJECTS[i.subject], i.text, i.key] for i in
                           suggestions.get_all()]
        locations = [b.location_name for b in beacon.get_list()]
        subjects = constants.SUBJECTS.items()
        template_values = {'rows': suggestion_list, 'locations': locations, 'subjects': subjects}
        template = JINJA_ENVIRONMENT.get_template('html/suggestions.html')
        self.response.write(template.render(template_values))

    def post(self):
        usr = users.get_current_user()
        entered_date = self.request.get('date').split("-")
        suggestions.add(self.request.get('message'),
                        datetime.date(int(entered_date[0]), int(entered_date[1]), int(entered_date[2])),
                        'lessoninfo',
                        self.request.get('subject'), self.request.get('location'), usr)
        time.sleep(0.1)
        self.redirect(self.request.referer)


class Locations(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
        beacons = [[i.location_name, i.uuid] for i in beacon.get_list()]
        template_values = {'beacons': beacons}
        template = JINJA_ENVIRONMENT.get_template('html/locations.html')
        self.response.write(template.render(template_values))

    def post(self):
        beacon.add(self.request.get('uuid'), self.request.get('location'), constants.SCHOOL)
        time.sleep(0.1)
        self.redirect(self.request.referer)


class Attendance(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
        locations = [b.location_name for b in beacon.get_list()]
        template_values = {'locations': locations, 'today': today}
        template = JINJA_ENVIRONMENT.get_template('html/attendance.html')
        self.response.write(template.render(template_values))

    def post(self):
        start_time = datetime.datetime.strptime(self.request.get('date') + "T" + self.request.get('start_time'),
                                                '%Y-%m-%dT%H:%M')
        end_time = datetime.datetime.strptime(self.request.get('date') + "T" + self.request.get('end_time'),
                                              '%Y-%m-%dT%H:%M')
        results = attendance.batch_check(self.request.get('location'), constants.SCHOOL, self.request.get('class'),
                                         start_time, end_time)
        rows = [[result['usr'].name, result['present']] for result in results if result['present'] == False]
        if self.request.get('show_all') == "on":
            rows = [[result['usr'].name, result['present']] for result in results]
        locations = [b.location_name for b in beacon.get_list()]
        data1 = [["Present", len([result for result in results if result['present']])],["Absent", len([result for result in results if not result['present']])]]
        data2 = attendance.get_frequent_latecomers(self.request.get('class'))
        template_values = {'locations': locations, 'rows': rows, "data1": data1, "data2": data2, "post": True}
        template = JINJA_ENVIRONMENT.get_template('html/attendance.html')
        self.response.write(template.render(template_values))


class Homework(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
        rows = [[i.title, constants.SUBJECTS[i.subject], i.cls, i.due_date] for i in task.get_tasks()]
        subjects = constants.SUBJECTS.items()
        template_values = {'rows': rows, 'subjects': subjects, 'today': today}
        template = JINJA_ENVIRONMENT.get_template('html/homework.html')
        self.response.write(template.render(template_values))

    def post(self):
        if self.request.get('start_date') != "":
            start = self.request.get('start_date').split("-")
            start = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        else:
            start = ""
        if self.request.get('end_date') != "":
            end = self.request.get('end_date').split("-")
            end = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        else:
            end = ""
        filter = [self.request.get('class'), self.request.get('subject'), start, end]
        rows = [[i.title, i.subject, i.cls, i.due_date] for i in task.get_all_tasks()]
        filtered = []
        for row in rows:
            if (filter[1] == "" or filter[1] == row[1]) and (filter[0] == "" or filter[0] == row[2]) and (
                    filter[2] == "" or filter[2] <= row[3]) and (filter[3] == "" or filter[3] >= row[3]):
                filtered.append(row)
        rows = filtered
        subjects = constants.SUBJECTS.items()
        dic= {}
        for row in rows:
            if row[1] in dic.keys():
                dic[row[1]] +=1
            else:
                dic[row[1]] = 1
        data1 = [[str(k),v] for k,v in dic.items()]
        data2 = []
        weekly = task.get_workload_weekly(self.request.get('class'))
        for i in range(0,5):
            data2.append(["Day "+ str(i*2+1)+"-"+str(i*2+2) , weekly[i]])
        template_values = {'rows': rows, 'subjects': subjects, 'data1': data1, 'data2': data2}
        template = JINJA_ENVIRONMENT.get_template('html/homework.html')
        self.response.write(template.render(template_values))


class Leaderboard(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('html/leaderboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
        cls = self.request.get("class")
        rows = [[i.name, i.points] for i in task.get_scoreboard(cls)]
        rows.sort(key=lambda row: row[1],reverse=True)
        template_values = {"cls":cls, "rows":rows}
        template = JINJA_ENVIRONMENT.get_template('html/leaderboard.html')
        self.response.write(template.render(template_values))

class Mail(webapp2.RequestHandler):
    def get(self):
        mail.send_mail(sender="latecoming@edu-auto.appspotmail.com",
                       to="<ng.jerrayl@dhs.sg>",
                       subject="Your child is late",
                       body="""Dear Parent:\n\nYour child, Lee Wei Jie, arrived in school late today. He/She reached school at 08:15 AM. This is the fourth time this semester he/she has been late, and his/her conduct grade will be lowered. Please let us know if you have any questions.\n\nDunman High School Student Development Department """)
        self.redirect("/attendance")

class Crowd(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
        rows = attendance.get_crowd()
        template_values = {'rows': rows}
        template = JINJA_ENVIRONMENT.get_template('html/crowd.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/add_users', AddUsers),
    ('/', Home),
    ('/suggestions', Suggestions),
    ('/attendance', Attendance),
    ('/homework', Homework),
    ('/locations', Locations),
    ('/leaderboard', Leaderboard),
    ('/mail', Mail),
    ('/crowd', Crowd)
], debug=True)
