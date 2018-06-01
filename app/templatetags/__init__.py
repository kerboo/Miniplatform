from django import template
from app.models import Assets,MonitorDatas
register = template.Library()


@register.filter
def get_ip_data(hostid):
     pass