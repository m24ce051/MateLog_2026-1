# tracking/templatetags/tracking_filters.py
# Template filters personalizados para las vistas matriciales

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Permite acceder a un elemento de un diccionario usando una clave dinámica.
    Uso: {{ dict|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def make_key(tipo, numero):
    """
    Crea una clave para el diccionario en formato 'tipo_numero'.
    Uso: {{ tipo|make_key:numero }}
    """
    return f"{tipo}_{numero}"
