from django.http import HttpResponse
from django.shortcuts import render_to_response
from viewer.models import Qcourses
from django.template.context import RequestContext

def index(request):
    classes = Qcourses.objects.order_by('-enrollment')[:20]
    return render_to_response('index.html', {'classes': classes}, context_instance=RequestContext(request))