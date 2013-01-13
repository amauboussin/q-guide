from django.http import HttpResponse
from viewer.models import *
from django.template.context import RequestContext
import string
from helper import *
from ajax_helper import *
from django.utils import simplejson

# returns comments within an inclusive, zero-indexed range in JSON form
def ajax_comments(request, course_field, course_number, first_comment, last_comment, year = None, term = None):
    # check that comment numbers are digits
    if not first_comment.isdigit() or not last_comment.isdigit():
        return failure_json()

    # convert into useful numbers
    first_comment = int(first_comment)
    last_comment = int(last_comment)

    # ensure comment range makes sense
    if first_comment < 0 or last_comment < 0:
        return failure_json()

    if last_comment < first_comment:
        return failure_json()

    # find courses matching URL parameters
    course_number = string.replace(string.upper(course_number),'_',' ')
    # get all instances of the course
    courses = Qcourses.objects.filter(field__exact = string.upper(course_field)).filter(number__exact = string.upper(course_number)).order_by('-term').order_by('-year')

    #filter by year and term (if defined in URL)
    selected_course = courses
    if year is not None:
        selected_course = selected_course.filter(year__exact = year).order_by('-term')
    if term is not None:
        if string.upper(term) != "FALL" and string.upper(term) != "SPRING":
            return failure_json()

        term_num = 1 if string.upper(term) == "FALL" else 2
        selected_course = selected_course.filter(term__exact = term_num).order_by('-year')

    if not selected_course:
        return failure_json()

    selected_course = selected_course[0]

    # first_comment = 0 corresponds to the first comment in the most recent course selected.  Subsequent comments will move 
    # to previous years, then loop back around to the most recent course's comments, then continue to move backward until it 
    # hits the most recent year selected again.

    courses_before_or_equal = []
    courses_after = []

    for course in courses:

        if course.year > selected_course.year:
            courses_after.append(course)
            continue

        if course.year < selected_course.year:
            courses_before_or_equal.append(course)
            continue

        if course.year == selected_course.year:

            if course.term <= selected_course.term:
                courses_before_or_equal.append(course)
                continue

            if course.term > selected_course.term:
                courses_after.append(course)
                continue


    courses_before_or_equal = sorted(courses_before_or_equal, key=lambda k: 10*k.year + k.term, reverse=True)
    courses_after = sorted(courses_after, key=lambda k: 10*k.year + k.term, reverse=True)

    # build ordered list of dicts in the form {"comment": comment_text, "course_info": associated_course_info}
    comments = []
    append_comments_to_list(comments, courses_before_or_equal)
    append_comments_to_list(comments, courses_after)

    comments_to_show = []

    for i in range(len(comments)):
        if i == last_comment:
            comments_to_show.append(comments[i])
            break
        if i >= first_comment:
            comments_to_show.append(comments[i])

    full_range = i == last_comment

    response = {
                    "i":                 i,
                    "success":           True,
                    "full_range":        full_range,
                    "first_comment":     first_comment, 
                    "last_comment":      last_comment, 
                    "comments_to_show":  comments_to_show
                }

#    courses_after_debug = []
#    for course in courses_after:
#        courses_after_debug.append(str(course.year) + "_" + str(course.term))
#
#    courses_before_or_equal_debug = []
#    for course in courses_before_or_equal:
#        courses_before_or_equal_debug.append(str(course.year) + "_" + str(course.term))
#
#    response = {
#                    "courses_after": courses_after_debug, 
#                    "courses_before_or_equal": courses_before_or_equal_debug,
#                    "term": selected_course.term
#                }

    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')