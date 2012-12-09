from django.conf.urls import patterns, url
from django.views.generic import ListView, TemplateView
from viewer.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', course_root, name = "course_root" ),
    url(r'^courses/$', course_root, name = "course_root" ),
    url(r'^courses/search/$', course_search_results, name='search'), #search

    url(r'^courses/top/$', top_courses, name='top_courses'), #filter_by
    url(r'^courses/([a-zA-Z&-]+)/$', department_view, name='department'), #department
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/$', course_detail, name = "course_detail" ), #courses


    url(r'^profs/search/$', prof_search_results, name = "prof_search" ),
    url(r'^profs/$', prof_root, name = "prof_root" ),
    url(r'^profs/(?P<id>\w+)/$', prof_detail, name = "prof_detail" ), #professors


    url(r'^about/', TemplateView.as_view(template_name="about.html")),


#    (r'^(\w+)/(\d{4})/$', CourseListView.as_view()), #deparment/year
#    (r'^(\w+)/(\w{4,6})/$', CourseListView.as_view()), #deparment/term
#    (r'^(\w+)/(\d{4})/(\w{4,6})$', CourseListView.as_view()), #department/year/term
#    (r'^(\w+)/(\w{4,6})/(\d{4})$', CourseListView.as_view()), #department/term/year


    # url(r'^q/', include('q.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
