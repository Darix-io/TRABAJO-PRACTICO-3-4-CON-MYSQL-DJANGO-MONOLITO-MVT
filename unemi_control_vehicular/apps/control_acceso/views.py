from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .services import GeneradorQRService, ValidacionAccesoService
from apps.vehiculos.models import Vehiculo
from .models import CodigoQR


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
    
    nombre_imagen = None
    if qr_activo:
        # Aquí está la magia: borramos el prefijo exacto en lugar de cortar por guiones
        prefijo = f"UNEMI-{vehiculo.placa}-"
        token_completo = qr_activo.contenido.replace(prefijo, "")
        token_corto = token_completo[:8]
        
        nombre_imagen = f"qr_{vehiculo.placa}_{token_corto}.png"
            
    context = {
        'vehiculo': vehiculo,
        'qr_activo': qr_activo,
        'nombre_imagen': nombre_imagen
    }
    return render(request, 'control_acceso/generar_qr.html', context)


def home_view(request):
    return redirect('escaner_qr')


def escanear_qr(request):
    guardia_id = 1 
    
    if request.method == 'POST':
        contenido_qr = request.POST.get('contenido_qr')
        tipo_movimiento = request.POST.get('tipo_movimiento', 'Ingreso')
        
        try:
            registro = ValidacionAccesoService.procesar_escaneo(contenido_qr, guardia_id, tipo_movimiento)
            messages.success(request, f"✅ ACCESO AUTORIZADO: {registro.id_vehiculo.placa} ({tipo_movimiento})")
        except ValueError as e:
            messages.error(request, str(e))
            
        return redirect('escaner_qr')
        
    return render(request, 'control_acceso/escaner.html')