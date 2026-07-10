import uuid
import qrcode
import os
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import CodigoQR, RegistroMovimiento, TipoMovimientoEnum, ResultadoValidacionEnum
from apps.vehiculos.models import Vehiculo
from apps.usuarios.models import PersonalSeguridad

class GeneradorQRService:
    @staticmethod
    def generar_nuevo_codigo(vehiculo_id, dias_vigencia=30):
        try:
            vehiculo = Vehiculo.objects.get(id_vehiculo=vehiculo_id)
            if vehiculo.estado.lower() != 'autorizado':
                raise ValueError("No se puede generar un QR para un vehículo no autorizado.")

            CodigoQR.objects.filter(id_vehiculo=vehiculo, activo=True).update(activo=False)
            
            token_unico = str(uuid.uuid4())
            contenido_seguro = f"UNEMI-{vehiculo.placa}-{token_unico}"
            
            fecha_actual = timezone.now().date()
            fecha_vencimiento = fecha_actual + timedelta(days=dias_vigencia)
            
            nuevo_qr = CodigoQR.objects.create(
                id_vehiculo=vehiculo,
                contenido=contenido_seguro,
                fecha_expiracion=fecha_vencimiento,
                activo=True
            )

            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(contenido_seguro)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white")
            
            ruta_carpeta = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
            os.makedirs(ruta_carpeta, exist_ok=True)
            
            nombre_archivo = f"qr_{vehiculo.placa}_{token_unico[:8]}.png"
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            img_qr.save(ruta_completa)
            
            return nuevo_qr
        except Vehiculo.DoesNotExist:
            raise ValueError("El vehículo especificado no existe en el sistema.")


class ValidacionAccesoService:
    @staticmethod
    def procesar_escaneo(contenido_qr, guardia_id, tipo_movimiento="Ingreso"):
        """
        Valida el QR escaneado y registra el movimiento vehicular.
        """
        try:
            # 1. Buscar al guardia de seguridad en turno
            guardia = PersonalSeguridad.objects.get(id_personal_seguridad=guardia_id)
            
            # 2. Buscar si el QR existe y está activo
            qr = CodigoQR.objects.get(contenido=contenido_qr, activo=True)
            
            # 3. Validar vigencia de la fecha
            if qr.fecha_expiracion < timezone.now().date():
                qr.activo = False
                qr.save()
                raise ValueError("Acceso Denegado: El código QR ha expirado.")
                
            # 4. Validar estado de autorización del vehículo
            if qr.id_vehiculo.estado.lower() != 'autorizado':
                raise ValueError("Acceso Denegado: El vehículo ya no está autorizado.")
                
            # 5. Configurar los catálogos automáticamente (Ingreso/Salida y Resultado)
            tipo_mov, _ = TipoMovimientoEnum.objects.get_or_create(nombre=tipo_movimiento)
            resultado_ok, _ = ResultadoValidacionEnum.objects.get_or_create(nombre='Autorizado')
            
            # 6. Registrar el movimiento exitoso en la base de datos
            registro = RegistroMovimiento.objects.create(
                id_vehiculo=qr.id_vehiculo,
                id_personal_seguridad=guardia,
                id_tipo_movimiento=tipo_mov,
                id_resultado_validacion=resultado_ok
            )
            
            # 7. Actualizar el registro del guardia
            guardia.codigo_qr_escaneado = contenido_qr
            guardia.save()
            
            return registro
            
        except CodigoQR.DoesNotExist:
            raise ValueError("Acceso Denegado: Código QR inválido o inactivo.")
        except PersonalSeguridad.DoesNotExist:
            raise ValueError("Error del sistema: Guardia de seguridad no identificado.")