
from django import template
register = template.Library()

@register.filter
def get_color(score, inverse):
    #colors = ["67001f","B2182B","D6604D","F4A582","FDDBC7","D1E5F0","92C5DE","4393C3","2166AC","053061"]

    colors = ["#B2182B","#D6604D","#F4A582","#FDDBC7","#D1E5F0","#92C5DE","#4393C3","#2166AC"]

    if not inverse:
        threshold = 2
        for color in colors:
            if score <= threshold:
                return color
            threshold += .375

    if inverse:
        threshold = 5
        for color in colors:
            if score >= threshold:
                return color
            threshold +=-.5