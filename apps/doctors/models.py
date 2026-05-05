from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.specialties.models import Specialty
from apps.users.models import User


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="doctor_profile",
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name="doctors",
    )
    professional_license = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=30, blank=True)
    office = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name"]
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"

    def clean(self):
        if self.user and self.user.role != User.Role.DOCTOR:
            raise ValidationError(
                {"user": "El usuario relacionado debe tener rol DOCTOR."}
            )

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} - {self.specialty.name}"
