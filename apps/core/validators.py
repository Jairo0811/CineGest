"""Validadores de documentos de identidad dominicanos.

La validación Luhn de cédula está adaptada de `ogticrd/cuenta-unica-registry`,
proyecto de OGTIC distribuido bajo licencia MIT.
"""

from __future__ import annotations

import hashlib
import re

from django.conf import settings
from django.core.exceptions import ValidationError

_ALLOWED_DOCUMENT_PATTERN = re.compile(r"^[0-9\-\s]+$")
_NON_DIGIT_PATTERN = re.compile(r"\D+")


def normalize_dominican_document(value: str) -> str:
    """Normaliza cédula/RNC a una representación compuesta únicamente por dígitos."""

    text = (value or "").strip()
    if not text:
        return ""

    if not _ALLOWED_DOCUMENT_PATTERN.fullmatch(text):
        raise ValidationError("El documento solo puede contener números, espacios y guiones.")

    return _NON_DIGIT_PATTERN.sub("", text)


def _passes_luhn(cedula: str) -> bool:
    """Replica el checksum Luhn usado por la referencia de OGTIC."""

    digits = [int(value) for value in reversed(cedula)]
    check_digit = digits.pop(0)

    total = 0
    for index, value in enumerate(digits):
        if index % 2 != 0:
            total += value
            continue

        doubled = value * 2
        total += doubled - 9 if doubled > 9 else doubled

    total += check_digit
    return total % 10 == 0


def _is_luhn_exception(cedula: str) -> bool:
    """Comprueba excepciones configuradas como hashes SHA-256, sin exponer cédulas."""

    exception_hashes = getattr(settings, "CEDULA_LUHN_EXCEPTION_HASHES", ())
    if not exception_hashes:
        return False

    cedula_hash = hashlib.sha256(cedula.encode("utf-8")).hexdigest()
    return cedula_hash.lower() in {value.lower() for value in exception_hashes}


def is_valid_dominican_cedula(value: str) -> bool:
    """Indica si una cédula dominicana tiene estructura y checksum válidos."""

    try:
        cedula = normalize_dominican_document(value)
    except ValidationError:
        return False

    if len(cedula) != 11 or not cedula.isdigit():
        return False

    # Evita aceptar secuencias triviales como 00000000000, que satisfacen Luhn.
    if len(set(cedula)) == 1:
        return False

    return _passes_luhn(cedula) or _is_luhn_exception(cedula)


def validate_dominican_cedula(value: str) -> None:
    """Validador Django para cédula dominicana."""

    cedula = normalize_dominican_document(value)

    if len(cedula) != 11:
        raise ValidationError("La cédula debe contener exactamente 11 dígitos.")

    if len(set(cedula)) == 1:
        raise ValidationError("La cédula indicada no es válida.")

    if not (_passes_luhn(cedula) or _is_luhn_exception(cedula)):
        raise ValidationError("La cédula indicada no supera la validación de checksum.")
