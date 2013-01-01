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

#page to allow users to find the top courses according to the criteria they define
def top_courses(request):

    #get number of courses to be on the page
    n = 50
    if ('n' in request.GET) and request.GET['n'].isdigit():
        n = request.GET['n']

    if ('category' in request.GET) and request.GET['category'].strip():
        filter = request.GET['category']
    else:
        filter = 'overall'


    #filter out generic expos 20 and courses that do not have scores in the database
    courses = Qcourses.objects.all().exclude(overall = None).exclude(cat_num = 5518)

    #set order of values
    if ('reverse' in request.GET) and request.GET['reverse'].strip() and string.lower(request.GET['reverse']) == 'true':
        courses=courses.order_by(filter)
    else:
        courses = courses.order_by('-'+filter)

    #filter by various traits
    if ('year' in request.GET) and request.GET['year'].strip() and string.lower(request.GET['year']) != 'all':
        print request.GET['year']
        courses=courses.filter(year__exact = int(request.GET['year']))

    if ('term' in request.GET) and request.GET['term'].strip() and string.lower(request.GET['term']) != 'both':
        courses=courses.filter(term__exact = convert_term(request.GET['term']) )

    if ('enrollment' in request.GET) and request.GET['enrollment'].strip():
        courses=courses.filter(enrollment__gte = (request.GET['enrollment']) ) #greater than or equal to min enrollment

    #take first n courses
    courses = courses[:n]

    return render_to_response('course_list_filters.html', {'course_list': courses}, context_instance=RequestContext(request))


#view all of the courses in a department
def department_view(request, field):

    field = string.upper(field)

    queryset = Qcourses.objects.filter(field__startswith = field).order_by('-overall')

    #check if additional filters are in get and refine accordingly
    if ('year' in request.GET) and request.GET['year'].strip():
        queryset=queryset.filter(year__exact = request.GET['year'])

    if ('term' in request.GET) and request.GET['term'].strip():
        queryset=queryset.filter(term__exact = convert_term(request.GET['term']) )

    return render_to_response('course_list.html', {'course_list': queryset},
        context_instance=RequestContext(request))

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

    #see what page is requested, default to 1
    p = 1
    if ('p' in request.GET) and request.GET['p'].isdigit():
        p = int(request.GET['p'])



    #group unique courses together
    unique = {}
    for course in courses:
        if course.cat_num in unique:
            unique[course.cat_num].append(course)
        else:
            unique[course.cat_num] = [course]

    #make each unique course into a new course object
    course_list = []

    #make the most recent instance of class (greatest year) the base isntance
    for years in unique.values():
        base = years[0]
        #assign the most recent year to the base
        for c in years:
            if c.year > base.year:
                base = c
        #gets the average rating for the course
        base.average_overall = average([c.overall for c in years ])
        course_list.append(base)


    #get the courses that should be on this page
    num_courses = len(course_list)
    start =  (p-1) * courses_per_page
    this_page = []
    for i, c in enumerate(course_list[start:]):
        #if true no more courses need to go on this page
        if i == courses_per_page: 
            break
        this_page.append(c)


    return render_to_response('search_results.html', {'course_list': this_page, 'q': query_string,
                                                      'pages': [x+1 for x in range(1+num_courses/courses_per_page)], 'results' : num_courses, 'hints' : hints,
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

    print query_string

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

#detailed view of a single course 
def course_detail(request, course_field, course_number):
    course_number = string.replace(string.upper(course_number),'_',' ')


    courses = Qcourses.objects.filter(field__exact = string.upper(course_field)).filter(number__exact = course_number).order_by('-year')

    if not courses:
        return render_to_response('no_course_found.html', {}, context_instance=RequestContext(request))

    #add a comments attribute to each course with all of its comments
    for course in courses:
        course.comments = Qcomments.objects.filter(course_id = course.course_id)

    return render_to_response('course.html', {'courses': courses}, context_instance=RequestContext(request))

#detailed view of a professor
def prof_detail(request, id):
    #get professor by id number
    prof_rows = Qinstructors.objects.filter(prof_id = id)

    #find the unique classes they teach
    classes = {}
    for row in prof_rows:
        #get an instance of a course
        row.course = Qcourses.objects.filter(course_id__exact = row.course_id)[0]

        #create a new table for the course if it is the first instance
        #otherwise add it to the list of the course's instances
        if row.course.cat_num in classes:
            classes[row.course.cat_num].append(row)
        else:
            classes[row.course.cat_num] = [row]

    return render_to_response('prof_detail.html', {'classes': classes.values() }, context_instance=RequestContext(request))


