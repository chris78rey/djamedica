from django import forms

from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty
from .models import Appointment


class AppointmentForm(forms.ModelForm):
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
            "created_by",
        )
        widgets = {
            "scheduled_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "reason": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["patient"].queryset = Patient.objects.filter(is_active=True).order_by(
            "last_name", "first_name"
        )
        self.fields["doctor"].queryset = Doctor.objects.select_related("user", "specialty").filter(
            is_available=True
        ).order_by("user__last_name", "user__first_name")
        self.fields["specialty"].queryset = Specialty.objects.filter(is_active=True).order_by("name")
