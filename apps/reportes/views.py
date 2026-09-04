from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from apps.rentas.models import Renta

from .exporters import build_excel, build_pdf
from .services import filtros_reporte, rentas_queryset


@login_required
def index(request):
    return render(
        request,
        "reportes/index.html",
        {
            "rentas": rentas_queryset(request.GET)[:100],
            "estados": Renta.Estado.choices,
        },
    )


@login_required
def exportar_excel(request):
    contenido = build_excel(rentas_queryset(request.GET))
    response = HttpResponse(
        contenido,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="cinegest-rentas.xlsx"'
    return response


@login_required
def exportar_pdf(request):
    contenido = build_pdf(
        rentas_queryset(request.GET),
        filtros_reporte(request.GET),
    )
    response = HttpResponse(contenido, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="cinegest-rentas.pdf"'
    return response
