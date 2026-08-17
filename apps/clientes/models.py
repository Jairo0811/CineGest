from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import SoftDeleteModel, TimeStampedModel
from apps.core.validators import normalize_dominican_document, validate_dominican_cedula


class Cliente(TimeStampedModel, SoftDeleteModel):
    class TipoPersona(models.TextChoices):
        FISICA = "FISICA", "Persona física"
        JURIDICA = "JURIDICA", "Persona jurídica"

    nombre = models.CharField(max_length=160)
    documento = models.CharField("Cédula/RNC", max_length=20, unique=True)
    tipo_persona = models.CharField(max_length=10, choices=TipoPersona.choices, default=TipoPersona.FISICA)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=25, blank=True)
    limite_credito = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    class Meta:
        ordering = ("nombre",)
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def clean(self) -> None:
        super().clean()
        self.documento = normalize_dominican_document(self.documento)

        if self.tipo_persona == self.TipoPersona.FISICA:
            validate_dominican_cedula(self.documento)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.documento})"
