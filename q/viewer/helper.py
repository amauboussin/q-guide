__author__ = 'Andrew'
from models import Qcourses
import string

def search_for_courses(q):
    return Qcourses.objects.filter(title__icontains = q)

def convert_term(term):
    if string.lower(term) == 'fall':
        return 1
    elif string.lower(term) == 'spring':
        return 2
    else:
        return 0 #term is not valid. filtering for term by 0 will return an empty queryset

