from django.db import models
from django.contrib.auth.models import AbstractUser

class RolEnum(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Rol")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'rol_enum'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class Usuario(AbstractUser):
    cedula = models.CharField(max_length=20, unique=True, verbose_name="Cédula de Identidad")
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    id_rol = models.ForeignKey(RolEnum, on_delete=models.PROTECT, db_column='id_rol', null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.nombre_completo}"

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='perfil_administrador')
    permiso = models.CharField(max_length=100, default='Full', verbose_name="Nivel de Permisos")

    def __str__(self):
        return f"Admin: {self.id_usuario.nombre_completo}"

    class Meta:
        db_table = 'administrador'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'


class PersonalSeguridad(models.Model):
    id_personal_seguridad = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='perfil_seguridad')
    punto_control = models.CharField(max_length=100, verbose_name="Punto de Control / Garita")
    codigo_qr_escaneado = models.CharField(max_length=255, null=True, blank=True, verbose_name="Último QR Escaneado")
    validacion_ingreso_salida = models.BooleanField(default=False, verbose_name="Validación de Acceso Activa")

    def __str__(self):
        return f"Guardia: {self.id_usuario.nombre_completo} - {self.punto_control}"

    class Meta:
        db_table = 'personal_seguridad'
        verbose_name = 'Personal de Seguridad'
        verbose_name_plural = 'Personal de Seguridad'