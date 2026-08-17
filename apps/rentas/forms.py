from django import forms

from apps.articulos.models import InventarioItem
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado


class NuevaRentaForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.none())
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.none())
    items = forms.ModelMultipleChoiceField(
        queryset=InventarioItem.objects.none(),
        label="Unidades de inventario",
        widget=forms.SelectMultiple(attrs={"size": 10}),
    )
    comentarios = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cliente"].queryset = Cliente.objects.filter(activo=True).order_by("nombre")
        self.fields["empleado"].queryset = Empleado.objects.filter(activo=True).order_by("nombre")
        self.fields["items"].queryset = (
            InventarioItem.objects.filter(estado=InventarioItem.Estado.DISPONIBLE, articulo__activo=True)
            .select_related("articulo")
            .order_by("articulo__titulo", "codigo")
        )

        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, (forms.Select, forms.SelectMultiple)) else "form-control"
            field.widget.attrs.setdefault("class", css)
