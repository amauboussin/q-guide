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
import charts

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

    prof_detail_data, prof_detail_labels = charts.get_prof_detail_chart(classes.values())

    print str(prof_detail_labels)

    return render_to_response('prof_detail.html', {'classes': classes.values(),
                'prof_detail_data' : prof_detail_data, 'prof_detail_labels' : str(prof_detail_labels)  },
                context_instance=RequestContext(request))