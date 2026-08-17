from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "documento", "tipo_persona", "limite_credito", "activo")
    list_filter = ("tipo_persona", "activo")
    search_fields = ("nombre", "documento", "email", "telefono")
    ordering = ("nombre",)
