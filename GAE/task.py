import user
import sgtime

from google.appengine.ext import ndb


class Task(ndb.Model):
    school = ndb.StringProperty(required=True)
    cls = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    usr = ndb.UserProperty(required=True)
    time_added = ndb.DateTimeProperty(required=True)
    subject = ndb.StringProperty(required=True)
    due_date = ndb.DateProperty(required=True)
    done_users = ndb.UserProperty(repeated=True)


# Get lists of relevant tasks from a group
def get_list(usr):
    user_info = user.get(usr)
    tasks = Task.query(
        Task.school == user_info.school,
        Task.due_date >= sgtime.get_datetime_now(),
        Task.cls == user_info.cls,
        Task.subject.IN(user_info.subjects)
    ).fetch()
    tasks.sort(key=lambda x: x.time_added, reverse=True)
    for t in tasks:
        t.done = usr in t.done_users
    return tasks


def get_tasks():
    tasks = Task.query(
        Task.due_date >= sgtime.get_datetime_now()
    ).fetch()
    tasks.sort(key=lambda x: x.time_added, reverse=True)
    return tasks


def get_all_tasks():
    tasks = Task.query(
    ).fetch()
    tasks.sort(key=lambda x: x.time_added, reverse=True)
    return tasks


def get_workload_weekly(cls):
    tasks = Task.query(
        Task.cls == cls
    ).fetch()
    arr = [0,0,0,0,0]
    for task in tasks:
        day = int(task.due_date.strftime('%d'))
        if 19 <= day <= 20:
            arr[0]+=1
        elif 21 <= day <= 23:
            arr[1] += 1
        elif 24 <= day <= 26 :
            arr[2] += 1
        elif 27 <= day <= 29 :
            arr[3] += 1
        else:
            arr[4] += 1
    return arr


def get(url_id, usr):
    user_info = user.get(usr)
    task = ndb.Key(urlsafe=url_id).get()

    if task.cls != user_info.cls:
        raise Exception('Unauthorized to view task')
    else:
        return task


def add(subject, cls, title, due_date, usr):
    user_info = user.get(usr)
    if cls == user_info.cls and (subject in user_info.subjects):
        Task(
            school=user_info.school,
            subject=subject,
            cls=cls,
            title=title,
            due_date=due_date,
            usr=usr,
            time_added=sgtime.get_datetime_now()
        ).put()
        user.increment_points(usr)
    else:
        raise Exception('Unauthorized to add task')


def edit(url_id, subject, cls, title, due_date, usr):
    task = ndb.Key(urlsafe=url_id).get()
    assert usr == task.usr
    task.subject = subject
    task.cls = cls
    task.title = title
    task.due_date = due_date
    task.put()


def remove(url_id, usr):
    task = ndb.Key(urlsafe=url_id).get()
    assert usr == task.usr
    task.key.delete()


def toggle_done(url_id, usr):
    task = ndb.Key(urlsafe=url_id).get()
    if usr in task.done_users:
        task.done_users.remove(usr)
    else:
        task.done_users.append(usr)
    task.put()


def get_scoreboard(cls):
    return user.User.query(
        user.User.cls == cls
    ).fetch()


def get_due_homework(usr, subject):
    today = sgtime.get_datetime_now().date()
    return [x for x in get_list(usr) if x.due_date == today or x.subject==subject]
