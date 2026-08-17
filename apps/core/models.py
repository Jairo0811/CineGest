from django.db import models


class TimeStampedModel(models.Model):
    """Base abstracta con marcas de creación y actualización."""

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Base abstracta para desactivar registros sin borrarlos físicamente."""

    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class BaseCatalogModel(TimeStampedModel, SoftDeleteModel):
    """Base reutilizable para catálogos simples de CineGest."""

    descripcion = models.CharField(max_length=120, unique=True)

    class Meta:
        abstract = True
        ordering = ("descripcion",)

    def __str__(self) -> str:
        return self.descripcion
