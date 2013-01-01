from django.conf.urls import patterns, url
from django.views.generic import ListView, TemplateView
from viewer.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', course_root, name = "course_root" ), #homepage
    url(r'^courses/$', course_root, name = "course_root" ), #homepage
    url(r'^courses/search/$', course_search_results, name='search'), #course search
    url(r'^courses/top/$', top_courses, name='top_courses'), # top courses page. parameters are defined by get variables
    url(r'^courses/([a-zA-Z&-]+)/$', department_view, name='department'), #view all of the courses in the department
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/$', course_detail, name = "course_detail" ), #detailed view of a course
    url(r'^profs/search/$', prof_search_results, name = "prof_search" ), #page with professor search box
    url(r'^profs/(?P<id>\w+)/$', prof_detail, name = "prof_detail" ), #all of the professor's courses in one page

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
