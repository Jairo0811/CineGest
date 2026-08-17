from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NuevaRentaForm
from .models import DetalleRenta, Renta
from .services import crear_renta, registrar_devolucion


@login_required
def lista(request):
    rentas = Renta.objects.select_related("cliente", "empleado").prefetch_related("detalles")[:100]
    return render(request, "rentas/lista.html", {"rentas": rentas})


@login_required
def nueva(request):
    form = NuevaRentaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            renta = crear_renta(
                cliente=form.cleaned_data["cliente"],
                empleado=form.cleaned_data["empleado"],
                items=form.cleaned_data["items"],
                comentarios=form.cleaned_data["comentarios"],
            )
        except ValidationError as exc:
            form.add_error(None, exc)
        else:
            messages.success(request, f"Renta #{renta.pk} registrada correctamente.")
            return redirect("rentas:detalle", pk=renta.pk)
    return render(request, "rentas/nueva.html", {"form": form})


@login_required
def detalle(request, pk):
    renta = get_object_or_404(
        Renta.objects.select_related("cliente", "empleado").prefetch_related(
            "detalles__inventario_item__articulo"
        ),
        pk=pk,
    )
    return render(request, "rentas/detalle.html", {"renta": renta})


@login_required
def devolver(request, detalle_id):
    if request.method != "POST":
        return redirect("rentas:lista")

    detalle = get_object_or_404(DetalleRenta, pk=detalle_id)
    renta_id = detalle.renta_id
    try:
        registrar_devolucion(detalle=detalle)
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))
    else:
        messages.success(request, "Devolución registrada correctamente.")
    return redirect("rentas:detalle", pk=renta_id)
