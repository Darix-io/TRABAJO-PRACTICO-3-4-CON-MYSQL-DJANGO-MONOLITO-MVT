from django.db import models
from apps.vehiculos.models import Vehiculo
from apps.usuarios.models import PersonalSeguridad, Administrador

class TipoMovimientoEnum(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Movimiento") # ingreso / salida

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipo_movimiento_enum'
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimiento'


class ResultadoValidacionEnum(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Resultado") # autorizado / denegado

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'resultado_validacion_enum'
        verbose_name = 'Resultado de Validación'
        verbose_name_plural = 'Resultados de Validación'


class CodigoQR(models.Model):
    id_codigo_qr = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='id_vehiculo')
    contenido = models.TextField(verbose_name="Contenido Encriptado")
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_expiracion = models.DateField(verbose_name="Fecha de Expiración")
    activo = models.BooleanField(default=True, verbose_name="QR Activo")

    def __str__(self):
        return f"QR Vehículo: {self.id_vehiculo.placa} - Activo: {self.activo}"

    class Meta:
        db_table = 'codigo_qr'
        verbose_name = 'Código QR'
        verbose_name_plural = 'Códigos QR'


class ConfiguracionQR(models.Model):
    id_configuracion_qr = models.AutoField(primary_key=True)
    id_administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='id_administrador')
    tiempo_renovacion = models.IntegerField(verbose_name="Tiempo de Renovación")
    unidad_tiempo = models.CharField(max_length=20, verbose_name="Unidad de Tiempo (Ej. Horas, Días)")
    fecha_modificacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"Renovación cada {self.tiempo_renovacion} {self.unidad_tiempo}"

    class Meta:
        db_table = 'configuracion_qr'
        verbose_name = 'Configuración de QR'
        verbose_name_plural = 'Configuraciones de QR'


class RegistroMovimiento(models.Model):
    id_registro_movimiento = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='id_vehiculo')
    id_personal_seguridad = models.ForeignKey(PersonalSeguridad, on_delete=models.CASCADE, db_column='id_personal_seguridad')
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    id_tipo_movimiento = models.ForeignKey(TipoMovimientoEnum, on_delete=models.PROTECT, db_column='id_tipo_movimiento')
    id_resultado_validacion = models.ForeignKey(ResultadoValidacionEnum, on_delete=models.PROTECT, db_column='id_resultado_validacion')

    def __str__(self):
        return f"{self.id_vehiculo.placa} - {self.id_tipo_movimiento.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        db_table = 'registro_movimiento'
        verbose_name = 'Registro de Movimiento'
        verbose_name_plural = 'Registros de Movimientos'
        