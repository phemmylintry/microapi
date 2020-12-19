from django import template
from user_dashboard.models import Configs

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_configs(confobj, pie):
    pe = confobj.get(konfigd_api=pie)
    return pe

@register.filter
def get_status(onj, attr):
    return getattr(onj, attr)

@register.filter
def addstr(arg1, arg2):
	"""concatenate arg1 & arg2"""
	return str(arg1) + str(arg2)