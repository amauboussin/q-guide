__author__ = 'Andrew'
from models import *
import string, re

def search_for_courses(q):

    # if the query is a catalog number
    if q.isdigit():
        return Qcourses.objects.filter(cat_num = q).order_by('-year')

    #hardcode in commonly used abbreviations for departments
    departments = {'cs':'compsci', 'am':'apmth', 'ec':'econ', 'ls': 'lifesci',
                   'neuro':'neurobio','spanish':'spansh', 'sls':'sci-livsys' }


    #check to see if the query is a course number i.e. compsci50 or cs50
    field = ''
    num = ''
    for char in q:
        if char.isdigit():
            field, num = q.split(char, 1)
            num = char+num #re-add the splitting digit
            break

    #strip whitespace
    field = string.strip(field)
    num = string.strip(num)

    print field, num
    #check if the query contains an abbreviation
    if field in departments:
        field = departments[field]

    # | chains queries together. i denotes a case insensitive lookup.
    # first see if any results come from querying the course number
    #next add keyword queries. first require q to be its own word then relax that constraint
    return Qcourses.objects.filter(field__iexact = field).filter(number__iexact = num) | \
           Qcourses.objects.filter(title__icontains = ' '+q+ ' ').order_by('-enrollment') |\
           Qcourses.objects.filter(title__istartswith = q).order_by('-enrollment') |\
           Qcourses.objects.filter(title__icontains = q).order_by('-enrollment')


#get a prof given his last name
def search_for_profs(q):
    return Qinstructors.objects.filter(last__iexact = q)| \
           Qinstructors.objects.filter(last__istartswith = q)

#return a numerical representation of the term
def convert_term(term):
    if string.lower(term) == 'fall':
        return 1
    elif string.lower(term) == 'spring':
        return 2
    else:
        return 0 #term is not valid. filtering for term by 0 will return an empty queryset

#average a list of values
def average(list):

    #get rid of bad values
    pop = []
    for i in range(len(list)):
        if list[i] == 'Null' or list[i] < 1:
            pop.append(i)
    for i in pop:
        list.pop(i)

    if len(list) > 0:
        return '%.2f' % (float(sum(list))/len(list))
    else:
        return 'NA'
