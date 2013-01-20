from django.http import HttpResponse
from viewer.models import *
from django.template.context import RequestContext
import string
from helper import *
from ajax_helper import *
from django.utils import simplejson

# returns data for two courses defined by get parameters in JSON form
def course_info(request):
    # validate GET parameters
    if request.method != 'GET':
        return failure_json("Use GET")

    if not "field" in request.GET or not "num" in request.GET:
        return failure_json("Need \"field\" and \"num\" parameters")

    #set default values for term and year
    year = None if "year" not in request.GET else request.GET["year"];
    term = None if "term" not in request.GET else request.GET["term"];

    # Get data for course.  Copy/pasted from course_views.course_detail
    comments_per_page = 10

    course_number = string.replace(string.upper(request.GET["num"]),'_',' ')
    # get all instances of the course
    courses = Qcourses.objects.filter(field__exact = string.upper(request.GET["field"])).filter(number__exact = string.upper(course_number)).order_by('-term').order_by('-year')

    # filter courses by additional parameters (if given)
    selected_courses = courses

    if year is not None:
        selected_courses = selected_courses.filter(year__exact = year).order_by('-term')
    if term is not None:
        if string.upper(term) != "FALL" and string.upper(term) != "SPRING":
            return failure_json("Invalid term")

        term_num = 1 if string.upper(term) == "FALL" else 2
        selected_courses = selected_courses.filter(term__exact = term_num).order_by('-year')

    if not selected_courses:
        return failure_json("No courses found")

    comments_per_page = 10
    comment_count = num_comments(courses)
    num_pages = comment_count / comments_per_page

    if comment_count % comments_per_page != 0:
        num_pages = num_pages + 1

    courses = list(courses)
    for i in range(len(courses)):
        courses[i] = courses[i].__dict__

    data = {
               'selected_course': selected_courses[0].__dict__, 
               'courses': courses, 
               'num_pages': num_pages
           }

    json = simplejson.dumps(data, default=json_encode_decimal)
    return HttpResponse(json, mimetype='application/json')

# returns comments within an inclusive, zero-indexed range in JSON form
def ajax_comments(request, course_field, course_number, year = None, term = None):

    if request.method != 'GET':
        return failure_json("Use GET")

    if not "first" in request.GET or not "last" in request.GET:
        return failure_json("Need \"first\" and \"last\" parameters")

    first_comment = request.GET["first"]
    last_comment = request.GET["last"]

    # check that comment numbers are digits
    if not first_comment.isdigit() or not last_comment.isdigit():
        return failure_json("\"first\" and \"last\" must be integers")

    # convert into useful numbers
    first_comment = int(first_comment)
    last_comment = int(last_comment)

    # ensure comment range makes sense
    if first_comment < 0 or last_comment < 0:
        return failure_json("Invalid comment range")

    if last_comment < first_comment:
        return failure_json("Invalid comment range")

    # find courses matching URL parameters
    course_number = string.replace(string.upper(course_number),'_',' ')
    # get all instances of the course
    courses = Qcourses.objects.filter(field__exact = string.upper(course_field)).filter(number__exact = string.upper(course_number)).order_by('-term').order_by('-year')

    # filter by year and term (if defined in URL)
    selected_course = courses
    if year is not None:
        selected_course = selected_course.filter(year__exact = year).order_by('-term')
    if term is not None:
        if string.upper(term) != "FALL" and string.upper(term) != "SPRING":
            return failure_json("Invalid term")

        term_num = 1 if string.upper(term) == "FALL" else 2
        selected_course = selected_course.filter(term__exact = term_num).order_by('-year')

    if not selected_course:
        return failure_json("No course found")

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

    # full range indicates whether or not all comments from first_comment to last_comment (inclusive) could be retrieved
    full_range = i == last_comment

    if not comments_to_show:
        return failure_json("No comments found")

    response = {
                    "success":           True,
                    "comments_to_show":  comments_to_show
                }

    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')