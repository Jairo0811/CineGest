from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.empleados.models import Empleado


class EmpleadoCedulaValidationTests(TestCase):
    def test_empleado_normaliza_y_acepta_cedula_valida(self):
        empleado = Empleado(nombre="Empleado Prueba", cedula="000-0000000-18", fecha_ingreso=date(2026, 1, 1))

        empleado.save()

        self.assertEqual(empleado.cedula, "00000000018")

    def test_empleado_rechaza_cedula_invalida(self):
        empleado = Empleado(nombre="Empleado Prueba", cedula="00000000019", fecha_ingreso=date(2026, 1, 1))

        with self.assertRaises(ValidationError):
            empleado.save()
