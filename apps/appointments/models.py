from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

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

    def __str__(self) -> str:
        return f"{self.patient.full_name} - {self.doctor.user.get_full_name() or self.doctor.user.username} - {self.scheduled_at}"

    def get_end_time(self):
        return self.scheduled_at + timedelta(minutes=self.duration_minutes)

    def clean(self):
        errors = {}

        self.reason = (self.reason or "").strip()
        self.notes = (self.notes or "").strip()

        if not self.patient_id:
            errors["patient"] = "El paciente es obligatorio."
        elif not self.patient.is_active:
            errors["patient"] = "No se puede agendar una cita para un paciente inactivo."

        if not self.doctor_id:
            errors["doctor"] = "El doctor es obligatorio."
        elif not self.doctor.is_available:
            errors["doctor"] = "No se puede agendar una cita con un doctor no disponible."

        if not self.specialty_id:
            errors["specialty"] = "La especialidad es obligatoria."
        elif not self.specialty.is_active:
            errors["specialty"] = "La especialidad de la cita debe estar activa."

        if self.doctor_id and self.specialty_id:
            if self.doctor.specialty_id != self.specialty_id:
                errors["specialty"] = "La especialidad de la cita debe coincidir con la del doctor."

        if not self.reason:
            errors["reason"] = "El motivo de la cita es obligatorio."

        if self.duration_minutes < 10 or self.duration_minutes > 240:
            errors["duration_minutes"] = "La duración debe estar entre 10 y 240 minutos."

        if self.scheduled_at:
            scheduled = self.scheduled_at
            if timezone.is_naive(scheduled):
                scheduled = timezone.make_aware(scheduled, timezone.get_current_timezone())

            now = timezone.now()

            if self.status in {self.Status.SCHEDULED, self.Status.CONFIRMED} and scheduled < now:
                errors["scheduled_at"] = "No se puede dejar una cita pendiente o confirmada en el pasado."

            if self.status == self.Status.COMPLETED and scheduled > now:
                errors["status"] = "Una cita completada no puede estar programada en el futuro."

        if self.doctor_id and self.scheduled_at and self.duration_minutes:
            current_start = self.scheduled_at
            if timezone.is_naive(current_start):
                current_start = timezone.make_aware(current_start, timezone.get_current_timezone())
            current_end = current_start + timedelta(minutes=self.duration_minutes)

            qs = Appointment.objects.filter(doctor_id=self.doctor_id).exclude(pk=self.pk)
            qs = qs.exclude(status__in=[self.Status.CANCELLED, self.Status.NO_SHOW])

            same_day = current_start.date()
            qs = qs.filter(scheduled_at__date=same_day)

            for other in qs:
                other_start = other.scheduled_at
                if timezone.is_naive(other_start):
                    other_start = timezone.make_aware(other_start, timezone.get_current_timezone())
                other_end = other_start + timedelta(minutes=other.duration_minutes)

                overlap = current_start < other_end and current_end > other_start
                if overlap:
                    errors["scheduled_at"] = (
                        f"El doctor ya tiene una cita que se cruza con este horario "
                        f"({other_start} - {other_end})."
                    )
                    break

        if errors:
            raise ValidationError(errors)
