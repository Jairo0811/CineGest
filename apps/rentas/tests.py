from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.articulos.models import Articulo, InventarioItem
from apps.catalogos.models import Idioma, TipoArticulo
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado

from .models import Renta
from .services import crear_renta, registrar_devolucion


class RentaServiceTests(TestCase):
    def setUp(self):
        tipo = TipoArticulo.objects.create(descripcion="Película")
        idioma = Idioma.objects.create(descripcion="Español")
        self.articulo = Articulo.objects.create(
            titulo="Película de prueba",
            tipo_articulo=tipo,
            idioma=idioma,
            monto_renta_dia=Decimal("100.00"),
            dias_renta=2,
            monto_entrega_tardia=Decimal("25.00"),
        )
        self.item = InventarioItem.objects.create(articulo=self.articulo, codigo="TEST-001")
        self.cliente = Cliente.objects.create(nombre="Cliente Prueba", documento="00000000018")
        self.empleado = Empleado.objects.create(
            nombre="Empleado Prueba",
            cedula="00100000009",
            fecha_ingreso=date.today(),
        )

    def test_crear_renta_cambia_inventario_a_rentado(self):
        renta = crear_renta(cliente=self.cliente, empleado=self.empleado, items=[self.item])
        self.item.refresh_from_db()
        self.assertEqual(renta.estado, Renta.Estado.ABIERTA)
        self.assertEqual(renta.detalles.count(), 1)
        self.assertEqual(self.item.estado, InventarioItem.Estado.RENTADO)
        self.assertEqual(renta.total, Decimal("200.00"))

    def test_devolucion_libera_inventario_y_cierra_renta(self):
        renta = crear_renta(cliente=self.cliente, empleado=self.empleado, items=[self.item])
        detalle = renta.detalles.get()
        registrar_devolucion(detalle=detalle, fecha=timezone.now())
        self.item.refresh_from_db()
        renta.refresh_from_db()
        self.assertEqual(self.item.estado, InventarioItem.Estado.DISPONIBLE)
        self.assertEqual(renta.estado, Renta.Estado.DEVUELTA)
