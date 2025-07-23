from django.contrib import admin
from .models import *
# Register your models here.

class ReporteFallasAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'salas', 'maquina', 'id_error', 'apagada', 'fecha', 'fecha_solucion', 'id_status')

class ServicioTecnicoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'clientes', 'descripcion', 'id_status', 'fecha', 'fecha_visita', 'fecha_final', 'create_at', 'update_at')

class RemisionesAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'clientes', 'contacto', 'id_status', 'fecha', 'fecha_envio', 'fecha_recibido', 'observacion', 'create_at', 'update_at')

class ReparacionesAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'clientes', 'descripcion',  'id_status', 'fecha_recibido', 'fecha_final', 'create_at', 'update_at')

class NovedadFallaAdmin(admin.ModelAdmin):
    list_display = ('idfalla', 'fechanovedad')

class DetalleRemisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'remision', 'sala')



admin.site.register(Falla, ReporteFallasAdmin)
admin.site.register(ServicioTecnico, ServicioTecnicoAdmin)
admin.site.register(Remisiones, RemisionesAdmin)
admin.site.register(Reparaciones, ReparacionesAdmin)
admin.site.register(NovedadFalla, NovedadFallaAdmin)
admin.site.register(DetalleRemision, DetalleRemisionAdmin)

