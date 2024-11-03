from django import template
from django.contrib.auth.models import User
import calendar
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

@register.filter
def get_item(lst, index):
    """Retorna el elemento en el índice especificado de una lista."""
    return lst[index] if 0 <= index < len(lst) else None

@register.filter
def get_by_index(lst, index):
    try:
        return lst[index]
    except:
        return None
    
@register.filter
def get_mes(mes):
    """Devuelve el nombre del mes dado su número (1-12)."""
    return calendar.month_name[mes] if 1 <= mes <= 12 else ''

def obtener_nombre_mes(mes):
    """Obtiene el nombre del mes correspondiente al número dado."""
    return calendar.month_name[mes]

@register.filter
def dict_key(dictionary, key):
    """Check if the key is in the dictionary."""
    return key in dictionary

@register.filter
def dict_get(dictionary, key):
    """Get value from dictionary by key."""
    return dictionary.get(key)