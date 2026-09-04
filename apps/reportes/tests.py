from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.articulos.models import Articulo, InventarioItem
from apps.catalogos.models import Idioma, TipoArticulo
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado
from apps.rentas.models import Renta
from apps.rentas.services import crear_renta


class ReportesViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="reportes",
            password="cinegest-test-password",
        )
        tipo = TipoArticulo.objects.create(descripcion="Película")
        idioma = Idioma.objects.create(descripcion="Español")
        articulo = Articulo.objects.create(
            titulo="Película de prueba",
            tipo_articulo=tipo,
            idioma=idioma,
            monto_renta_dia=Decimal("100.00"),
            dias_renta=2,
            monto_entrega_tardia=Decimal("25.00"),
        )
        item = InventarioItem.objects.create(articulo=articulo, codigo="REPORT-001")
        cliente = Cliente.objects.create(
            nombre="Cliente Reporte",
            documento="00000000018",
        )
        empleado = Empleado.objects.create(
            nombre="Empleado Reporte",
            cedula="00100000009",
            fecha_ingreso=date.today(),
        )
        self.renta = crear_renta(cliente=cliente, empleado=empleado, items=[item])

    def test_reportes_requieren_autenticacion(self):
        response = self.client.get(reverse("reportes:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_index_autenticado_muestra_renta(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reportes:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cliente Reporte")

    def test_filtro_estado_valido(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reportes:index"), {"estado": Renta.Estado.DEVUELTA})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Cliente Reporte")

    def test_filtro_fecha_invalida_no_rompe_reporte(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reportes:index"), {"desde": "fecha-invalida"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cliente Reporte")

    def test_exportar_excel_devuelve_xlsx(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reportes:excel"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertTrue(response.content.startswith(b"PK"))

    def test_exportar_pdf_devuelve_pdf(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reportes:pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))
