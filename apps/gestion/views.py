from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.articulos.models import Articulo, InventarioItem
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado
from apps.gestion.forms import ArticuloForm, ClienteForm, EmpleadoForm, InventarioItemForm


@dataclass(frozen=True)
class ResourceConfig:
    model: type
    form_class: type
    title: str
    singular: str
    icon: str
    headers: tuple[str, ...]


RESOURCES = {
    "articulos": ResourceConfig(
        model=Articulo,
        form_class=ArticuloForm,
        title="Artículos",
        singular="Artículo",
        icon="bi-collection-play-fill",
        headers=("Título", "Tipo", "Idioma", "Renta/día", "Estado"),
    ),
    "inventario": ResourceConfig(
        model=InventarioItem,
        form_class=InventarioItemForm,
        title="Inventario",
        singular="Unidad de inventario",
        icon="bi-box-seam-fill",
        headers=("Código", "Artículo", "Estado", "Observaciones"),
    ),
    "clientes": ResourceConfig(
        model=Cliente,
        form_class=ClienteForm,
        title="Clientes",
        singular="Cliente",
        icon="bi-people-fill",
        headers=("Nombre", "Documento", "Tipo", "Teléfono", "Estado"),
    ),
    "empleados": ResourceConfig(
        model=Empleado,
        form_class=EmpleadoForm,
        title="Empleados",
        singular="Empleado",
        icon="bi-person-badge-fill",
        headers=("Nombre", "Cédula", "Tanda", "Comisión", "Estado"),
    ),
}


def _config(resource):
    try:
        return RESOURCES[resource]
    except KeyError as exc:
        raise Http404("Recurso de gestión no encontrado") from exc


def _rows(resource, queryset):
    rows = []
    for item in queryset:
        if resource == "articulos":
            values = [
                item.titulo,
                str(item.tipo_articulo),
                str(item.idioma),
                f"RD$ {item.monto_renta_dia:,.2f}",
                "Activo" if item.activo else "Inactivo",
            ]
        elif resource == "inventario":
            values = [item.codigo, str(item.articulo), item.get_estado_display(), item.observaciones or "—"]
        elif resource == "clientes":
            values = [
                item.nombre,
                item.documento,
                item.get_tipo_persona_display(),
                item.telefono or "—",
                "Activo" if item.activo else "Inactivo",
            ]
        else:
            values = [
                item.nombre,
                item.cedula,
                item.get_tanda_display(),
                f"{item.porcentaje_comision}%",
                "Activo" if item.activo else "Inactivo",
            ]
        rows.append({"object": item, "values": values})
    return rows


@login_required
def lista(request, resource):
    config = _config(resource)
    queryset = config.model.objects.all()
    if resource == "articulos":
        queryset = queryset.select_related("tipo_articulo", "idioma")
    elif resource == "inventario":
        queryset = queryset.select_related("articulo")

    query = request.GET.get("q", "").strip()
    if query:
        if resource == "articulos":
            queryset = queryset.filter(titulo__icontains=query)
        elif resource == "inventario":
            queryset = queryset.filter(codigo__icontains=query)
        elif resource == "clientes":
            queryset = queryset.filter(nombre__icontains=query)
        else:
            queryset = queryset.filter(nombre__icontains=query)

    return render(
        request,
        "gestion/lista.html",
        {
            "resource": resource,
            "config": config,
            "rows": _rows(resource, queryset),
            "query": query,
        },
    )


@login_required
def crear(request, resource):
    config = _config(resource)
    form = config.form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{config.singular} creado correctamente.")
        return redirect("gestion:lista", resource=resource)
    return render(request, "gestion/form.html", {"resource": resource, "config": config, "form": form, "is_edit": False})


@login_required
def editar(request, resource, pk):
    config = _config(resource)
    instance = get_object_or_404(config.model, pk=pk)
    form = config.form_class(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{config.singular} actualizado correctamente.")
        return redirect("gestion:lista", resource=resource)
    return render(request, "gestion/form.html", {"resource": resource, "config": config, "form": form, "is_edit": True})
