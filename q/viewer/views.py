from django.http import HttpResponse
from django.shortcuts import render_to_response
from viewer.models import *
from django.template.context import RequestContext
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
import string
from helper import *
from django.db.models import Q


def index(request):
    classes = Qcourses.objects.order_by('-overall')[:20]
    return render_to_response('index.html', {'classes': classes}, context_instance=RequestContext(request))

def course_detail(request, course_field, course_number):
    #print 'course number: ',course_number
    course_number = string.replace(string.upper(course_number),'_',' ')

    courses = Qcourses.objects.filter(field__exact = string.upper(course_field)).filter(number__exact = course_number)

    if not courses:
        return render_to_response('no_course_found.html', {}, context_instance=RequestContext(request))

    return render_to_response('course.html', {'courses': courses}, context_instance=RequestContext(request))


def course_root(request):
    fields = Qfields.objects.all()
    return render_to_response('course_root.html', {'fields': fields}, context_instance=RequestContext(request))

def top_courses(request):
    courses = Qcourses.objects.filter(year__exact = 2011).exclude(number__exact = "EXPOS 20").order_by('-enrollment')[:21]
#    for c in courses:
#        if c.get_profs():
#
#            print c.__unicode__(),c.course_id, ', '.join([ p.first+p.last for p in c.get_profs()])
#        else:
#            print c.__unicode__(), 'NO PROF'

    return render_to_response('course_list.html', {'course_list': courses}, context_instance=RequestContext(request))


def search_results(request):
    courses_per_page = 30 #constant

    courses = []
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        courses = search_for_courses(query_string)

    p = 1
    if ('p' in request.GET) and request.GET['p'].isdigit():
        p = int(request.GET['p'])

    num_courses = courses.count()

    #get the courses that should be on this page
    start =  (p-1) * courses_per_page
    this_page = []
    for i, c in enumerate(courses[start:]):
        if i == courses_per_page: #no more courses need to go on this page
            break
        this_page.append(c)

    return render_to_response('search_results.html', {'course_list': this_page, 'q': query_string,
        'pages': [x+1 for x in range(1+num_courses/courses_per_page)], 'results' : num_courses,
        'num_pages': 1+num_courses/courses_per_page},
        context_instance=RequestContext(request))
#

def prof_detail(request, prof_first, prof_last):
    first = string.replace(prof_first.title(), '_', ' ')
    last = string.replace(prof_last.title(), '_', ' ')
    prof_rows = Qinstructors.objects.filter(first__exact = first).filter(last__exact = last)
    ids = []
    for row in prof_rows:
        if row.course_id not in ids:
            ids.append(row.course_id)

    courses = Qcourses.objects.filter(reduce(lambda x, y: x | y, [Q(course_id__exact=id) for id in ids]))

    #    cat_nums = [prof_row.cat_num for prof_row in prof_rows]
#    courses = Qcourses.objects.filter(cat_num__exact = prof.cat_num)
    return render_to_response('prof_detail.html', {'prof_rows': prof_rows, 'courses':courses }, context_instance=RequestContext(request))


class CourseListView(ListView):

    context_object_name = "course_list"
    template_name = "course_list.html"

    def get_queryset(self):

        field = string.upper(self.args[0])
        year = ''; term = ''
        for i in range(1,len(self.args)):
            if (self.args[i]).isdigit() and len(self.args[i]) == 4: #parameter is a year
                year = int(self.args[i])
            else: #if this is anything but fall or spring the query will be blank
                term = convert_term(self.args[i])

        queryset = Qcourses.objects.filter(field__startswith = field)
        if year != '':
            queryset=queryset.filter(year__exact = year)
        if term !='':
            queryset=queryset.filter(term__exact = term)

        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseListView, self).get_context_data(**kwargs)

        #add term data and styling for bar
        for course in context['course_list']:
            if 4<course.overall:
                course.style = 'progress-success'
            elif 3<=course.overall<=4 :
                course.style = 'progress-warning'
            else:
                course.style = 'progress-danger'
            course.percent = course.overall * 20

        return context