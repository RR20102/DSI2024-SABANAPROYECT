from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.filter
def format_dui(value):
    if len(value) == 9:
        return f"{value[:8]}-{value[8]}"
    return value

@register.filter
def format_phone(value):
    if len(value) == 8:
        return f"{value[:4]}-{value[4:]}"
    return value