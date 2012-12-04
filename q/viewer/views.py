from django.http import HttpResponse
from django.shortcuts import render_to_response
from viewer.models import Qcourses
from django.template.context import RequestContext
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
import string
from helper import *


def index(request):
    classes = Qcourses.objects.order_by('-enrollment')[:20]
    return render_to_response('index.html', {'classes': classes}, context_instance=RequestContext(request))

def course_detail(request, course_number):
    course_number = string.replace(string.upper(course_number),'_',' ')
    courses = Qcourses.objects.filter(number__exact = course_number)
    for course in courses:
        course.term = get_term(course.term)
    return render_to_response('course.html', {'courses': courses}, context_instance=RequestContext(request))

def course_root(request):
    return ''


class CourseListView(ListView):

    context_object_name = "course_list"
    template_name = "course_list.html"

    def get_queryset(self):

        department = string.upper(self.args[0])
        year = ''; term = ''
        for i in range(1,len(self.args)):
            if (self.args[i]).isdigit() and len(self.args[i]) == 4: #parameter is a year
                year = int(self.args[i])
            else: #if this is anything but fall or spring the query will be blank
                term = convert_term(self.args[i])

        queryset = Qcourses.objects.filter(number__startswith = department)
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
            course.term = get_term(course.term)
            if 4<course.overall:
                course.style = 'progress-success'
            elif 3<=course.overall<=4 :
                course.style = 'progress-warning'
            else:
                course.style = 'progress-danger'
            course.percent = course.overall * 20
        return context



#def CourseDetailView(DetailView):
#
#    context_object_name = "course"
#    model = Qcourses
#
#    def get_context_data(self, **kwargs):
#        # Call the base implementation first to get a context
#        context = super(CourseDetailView, self).get_context_data(**kwargs)
#        # Add in a QuerySet of all the books
#        return context