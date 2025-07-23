from django.db import models

# Create your models here.

class DescuentosLiquidacion(models.Model):
    año = models.CharField(max_length=4, verbose_name="Año", default=2022)
    participacion = models.FloatField(default=0, verbose_name="% Participación")
    variable = models.FloatField(default=0, verbose_name="% variable")
    diasintransmision = models.FloatField(default=0, verbose_name="Cobro * dia no transmitido")
    valoriva = models.FloatField(default=0, verbose_name="$ Valor IVA")

    def descuentos(self):
        return "{}".format(self.id)

    def __str__(self):
        return self.descuentos()

class Festivo(models.Model):
    fecha =  models.DateField(null=True, auto_now=True)
    idano = models.IntegerField(default=0, null=True, blank=True)
    Descripcion = models.CharField(max_length=50, null=True, blank=True)
    activo = models.IntegerField(default=0, null=True, blank=True)
    eliminar = models.IntegerField(default=0, null=True, blank=True)
    idseguridad = models.IntegerField(default=0, null=True, blank=True)
    fechaseguridad = models.DateField(auto_now_add=True, null=True)
    sincroniza = models.IntegerField(default=0, null=True, blank=True)
    fechasincroniza = models.DateField(auto_now_add=True, null=True)

