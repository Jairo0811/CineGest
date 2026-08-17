from apps.core.models import BaseCatalogModel


class TipoArticulo(BaseCatalogModel):
    class Meta(BaseCatalogModel.Meta):
        verbose_name = "Tipo de artículo"
        verbose_name_plural = "Tipos de artículos"


class Genero(BaseCatalogModel):
    class Meta(BaseCatalogModel.Meta):
        verbose_name = "Género"
        verbose_name_plural = "Géneros"


class Idioma(BaseCatalogModel):
    class Meta(BaseCatalogModel.Meta):
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"
