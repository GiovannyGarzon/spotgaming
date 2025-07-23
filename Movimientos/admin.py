from django.contrib import admin
from .models import *
# Register your models here.

class MovAsignacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_cliente')

admin.site.register(MovAsignacion, MovAsignacionAdmin)