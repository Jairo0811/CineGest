from datetime import datetime
from decimal import Decimal
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.rentas.models import Renta


CINEGEST_NAVY = colors.HexColor("#071B3A")
CINEGEST_BLUE = colors.HexColor("#1565C0")
CINEGEST_LIGHT_BLUE = colors.HexColor("#EAF3FF")
CINEGEST_YELLOW = colors.HexColor("#FFC400")
CINEGEST_LIGHT_YELLOW = colors.HexColor("#FFF7D6")
CINEGEST_TEXT = colors.HexColor("#172033")
CINEGEST_MUTED = colors.HexColor("#667085")
CINEGEST_BORDER = colors.HexColor("#D9E2F0")
CINEGEST_BACKGROUND = colors.HexColor("#F7F9FC")


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

    return qs.order_by("-fecha_renta")


def _filtros_reporte(request):
    return {
        "desde": request.GET.get("desde") or "Sin límite",
        "hasta": request.GET.get("hasta") or "Sin límite",
        "estado": request.GET.get("estado") or "Todos",
    }


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


def _logo_path():
    """Resuelve el logo usando el sistema de archivos estáticos de Django."""
    return finders.find("images/cinegest-logo.png")


def _dibujar_encabezado_pagina(canvas, doc):
    canvas.saveState()
    page_width, page_height = landscape(letter)

    canvas.setFillColor(CINEGEST_NAVY)
    canvas.rect(0, page_height - 54, page_width, 54, fill=1, stroke=0)

    canvas.setFillColor(CINEGEST_YELLOW)
    canvas.rect(0, page_height - 58, page_width, 4, fill=1, stroke=0)

    logo_path = _logo_path()
    if logo_path:
        logo = ImageReader(logo_path)
        image_width, image_height = logo.getSize()
        max_width = 150
        max_height = 42
        scale = min(max_width / image_width, max_height / image_height)
        draw_width = image_width * scale
        draw_height = image_height * scale
        canvas.drawImage(
            logo,
            doc.leftMargin,
            page_height - 49,
            width=draw_width,
            height=draw_height,
            preserveAspectRatio=True,
            mask="auto",
        )
    else:
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(doc.leftMargin, page_height - 32, "CineGest")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        page_width - doc.rightMargin,
        page_height - 32,
        "Sistema de Gestión para Video Club",
    )

    canvas.setStrokeColor(CINEGEST_BORDER)
    canvas.line(doc.leftMargin, 30, page_width - doc.rightMargin, 30)

    canvas.setFillColor(CINEGEST_MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(
        doc.leftMargin,
        18,
        "CineGest · Reporte generado automáticamente",
    )
    canvas.drawRightString(
        page_width - doc.rightMargin,
        18,
        f"Página {doc.page}",
    )

    canvas.restoreState()


@login_required
def exportar_pdf(request):
    stream = BytesIO()
    rentas = list(_rentas_queryset(request))
    filtros = _filtros_reporte(request)

    doc = SimpleDocTemplate(
        stream,
        pagesize=landscape(letter),
        rightMargin=36,
        leftMargin=36,
        topMargin=78,
        bottomMargin=45,
        title="CineGest - Reporte de Rentas",
        author="CineGest",
        subject="Reporte operativo de rentas",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CineGestTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=CINEGEST_NAVY,
        spaceAfter=5,
    )
    subtitle_style = ParagraphStyle(
        "CineGestSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=CINEGEST_MUTED,
        spaceAfter=16,
    )
    section_style = ParagraphStyle(
        "CineGestSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=CINEGEST_NAVY,
        spaceAfter=8,
    )
    center_style = ParagraphStyle(
        "CineGestCenter",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=9,
        textColor=CINEGEST_MUTED,
    )

    story = [
        Paragraph("Reporte de Rentas", title_style),
        Paragraph(
            f"Resumen operativo generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}.",
            subtitle_style,
        ),
    ]

    total_general = sum((renta.total for renta in rentas), Decimal("0.00"))
    resumen_table = Table(
        [
            ["TOTAL DE RENTAS", "MONTO TOTAL", "DESDE", "HASTA"],
            [
                str(len(rentas)),
                f"RD$ {total_general:,.2f}",
                filtros["desde"],
                filtros["hasta"],
            ],
        ],
        colWidths=[1.65 * inch, 1.85 * inch, 1.65 * inch, 1.65 * inch],
    )
    resumen_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CINEGEST_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7),
        ("BACKGROUND", (0, 1), (-1, 1), CINEGEST_LIGHT_BLUE),
        ("TEXTCOLOR", (0, 1), (-1, 1), CINEGEST_TEXT),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, 1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, CINEGEST_BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, CINEGEST_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([resumen_table, Spacer(1, 14)])

    estado_display = filtros["estado"]
    if filtros["estado"] != "Todos":
        estado_display = dict(Renta.Estado.choices).get(filtros["estado"], filtros["estado"])

    filtros_table = Table(
        [[
            Paragraph("<b>Filtros aplicados</b>", styles["Normal"]),
            f"Desde: {filtros['desde']}   |   Hasta: {filtros['hasta']}   |   Estado: {estado_display}",
        ]],
        colWidths=[1.4 * inch, 8.3 * inch],
    )
    filtros_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), CINEGEST_YELLOW),
        ("BACKGROUND", (1, 0), (1, 0), CINEGEST_LIGHT_YELLOW),
        ("TEXTCOLOR", (0, 0), (-1, -1), CINEGEST_TEXT),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, CINEGEST_BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([filtros_table, Spacer(1, 18), Paragraph("Detalle de operaciones", section_style)])

    if rentas:
        table_data = [["#", "Fecha", "Cliente", "Empleado", "Estado", "Total"]]
        for renta in rentas:
            table_data.append([
                str(renta.id),
                renta.fecha_renta.strftime("%d/%m/%Y"),
                renta.cliente.nombre,
                renta.empleado.nombre,
                renta.get_estado_display(),
                f"RD$ {renta.total:,.2f}",
            ])

        detail_table = Table(
            table_data,
            repeatRows=1,
            colWidths=[0.55 * inch, 1.15 * inch, 2.35 * inch, 2.15 * inch, 1.35 * inch, 1.35 * inch],
        )
        detail_style = [
            ("BACKGROUND", (0, 0), (-1, 0), CINEGEST_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("TEXTCOLOR", (0, 1), (-1, -1), CINEGEST_TEXT),
            ("GRID", (0, 0), (-1, -1), 0.35, CINEGEST_BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
        for row_index in range(1, len(table_data)):
            if row_index % 2 == 0:
                detail_style.append(("BACKGROUND", (0, row_index), (-1, row_index), CINEGEST_BACKGROUND))
        detail_table.setStyle(TableStyle(detail_style))
        story.append(detail_table)
    else:
        empty_table = Table(
            [[Paragraph(
                "<b>No se encontraron rentas</b><br/>No existen operaciones que coincidan con los criterios seleccionados.",
                center_style,
            )]],
            colWidths=[9.7 * inch],
            rowHeights=[1.1 * inch],
        )
        empty_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CINEGEST_BACKGROUND),
            ("BOX", (0, 0), (-1, -1), 0.5, CINEGEST_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        story.append(empty_table)

    doc.build(
        story,
        onFirstPage=_dibujar_encabezado_pagina,
        onLaterPages=_dibujar_encabezado_pagina,
    )

    response = HttpResponse(stream.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="cinegest-rentas.pdf"'
    return response
