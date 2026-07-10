import os
import re
import uuid
from datetime import timedelta

import qrcode
from django.conf import settings
from django.utils import timezone

from apps.vehiculos.models import Vehiculo
from .models import CodigoQR


class GeneradorQRService:
    @staticmethod
    def construir_nombre_archivo(placa, token):
        placa_sanitizada = re.sub(r'[^A-Za-z0-9]+', '_', str(placa)).strip('_')
        token_sanitizado = re.sub(r'[^A-Za-z0-9]+', '_', str(token)).strip('_')
        return f"qr_{placa_sanitizada}_{token_sanitizado}.png"

    @staticmethod
    def extraer_token_del_contenido(contenido, placa):
        prefijo = f"UNEMI-{placa}-"
        if contenido.startswith(prefijo):
            return contenido[len(prefijo):]
        return contenido

    @staticmethod
    def generar_archivo_qr(contenido, placa, nombre_archivo=None):
        ruta_carpeta = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        os.makedirs(ruta_carpeta, exist_ok=True)

        if nombre_archivo is None:
            token = GeneradorQRService.extraer_token_del_contenido(contenido, placa)[:8]
            nombre_archivo = GeneradorQRService.construir_nombre_archivo(placa, token)

        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(contenido)
        qr.make(fit=True)

        img_qr = qr.make_image(fill_color="black", back_color="white")
        img_qr.save(ruta_completa)
        return ruta_completa

    @staticmethod
    def asegurar_archivo_qr(qr_objeto, vehiculo):
        token = GeneradorQRService.extraer_token_del_contenido(qr_objeto.contenido, vehiculo.placa)[:8]
        nombre_archivo = GeneradorQRService.construir_nombre_archivo(vehiculo.placa, token)
        ruta_completa = os.path.join(settings.MEDIA_ROOT, 'qrcodes', nombre_archivo)

        if not os.path.exists(ruta_completa):
            return GeneradorQRService.generar_archivo_qr(qr_objeto.contenido, vehiculo.placa, nombre_archivo)

        return ruta_completa

    @staticmethod
    def generar_nuevo_codigo(vehiculo_id, dias_vigencia=30):
        """
        Genera un nuevo Código QR para un vehículo autorizado,
        invalidando los anteriores y creando el archivo .png físicamente.
        """
        try:
            vehiculo = Vehiculo.objects.get(id_vehiculo=vehiculo_id)
            
            # 1. Verificar si el vehículo está autorizado
            if vehiculo.estado.lower() != 'autorizado':
                raise ValueError("No se puede generar un QR para un vehículo no autorizado.")

            # 2. Invalidar QRs anteriores
            CodigoQR.objects.filter(id_vehiculo=vehiculo, activo=True).update(activo=False)
            
            # 3. Generar token criptográfico
            token_unico = str(uuid.uuid4())
            contenido_seguro = f"UNEMI-{vehiculo.placa}-{token_unico}"
            
            # 4. Calcular fechas
            fecha_actual = timezone.now().date()
            fecha_vencimiento = fecha_actual + timedelta(days=dias_vigencia)
            
            # 5. Registrar en MySQL
            nuevo_qr = CodigoQR.objects.create(
                id_vehiculo=vehiculo,
                contenido=contenido_seguro,
                fecha_expiracion=fecha_vencimiento,
                activo=True
            )

            # 6. Crear la imagen gráfica del QR y guardarla en media/qrcodes
            GeneradorQRService.generar_archivo_qr(
                contenido_seguro,
                vehiculo.placa,
                GeneradorQRService.construir_nombre_archivo(vehiculo.placa, token_unico[:8]),
            )
            
            return nuevo_qr
            
        except Vehiculo.DoesNotExist:
            raise ValueError("El vehículo especificado no existe en el sistema.")