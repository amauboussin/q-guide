from django.http import HttpResponse
from django.shortcuts import render_to_response
from viewer.models import Qcourses
from django.template.context import RequestContext
from django.views.generic import ListView, TemplateView
from django.shortcuts import get_object_or_404
import string


def index(request):
    classes = Qcourses.objects.order_by('-enrollment')[:20]
    return render_to_response('index.html', {'classes': classes}, context_instance=RequestContext(request))

def course(request):
    return ''

class CourseListView(ListView):

    context_object_name = "course_list"
    template_name = "course_list.html"

    def get_queryset(self):
        department = string.upper(self.args[0])

        #if year if specified in url
        if len(self.args) > 1:
            year = int(self.args[1])

            #if nothing else return
            if len(self.args) == 2:
                return  Qcourses.objects.filter\
                    (number__startswith = department).filter(
                    year__exact = year
                )
            #if term is specified in url
            if len(self.args) == 3:
                 if string.lower(self.args[2]) == 'fall':
                     term = 1
                 elif string.lower(self.args[2]) == 'spring':
                     term = 2
                 else: term = 0

                 return  Qcourses.objects.filter \
                     (number__startswith = department).filter(
                     year__exact = year
                     ).filter(term__exact = term)

        return  Qcourses.objects.filter(number__startswith = department)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseListView, self).get_context_data(**kwargs)
        for course in context['course_list']:
            if course.term == 1:
                course.term = 'Fall'
            else:
                course.term = 'Spring'
            if 4<course.overall:
                course.style = 'progress-success'
            elif 3<=course.overall<=4 :
                course.style = 'progress-warning'
            else:
                course.style = 'progress-danger'
            course.percent = course.overall * 20
        #context['percentages'] = percentages
        return context