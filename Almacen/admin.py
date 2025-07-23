from django.contrib import admin
from .models import *

# Register your models here.
class InventarioAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'descripcion', 'id_status', 'fecha_despacho', 'tipo', 'clientes')
    list_filter = ('tipo', )
    search_fields = ('serial',)

class RetornoremisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')

class eparacionremisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tecnico', 'status')

class DeclaracioneAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'proveedor', 'fecha', 'factura', 'create_at')
    search_fields = ('numero', 'proveedor__nombre', 'factura')


admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Retornoremision, RetornoremisionAdmin)
admin.site.register(eparacionremision, eparacionremisionAdmin)
admin.site.register(Declaracione, DeclaracioneAdmin)
