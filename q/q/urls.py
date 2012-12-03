from django.conf.urls import patterns, url
from django.views.generic import ListView, TemplateView
from viewer.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', index, name='index'),

    url(r'^about/', TemplateView.as_view(template_name="about.html")),
    (r'^(\w+)/$', CourseListView.as_view()),

    (r'^(\w+)/(\d{4})$', CourseListView.as_view()),
    (r'^(\w+)/(\d{4})/(\w+)$', CourseListView.as_view()),
    (r'^(\w+)/(\d{4})/(\w+)$', CourseListView.as_view()),
    (r'^(\w+)/(\d{4})/(\w+)$', CourseListView.as_view())
    # url(r'^q/', include('q.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
