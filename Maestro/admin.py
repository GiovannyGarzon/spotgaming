from django.contrib import admin
from .models import *
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'nit', 'id_inspired', 'nombre', 'razon', 'Grupos', 'activo', 'emeailrecmaquina', 'visor', 'tipo_liquida', 'dia_liquida')
    list_per_page = 35#
    search_fields = ('nombre',)
    ordering = ['nombre']

class SalaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id_codigo', 'id_inspired', 'nombre', 'ciudad', 'clientes', 'razon', 'activo', 'liquida', 'dia_liquida')
    search_fields = ('nombre',)
    list_per_page = 35  #

class MaquinaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'id_codigo', 'serie_PMV', 'familia', 'clientes', 'id_status', 'id_condicion', 'pripiedad', 'reservacion', 'tipo_operacion')
    search_fields = ('id_codigo',)
    list_per_page = 35  #

class ProovedorAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('nit', 'razon_social', 'contacto', 'id_clase')


class CausaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'descripcion_sp', 'activo')

class SolucionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'descripcion_sp', 'activo')

class ProcedimientofallaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'titulo', 'categorias', 'activo')

class CodigoFallaAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'codigo', 'descripcion_sp', 'categoria', 'activo')



admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Maquina, MaquinaAdmin)
admin.site.register(Proveedore, ProovedorAdmin)
admin.site.register(CausasFalla, CausaAdmin)
admin.site.register(SolucionFalla, SolucionAdmin)
admin.site.register(ProcedimientosSFP, ProcedimientofallaAdmin)
admin.site.register(CodigoFalla, CodigoFallaAdmin)