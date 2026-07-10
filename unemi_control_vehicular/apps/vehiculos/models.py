from django.db import models

class Propietario(models.Model):
    id_propietario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    numero_identidad = models.CharField(max_length=20, verbose_name="Cédula o ID")
    celular = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100)
    tipo = models.CharField(max_length=50, verbose_name="Tipo de Propietario")

    def __str__(self):
        return f"{self.nombre} - {self.numero_identidad}"

    class Meta:
        db_table = 'propietario'
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, db_column='id_propietario')
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    estado = models.CharField(max_length=50, default='Autorizado')

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

    class Meta:
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'