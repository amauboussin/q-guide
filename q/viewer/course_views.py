from django.http import HttpResponse
from django.shortcuts import render_to_response
from viewer.models import *
from django.template.context import RequestContext
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
import string
from helper import *
from django.db.models import Q
from operator import attrgetter

#homepage. presents 3 ways to find courses
def course_root(request):
    fields = Qfields.objects.all()
    return render_to_response('course_root.html', {'fields': fields}, context_instance=RequestContext(request))

#detailed view of a single course 
def course_detail(request, course_field, course_number, year = None, term = None):

    course_number = string.replace(string.upper(course_number),'_',' ')
    #get all instances of the course
    courses = Qcourses.objects.filter(field__exact = string.upper(course_field)).filter(number__exact = string.upper(course_number)).order_by('-term').order_by('-year')

    if year is not None:
        courses = courses.filter(year__exact = year).order_by('-term')
    if term is not None:
        if string.upper(term) != "FALL" and string.upper(term) != "SPRING":
            return render_to_response('no_course_found.html', {}, context_instance=RequestContext(request))

        term_num = 1 if string.upper(term) == "FALL" else 2
        courses = courses.filter(term__exact = term_num).order_by('-year')

    if not courses:
        return render_to_response('no_course_found.html', {}, context_instance=RequestContext(request))

    #add a comments attribute to each course with all of its comments
    for course in courses:
        course.comments = Qcomments.objects.filter(course_id = course.course_id)


    return render_to_response('course.html', {'courses': courses}, context_instance=RequestContext(request))

#page to allow users to find the top courses according to the criteria they define
def top_courses(request):

    #get number of courses to be on the page
    n = 50
    if ('n' in request.GET) and request.GET['n'].isdigit():
        n = request.GET['n']

#    if ('category' in request.GET) and request.GET['category'].strip():
#        filter = request.GET['category']
#    else:
#        filter = 'overall'


    #filter out generic expos 20 and courses that do not have scores in the database to get baseline courses
    courses = Qcourses.objects.all().exclude(overall = None).exclude(cat_num = 5518)

    courses = filter_courses(courses, request.GET)


    #take first n courses
    courses = courses[:n]

    return render_to_response('course_list_filters.html', {'course_list': courses}, context_instance=RequestContext(request))


#view all of the courses in a department
def department_view(request, field):

    field = string.upper(field)
    queryset = Qcourses.objects.filter(field__startswith = field).order_by('-overall')
    filtered = filter_courses(queryset, request.GET)
    course_list = group_courses(filtered)


    #reorder courses
    if ('reverse' in request.GET) and request.GET['reverse'].strip() and string.lower(request.GET['reverse']) == 'true':
        to_reverse = False
    else:
        to_reverse = True

    if ('category' in request.GET) and request.GET['category'].strip():
            field_name = request.GET['category']
    else:
        field_name = 'overall'


    course_list.sort( key = lambda x: getattr(x, field_name), reverse = to_reverse)


    return render_to_response('course_list_filters.html', {'course_list': course_list},
        context_instance=RequestContext(request))