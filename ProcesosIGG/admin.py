from django.contrib import admin
from .models import *
from django.db.models import Q
# Register your models here.
class ContratoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'clientes', 'razon', 'clase', 'tipo', 'modelo', 'id_status', 'fecha_contrato', 'fecha_instalacion')

class AsignacionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'clientes', 'contacto','stado', 'fecha_asignacion', 'modelo')
    autocomplete_fields = ['clientes']


class DespachoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'id_cliente', 'id_status', 'fecha_despacho')

class RetiroAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'numero', 'clientes', 'id_status', 'fecha_retiro')

class InstalacionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'update_at')

    def cliente_nombre(self, obj):
        return obj.clientes.nombre  # Asegúrate que 'nombre' es un campo en el modelo Cliente

    cliente_nombre.short_description = 'Cliente'

    list_display = ('id', 'cliente_nombre', 'status', 'maquinas', 'status')

    # Busca por ID exacto, por código de máquina y nombre del cliente
    search_fields = ('=id', 'maquinas__id_codigo', 'clientes__nombre')

    def get_search_results(self, request, queryset, search_term):
        # Lógica original para search_fields
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Añade más coincidencias por cliente y código de máquina
            extra_queryset = self.model.objects.filter(
                Q(clientes__nombre__icontains=search_term) |
                Q(maquinas__id_codigo__icontains=search_term)
            )
            queryset |= extra_queryset

        return queryset, use_distinct

class SerialesAdmin(admin.ModelAdmin):
    #readonly_fields = ('create_at', 'update_at')
    list_display = ('id', 'id_cliente', 'id_asignacion', 'id_maquina')

class MovRetirosAdmin(admin.ModelAdmin):
    list_display = ('id', 'retiro', 'maquina', 'sala', 'ums', 'fecha', 'igg', 'posicion')

admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Asignacione, AsignacionAdmin)
admin.site.register(Despacho, DespachoAdmin)
admin.site.register(Retiro, RetiroAdmin)
admin.site.register(Instalacion, InstalacionAdmin)
admin.site.register(Seriales, SerialesAdmin)
admin.site.register(MovRetiros, MovRetirosAdmin)