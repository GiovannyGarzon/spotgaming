from django.db import models

# Create your models here.
from django.db import models
#from Maestro.models import *

# Create your models here.

class Departamento (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    dane = models.CharField(max_length=100)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def departamento_nombre(self):
        return  "{}".format(self.id)

    def __str__(self):
        return self.departamento_nombre()

class Ciudad (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    dane = models.CharField(max_length=100)
    eliminar = models.IntegerField(default=0, null=True)
    departamentos = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def ciudades(self):
        return  "{}".format(self.id)

    def __str__(self):
        return self.ciudades()

class Razos_Social (models.Model):
    id_codigo = models.CharField(max_length=8)
    id_inspired = models.IntegerField()
    nombre = models.CharField(max_length=100)
    corto = models.CharField(max_length=100, blank=True)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True, blank=True)
    id_seguridad = models.IntegerField(default=0, blank=True)
    fecha_seguridad = models.CharField(max_length=50,blank=True)
    sincroniza = models.IntegerField(default=0, blank=True)
    fecha_sincroniza = models.CharField(max_length=50, blank=True)
    departamentos = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    #clientes = models(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    clientes = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100)
    nit = models.CharField(max_length=15, null=True)
    cedula = models.CharField(max_length=15, null=True)
    representante = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    #ciudad_nit = models.CharField(max_length=30, null=True)
    ciudad_nit = models.ForeignKey(Ciudad, related_name='razos_social_nit', on_delete=models.CASCADE, null=True, blank=True)
    ciudad_cedula = models.ForeignKey(Ciudad, related_name='razos_social_cedula', on_delete=models.CASCADE, null=True, blank=True)
    liquida_mes = models.IntegerField(default=0, null=True)
    enviar_email = models.CharField(max_length=200, null=True, blank=True)
    create_at = models.CharField(max_length=50, verbose_name="Creado")
    update_at = models.CharField(max_length=50, verbose_name="Editado")

    def razon_social(self):
        return  "{}".format(self.id)

    def __str__(self):
        return self.nombre  # En lugar de self.razon_social()

class FamiliaMaquina (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def familias(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.familias()

class TipoJuego (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def tipo_juego(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.tipo_juego()

class Juego (models.Model):
    id_codigo = models.CharField(max_length=8)
    id_inspired = models.IntegerField()
    nombre = models.CharField(max_length=100)
    corto = models.CharField(max_length=50)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    estado = models.CharField(max_length=50)
    minimaapuesta = models.CharField(max_length=50)
    nrolineas = models.CharField(max_length=50)
    id_clasejuego = models.IntegerField(default=0, null=True)
    liquida_mes = models.IntegerField(default=0, null=True)
    tipo_juego = models.ForeignKey(TipoJuego, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

class Marca(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def Marcas(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.Marcas()

class Menu(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def menus(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.menus()

class Modelo(models.Model):
    id_codigo = models.CharField(max_length=8)
    id_inspired = models.IntegerField()
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    familia = models.ForeignKey(FamiliaMaquina, on_delete=models.CASCADE, null=True, blank=True)
    id_tipo_maquina = models.CharField(max_length=8)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def modelos(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.modelos()

class Propiedad (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def Propiedades(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.Propiedades()

class Pieza (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

class TipoContacto (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

class Tecnico (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def Tecnico(self):
        return  "{}".format(self.id)

    def __str__(self):
        return self.Tecnico()

class TipoMoneda (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

class TipoSala (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

class Transporte(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def TipoTransporte(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.TipoTransporte()

class TiposRMA (models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

class Status(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def nombre_status(self):
        return  "{}".format(self.id)

    def __str__(self):
        return self.nombre_status()

class Condicion(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def Condiciones(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.Condiciones()

class CategoriaFalla(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def CategoriaFallas(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.CategoriaFallas()

class Grupos(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def Gruponombre(self):
        return  "{}".format(self.id)

    def __str__(self):
        return self.Gruponombre()

class TipoOperacion(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    nombrecorto = models.CharField(max_length=2, blank=True)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def Operacionnombre(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.Operacionnombre()

class StatusAsignacion(models.Model):
    nombre = models.CharField(max_length=100)
    nombrecorto = models.CharField(max_length=2, blank=True)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def StatusAsignar(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.StatusAsignar()

class tipomaquina(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def tipomaquina(self):
        return  "{}".format(self.nombre)

    def __str__(self):
        return self.tipomaquina()

class modeloliquidacion(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def modeloliquidacion(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.modeloliquidacion()

class statusfalla(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def statusfalla(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.statusfalla()

class solucionesfalla(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def solucionesfalla(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.solucionesfalla()

class statusinstalacion(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def statusintalacion(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.statusintalacion()

class statusretiro(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def statusretiro(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.statusretiro()

class statusserviciotecnico(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def statusserviciotecnico(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.statusserviciotecnico()

class statusremision(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def statusremision(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.statusremision()

class arquitectura(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def arquitectura(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.arquitectura()

class repuestos(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=150, blank=True)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def repuestos(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.repuestos()

class statusinventario(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=150, blank=True)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def statusinventario(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.statusinventario()

class estadoinventario(models.Model):
    id_codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=150, blank=True)
    activo = models.IntegerField(default=1, null=True)
    eliminar = models.IntegerField(default=0, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado")

    def estadoinventario(self):
        return "{}".format(self.nombre)

    def __str__(self):
        return self.estadoinventario()

