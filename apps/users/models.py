from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        DOCTOR = "DOCTOR", "Doctor"
        STAFF = "STAFF", "Personal"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
    )
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        full_name = self.get_full_name().strip()
        return full_name or self.username
