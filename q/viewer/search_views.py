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
from django.http import HttpResponseRedirect

from course_views import course_detail

#search results page for courses
def course_search_results(request):
    courses_per_page = 30 #constant
    hints = "Type a course's abbreviation (cs50), catalog number (4949), or just try some keywords (introduction to computer science)."

    #get query string from GET
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        courses = search_for_courses(query_string)
    else:
        courses = []

    course_list = group_courses(courses)

    #redirect directly to page if only one result
    if len(course_list) == 1:
        return HttpResponseRedirect(course_list[0].get_absolute_url())

    #see what page is requested, default to 1
    p = 1
    if ('p' in request.GET) and request.GET['p'].isdigit():
        p = int(request.GET['p'])


    print 'im here in search views'
    print course_list
    #get the courses that should be on this page
    num_courses = len(course_list)
    start =  (p-1) * courses_per_page
    this_page = []
    for i, c in enumerate(course_list[start:]):
        #if true no more courses need to go on this page
        if i == courses_per_page: 
            break
        this_page.append(c)

    pages = [x+1 for x in range(1+num_courses/courses_per_page)]

    print 'im here later in search views'
    print  this_page
    return render_to_response('search_results.html', {'course_list': this_page, 'q': query_string,
                                                      'pages': pages, 'results' : num_courses, 'hints' : hints,
                                                      'num_pages': 1+num_courses/courses_per_page, 'page' : p, 'extend':"course_list.html", "form_action" : "/courses/search/"},
        context_instance=RequestContext(request))

#search results page for professors
def prof_search_results(request):
    profs_per_page = 20 # constant
    hints = 'Type the last name of any professor.'

    #get the profs according to the defined query
    query_string = ''
    profs = []
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        profs = search_for_profs(query_string)


    #see what page is requested, default to 1
    p = 1
    if ('p' in request.GET) and request.GET['p'].isdigit():
        p = int(request.GET['p'])

    #group unique professors together
    unique = {}
    for prof in profs:
        if prof.prof_id in unique:
            unique[prof.prof_id].append(prof)
        else:
            unique[prof.prof_id] = [prof]

    #make each unique professor into a new professor object
    prof_list = []
    for prof_classes in unique.values():
        base = prof_classes[0]
        base.average_overall = average([float(c.overall) for c in prof_classes ])
        prof_list.append(base)

    num_profs = len(prof_list)

    #get the professors that should be on this page
    start =  (p-1) * profs_per_page
    this_page = []
    for i, c in enumerate(prof_list[start:]):
        if i == profs_per_page: #no more professors need to go on this page
            break
        this_page.append(c)

    return render_to_response('search_results.html', {'profs': this_page, 'q': query_string,
        'pages': [x+1 for x in range(1+num_profs/profs_per_page)], 'results' : num_profs, 'hints': hints,
        'num_pages': 1+num_profs/profs_per_page, 'page' : p, 'extend':"prof_list.html", "form_action" : "/profs/search/"},
        context_instance=RequestContext(request))