from django.db import models
from Maestro.models import *
from ProcesosIGG.models import *
from Anexos.models import *
# Create your models here.

class MovAsignacion(models.Model):
    id_entrega_serial = models.IntegerField(null=True, blank=True)
    id_asignacion = models.ForeignKey(Asignacione, on_delete=models.CASCADE, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    id_sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True)
    id_inspired = models.CharField(max_length=15)
    id_posicion = models.IntegerField(null=True)
    #id_maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, null=True)
    id_status = models.ForeignKey(StatusAsignacion, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    serie_pmv = models.ForeignKey(Maquina, on_delete=models.CASCADE, null=True)
    serie_igg = models.CharField(max_length=15, null=True, blank=True)
    observacion = models.CharField(max_length=150, blank=True)
    fecha_instalacion = models.DateField(null=True, blank=True)
    id_retiro = models.IntegerField(null=True, blank=True)
    fecha_retiro = models.DateField(null=True, blank=True)
    fecha_despacho = models.DateField(null=True, blank=True)
    eliminar = models.IntegerField(default=0, blank=True)#este va a ser el campo de condicion para enviar lña condicion a la maquina
    id_seguridad = models.IntegerField(default=0, blank=True)
    fecha_seguridad = models.DateField(null=True, blank=True)
    fecha_codigos = models.DateField()
    direccionn = models.CharField(max_length=50, blank=True, null=True)
    fecha_traslado = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    id_contrato = models.CharField(max_length=20, blank=True, null=True)
    menu_mix = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    #menu_mixn
    internet = models.IntegerField(blank=True, null=True)
    ums = models.IntegerField(blank=True, null=True)
    soporte = models.IntegerField(blank=True, null=True)
    operacion = models.IntegerField(blank=True, null=True)
    vendida = models.IntegerField(blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)
    liquida = models.IntegerField()
    actualiza = models.IntegerField(blank=True, null=True)
    tipo_operacion = models.ForeignKey(TipoOperacion, on_delete=models.CASCADE, null=True)
    #soporte_tiempo
    #actualiza_tiempo
    garantia = models.IntegerField()
    #garantia_tiempo
    #liquida_tiempo
    nuc = models.CharField(max_length=25)
    resolucion = models.CharField(max_length=25)
    #numero_resolucion
    #monto_soporte
    #id_moneda_soporte
    despacho = models.IntegerField(blank=True, null=True)
    tarifa = models.CharField(max_length=25, blank=True, null=True)
    razon = models.ForeignKey(Razos_Social, on_delete=models.CASCADE, null=True, blank = True)
    fechaliquida = models.DateField(null=True, blank=True)
    diasliquida = models.IntegerField(blank=True, null=True)
    numeroresolucion = models.CharField(max_length=15, null=True)
    repcoljuegos = models.CharField(max_length=15, null=True)
    produccionigg = models.CharField(max_length=15, null=True)

    #tipo

