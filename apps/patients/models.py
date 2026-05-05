from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.users.models import User


def _validate_ec_cedula(value: str) -> bool:
    if len(value) != 10 or not value.isdigit():
        return False

    province = int(value[:2])
    third_digit = int(value[2])

    if province < 1 or province > 24:
        return False

    if third_digit >= 6:
        return False

    digits = [int(d) for d in value]
    total = 0

    for i in range(9):
        num = digits[i]
        if i % 2 == 0:
            num *= 2
            if num > 9:
                num -= 9
        total += num

    verifier = (10 - (total % 10)) % 10
    return verifier == digits[9]


class Patient(models.Model):
    class DocumentType(models.TextChoices):
        CEDULA = "CEDULA", "Cédula"
        PASSPORT = "PASSPORT", "Pasaporte"
        OTHER = "OTHER", "Otro"

    class Sex(models.TextChoices):
        MALE = "M", "Masculino"
        FEMALE = "F", "Femenino"
        OTHER = "O", "Otro"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="patient_profile",
    )

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.CEDULA,
    )
    document_number = models.CharField(max_length=30, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=1,
        choices=Sex.choices,
        blank=True,
    )
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def clean(self):
        errors = {}

        self.first_name = (self.first_name or "").strip()
        self.last_name = (self.last_name or "").strip()
        self.document_number = (self.document_number or "").strip().upper()
        self.phone = (self.phone or "").strip()
        self.email = (self.email or "").strip().lower()
        self.emergency_contact_name = (self.emergency_contact_name or "").strip()
        self.emergency_contact_phone = (self.emergency_contact_phone or "").strip()

        if not self.first_name:
            errors["first_name"] = "El nombre es obligatorio."

        if not self.last_name:
            errors["last_name"] = "El apellido es obligatorio."

        if not self.document_number:
            errors["document_number"] = "El número de documento es obligatorio."
        else:
            if self.document_type == self.DocumentType.CEDULA:
                if not _validate_ec_cedula(self.document_number):
                    errors["document_number"] = "La cédula ecuatoriana no es válida."
            elif self.document_type == self.DocumentType.PASSPORT:
                if not self.document_number.replace("-", "").isalnum():
                    errors["document_number"] = "El pasaporte solo puede tener letras, números o guiones."
                elif len(self.document_number) < 6:
                    errors["document_number"] = "El pasaporte es demasiado corto."

        if self.birth_date and self.birth_date > timezone.localdate():
            errors["birth_date"] = "La fecha de nacimiento no puede estar en el futuro."

        if self.email:
            qs = Patient.objects.filter(email__iexact=self.email).exclude(pk=self.pk)
            if qs.exists():
                errors["email"] = "Ya existe otro paciente con ese correo."

        if self.user_id:
            if self.user.role != User.Role.PATIENT:
                errors["user"] = "El usuario relacionado debe tener rol PACIENTE."
            elif not self.user.is_active:
                errors["user"] = "El usuario relacionado debe estar activo."

        if errors:
            raise ValidationError(errors)
