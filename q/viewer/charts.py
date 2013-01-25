import string

def get_prof_history_chart(courses):
    data = ""
    prof_history = {}

    for i, c in enumerate(courses.reverse()):
        for prof in c.get_profs():
            if prof is not None:
                value = { 'x' :c.year, 'y':float(prof.overall), 'size': 10}
                #value = [float(c.year), float(prof.overall)]

                if prof.get_name() in prof_history:
                    prof_history[prof.get_name()].append(value)

                else:
                    prof_history[prof.get_name()] = [value]

    data = ""
    for k,v in prof_history.items():
        data += "{\n"
        data += "key: '" + k +"'"
        data += ",\n"
        data += "values: " + string.replace(str(v),"'", '') + ",\n},"

    return data

def get_ratings_chart(courses):
    series = ['overall', 'workload','difficulty', 'materials','assignments','feedback','section','recommend']
    data = '['
    for s in series:
        data += get_values(courses, s)+','

    data += "];"
    return data

def get_enrollment_chart(courses):
    return '[ %s ];' % get_values(courses, 'enrollment')

def get_values(courses, field):
    active = ['enrollment','overall', 'workload', 'difficulty']
    disabled = '\n disabled: true,\n'
    if field in active:
        disabled = ''
    return """
        {
            area: false, %s
            values: [ %s ].reverse(),
            key: "%s"
    }

    """ % (disabled,','.join([c.get_ratings_point(field) for c in courses]), field.title())




