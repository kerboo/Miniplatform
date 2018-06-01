from django import template
from app.models import Assets,MonitorDatas
from django.utils.html import format_html
register = template.Library()


@register.filter
def get_last_data(hostid):
    result = MonitorDatas.objects.filter(hostid_id=hostid).latest('id') 
    return result

