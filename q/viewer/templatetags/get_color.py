
from django import template
register = template.Library()

@register.filter
def get_color(score, inverse):
    #colors = ["67001f","B2182B","D6604D","F4A582","FDDBC7","D1E5F0","92C5DE","4393C3","2166AC","053061"]
    colors = ["#B2182B","#D6604D","#F4A582","#FDDBC7","#D1E5F0","#92C5DE","#4393C3","#2166AC"]

    bounds = [2,2.42857142857,2.85714285714,3.28571428571,3.71428571429,4.14285714286,4.57142857143 ]
    if inverse: bounds = [5,  4.42857142857,  3.85714285714,  3.28571428571,  2.71428571429,  2.14285714286,  1.57142857143]

    #not a valid score
    if score <1:
        return '#FFFFFF'

    color = 0
    for b in bounds:
        if not inverse:
            if score <= b:
                return colors[color]
        else:
            if score >= b:
                return colors[len(colors) - color - 1]
        color += 1

    #if the score did not fall into any bins leave it white
    return '#FFFFFF'