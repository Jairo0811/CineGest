from django.urls import path

from . import views

app_name = "rentas"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("nueva/", views.nueva, name="nueva"),
    path("<int:pk>/", views.detalle, name="detalle"),
    path("detalle/<int:detalle_id>/devolver/", views.devolver, name="devolver"),
]
