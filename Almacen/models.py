from django.db import models
from Maestro.models import *
from Anexos.models import *
from Fallas_sporte.models import *
from .choices import *

# Create your models here.
class Importaciones(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

class Declaracione(models.Model):
    numero = models.CharField(max_length=20, blank=True)
    proveedor = models.ForeignKey(Proveedore, on_delete=models.CASCADE, null=True, blank=True)
    id_status = models.IntegerField(default=0)
    id_ano = models.IntegerField(default=0)
    fecha = models.DateTimeField()
    fecha_factura = models.DateTimeField()
    fecha_recibido = models.DateTimeField()
    observacion = models.CharField(max_length=100)
    eliminar = models.IntegerField()
    id_seguridad = models.IntegerField(default=0)
    fecha_seguridad = models.DateTimeField()
    factura = models.CharField(max_length=20)
    referencia = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='declaraciones/pdfs/', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def declaracion_nombre(self):
        return  "{}".format(self.id)

    def __str__(self):
        return self.declaracion_nombre()

class Inventario(models.Model):
    numero = models.CharField(max_length=20)
    id_declaracion = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=100)
    tipo = models.ForeignKey(repuestos, on_delete=models.CASCADE, null=True, blank=True)
    id_status = models.ForeignKey(statusinventario, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.ForeignKey(estadoinventario, on_delete=models.CASCADE, null=True, blank=True)
    fecha_despacho = models.DateTimeField(null=True, blank=True)  # Puede ser nulo
    fecha_ingreso = models.DateTimeField(null=True, blank=True)
    serial = models.CharField(max_length=30)#*
    piezas = models.ForeignKey(Pieza, on_delete=models.CASCADE, null=True, blank=True)
    clientes = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")
    responsable = models.CharField(max_length=100, blank=True, null=True)
    declaracion = models.ForeignKey(Declaracione, on_delete=models.CASCADE, null=True, blank=True)

class Retornoremision(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.ForeignKey(repuestos, on_delete=models.CASCADE, null=True, blank=True)
    serial = models.CharField(max_length=30)
    fecha = models.DateField(null=True)
    fecha_recibido = models.DateField(null=True)
    contacto = models.CharField(max_length=50)
    guia = models.CharField(max_length=30, blank=True)
    id_transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE, null=True)
    elaborado = models.CharField(max_length=50, blank=True)
    status = models.ForeignKey(statusremision, on_delete=models.CASCADE, null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)

class eparacionremision(models.Model):
    tipo = models.ForeignKey(repuestos, on_delete=models.CASCADE, null=True, blank=True)
    serial = models.CharField(max_length=30)
    fecha = models.DateField(null=True)
    fecha_entrega_tecnico = models.DateField(null=True)
    fecha_retorno_almacen = models.DateField(null=True)
    elaborado = models.CharField(max_length=50, blank=True)
    tecnico = models.CharField(max_length=60, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    status = models.ForeignKey(statusremision, on_delete=models.CASCADE, null=True)
    observacion = models.TextField(blank=True, null=True)
