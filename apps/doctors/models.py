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
        errors = {}

        self.professional_license = (self.professional_license or "").strip().upper()
        self.phone = (self.phone or "").strip()
        self.office = (self.office or "").strip()
        self.bio = (self.bio or "").strip()

        if not self.user_id:
            errors["user"] = "El usuario del doctor es obligatorio."
        elif self.user.role != User.Role.DOCTOR:
            errors["user"] = "El usuario relacionado debe tener rol DOCTOR."
        elif not self.user.is_active:
            errors["user"] = "El usuario relacionado debe estar activo."

        if not self.specialty_id:
            errors["specialty"] = "La especialidad es obligatoria."
        elif not self.specialty.is_active:
            errors["specialty"] = "La especialidad del doctor debe estar activa."

        if not self.professional_license:
            errors["professional_license"] = "La licencia profesional es obligatoria."

        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} - {self.specialty.name}"
