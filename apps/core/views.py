from django.http import JsonResponse
from django.shortcuts import render

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty
from apps.users.models import User


def home(request):
    return render(request, "base.html", {"project_name": "Djamedica"})


def health(request):
    return JsonResponse(
        {"status": "ok", "app": "djamedica", "framework": "django"}
    )


def dashboard(request):
    return JsonResponse(
        {
            "users": User.objects.count(),
            "specialties": Specialty.objects.count(),
            "patients": Patient.objects.count(),
            "doctors": Doctor.objects.count(),
            "appointments": Appointment.objects.count(),
        }
    )
