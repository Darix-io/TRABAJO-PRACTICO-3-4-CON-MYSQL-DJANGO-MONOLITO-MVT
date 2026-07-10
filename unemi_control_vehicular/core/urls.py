from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.control_acceso import views as control_views

urlpatterns = [
    path('', control_views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('control/', include('apps.control_acceso.urls')),
]

# Necesario para poder ver las imágenes de los QR generados
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)