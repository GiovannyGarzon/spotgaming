from django import template
from Anexos.models import *

register = template.Library()

@register.filter(name='get_nombre')
def get_nombre(obj):
    if obj is not None:
        return obj.nombre
    return 'Desconocido'

@register.filter(name='get_day_value')
def get_day_value(maquina, day):
    # Supongamos que tienes un modelo Reporte asociado a Maquina
    # con un campo fecha que puedes consultar.
    reportes = Reporte.objects.filter(maquina=maquina, fecha__day=day)
    return reportes.exists()

# Aquí agregamos el nuevo filtro 'get_item'
@register.filter(name='get_item')
def get_item(dictionary, key):
    """Obtiene un valor de un diccionario basado en la clave proporcionada."""
    return dictionary.get(key)

@register.filter(name='lookup')
def lookup(dictionary, key):
    if dictionary is not None:
        return dictionary.get(key)
    return None  # O puedes retornar un valor por defecto, como 'No disponible'

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def custom_intcomma(value):
    if isinstance(value, (int, float)):
        # Formatear el valor con coma como separador de miles y luego reemplazar la coma por punto
        return '{:,.0f}'.format(value).replace(",", ".")
    return value

@register.filter(name='get_day_status')
def get_day_status(maquina, day):
    return maquina.get_day_status(day)  # Asume que el método `get_day_status` está definido en tu modelo.

@register.filter(name='to_range')
def to_range(value, end):
    try:
        # Esto generará un rango desde 'value' hasta 'end' (no incluye 'end')
        return range(value, end)
    except TypeError:
        return []

@register.filter
def formato_pesos(value):
    try:
        value = float(value)
        return "${:,.0f}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value