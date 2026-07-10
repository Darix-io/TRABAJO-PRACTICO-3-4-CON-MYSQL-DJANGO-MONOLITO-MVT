from django.contrib import admin
from .models import TipoMovimientoEnum, ResultadoValidacionEnum, CodigoQR, ConfiguracionQR, RegistroMovimiento

@admin.register(TipoMovimientoEnum)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(ResultadoValidacionEnum)
class ResultadoValidacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(CodigoQR)
class CodigoQRAdmin(admin.ModelAdmin):
    list_display = ('id_vehiculo', 'fecha_creacion', 'fecha_expiracion', 'activo')
    list_filter = ('activo',)
    search_fields = ('id_vehiculo__placa',)

@admin.register(ConfiguracionQR)
class ConfiguracionQRAdmin(admin.ModelAdmin):
    list_display = ('id_administrador', 'tiempo_renovacion', 'unidad_tiempo')

@admin.register(RegistroMovimiento)
class RegistroMovimientoAdmin(admin.ModelAdmin):
    list_display = ('id_vehiculo', 'fecha_hora', 'id_tipo_movimiento', 'id_resultado_validacion')
    list_filter = ('id_tipo_movimiento', 'id_resultado_validacion')
    search_fields = ('id_vehiculo__placa',)