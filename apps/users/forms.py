from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty

from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "is_active",
            "is_staff",
        )

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("El correo es obligatorio.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo.")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "is_active",
            "is_staff",
        )

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("El correo es obligatorio.")
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe otro usuario con ese correo.")
        return email


class BaseSelfRegistrationForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(label="Nombres", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150)
    phone = forms.CharField(label="Teléfono", max_length=30, required=False)
    profile_photo = forms.ImageField(
        label="Foto de perfil",
        required=True,
        help_text="Suba una imagen JPG, PNG o WEBP.",
    )
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese usuario.")
        return username

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo.")
        return email

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        if password1:
            password_validation.validate_password(password1)

        return cleaned

    def _create_user(self, role):
        return User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data["first_name"].strip(),
            last_name=self.cleaned_data["last_name"].strip(),
            role=role,
            phone=(self.cleaned_data.get("phone") or "").strip(),
            profile_photo=self.cleaned_data.get("profile_photo"),
            is_active=True,
            is_staff=False,
        )


class PatientSelfRegistrationForm(BaseSelfRegistrationForm):
    document_type = forms.ChoiceField(
        label="Tipo de documento",
        choices=Patient.DocumentType.choices,
        initial=Patient.DocumentType.CEDULA,
    )
    document_number = forms.CharField(label="Número de documento", max_length=30)

    @transaction.atomic
    def save(self):
        user = self._create_user(User.Role.PATIENT)

        patient = Patient(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            document_type=self.cleaned_data["document_type"],
            document_number=self.cleaned_data["document_number"],
            phone=user.phone,
            email=user.email,
            is_active=True,
        )
        patient.full_clean()
        patient.save()

        return user


class DoctorSelfRegistrationForm(BaseSelfRegistrationForm):
    specialty = forms.ModelChoiceField(
        label="Especialidad",
        queryset=Specialty.objects.none(),
    )
    professional_license = forms.CharField(label="Registro profesional", max_length=50)
    office = forms.CharField(label="Consultorio", max_length=80, required=False)
    bio = forms.CharField(
        label="Biografía profesional",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["specialty"].queryset = Specialty.objects.filter(
            is_active=True
        ).order_by("name")

    def clean_professional_license(self):
        professional_license = (
            self.cleaned_data.get("professional_license") or ""
        ).strip().upper()

        if Doctor.objects.filter(
            professional_license__iexact=professional_license
        ).exists():
            raise forms.ValidationError("Ya existe un médico con ese registro profesional.")

        return professional_license

    @transaction.atomic
    def save(self):
        user = self._create_user(User.Role.DOCTOR)

        doctor = Doctor(
            user=user,
            specialty=self.cleaned_data["specialty"],
            professional_license=self.cleaned_data["professional_license"],
            phone=user.phone,
            office=(self.cleaned_data.get("office") or "").strip(),
            bio=(self.cleaned_data.get("bio") or "").strip(),
            is_available=False,
        )
        doctor.full_clean()
        doctor.save()

        return user
