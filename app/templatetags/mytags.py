from django import template
from app.models import Assets,MonitorDatas
from django.utils.html import format_html
register = template.Library()


@register.filter
#@register.simple_tag()
def covert_fmt(strs):
    if strs is None:
        strs = ""       
    return strs
        

@register.filter
def get_disk_detailes(disk_str):
    parts = eval(disk_str)
    num =  len(parts.keys())
    if num == 2:
        elemt1 = """%s: %s | %s: %s""" %(parts.keys()[0],parts[parts.keys()[0]],parts.keys()[1],parts[parts.keys()[1]])    
    elif num == 3:
        elemt1 = """%s: %s | %s: %s | %s: %s""" %(parts.keys()[0],parts[parts.keys()[0]],parts.keys()[1],parts[parts.keys()[1]],parts.keys()[2],parts[parts.keys()[2]])
    return elemt1