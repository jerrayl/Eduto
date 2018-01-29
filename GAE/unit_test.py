import unittest
import datetime
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.api import users

import user
import beacon
import task
import attendance
import sgtime


class MainTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        ndb.get_context().clear_cache()

        # Add users
        user.add(
            email="lee.weijie@dhs.sg",
            name="Lee Wei Jie",
            cls="5C23",
            subjects=["COMP", "PHY", "MATH"],
            school="dhs"
        )

        user.add(
            email="ng.jerrayl@dhs.sg",
            name="Jerrayl",
            cls="5C23",
            subjects=["COMP", "MATH"],
            school="dhs"
        )

        self.weijie = users.User("lee.weijie@dhs.sg")
        self.jerrayl = users.User("ng.jerrayl@dhs.sg")

        # Add beacon
        beacon.add(
            uuid="123",
            location_name="test",
            school="dhs"
        )

    def test_task(self):
        task.add(
            subject="PHY",
            cls="5C23",
            title="test1",
            due_date=datetime.date(2016, 8, 28),
            usr=self.weijie
        )

        # Check task filtering by subject combination
        tasks = task.get_list(self.weijie)
        self.assertEqual(tasks[0].title, "test1")
        task_key = tasks[0].key.urlsafe()

        tasks = task.get_list(self.jerrayl)
        self.assertEqual(tasks, [])

        # Check edit & get task
        task.edit(
            subject="PHY",
            cls="5C23",
            title="test2",
            due_date=datetime.date(2016, 8, 28),
            url_id=task_key,
            usr=self.weijie
        )

        task1 = task.get(task_key, self.weijie)
        assert task1.title == "test2"

        # Check delete task
        task.remove(task_key, self.weijie)
        assert not task.get_list(self.weijie)

    def test_attendance(self):
        # Enter
        attendance.add_event("123", 1, self.weijie)
        location = attendance.get_user_location(self.weijie)
        self.assertEqual(location, "test")

        # Exit
        attendance.add_event("123", 0, self.weijie)
        location = attendance.get_user_location(self.weijie)
        self.assertNotEqual(location, "test")

        # Attendance checks
        now = sgtime.get_datetime_now()
        status = attendance.check("test", self.weijie, now-datetime.timedelta(hours=1), now)
        self.assertEqual(status, True)

        status = attendance.check("test", self.jerrayl, now - datetime.timedelta(hours=1), now)
        self.assertEqual(status, False)

        # Pre-marked attendance
        attendance.AttendanceActivity(
            uuid="123",
            usr=self.jerrayl,
            type=1,
            time=now - datetime.timedelta(hours=2)
        ).put()

        status = attendance.check("test", self.jerrayl, now - datetime.timedelta(hours=1), now)
        self.assertEqual(status, True)

        attendance.AttendanceActivity(
            uuid="123",
            usr=self.jerrayl,
            type=0,
            time=now - datetime.timedelta(hours=1, minutes=30)
        ).put()

        status = attendance.check("test", self.jerrayl, now - datetime.timedelta(hours=1), now)
        self.assertEqual(status, False)










