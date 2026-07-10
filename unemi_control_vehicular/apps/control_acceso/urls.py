from django.urls import path
from . import views

urlpatterns = [
    path('generar-qr/<int:vehiculo_id>/', views.generar_qr_vehiculo, name='generar_qr'),
    path('escaner/', views.escanear_qr, name='escaner_qr'),
]