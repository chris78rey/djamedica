from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Agendada"
        CONFIRMED = "CONFIRMED", "Confirmada"
        COMPLETED = "COMPLETED", "Completada"
        CANCELLED = "CANCELLED", "Cancelada"
        NO_SHOW = "NO_SHOW", "No asistió"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    reason = models.TextField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_appointments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_at"]
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "scheduled_at"],
                name="uq_appointment_doctor_scheduled_at",
            )
        ]

    def clean(self):
        if self.doctor_id and self.specialty_id:
            if self.doctor.specialty_id != self.specialty_id:
                raise ValidationError(
                    {
                        "specialty": "La especialidad de la cita debe coincidir con la del doctor."
                    }
                )

    def __str__(self) -> str:
        return f"{self.patient.full_name} - {self.doctor.user.get_full_name() or self.doctor.user.username} - {self.scheduled_at}"
