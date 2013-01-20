import decimal
from django.http import HttpResponse
from django.utils import simplejson
from viewer.models import *

# generates HttpResponse containing JSON that indicates failure
def failure_json(message = None):
    response = {"success": False}
    if message is not None:
        response["message"] = message
    else:
        response["message"] = "error"

    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')

# appends comments associated with each course in courses to a list of dicts in the form {"comment": comment_text, "course_info": {"year": year, "term": term, "profs": profs[]}}
def append_comments_to_list(comments, courses):
    for course in courses:
        # find associated comments
        comments_associated = Qcomments.objects.filter(course_id__exact=course.course_id)

        # skip course if found no comments
        if not comments_associated:
            continue

        # make list of profs who taught this course
        profs = course.get_profs()
        profs_list = []
        for prof in profs:
            profs_list.append(prof.first + " " + prof.last)

        course_info = {
                           "year":  course.year,
                           "term":  course.term,
                           "profs": profs_list
                      }

        for comment in comments_associated:
            entry = {"comment": comment.comment, "course_info": course_info}
            comments.append(entry)

def num_comments(courses):

    comment_count = 0
    for course in courses:
        comments = Qcomments.objects.filter(course_id__exact=course.course_id)
        comment_count = comment_count + comments.count()
    return comment_count

# Thanks to Anurag Uniyal at http://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object#answer-1960553
# Serialize objects with decimals
def json_encode_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)