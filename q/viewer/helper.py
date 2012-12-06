__author__ = 'Andrew'
import string

def convert_term(term):
    if string.lower(term) == 'fall':
        return 1
    elif string.lower(term) == 'spring':
        return 2
    else:
        return 0 #term is not valid. filtering for term by 0 will return an empty queryset



def get_color(score):
    colors = ["67001f","B2182B","D6604D","F4A582","FDDBC7","D1E5F0","92C5DE","4393C3","2166AC","053061"]
    threshold = 2
    for color in colors:
        if score <= threshold:
            print threshold
            return color
        threshold += .33
