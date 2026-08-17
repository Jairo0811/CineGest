from django import forms

from apps.articulos.models import Articulo, InventarioItem
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, (forms.Select, forms.SelectMultiple)) else "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            field.widget.attrs["class"] = css_class


class ArticuloForm(StyledModelForm):
    class Meta:
        model = Articulo
        fields = [
            "titulo",
            "tipo_articulo",
            "idioma",
            "generos",
            "descripcion",
            "monto_renta_dia",
            "dias_renta",
            "monto_entrega_tardia",
            "activo",
        ]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 4})}


class InventarioItemForm(StyledModelForm):
    class Meta:
        model = InventarioItem
        fields = ["articulo", "codigo", "estado", "observaciones"]


class ClienteForm(StyledModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "documento", "tipo_persona", "email", "telefono", "limite_credito", "activo"]


class EmpleadoForm(StyledModelForm):
    class Meta:
        model = Empleado
        fields = ["usuario", "nombre", "cedula", "tanda", "porcentaje_comision", "fecha_ingreso", "activo"]
        widgets = {"fecha_ingreso": forms.DateInput(attrs={"type": "date"})}
