from django.contrib import admin

from .models import DetalleRenta, Renta


class DetalleRentaInline(admin.TabularInline):
    model = DetalleRenta
    extra = 0
    readonly_fields = ("precio_dia", "dias_renta", "fecha_esperada_devolucion", "fecha_devolucion", "recargo")


@admin.register(Renta)
class RentaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "empleado", "fecha_renta", "estado", "total")
    list_filter = ("estado", "fecha_renta")
    search_fields = ("cliente__nombre", "cliente__documento", "empleado__nombre")
    readonly_fields = ("fecha_renta",)
    inlines = (DetalleRentaInline,)


@admin.register(DetalleRenta)
class DetalleRentaAdmin(admin.ModelAdmin):
    list_display = ("id", "renta", "inventario_item", "fecha_esperada_devolucion", "fecha_devolucion", "recargo")
    list_filter = ("fecha_devolucion",)
    search_fields = ("inventario_item__codigo", "inventario_item__articulo__titulo", "renta__cliente__nombre")
