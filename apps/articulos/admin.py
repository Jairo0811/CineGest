from django.contrib import admin

from .models import Articulo, ArticuloElenco, InventarioItem, PersonaElenco


class ArticuloElencoInline(admin.TabularInline):
    model = ArticuloElenco
    extra = 0


class InventarioItemInline(admin.TabularInline):
    model = InventarioItem
    extra = 0


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_articulo", "idioma", "monto_renta_dia", "dias_renta", "activo")
    list_filter = ("tipo_articulo", "idioma", "activo", "generos")
    search_fields = ("titulo", "descripcion")
    filter_horizontal = ("generos",)
    inlines = (ArticuloElencoInline, InventarioItemInline)
    ordering = ("titulo",)


@admin.register(PersonaElenco)
class PersonaElencoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nombre_artistico", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "nombre_artistico")
    ordering = ("nombre",)


@admin.register(InventarioItem)
class InventarioItemAdmin(admin.ModelAdmin):
    list_display = ("codigo", "articulo", "estado", "creado_en")
    list_filter = ("estado",)
    search_fields = ("codigo", "articulo__titulo")
    autocomplete_fields = ("articulo",)


@admin.register(ArticuloElenco)
class ArticuloElencoAdmin(admin.ModelAdmin):
    list_display = ("articulo", "persona", "rol")
    list_filter = ("rol",)
    search_fields = ("articulo__titulo", "persona__nombre", "persona__nombre_artistico")
    autocomplete_fields = ("articulo", "persona")
