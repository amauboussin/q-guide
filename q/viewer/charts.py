import string


def get_prof_detail_chart(classes):

    labels = {}
    label_index = 0
    course_data = {}
    for c in classes:
        course_data[c[0].course.title] = []
        for prof_row in sorted(c, key = lambda c: c.course.order_by()):
            label = get_label(prof_row.course)
            print label
            if not label in labels:
                label_index += 1
                labels[label] = label_index
            value = { 'x' : labels[label], 'y': float(prof_row.overall) }
            course_data[prof_row.course.title].append(value)

    labels_output = [t[0] for t in sorted(labels.items(), key=lambda x: x[1]) ]


    data = ""
    for k,v in course_data.items():
        data += "{\n"
        data += "key: '" + k +"'"
        data += ",\n"
        data += "values: " + string.replace(str(v),"'", '') + ",\n},"

    return data, [str(l) for l in labels_output]

def get_prof_history_chart(courses, selected):

    labels = []
    label_index = 0

    data = ""
    prof_history = {}
    for i, c in enumerate(courses.reverse()):

        for prof in c.get_profs():
            if prof is not None:
                #create value
                value = { 'x' :label_index, 'y':float(prof.overall) }
                #add value to appropriate prof
                if prof.get_name() in prof_history:
                    prof_history[prof.get_name()].append(value)

                else:
                    prof_history[prof.get_name()] = [value]

        #create label
        label_index += 1
        labels.append(get_label(c))

    # too many profs1!!!!
    if len(prof_history.items()) > 8:
        include = []
        for prof, values in prof_history.items():

            #take only the profs that taught in the selected year
            for value in values:
                if labels[value['x']] == get_label(selected):
                    include.append(prof)

        #prof_history = {k:v for k, v in prof_history.items() if k in include}

        filtered_prof_history = {}
        for k,v in prof_history.items():
            if k in include:
                filtered_prof_history[k] = v

        prof_history = filtered_prof_history

    data = ""
    for k,v in prof_history.items():
        data += "{\n"
        data += "key: '" + k +"'"
        data += ",\n"
        data += "values: " + string.replace(str(v),"'", '') + ",\n},"

    print labels
    return data, labels


def get_label(course):
    return "%s %s" % (course.term_text(), course.year)

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




