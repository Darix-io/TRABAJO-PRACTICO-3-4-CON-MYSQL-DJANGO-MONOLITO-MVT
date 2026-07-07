from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from security.views import InicioTemplate, LoginPageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", InicioTemplate.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("security/", include("security.urls")),
    path("catalog/", include("catalog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)