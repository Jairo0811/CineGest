from django.urls import path

from apps.gestion import views

app_name = "gestion"

urlpatterns = [
    path("<str:resource>/", views.lista, name="lista"),
    path("<str:resource>/nuevo/", views.crear, name="crear"),
    path("<str:resource>/<int:pk>/editar/", views.editar, name="editar"),
]
