__author__ = 'Andrew'
from models import *
import string, re
import constants

def unified_search(q):
    return search_for_courses(q) | search_for_profs(q)

def search_for_courses(q):

    # if the query is a catalog number
    if q.isdigit():
        return Qcourses.objects.filter(cat_num = q).order_by('-year')

    #hardcode in commonly used abbreviations for departments
#    departments = {'cs':'compsci', 'am':'apmth', 'ec':'econ', 'ls': 'lifesci',
#                   'neuro':'neurobio','spanish':'spansh', 'sls':'sci-livsys' }


    #check to see if the query is a course number i.e. compsci50 or cs50
    field = ''
    num = ''

    #matches COMPSCI
    matched_department_code = []
    #matches "Computer Science" or "cs"
    matched_whole_alias = []
    #contains computer or science
    matched_partial_alias = []
    skip_step_3 = False

    for key, value in constants.DEPARTMENTS.items():
        
        # Step 1: exact match for department code?
        regex = re.compile("^\s*" + value + "\s*(?P<num>[a-zA-Z0-9&-_]+)?", re.IGNORECASE)
        result = regex.search(q)
        if result is not None:
            # If exact match, add values 
            matched_department_code.append((value, result.group("num")))
            # forget about partial aliases if we're pretty certain we have a real course on our hands (i.e. if num contains a number)
            if result.group("num"):
                if re.search(re.compile("[0-9]"), result.group("num")):
                    matched_partial_alias = []
                    skip_step_3 = True

        # Step 2: matched whole alias?
        regex = re.compile("^\s*" + key + "\s*(?P<num>[a-zA-Z&-_]+)", re.IGNORECASE)
        result = regex.search(q)
        if result is not None:
            # If exact match, add values 
            matched_whole_alias.append((value, result.group("num")))
            # forget about partial aliases if we're pretty certain we have a real course on our hands (i.e. if num contains a number)
            if result.group("num"):
                if re.search(re.compile("[0-9]"), result.group("num")):
                    matched_partial_alias = []
                    skip_step_3 = True

        # Step 3: matched partial alias?
        if not skip_step_3:
            partial_aliases = key.split()
            for word in partial_aliases:
                regex = re.compile("^\s*" + word + "\s*(?P<num>[a-zA-Z&-_]+)", re.IGNORECASE)
                result = regex.search(q)
                if result is not None:
                    matched_partial_alias.append((value, result.group("num")))
            
    # is it compsci50?
    if matched_department_code and matched_department_code[0][1]:
        query = Qcourses.objects.filter(field__iexact = matched_department_code[0][0]).filter(number__istartswith = matched_department_code[0][1])
        if query.count() >= 1:
            return query

    # is it cs 50?
    if matched_whole_alias and matched_whole_alias[0][1]:
        query = Qcourses.objects.filter(field__iexact = matched_whole_alias[0][0]).filter(number__istartswith = matched_whole_alias[0][1])
        if query.count() >= 1:
            return query

    print matched_department_code
    print matched_whole_alias
    print matched_partial_alias

    result_set = Qcourses.objects.none()
    results = []

    # title_results = Qcourses.objects.filter(title__icontains = q).order_by('-enrollment')


    #does the title contain the query?
    #result_set = Qcourses.objects.filter(title__icontains = q).order_by('-enrollment')

    result_set = list(Qcourses.objects.filter(title__icontains = q).order_by('-enrollment'))
    for match in matched_department_code + matched_whole_alias + matched_partial_alias:
        next_filter = Qcourses.objects.filter(field__iexact = match[0])
        if match[1] is not None:
            next_filter.filter(number__istartswith = match[1])
        #result_set = result_set | next_filter
        result_set +=  list(next_filter)

    # for course in title_results:
    #     results.append(course)

    # for course in result_set:
    #     results.append(course)

    print result_set
    return result_set

    # return results
    # print result_set



    # for char in q:
    #     if char.isdigit():
    #         field, num = q.split(char, 1)
    #         num = char+num #re-add the splitting digit
    #         break

    # #strip whitespace
    # field = string.strip(field)
    # num = string.strip(num)

    # print field, num
    # #check if the query contains an abbreviation
    # if field in departments:
    #     field = departments[field]

    # # | chains queries together. i denotes a case insensitive lookup.
    # # first see if any results come from querying the course number
    # #next add keyword queries. first require q to be its own word then relax that constraint
    # return Qcourses.objects.filter(field__iexact = field).filter(number__istartswith = num) | \
    #        Qcourses.objects.filter(title__icontains = ' '+q+ ' ').order_by('-enrollment') |\
    #        Qcourses.objects.filter(title__istartswith = q).order_by('-enrollment') |\
    #        Qcourses.objects.filter(title__icontains = q).order_by('-enrollment')


#get a prof given his last name
def search_for_profs(q):
    return Qinstructors.objects.filter(last__iexact = q)| \
           Qinstructors.objects.filter(last__istartswith = q)

#return a numerical representation of the term
def convert_term(term):
    if string.lower(term) == 'fall':
        return 1
    elif string.lower(term) == 'spring':
        return 2
    else:
        return 0 #term is not valid. filtering for term by 0 will return an empty queryset


def filter_courses(courses, parameters):
    print courses
    if ('category' in parameters) and parameters['category'].strip():
        filter = parameters['category']
    else:
        filter = 'overall'
    #set order of values
    if ('reverse' in parameters) and parameters['reverse'].strip() and string.lower(parameters['reverse']) == 'true':
        courses=courses.order_by(filter)
    else:
        courses = courses.order_by('-'+filter)

    #filter by various traits
    if ('year' in parameters) and parameters['year'].strip() and string.lower(parameters['year']) != 'all':
        courses=courses.filter(year__exact = int(parameters['year']))

    if ('term' in parameters) and parameters['term'].strip() and string.lower(parameters['term']) != 'both':
        courses=courses.filter(term__exact = convert_term(parameters['term']) )

    if ('enrollment' in parameters) and parameters['enrollment'].strip():
        courses=courses.filter(enrollment__gte = (parameters['enrollment']) ) #greater than or equal to min enrollment

    return courses


#group instances of the same class together
def group_courses(courses):
    print 'hi im here in group courses'
    print courses

    #order = map(lambda c:c.cat_num, courses)

    unique = {}
    for course in courses:
        if course.cat_num in unique:
            unique[course.cat_num].append(course)
        else:
            unique[course.cat_num] = [course]

    #make each unique course into a new course object
    course_list = []

    #make the most recent instance of class (greatest year) the base instance
    for years in unique.values():
        base = years[0]
        #assign the most recent year to the base
        for c in years:
            if c.year > base.year:
                base = c
            #gets the average rating for the course
        base.average_overall = average([c.overall for c in years ])
        course_list.append(base)

#    ordered_list = []
#    for old_course in order:
#        for new_course in course_list:
#            if old_course == new_course.cat_num:
#                ordered_list.append(new_course)
#
#    print ordered_list

    return course_list


#average a list of values
def average(list):

    if list is None:
        return 'NA'
    list[:] = filter(None, list)
    if len(list) > 0:
        return '%.2f' % (float(sum(list))/len(list))
    else:
        return 'NA'
