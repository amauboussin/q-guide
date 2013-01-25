from django.http import HttpResponse
from django.shortcuts import render_to_response
from viewer.models import *
from django.template.context import RequestContext
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
import string
from helper import *
from charts import *
from django.db.models import Q
from operator import attrgetter
from ajax_helper import num_comments

#homepage. presents 3 ways to find courses
def course_root(request):
    fields = Qfields.objects.all()
    return render_to_response('course_root.html', {'fields': fields}, context_instance=RequestContext(request))

#detailed view of a single course 
def course_detail(request, course_field, course_number, year = None, term = None):
    comments_per_page = 10

    course_number = string.replace(string.upper(course_number),'_',' ')
    #get all instances of the course
    courses = Qcourses.objects.filter(field__exact = string.upper(course_field)).filter(number__exact = string.upper(course_number)).order_by('-term').order_by('-year')


    #filter courses by additional parameters (if given)
    selected_courses = courses

    if year is not None:
        selected_courses = selected_courses.filter(year__exact = year).order_by('-term')

    if term is not None:
        if string.upper(term) != "FALL" and string.upper(term) != "SPRING":
            return render_to_response('no_course_found.html', {}, context_instance=RequestContext(request))

        term_num = 1 if string.upper(term) == "FALL" else 2
        selected_courses = selected_courses.filter(term__exact = term_num).order_by('-year')

    if not selected_courses:
        return render_to_response('404.html', {}, context_instance=RequestContext(request))


    selected = selected_courses[0]


    prof_history_data, prof_history_labels = get_prof_history_chart(courses, selected)
    prof_chart_data, num_profs = selected.get_prof_chart()
    enrollment_data = get_enrollment_chart(courses)
    ratings_data = get_ratings_chart(courses)



    comments_per_page = 10
    comment_count = num_comments(courses)
    num_pages = comment_count / comments_per_page

    if comment_count % comments_per_page != 0:
        num_pages += 1

    return render_to_response('course.html', {'selected_course': selected, 'courses': courses, 'num_pages': num_pages,
            'enrollment_data': enrollment_data, 'prof_chart_data': prof_chart_data, 'one_prof': num_profs <2, 'prof_history_labels': str(prof_history_labels),'prof_history_data' : prof_history_data,
            'ratings_data': ratings_data}, context_instance=RequestContext(request))

#page to allow users to find the top courses according to the criteria they define
def top_courses(request):

    #get number of courses to be on the page
    n = 50
    if ('n' in request.GET) and request.GET['n'].isdigit():
        n = request.GET['n']

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

def trends(request):
    fields = list(Qfields.objects.all())
    for field in fields:
        courses = list(Qcourses.objects.filter(field__startswith = field.field).filter(year = 2011))
        field.n = len(courses)
        sum = 0
        for c in courses:
            if c.enrollment is not None:
                sum += c.enrollment
        field.enrollment = sum


    fields[:] = [f for f in fields if f.enrollment > 50]


    return render_to_response('trends.html', {'fields': fields},
        context_instance=RequestContext(request))