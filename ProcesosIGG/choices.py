Status_Contrato=(
    ('E', 'ELABORADO'),
    ('P', 'PARA FIRMA'),
    ('DOCUM RECIBIDO', 'DOCUM RECIBIDO'),
    ('A', 'ANULADO'),
)

Clase=(
    ('C', 'CONTRATO'),
    ('O', 'OTROS SI'),
)

Tipo=(
    ('E', 'EMPRESA'),
    ('P', 'PERSONAL'),
)

Modelo_ProcesoIGG=(
    ('PA', 'PA'), #SOLO PARTICIPACION
    ('OC', 'OC'), #PARTICIPACION CON OPC COMPRA
    ('VP', 'VP'), #VENTA CON PARTICIPACION
    ('VS', 'VS'), #VENTA SIN PARTICIPACION
    ('VF', 'VF'), #VENTA CON CUOTA FIJA
    ('AR', 'AR'), #ARRENDAIENTO MENSUAL
)

Status_Asignacion=(
    ('ABIERTA', 'ABIERTA'),
    ('PRE ASIGNADO', 'PRE ASIGNADO'),
    ('ASIGNADO', 'ASIGNADO'),
    ('ANULADO', 'ANULADO'),
)

Status_Retiro=(
    ('SOLICITUD', 'SOLICITUD'),
    ('POR RETIRAR', 'POR RETIRAR'),
    ('RETIRADO', 'RETIRADO'),
    ('UMS PROCESADO', 'UMS PROCESADO'),
)

Status_Despacho=(
    ('C', 'CODIGOO IGG'),
    ('A', 'ALISTAMIENTO'),
    ('D', 'DESPACHADO'),
)

Status_Instalacion=(
    ('DESPACHADO', 'DESPACHADO'),
    ('POR INSTALAR', 'POR INSTALAR'),
    ('EN OPERACION', 'EN OPERACION'),
    ('UMS PROCESADO', 'UMS PROCESADO'),
)