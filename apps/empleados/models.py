from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import SoftDeleteModel, TimeStampedModel


class Empleado(TimeStampedModel, SoftDeleteModel):
    class Tanda(models.TextChoices):
        MATUTINA = "MATUTINA", "Matutina"
        VESPERTINA = "VESPERTINA", "Vespertina"
        NOCTURNA = "NOCTURNA", "Nocturna"
        MIXTA = "MIXTA", "Mixta"

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="empleado",
        null=True,
        blank=True,
    )
    nombre = models.CharField(max_length=160)
    cedula = models.CharField(max_length=20, unique=True)
    tanda = models.CharField(max_length=12, choices=Tanda.choices, default=Tanda.MATUTINA)
    porcentaje_comision = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("100.00"))],
    )
    fecha_ingreso = models.DateField()

    class Meta:
        ordering = ("nombre",)
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self) -> str:
        return f"{self.nombre} ({self.cedula})"
