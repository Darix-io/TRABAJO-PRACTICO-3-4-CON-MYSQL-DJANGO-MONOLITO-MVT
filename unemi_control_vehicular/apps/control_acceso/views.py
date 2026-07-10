from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .services import GeneradorQRService
from apps.vehiculos.models import Vehiculo
from .models import CodigoQR


def home_view(request):
    return render(request, 'control_acceso/home.html', {'title': 'Control Vehicular UNEMI'})


def generar_qr_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=vehiculo_id)
    
    if request.method == 'POST':
        try:
            nuevo_qr = GeneradorQRService.generar_nuevo_codigo(vehiculo.id_vehiculo)
            messages.success(request, f'¡Código QR generado exitosamente para la placa {vehiculo.placa}!')
            return redirect('generar_qr', vehiculo_id=vehiculo.id_vehiculo)
        except ValueError as e:
            messages.error(request, str(e))
            
    qr_activo = CodigoQR.objects.filter(id_vehiculo=vehiculo, activo=True).first()
    
    # Extraer el nombre de la imagen de forma dinámica y segura
    nombre_imagen = None
    if qr_activo:
        GeneradorQRService.asegurar_archivo_qr(qr_activo, vehiculo)
        token = GeneradorQRService.extraer_token_del_contenido(qr_activo.contenido, vehiculo.placa)[:8]
        nombre_imagen = GeneradorQRService.construir_nombre_archivo(vehiculo.placa, token)

    context = {
        'vehiculo': vehiculo,
        'qr_activo': qr_activo,
        'nombre_imagen': nombre_imagen
    }
    return render(request, 'control_acceso/generar_qr.html', context)