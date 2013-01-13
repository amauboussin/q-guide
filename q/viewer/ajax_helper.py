from django.http import HttpResponse
from django.utils import simplejson
from viewer.models import *

# generates HttpResponse containing JSON that indicates failure
def failure_json():
    json = simplejson.dumps({"success": False})
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