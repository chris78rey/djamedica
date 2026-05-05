from django import forms

from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Appointment
        fields = (
            "patient",
            "doctor",
            "specialty",
            "scheduled_at",
            "duration_minutes",
            "status",
            "reason",
            "notes",
        )
        widgets = {
            "reason": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        patient_qs = Patient.objects.filter(is_active=True).order_by("last_name", "first_name")
        doctor_qs = Doctor.objects.select_related("user", "specialty").filter(is_available=True).order_by(
            "user__last_name", "user__first_name"
        )
        specialty_qs = Specialty.objects.filter(is_active=True).order_by("name")

        if self.instance and self.instance.pk:
            patient_qs = patient_qs | Patient.objects.filter(pk=self.instance.patient_id)
            doctor_qs = doctor_qs | Doctor.objects.filter(pk=self.instance.doctor_id)
            specialty_qs = specialty_qs | Specialty.objects.filter(pk=self.instance.specialty_id)

            if self.instance.scheduled_at:
                self.initial["scheduled_at"] = self.instance.scheduled_at.strftime("%Y-%m-%dT%H:%M")

        self.fields["patient"].queryset = patient_qs.distinct()
        self.fields["doctor"].queryset = doctor_qs.distinct()
        self.fields["specialty"].queryset = specialty_qs.distinct()
