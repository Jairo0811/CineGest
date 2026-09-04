from django.utils.dateparse import parse_date

from apps.rentas.models import Renta


def rentas_queryset(params):
    """Construye el queryset de rentas a partir de filtros HTTP validados."""
    qs = (
        Renta.objects.select_related("cliente", "empleado")
        .prefetch_related("detalles")
        .all()
    )

    desde_raw = params.get("desde")
    hasta_raw = params.get("hasta")
    estado = params.get("estado")

    desde = parse_date(desde_raw) if desde_raw else None
    hasta = parse_date(hasta_raw) if hasta_raw else None

    if desde:
        qs = qs.filter(fecha_renta__date__gte=desde)
    if hasta:
        qs = qs.filter(fecha_renta__date__lte=hasta)
    if estado in Renta.Estado.values:
        qs = qs.filter(estado=estado)

    return qs.order_by("-fecha_renta")


def filtros_reporte(params):
    """Devuelve una representación segura y legible de los filtros aplicados."""
    estado = params.get("estado")
    estado_label = dict(Renta.Estado.choices).get(estado, "Todos")

    return {
        "desde": params.get("desde") or "Sin límite",
        "hasta": params.get("hasta") or "Sin límite",
        "estado": estado_label,
    }
