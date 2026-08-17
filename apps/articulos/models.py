from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.catalogos.models import Genero, Idioma, TipoArticulo
from apps.core.models import SoftDeleteModel, TimeStampedModel


class PersonaElenco(TimeStampedModel, SoftDeleteModel):
    nombre = models.CharField(max_length=160)
    nombre_artistico = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("nombre",)
        verbose_name = "Persona de elenco"
        verbose_name_plural = "Personas de elenco"

    def __str__(self) -> str:
        return self.nombre_artistico or self.nombre


class Articulo(TimeStampedModel, SoftDeleteModel):
    titulo = models.CharField(max_length=200, db_index=True)
    tipo_articulo = models.ForeignKey(TipoArticulo, on_delete=models.PROTECT, related_name="articulos")
    idioma = models.ForeignKey(Idioma, on_delete=models.PROTECT, related_name="articulos")
    generos = models.ManyToManyField(Genero, related_name="articulos", blank=True)
    elenco = models.ManyToManyField(PersonaElenco, through="ArticuloElenco", related_name="articulos", blank=True)
    descripcion = models.TextField(blank=True)
    monto_renta_dia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    dias_renta = models.PositiveSmallIntegerField(default=1)
    monto_entrega_tardia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    class Meta:
        ordering = ("titulo",)
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"

    def __str__(self) -> str:
        return self.titulo


class ArticuloElenco(TimeStampedModel):
    class Rol(models.TextChoices):
        ACTOR = "ACTOR", "Actor/Actriz"
        DIRECTOR = "DIRECTOR", "Director/a"
        PRODUCTOR = "PRODUCTOR", "Productor/a"
        AUTOR = "AUTOR", "Autor/a"
        INTERPRETE = "INTERPRETE", "Intérprete"
        OTRO = "OTRO", "Otro"

    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name="participaciones_elenco")
    persona = models.ForeignKey(PersonaElenco, on_delete=models.PROTECT, related_name="participaciones")
    rol = models.CharField(max_length=20, choices=Rol.choices)

    class Meta:
        ordering = ("articulo__titulo", "persona__nombre", "rol")
        constraints = [
            models.UniqueConstraint(fields=("articulo", "persona", "rol"), name="uq_articulo_persona_rol"),
        ]
        verbose_name = "Participación de elenco"
        verbose_name_plural = "Participaciones de elenco"

    def __str__(self) -> str:
        return f"{self.persona} - {self.get_rol_display()} en {self.articulo}"


class InventarioItem(TimeStampedModel):
    class Estado(models.TextChoices):
        DISPONIBLE = "DISPONIBLE", "Disponible"
        RENTADO = "RENTADO", "Rentado"
        MANTENIMIENTO = "MANTENIMIENTO", "Mantenimiento"
        RETIRADO = "RETIRADO", "Retirado"

    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT, related_name="inventario")
    codigo = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.DISPONIBLE, db_index=True)
    observaciones = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("codigo",)
        verbose_name = "Unidad de inventario"
        verbose_name_plural = "Unidades de inventario"

    def __str__(self) -> str:
        return f"{self.codigo} - {self.articulo}"
