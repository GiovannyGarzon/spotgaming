from django.contrib import admin
from .models import *
# Register your models here.

class AdminDescuentosLiquidacion(admin.ModelAdmin):
    list_display = ('participacion', 'variable', 'diasintransmision', 'valoriva')

admin.site.register(DescuentosLiquidacion, AdminDescuentosLiquidacion)