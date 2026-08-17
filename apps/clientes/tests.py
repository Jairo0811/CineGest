from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.clientes.models import Cliente


class ClienteDocumentValidationTests(TestCase):
    def test_persona_fisica_normaliza_y_acepta_cedula_valida(self):
        cliente = Cliente(nombre="Cliente Prueba", documento="000-0000000-18", tipo_persona=Cliente.TipoPersona.FISICA)

        cliente.save()

        self.assertEqual(cliente.documento, "00000000018")

    def test_persona_fisica_rechaza_cedula_invalida(self):
        cliente = Cliente(nombre="Cliente Prueba", documento="00000000019", tipo_persona=Cliente.TipoPersona.FISICA)

        with self.assertRaises(ValidationError):
            cliente.save()

    def test_persona_juridica_no_aplica_checksum_de_cedula(self):
        cliente = Cliente(nombre="Empresa Prueba", documento="1-01-12345-6", tipo_persona=Cliente.TipoPersona.JURIDICA)

        cliente.save()

        self.assertEqual(cliente.documento, "101123456")
