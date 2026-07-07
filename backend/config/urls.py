from django.contrib import admin
from django.urls import include, path
from security.views import InicioTemplate, LoginPageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", InicioTemplate.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("security/", include("security.urls")),
]