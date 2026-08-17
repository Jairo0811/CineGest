from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.articulos.models import InventarioItem
from apps.clientes.models import Cliente
from apps.core.models import TimeStampedModel
from apps.empleados.models import Empleado


class Renta(TimeStampedModel):
    class Estado(models.TextChoices):
        ABIERTA = "ABIERTA", "Abierta"
        PARCIAL = "PARCIAL", "Parcialmente devuelta"
        DEVUELTA = "DEVUELTA", "Devuelta"
        CANCELADA = "CANCELADA", "Cancelada"

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="rentas")
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name="rentas")
    fecha_renta = models.DateTimeField(auto_now_add=True, db_index=True)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.ABIERTA, db_index=True)
    comentarios = models.TextField(blank=True)

    class Meta:
        ordering = ("-fecha_renta",)
        verbose_name = "Renta"
        verbose_name_plural = "Rentas"

    @property
    def total(self):
        return sum((detalle.subtotal + detalle.recargo for detalle in self.detalles.all()), Decimal("0.00"))

    def __str__(self):
        return f"Renta #{self.pk or 'nueva'} - {self.cliente}"


class DetalleRenta(TimeStampedModel):
    renta = models.ForeignKey(Renta, on_delete=models.CASCADE, related_name="detalles")
    inventario_item = models.ForeignKey(InventarioItem, on_delete=models.PROTECT, related_name="detalles_renta")
    precio_dia = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    dias_renta = models.PositiveSmallIntegerField(default=1)
    fecha_esperada_devolucion = models.DateTimeField(db_index=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True, db_index=True)
    recargo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])

    class Meta:
        ordering = ("renta_id", "id")
        constraints = [
            models.UniqueConstraint(fields=("renta", "inventario_item"), name="uq_renta_inventario_item"),
        ]
        verbose_name = "Detalle de renta"
        verbose_name_plural = "Detalles de renta"

    @property
    def subtotal(self):
        return self.precio_dia * self.dias_renta

    @property
    def devuelto(self):
        return self.fecha_devolucion is not None

    def __str__(self):
        return f"{self.renta} - {self.inventario_item}"
