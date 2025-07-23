from django.contrib import admin
from .models import *
# Register your models here.
class RazonSocialAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id','id_codigo', 'id_inspired', 'nombre', 'activo')
    search_fields = ('nombre',)

class DepartamentoAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'dane', 'activo')

class CiudadAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'dane', 'activo', 'departamentos')
    search_fields = ('id_codigo', 'nombre')

class FamiliaAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'activo')

class TipoJuegoAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'activo')

class JuegoAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'id_inspired', 'nombre', 'tipo_juego', 'activo')

class MarcaAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'activo')

class MenuAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'activo')

class TecnicoAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'activo')

class CondicionAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'id_codigo', 'nombre', 'activo')

class StatusAdmin (admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ( 'id', 'id_codigo', 'nombre', 'activo')

class CategoriaFallaadmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'nombre', 'activo')

class PiezaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'id_codigo', 'nombre', 'activo')

class GrupoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'id_codigo', 'nombre', 'activo')

class TransporteAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'id_codigo', 'nombre', 'activo')

class StatusAsginarAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class TipoOperacionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class TipoModeloAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class Tipomaquina(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class StatusinstalacionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class StatusretiroAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class modeloliuqidacionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class tiposalaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class statusfallaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class solucionesfallaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class statusserviciotecnicoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class statusremisionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class arquitecturaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo')

class repuestosAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo', 'marca')

class statusinventariosAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo', 'marca')

class estadoinventarioAdmin(admin.ModelAdmin):
    eadonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nombre', 'activo', 'marca')

admin.site.register(Razos_Social, RazonSocialAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(FamiliaMaquina, FamiliaAdmin)
admin.site.register(Juego, JuegoAdmin)
admin.site.register(TipoJuego, TipoJuegoAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Tecnico, TecnicoAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Condicion, CondicionAdmin)
admin.site.register(CategoriaFalla, CondicionAdmin)
admin.site.register(Pieza, PiezaAdmin)
admin.site.register(Grupos, GrupoAdmin)
admin.site.register(Transporte, TransporteAdmin)
admin.site.register(StatusAsignacion, StatusAsginarAdmin)
admin.site.register(TipoOperacion, TipoOperacionAdmin)
admin.site.register(Modelo, TipoModeloAdmin)
admin.site.register(tipomaquina, TipoModeloAdmin)
admin.site.register(statusinstalacion, StatusinstalacionAdmin)
admin.site.register(statusretiro, StatusretiroAdmin)
admin.site.register(modeloliquidacion, modeloliuqidacionAdmin)
admin.site.register(TipoSala, tiposalaAdmin)
admin.site.register(statusfalla, statusfallaAdmin)
admin.site.register(solucionesfalla, solucionesfallaAdmin)
admin.site.register(statusserviciotecnico, statusserviciotecnicoAdmin)
admin.site.register(statusremision, statusremisionAdmin)
admin.site.register(arquitectura, arquitecturaAdmin)
admin.site.register(repuestos, repuestosAdmin)
admin.site.register(statusinventario, statusinventariosAdmin)
admin.site.register(estadoinventario, estadoinventarioAdmin)