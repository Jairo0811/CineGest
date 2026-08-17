from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render

from apps.articulos.models import Articulo, InventarioItem
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado
from apps.rentas.models import DetalleRenta, Renta


@login_required
def index(request):
    context = {
        "clientes_activos": Cliente.objects.filter(activo=True).count(),
        "empleados_activos": Empleado.objects.filter(activo=True).count(),
        "articulos_activos": Articulo.objects.filter(activo=True).count(),
        "unidades_disponibles": InventarioItem.objects.filter(estado=InventarioItem.Estado.DISPONIBLE).count(),
        "rentas_abiertas": Renta.objects.filter(estado__in=[Renta.Estado.ABIERTA, Renta.Estado.PARCIAL]).count(),
        "recargos_acumulados": DetalleRenta.objects.aggregate(total=Sum("recargo"))["total"] or 0,
        "ultimas_rentas": Renta.objects.select_related("cliente", "empleado").prefetch_related("detalles")[:8],
        "articulos_mas_rentados": (
            DetalleRenta.objects.values("inventario_item__articulo__titulo")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        ),
    }
    return render(request, "dashboard/index.html", context)
