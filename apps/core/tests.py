import hashlib

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, override_settings

from apps.core.validators import is_valid_dominican_cedula, normalize_dominican_document, validate_dominican_cedula


class DominicanCedulaValidatorTests(SimpleTestCase):
    def test_normalize_dominican_document_removes_formatting(self):
        self.assertEqual(normalize_dominican_document("000-0000001-8"), "00000000018")

    def test_rejects_invalid_characters(self):
        with self.assertRaises(ValidationError):
            normalize_dominican_document("000-ABC-0018")

    def test_accepts_valid_luhn_checksum(self):
        self.assertTrue(is_valid_dominican_cedula("00000000018"))

    def test_rejects_invalid_luhn_checksum(self):
        self.assertFalse(is_valid_dominican_cedula("00000000019"))
        with self.assertRaises(ValidationError):
            validate_dominican_cedula("00000000019")

    def test_rejects_trivial_repeated_digits(self):
        self.assertFalse(is_valid_dominican_cedula("00000000000"))

    def test_accepts_configured_sha256_exception(self):
        cedula = "00000000019"
        digest = hashlib.sha256(cedula.encode("utf-8")).hexdigest()

        with override_settings(CEDULA_LUHN_EXCEPTION_HASHES=(digest,)):
            self.assertTrue(is_valid_dominican_cedula(cedula))
            validate_dominican_cedula(cedula)
