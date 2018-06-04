from django import template
from app.models import Assets,MonitorDatas
from django.utils.html import format_html
register = template.Library()


@register.filter
def num_covert_str(value):
    pass
        


