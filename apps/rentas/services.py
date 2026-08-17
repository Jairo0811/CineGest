from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.articulos.models import InventarioItem

from .models import DetalleRenta, Renta


@transaction.atomic
def crear_renta(*, cliente, empleado, items, comentarios=""):
    if not cliente.activo:
        raise ValidationError("El cliente está inactivo.")
    if not empleado.activo:
        raise ValidationError("El empleado está inactivo.")

    items = list(items)
    if not items:
        raise ValidationError("La renta debe contener al menos un artículo.")

    bloqueados = list(
        InventarioItem.objects.select_for_update()
        .select_related("articulo")
        .filter(pk__in=[item.pk for item in items])
    )
    if len(bloqueados) != len(items):
        raise ValidationError("Uno o más artículos de inventario no existen.")

    no_disponibles = [item.codigo for item in bloqueados if item.estado != InventarioItem.Estado.DISPONIBLE]
    if no_disponibles:
        raise ValidationError(f"Unidades no disponibles: {', '.join(no_disponibles)}")

    renta = Renta.objects.create(cliente=cliente, empleado=empleado, comentarios=comentarios)
    ahora = timezone.now()

    for item in bloqueados:
        articulo = item.articulo
        DetalleRenta.objects.create(
            renta=renta,
            inventario_item=item,
            precio_dia=articulo.monto_renta_dia,
            dias_renta=articulo.dias_renta,
            fecha_esperada_devolucion=ahora + timedelta(days=articulo.dias_renta),
        )
        item.estado = InventarioItem.Estado.RENTADO
        item.save(update_fields=("estado", "actualizado_en"))

    return renta


@transaction.atomic
def registrar_devolucion(*, detalle, fecha=None):
    detalle = DetalleRenta.objects.select_for_update().select_related(
        "renta", "inventario_item", "inventario_item__articulo"
    ).get(pk=detalle.pk)

    if detalle.fecha_devolucion:
        raise ValidationError("Este artículo ya fue devuelto.")

    fecha = fecha or timezone.now()
    dias_atraso = max((fecha.date() - detalle.fecha_esperada_devolucion.date()).days, 0)
    tarifa_tardia = detalle.inventario_item.articulo.monto_entrega_tardia
    detalle.fecha_devolucion = fecha
    detalle.recargo = Decimal(dias_atraso) * tarifa_tardia
    detalle.save(update_fields=("fecha_devolucion", "recargo", "actualizado_en"))

    item = detalle.inventario_item
    item.estado = InventarioItem.Estado.DISPONIBLE
    item.save(update_fields=("estado", "actualizado_en"))

    renta = detalle.renta
    pendientes = renta.detalles.filter(fecha_devolucion__isnull=True).exists()
    devueltos = renta.detalles.filter(fecha_devolucion__isnull=False).exists()
    if pendientes and devueltos:
        renta.estado = Renta.Estado.PARCIAL
    elif not pendientes:
        renta.estado = Renta.Estado.DEVUELTA
    renta.save(update_fields=("estado", "actualizado_en"))

    return detalle
