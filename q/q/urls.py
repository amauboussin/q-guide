from django.conf.urls import patterns, url
from django.views.generic import ListView, TemplateView
from viewer.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', index, name='index'),
    url(r'^courses/$', course_root, name = "course_root" ),
    url(r'^courses/(?P<course_field>\w+)/(?P<course_number>\w+)/$', course_detail, name = "course_detail" ), #courses
    url(r'^profs/(?P<prof_first>\w+)-(?P<prof_last>\w+)/$', prof_detail, name = "prof_detail" ), #professors


    url(r'^about/', TemplateView.as_view(template_name="about.html")),
    (r'^courses/(\w+)/$', CourseListView.as_view()), #department
    (r'^(\w+)/$', CourseListView.as_view()),

    (r'^(\w+)/(\d{4})/$', CourseListView.as_view()), #deparment/year
    (r'^(\w+)/(\w{4,6})/$', CourseListView.as_view()), #deparment/term
    (r'^(\w+)/(\d{4})/(\w{4,6})$', CourseListView.as_view()), #department/year/term
    (r'^(\w+)/(\w{4,6})/(\d{4})$', CourseListView.as_view()), #department/term/year


    # url(r'^q/', include('q.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
