from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Seriales(models.Model):
    id_inventario = models.IntegerField(default=0, blank=True)
    id_entrega = models.IntegerField(default=0, blank=True)
    id_produccion = models.IntegerField(default=0, blank=True)
    id_maquina = models.IntegerField(default=0, blank=True)
    id_asignacion = models.IntegerField(default=0, blank=True)
    id_despacho = models.IntegerField(default=0, blank=True)
    id_status = models.IntegerField(default=0, blank=True)
    serie_pmv = models.CharField(max_length=20)
    serie_igg = models.CharField(max_length=20)
    fecha = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField(auto_now_add=True)
    fecha_produccion = models.DateField(auto_now_add=True)
    eliminar = models.IntegerField(default=0, blank=True)
    id_seguridad = models.IntegerField(default=0, blank=True)
    fecha_seguridad = models.DateField(auto_now_add=True)
    fecha_despacho = models.DateField(auto_now_add=True)
    fecha_operacion = models.DateField(auto_now_add=True)
    fecha_asignacion = models.DateField(auto_now_add=True)
    id_entrega_serial  = models.IntegerField(default=0, blank=True)
    produccion_igg = models.DateField(auto_now_add=True)
    fecha_codigos = models.DateField(auto_now_add=True)
    id_cliente = models.IntegerField(default=0, blank=True)
    id_sala = models.IntegerField(default=0, blank=True)
    id_retiro = models.IntegerField(default=0, blank=True)
    fecha_retiro = models.DateField(auto_now_add=True)
    factura_pmv = models.CharField(max_length=15)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60, default=0)

    def __str__(self):
        return f'Perfil de {self.user.username}'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.content}'