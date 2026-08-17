from django.contrib import admin

from .models import Empleado


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cedula", "tanda", "porcentaje_comision", "fecha_ingreso", "activo")
    list_filter = ("tanda", "activo")
    search_fields = ("nombre", "cedula", "usuario__username", "usuario__email")
    autocomplete_fields = ("usuario",)
    ordering = ("nombre",)
