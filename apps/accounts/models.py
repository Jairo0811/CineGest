from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = "ADMIN", "Administrador"
        EMPLOYEE = "EMPLOYEE", "Empleado"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        db_index=True,
    )

    def __str__(self) -> str:
        return self.get_full_name() or self.username
