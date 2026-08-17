from django.contrib import admin

from .models import Genero, Idioma, TipoArticulo


@admin.register(TipoArticulo, Genero, Idioma)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ("descripcion", "activo", "creado_en", "actualizado_en")
    list_filter = ("activo",)
    search_fields = ("descripcion",)
    ordering = ("descripcion",)
