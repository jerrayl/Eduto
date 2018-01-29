from google.appengine.ext import ndb
# import csv
# import re


def calculate_rank(usr):
    if usr.points < 10:
        return 1
    elif usr.points < 30:
        return 2
    elif usr.points < 50:
        return 3
    elif usr.points < 100:
        return 4
    else:
        return 5


class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
    cls = ndb.StringProperty(required=True)
    subjects = ndb.StringProperty(repeated=True)
    is_teacher = ndb.BooleanProperty(default=False, required=True)
    points = ndb.IntegerProperty(default=0, required=True)
    rank = ndb.ComputedProperty(calculate_rank)


def add(email, name, cls, subjects, school):
    User(
        email=email,
        name=name,
        cls=cls,
        subjects=subjects,
        school=school
    ).put()

    # jh = open('y1234out.csv')
    # file = csv.reader(jh)
    # for f in file:
    #     email = f[0]
    #     name = f[1]
    #     cls = f[2]
    #     if cls[0] == 1 or cls[0] == 2:
    #         subjects = ['LA', 'CL', 'MATH', 'PHY', 'CHEM', 'BIO', 'HIST', 'GEO']
    #     else:
    #         subjects = ['LA', 'CL', 'MATH', 'PHY', 'CHEM', 'BIO', 'HIST', 'GEO', 'ELIT', 'ELL', 'CLL']
    #     User(
    #         email=email,
    #         name=name,
    #         cls=cls,
    #         subjects=subjects,
    #         school='dhs'
    #     ).put()
    #
    # file2 = csv.reader(open('y6out.csv'))
    # for f in file2:
    #     User(
    #         email=f[0],
    #         name=f[1],
    #         cls=f[2],
    #         subjects=(re.split('H1|H2', f[3])[1:]) + ['PW'],
    #         school='dhs'
    #     ).put()
    #
    # file3 = csv.reader(open('y5out.csv'))
    # for f in file3:
    #     User(
    #         email=f[0],
    #         name=f[1],
    #         cls=f[2],
    #         subjects=(re.split('H1|H2', f[3])[1:]) + ['PW'],
    #         school='dhs'
    #     ).put()


def get(usr):
    return User.query(
        User.email == usr.email()
    ).fetch()[0]


def increment_points(usr):
    user = get(usr)
    user.points += 1
    user.put()


def get_scoreboard(usr):
    user = get(usr)
    return User.query(
        User.school == user.school,
        User.cls == user.cls
    ).order(-User.points).fetch()
