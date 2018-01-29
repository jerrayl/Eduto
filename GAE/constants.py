from collections import OrderedDict

SCHOOL = 'dhs'

ENTER = 1
EXIT = 0

SUBJECTS = OrderedDict(sorted({'ART': 'Art',
                               'BIO': 'Biology',
                               'CHEM': 'Chemistry',
                               'CL': 'Chinese Language',
                               'CLTRANS': 'Translation',
                               'CLL': 'Chinese Literature',
                               'CSC': 'Chinese Studies in Chinese',
                               'COMP': 'Computing',
                               'ELL': 'English Linguistic',
                               'ELIT': 'English Literature',
                               'ECONS': 'Economics',
                               'FM': 'Further Math',
                               'GP': 'General Paper',
                               'GSC': 'General Studies in Chinese',
                               'GEO': 'Geography',
                               'LA': 'Language Arts',
                               'HIST': 'History',
                               'MATH': 'Math',
                               'PHY': 'Physics',
                               'PW': 'Project Work'
                               }.items(), key=lambda (code, name): name))
