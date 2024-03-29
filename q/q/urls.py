from django.conf.urls import patterns, url
from django.views.generic import ListView, TemplateView
import viewer.course_views
from viewer import ajax, course_views, prof_views, search_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    # Splash page
    url(r'^preview/$', course_views.splash, name = "preview"),
    # demo page - open to the world
    url(r'^demo/$', course_views.demo, name = "demo"),

    # URLs that return JSON (for Ajax)
    # Comments URLs: course_url/comments/?first=num1&last=num2
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/(?P<year>[0-9]+)/(?P<term>[a-zA-Z]+)/comments/$', ajax.ajax_comments, name = "comments" ), # inclusive, zero-indexed range of comments for  course in term/year
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/(?P<year>[0-9]+)/comments/$', ajax.ajax_comments, name = "comments" ), # inclusive, zero-indexed range of comments for latest course in year
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/(?P<term>[a-zA-Z]+)/comments/$', ajax.ajax_comments, name = "comments" ), # inclusive, zero-indexed range of comments for latest course in term
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/comments/$', ajax.ajax_comments, name = "comments" ), # inclusive, zero-indexed range of comments for latest course

    # url(r'^$', course_root, name = "course_root" ), #homepage
    url(r'^$', course_views.home, name = "homepage" ), #homepage
    url(r'^courses/$', course_views.course_root, name = "course_root" ), #homepage
    url(r'^courses/search/$', search_views.course_search_results, name='search'), #course search
    url(r'^courses/top/$', course_views.top_courses, name='top_courses'), # top courses page. parameters are defined by get variables
    url(r'^courses/([a-zA-Z&-]+)/$', course_views.department_view, name='department'), #view all of the courses in the department
    # course detail URLs
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/(?P<year>[0-9]+)/(?P<term>[a-zA-Z]+)/$', course_views.course_detail, name = "course_detail" ), # detailed view of a course with defined year/term
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/(?P<year>[0-9]+)/$', course_views.course_detail, name = "course_detail" ), # detailed view of a course, defaults to most current term
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/(?P<term>[a-zA-Z]+)/$', course_views.course_detail, name = "course_detail" ), # detailed view of course, defaults to most current year
    url(r'^courses/(?P<course_field>[a-zA-Z&-]+)/(?P<course_number>[0-9.a-zA-Z]+)/$', course_views.course_detail, name = "course_detail" ), # detailed view of a course, defaults to most current year/term
    # instructor URLs
    url(r'^profs/search/$', search_views.prof_search_results, name = "prof_search" ), #page with professor search box
    url(r'^profs/(?P<id>\w+)/$', prof_views.prof_detail, name = "prof_detail" ), #all of the professor's courses in one page

    # url(r'^home/$', home, name = "home" ),

    # (r'^compare/$', 'django.views.generic.simple.direct_to_template', {'template': 'static/compare_courses.html'}),

    url(r'^trends/$', course_views.trends, name='trends'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)