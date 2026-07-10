from django.contrib import admin
from .models import Propietario, Vehiculo

@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('id_propietario', 'nombre', 'numero_identidad', 'celular', 'tipo')
    search_fields = ('nombre', 'numero_identidad')
    list_filter = ('tipo',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'id_propietario', 'estado')
    search_fields = ('placa', 'id_propietario__nombre')
    list_filter = ('estado', 'marca')