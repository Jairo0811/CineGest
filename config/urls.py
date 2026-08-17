from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apps.dashboard.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("gestion/", include("apps.gestion.urls")),
    path("rentas/", include("apps.rentas.urls")),
    path("reportes/", include("apps.reportes.urls")),
]
