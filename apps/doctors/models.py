import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from apps.specialties.models import Specialty
from apps.users.models import User


def doctor_senescyt_upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    doctor_id = instance.doctor_id or "pending"
    specialty_id = instance.specialty_id or "specialty"
    safe_name = f"{uuid.uuid4().hex}.{ext}"

    return (
        f"doctors/senescyt/"
        f"doctor_{doctor_id}/"
        f"specialty_{specialty_id}/"
        f"{safe_name}"
    )


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


class DoctorSpecialtyCredential(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobado"
        REJECTED = "REJECTED", "Rechazado"

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="specialty_credentials",
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name="doctor_credentials",
    )
    senescyt_pdf = models.FileField(
        upload_to=doctor_senescyt_upload_path,
        validators=[FileExtensionValidator(["pdf"])],
    )
    registration_code = models.CharField(
        max_length=80,
        blank=True,
        help_text="Código o número de registro SENESCYT, si aplica.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_doctor_specialty_credentials",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["doctor__user__last_name", "specialty__name"]
        verbose_name = "Credencial SENESCYT por especialidad"
        verbose_name_plural = "Credenciales SENESCYT por especialidad"
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "specialty"],
                name="uq_doctor_specialty_credential",
            )
        ]

    def clean(self):
        errors = {}

        if not self.doctor_id:
            errors["doctor"] = "El médico es obligatorio."

        if not self.specialty_id:
            errors["specialty"] = "La especialidad es obligatoria."
        elif not self.specialty.is_active:
            errors["specialty"] = "La especialidad debe estar activa."

        if not self.senescyt_pdf:
            errors["senescyt_pdf"] = "Debe subir el PDF SENESCYT de esta especialidad."

        if self.status == self.Status.APPROVED and not self.reviewed_at:
            self.reviewed_at = timezone.now()

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.doctor} - {self.specialty} - {self.get_status_display()}"
