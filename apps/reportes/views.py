from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from apps.rentas.models import Renta


def _rentas_queryset(request):
    qs = Renta.objects.select_related("cliente", "empleado").prefetch_related("detalles")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")
    estado = request.GET.get("estado")
    if desde:
        qs = qs.filter(fecha_renta__date__gte=desde)
    if hasta:
        qs = qs.filter(fecha_renta__date__lte=hasta)
    if estado:
        qs = qs.filter(estado=estado)
    return qs


@login_required
def index(request):
    return render(
        request,
        "reportes/index.html",
        {"rentas": _rentas_queryset(request)[:100], "estados": Renta.Estado.choices},
    )


@login_required
def exportar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rentas"
    ws.append(["ID", "Fecha", "Cliente", "Empleado", "Estado", "Total"])
    for renta in _rentas_queryset(request):
        ws.append([
            renta.id,
            renta.fecha_renta.strftime("%Y-%m-%d %H:%M"),
            renta.cliente.nombre,
            renta.empleado.nombre,
            renta.get_estado_display(),
            float(renta.total),
        ])

    stream = BytesIO()
    wb.save(stream)
    response = HttpResponse(
        stream.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="cinegest-rentas.xlsx"'
    return response


@login_required
def exportar_pdf(request):
    stream = BytesIO()
    pdf = canvas.Canvas(stream, pagesize=letter)
    width, height = letter
    y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "CineGest - Reporte de Rentas")
    y -= 30
    pdf.setFont("Helvetica", 9)

    for renta in _rentas_queryset(request):
        linea = f"#{renta.id} | {renta.fecha_renta:%Y-%m-%d} | {renta.cliente.nombre} | {renta.get_estado_display()} | RD$ {renta.total:.2f}"
        pdf.drawString(50, y, linea[:110])
        y -= 16
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 9)
            y = height - 50

    pdf.save()
    response = HttpResponse(stream.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="cinegest-rentas.pdf"'
    return response
