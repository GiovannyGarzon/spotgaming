from datetime import date
import calendar
from collections import defaultdict
from Maestro.models import *
from Auditoria.models import *


def obtener_datos_liquidacion(cliente_id, mes, anio):
    cliente = Cliente.objects.get(id=cliente_id)

    mes = int(mes)
    anio = int(anio)

    # Rango de fechas para la liquidación
    fecha_desde = date(anio, mes, 1)
    if mes == 12:
        fecha_hasta = date(anio + 1, 1, 1) - date.resolution
    else:
        fecha_hasta = date(anio, mes + 1, 1) - date.resolution

    # Inicializamos los totales
    total = {
        'neto': 0,
        'impuesto': 0,
        'iva': 0,
        'descuento': 0,
        'pago_cliente': 0,
        'pago_dueno': 0,
        'entrada': 0,
        'salida': 0,
        'bill': 0,
        'play': 0,
        'monto_a_dividir': 0,
    }

    resumen_salas = []

    detalles = DetalleLiquidacion.objects.filter(
        maquina__clientes=cliente,
        mes=mes,
        anio=anio
    ).select_related('maquina', 'maquina__salas')

    agrupado_por_sala = defaultdict(list)

    for d in detalles:
        sala = d.maquina.salas.nombre if d.maquina.salas else 'Sin sala'
        agrupado_por_sala[sala].append(d)

        total['neto'] += d.neto_total
        total['impuesto'] += d.impuesto_coljuegos
        total['iva'] += d.valor_iva
        total['descuento'] += d.valor_a_descontar
        total['pago_cliente'] += d.pago_cliente
        total['pago_dueno'] += d.pago_dueno
        total['entrada'] += d.entrada_total
        total['salida'] += d.salida_total
        total['bill'] += d.bill_total
        total['play'] += d.play_total
        total['monto_a_dividir'] += d.monto_a_dividir

    for sala, items in agrupado_por_sala.items():
        resumen_salas.append({
            'nombre': sala,
            'detalles': items,
            'totales': {
                'neto': sum(d.neto_total for d in items),
                'descuento': sum(d.valor_a_descontar for d in items),
                'pago_cliente': sum(d.pago_cliente for d in items),
                'pago_dueno': sum(d.pago_dueno for d in items),
                'entrada': sum(d.entrada_total for d in items),
                'salida': sum(d.salida_total for d in items),
                'bill': sum(d.bill_total for d in items),
                'play': sum(d.play_total for d in items),
                'monto_a_dividir': sum(d.monto_a_dividir for d in items),

            }
        })

    nombre_mes = fecha_desde.strftime("%B").capitalize()
    fecha_liquidacion = detalles.first().fecha if detalles.exists() else date.today()

    return cliente, total, resumen_salas, fecha_desde, fecha_hasta, nombre_mes, fecha_liquidacion, detalles