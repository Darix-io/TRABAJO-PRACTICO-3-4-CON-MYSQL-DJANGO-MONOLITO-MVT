from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Administrador, PersonalSeguridad, RolEnum, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'nombre_completo', 'cedula', 'id_rol', 'is_staff', 'is_active')
    search_fields = ('username', 'nombre_completo', 'cedula')
    list_filter = ('id_rol', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('nombre_completo', 'cedula', 'email', 'first_name', 'last_name')}),
        ('Permisos', {'fields': ('id_rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'nombre_completo', 'cedula', 'email', 'id_rol', 'is_staff', 'is_active'),
        }),
    )


@admin.register(RolEnum)
class RolEnumAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('id_administrador', 'id_usuario', 'permiso')
    search_fields = ('id_usuario__nombre_completo', 'permiso')


@admin.register(PersonalSeguridad)
class PersonalSeguridadAdmin(admin.ModelAdmin):
    list_display = ('id_personal_seguridad', 'id_usuario', 'punto_control', 'validacion_ingreso_salida')
    search_fields = ('id_usuario__nombre_completo', 'punto_control')
    list_filter = ('validacion_ingreso_salida',)
